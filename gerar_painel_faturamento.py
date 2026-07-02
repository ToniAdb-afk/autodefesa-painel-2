import pandas as pd
import sys
import os
import json
from datetime import datetime

def gerar_painel(arquivo_excel, logo_path=None):
    df = pd.read_excel(arquivo_excel)
    df.columns = df.columns.str.strip()
    df['VALOR'] = pd.to_numeric(df['VALOR'], errors='coerce').fillna(0)
    df['MÊS']  = df['MÊS'].astype(str).str.strip()
    df['CLIENTE'] = df['CLIENTE'].astype(str).str.strip()
    df['CLASSIFICAÇÃO'] = df['CLASSIFICAÇÃO'].astype(str).str.strip()
    df['STATUS'] = df['STATUS'].astype(str).str.strip()
    df['Observação'] = df['Observação'].astype(str).str.strip()

    total          = df['VALOR'].sum()
    aprovado       = df[df['STATUS'] == 'Aprovado']['VALOR'].sum()
    aguardando     = df[df['STATUS'] == 'Aguardando Aprovação']['VALOR'].sum()
    em_medicao     = df[df['STATUS'] == 'Em medição']['VALOR'].sum()
    recorrente     = df[df['CLASSIFICAÇÃO'] == 'RECORRENTE']['VALOR'].sum()
    avulso         = df[df['CLASSIFICAÇÃO'] == 'AVULSO']['VALOR'].sum()
    n_clientes     = df['CLIENTE'].nunique()
    n_registros    = len(df)

    por_cliente = df.groupby('CLIENTE')['VALOR'].sum().sort_values(ascending=False)
    por_mes     = df.groupby('MÊS')['VALOR'].sum().sort_values(ascending=False)
    por_status  = df.groupby('STATUS')['VALOR'].sum()

    # JSON com todos os registros para filtro/export
    registros_json = json.dumps([
        {
            'MES': str(r['MÊS']),
            'CLIENTE': str(r['CLIENTE']),
            'CLASSIFICACAO': str(r['CLASSIFICAÇÃO']),
            'VALOR': float(r['VALOR']),
            'STATUS': str(r['STATUS']),
            'OBSERVACAO': str(r['Observação'])
        }
        for _, r in df.iterrows()
    ], ensure_ascii=False)

    clientes_json = json.dumps(sorted(df['CLIENTE'].unique().tolist()), ensure_ascii=False)
    meses_json    = json.dumps(sorted(df['MÊS'].unique().tolist()), ensure_ascii=False)

    def fmt(v):
        return f"R$ {v:,.2f}".replace(',','X').replace('.',',').replace('X','.')
    def pct(v, total):
        return f"{(v/total*100):.1f}%" if total > 0 else "0%"

    logo_html = ""
    if logo_path and os.path.exists(logo_path):
        import base64
        ext = logo_path.rsplit('.', 1)[-1].lower()
        mime = {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','webp':'image/webp'}.get(ext,'image/png')
        with open(logo_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:{mime};base64,{b64}" style="height:38px;object-fit:contain;margin-right:12px;">'

    max_cli = por_cliente.max() if len(por_cliente) else 1
    barras_clientes = ""
    cores_cli = ['#27ae60','#2ecc71','#1abc9c','#16a085','#0d7a63']
    for i, (cli, val) in enumerate(por_cliente.items()):
        cor = cores_cli[i % len(cores_cli)]
        w   = val / max_cli * 100
        barras_clientes += f"""
        <div class="bar-row">
          <div class="bar-label">{cli}</div>
          <div class="bar-wrap"><div class="bar-fill" style="width:{w:.1f}%;background:{cor};"></div></div>
          <div class="bar-val">{fmt(val)}</div>
        </div>"""

    max_mes = por_mes.max() if len(por_mes) else 1
    barras_meses = ""
    cores_mes = ['#27ae60','#f39c12','#e74c3c','#3498db','#9b59b6']
    for i, (mes, val) in enumerate(por_mes.items()):
        cor = cores_mes[i % len(cores_mes)]
        w   = val / max_mes * 100
        barras_meses += f"""
        <div class="bar-row">
          <div class="bar-label">{mes}</div>
          <div class="bar-wrap"><div class="bar-fill" style="width:{w:.1f}%;background:{cor};"></div></div>
          <div class="bar-val">{fmt(val)}</div>
        </div>"""

    status_cores = {
        'Aprovado':             ('rgba(39,174,96,.15)',  '#27ae60'),
        'Aguardando Aprovação': ('rgba(243,156,18,.15)', '#f39c12'),
        'Em medição':           ('rgba(52,152,219,.15)', '#3498db'),
    }

    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Painel de Faturamento — Autodefesa Brasil</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
:root{{--bg:#080b10;--bg2:#0e1420;--bg3:#111824;--border:#1e2d4a;--text:#e8edf5;--text2:#7a8ba8;--text3:#4a5f7a;--green:#27ae60;--green2:#2ecc71;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}}
.header{{background:linear-gradient(180deg,#0a0f1a,#080b10);border-bottom:1px solid #27ae6044;padding:0 32px;position:sticky;top:0;z-index:100;}}
.header-inner{{max-width:1300px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:64px;}}
.header-left{{display:flex;align-items:center;gap:14px;}}
.logo-text strong{{font-size:14px;font-weight:800;letter-spacing:1.5px;}}
.logo-text span{{font-size:10px;color:var(--text2);letter-spacing:2px;text-transform:uppercase;display:block;margin-top:2px;}}
.back-btn{{color:var(--text2);text-decoration:none;font-size:12px;border:1px solid var(--border);padding:6px 14px;border-radius:8px;transition:all .2s;}}
.back-btn:hover{{color:var(--green);border-color:var(--green);}}
.update-badge{{font-size:11px;color:var(--text3);}}
.content{{max-width:1300px;margin:0 auto;padding:36px 32px;}}
.page-title{{font-size:26px;font-weight:900;letter-spacing:-0.5px;margin-bottom:4px;}}
.page-title span{{color:var(--green);}}
.page-sub{{font-size:13px;color:var(--text2);margin-bottom:24px;}}

/* ── FILTROS ── */
.filtros{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:20px 24px;margin-bottom:24px;display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end;}}
.filtro-group{{display:flex;flex-direction:column;gap:6px;}}
.filtro-group label{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;font-weight:600;}}
.filtro-group select,
.filtro-group input{{background:#111824;border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:8px;font-size:13px;font-family:'Inter',sans-serif;outline:none;min-width:160px;}}
.filtro-group select:focus,
.filtro-group input:focus{{border-color:var(--green);}}
.btn-filtro{{padding:8px 18px;border-radius:8px;border:none;font-size:13px;font-weight:600;cursor:pointer;font-family:'Inter',sans-serif;transition:all .2s;}}
.btn-limpar{{background:var(--bg3);color:var(--text2);border:1px solid var(--border);}}
.btn-limpar:hover{{color:var(--text);border-color:var(--text2);}}
.btn-export{{background:var(--green);color:#fff;display:flex;align-items:center;gap:8px;}}
.btn-export:hover{{background:#219a52;}}
.filtro-info{{font-size:12px;color:var(--text3);align-self:center;margin-left:auto;}}

/* KPIs */
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px;}}
.kpi{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:22px 20px;position:relative;overflow:hidden;}}
.kpi::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:14px 14px 0 0;}}
.kpi.green::before{{background:var(--green);}}
.kpi.orange::before{{background:#f39c12;}}
.kpi.blue::before{{background:#3498db;}}
.kpi-label{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;}}
.kpi-value{{font-size:22px;font-weight:800;letter-spacing:-0.5px;}}
.kpi-sub{{font-size:11px;color:var(--text3);margin-top:6px;}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;}}
.panel{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:24px;}}
.panel-title{{font-size:13px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:1px;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid var(--border);}}
.status-items{{display:flex;flex-direction:column;gap:12px;}}
.status-row{{display:flex;align-items:center;justify-content:space-between;}}
.status-left{{display:flex;align-items:center;gap:10px;}}
.status-dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0;}}
.status-name{{font-size:13px;color:var(--text);}}
.status-right{{text-align:right;}}
.status-val{{font-size:13px;font-weight:700;}}
.status-pct{{font-size:11px;color:var(--text3);}}
.status-bar-bg{{height:4px;background:var(--border);border-radius:4px;margin-top:6px;}}
.status-bar-fill{{height:4px;border-radius:4px;}}
.bar-row{{display:flex;align-items:center;gap:10px;margin-bottom:10px;}}
.bar-label{{font-size:12px;color:var(--text2);width:140px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.bar-wrap{{flex:1;background:var(--border);border-radius:4px;height:8px;overflow:hidden;}}
.bar-fill{{height:8px;border-radius:4px;}}
.bar-val{{font-size:12px;font-weight:700;width:110px;text-align:right;flex-shrink:0;}}
.classif-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}
.classif-card{{border-radius:10px;padding:16px;text-align:center;}}
.classif-card.rec{{background:rgba(39,174,96,.1);border:1px solid rgba(39,174,96,.25);}}
.classif-card.avu{{background:rgba(52,152,219,.1);border:1px solid rgba(52,152,219,.25);}}
.classif-name{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;}}
.classif-card.rec .classif-name{{color:var(--green);}}
.classif-card.avu .classif-name{{color:#3498db;}}
.classif-val{{font-size:18px;font-weight:900;}}
.classif-pct{{font-size:11px;color:var(--text3);margin-top:4px;}}
.table-wrap{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:24px;margin-bottom:20px;}}
.table-header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--border);}}
.table-scroll{{overflow-x:auto;}}
table{{width:100%;border-collapse:collapse;}}
th{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;padding:10px 12px;text-align:left;border-bottom:1px solid var(--border);}}
td{{font-size:13px;padding:11px 12px;border-bottom:1px solid #1a2740;vertical-align:middle;}}
tr:last-child td{{border-bottom:none;}}
tr:hover td{{background:rgba(39,174,96,.03);}}
.val-col{{font-weight:700;}}
.badge{{font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;white-space:nowrap;}}
.classif{{font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;}}
.classif.rec{{background:rgba(39,174,96,.15);color:var(--green);}}
.classif.avu{{background:rgba(52,152,219,.15);color:#3498db;}}
.obs{{font-size:11px;color:var(--text3);}}
.empty-msg{{text-align:center;padding:40px;color:var(--text3);font-size:13px;}}
.footer{{text-align:center;padding:24px;color:var(--text3);font-size:11px;border-top:1px solid var(--border);margin-top:8px;}}
@media(max-width:900px){{.kpis{{grid-template-columns:1fr 1fr;}}.grid2{{grid-template-columns:1fr;}}}}
@media(max-width:500px){{.kpis{{grid-template-columns:1fr;}}}}
</style>
</head>
<body>

<div class="header">
  <div class="header-inner">
    <div class="header-left">
      {logo_html}
      <div class="logo-text">
        <strong>🛡️ AUTODEFESA BRASIL</strong>
        <span>Gestão &amp; Tecnologia em Segurança</span>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:16px;">
      <span class="update-badge">Atualizado em {data_hora}</span>
      <a href="index.html" class="back-btn">← Hub</a>
    </div>
  </div>
</div>

<div class="content">
  <div class="page-title">Painel de <span>Faturamento</span></div>
  <div class="page-sub" id="page-sub">{n_registros} registros · {n_clientes} clientes</div>

  <!-- FILTROS -->
  <div class="filtros">
    <div class="filtro-group">
      <label>Período</label>
      <select id="filtro-mes">
        <option value="">Todos os meses</option>
      </select>
    </div>
    <div class="filtro-group">
      <label>Cliente</label>
      <select id="filtro-cliente">
        <option value="">Todos os clientes</option>
      </select>
    </div>
    <div class="filtro-group">
      <label>Status</label>
      <select id="filtro-status">
        <option value="">Todos os status</option>
        <option value="Aprovado">Aprovado</option>
        <option value="Aguardando Aprovação">Aguardando Aprovação</option>
        <option value="Em medição">Em medição</option>
      </select>
    </div>
    <div class="filtro-group">
      <label>Classificação</label>
      <select id="filtro-classif">
        <option value="">Todas</option>
        <option value="RECORRENTE">Recorrente</option>
        <option value="AVULSO">Avulso</option>
      </select>
    </div>
    <button class="btn-filtro btn-limpar" onclick="limparFiltros()">✕ Limpar</button>
    <button class="btn-filtro btn-export" onclick="exportarExcel()">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
      Exportar Excel
    </button>
    <span class="filtro-info" id="filtro-info"></span>
  </div>

  <!-- KPIs dinâmicos -->
  <div class="kpis">
    <div class="kpi green"><div class="kpi-label">💰 Total Faturado</div><div class="kpi-value" id="kpi-total">—</div><div class="kpi-sub" id="kpi-total-sub">—</div></div>
    <div class="kpi green"><div class="kpi-label">✅ Aprovado</div><div class="kpi-value" id="kpi-aprov">—</div><div class="kpi-sub" id="kpi-aprov-sub">—</div></div>
    <div class="kpi orange"><div class="kpi-label">⏳ Aguardando</div><div class="kpi-value" id="kpi-agu">—</div><div class="kpi-sub" id="kpi-agu-sub">—</div></div>
    <div class="kpi blue"><div class="kpi-label">📐 Em Medição</div><div class="kpi-value" id="kpi-med">—</div><div class="kpi-sub" id="kpi-med-sub">—</div></div>
  </div>

  <!-- Tabela dinâmica -->
  <div class="table-wrap">
    <div class="table-header">
      <div class="panel-title" style="border:none;margin:0;padding:0;">Registros Detalhados</div>
    </div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Período</th><th>Cliente</th><th>Tipo</th>
            <th>Valor</th><th>Status</th><th>Observação</th>
          </tr>
        </thead>
        <tbody id="tabela-body"></tbody>
      </table>
    </div>
  </div>
</div>

<div class="footer">Autodefesa Brasil · Painel de Faturamento · Gerado em {data_hora}</div>

<script>
const DADOS = {registros_json};
const CLIENTES = {clientes_json};
const MESES = {meses_json};

// Popula selects
const selMes = document.getElementById('filtro-mes');
const selCli = document.getElementById('filtro-cliente');
MESES.forEach(m => {{ const o = document.createElement('option'); o.value = m; o.textContent = m; selMes.appendChild(o); }});
CLIENTES.forEach(c => {{ const o = document.createElement('option'); o.value = c; o.textContent = c; selCli.appendChild(o); }});

// Eventos
['filtro-mes','filtro-cliente','filtro-status','filtro-classif'].forEach(id => {{
  document.getElementById(id).addEventListener('change', aplicarFiltros);
}});

function getDados() {{
  const mes    = document.getElementById('filtro-mes').value;
  const cli    = document.getElementById('filtro-cliente').value;
  const status = document.getElementById('filtro-status').value;
  const classif= document.getElementById('filtro-classif').value;
  return DADOS.filter(r =>
    (!mes    || r.MES === mes) &&
    (!cli    || r.CLIENTE === cli) &&
    (!status || r.STATUS === status) &&
    (!classif|| r.CLASSIFICACAO === classif)
  );
}}

function fmt(v) {{
  return 'R$ ' + v.toLocaleString('pt-BR', {{minimumFractionDigits:2, maximumFractionDigits:2}});
}}

function aplicarFiltros() {{
  const dados = getDados();
  const total    = dados.reduce((s,r) => s + r.VALOR, 0);
  const aprovado = dados.filter(r => r.STATUS === 'Aprovado').reduce((s,r) => s + r.VALOR, 0);
  const agu      = dados.filter(r => r.STATUS === 'Aguardando Aprovação').reduce((s,r) => s + r.VALOR, 0);
  const med      = dados.filter(r => r.STATUS === 'Em medição').reduce((s,r) => s + r.VALOR, 0);
  const pct = (v) => total > 0 ? (v/total*100).toFixed(1)+'%' : '0%';

  document.getElementById('kpi-total').textContent = fmt(total);
  document.getElementById('kpi-total-sub').textContent = dados.length + ' registros';
  document.getElementById('kpi-aprov').textContent = fmt(aprovado);
  document.getElementById('kpi-aprov-sub').textContent = pct(aprovado) + ' do total';
  document.getElementById('kpi-agu').textContent = fmt(agu);
  document.getElementById('kpi-agu-sub').textContent = pct(agu) + ' do total';
  document.getElementById('kpi-med').textContent = fmt(med);
  document.getElementById('kpi-med-sub').textContent = pct(med) + ' do total';
  document.getElementById('filtro-info').textContent = dados.length + ' de ' + DADOS.length + ' registros';

  const STATUS_COR = {{
    'Aprovado':             ['rgba(39,174,96,.15)',  '#27ae60'],
    'Aguardando Aprovação': ['rgba(243,156,18,.15)', '#f39c12'],
    'Em medição':           ['rgba(52,152,219,.15)', '#3498db'],
  }};

  const tbody = document.getElementById('tabela-body');
  if (dados.length === 0) {{
    tbody.innerHTML = '<tr><td colspan="6" class="empty-msg">Nenhum registro encontrado para os filtros selecionados.</td></tr>';
    return;
  }}
  tbody.innerHTML = dados.map(r => {{
    const [bg, fg] = STATUS_COR[r.STATUS] || ['rgba(255,255,255,.05)','#aaa'];
    const tipo = r.CLASSIFICACAO === 'RECORRENTE'
      ? '<span class="classif rec">RECORRENTE</span>'
      : '<span class="classif avu">AVULSO</span>';
    return `<tr>
      <td>${{r.MES}}</td>
      <td><strong>${{r.CLIENTE}}</strong></td>
      <td>${{tipo}}</td>
      <td class="val-col">${{fmt(r.VALOR)}}</td>
      <td><span class="badge" style="background:${{bg}};color:${{fg}};">${{r.STATUS}}</span></td>
      <td class="obs">${{r.OBSERVACAO}}</td>
    </tr>`;
  }}).join('');
}}

function limparFiltros() {{
  ['filtro-mes','filtro-cliente','filtro-status','filtro-classif'].forEach(id => {{
    document.getElementById(id).value = '';
  }});
  aplicarFiltros();
}}

function exportarExcel() {{
  const dados = getDados();
  if (dados.length === 0) {{ alert('Nenhum dado para exportar.'); return; }}
  const ws_data = [
    ['Período', 'Cliente', 'Classificação', 'Valor (R$)', 'Status', 'Observação'],
    ...dados.map(r => [r.MES, r.CLIENTE, r.CLASSIFICACAO, r.VALOR, r.STATUS, r.OBSERVACAO])
  ];
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(ws_data);
  ws['!cols'] = [{{wch:12}},{{wch:30}},{{wch:15}},{{wch:18}},{{wch:25}},{{wch:40}}];
  XLSX.utils.book_append_sheet(wb, ws, 'Faturamento');
  const data = new Date().toLocaleDateString('pt-BR').replace(/\//g,'-');
  XLSX.writeFile(wb, `Faturamento_ADB_${{data}}.xlsx`);
}}

// Inicia
aplicarFiltros();
</script>
</body>
</html>"""
    return html

if __name__ == '__main__':
    arquivo = sys.argv[1] if len(sys.argv) > 1 else 'BASE_DE_FATURAMENTO.xlsx'
    logo    = sys.argv[2] if len(sys.argv) > 2 else None
    if not os.path.exists(arquivo):
        print(f"Arquivo não encontrado: {arquivo}")
        sys.exit(1)
    html = gerar_painel(arquivo, logo)
    with open('painel_faturamento.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ painel_faturamento.html gerado com sucesso!")
