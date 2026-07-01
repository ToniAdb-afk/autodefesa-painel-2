import pandas as pd
import sys
import os
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

    def fmt(v):
        return f"R$ {v:,.2f}".replace(',','X').replace('.',',').replace('X','.')

    def pct(v, total):
        return f"{(v/total*100):.1f}%" if total > 0 else "0%"

    # Logo
    logo_html = ""
    if logo_path and os.path.exists(logo_path):
        import base64
        ext = logo_path.rsplit('.', 1)[-1].lower()
        mime = {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','webp':'image/webp'}.get(ext,'image/png')
        with open(logo_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:{mime};base64,{b64}" style="height:38px;object-fit:contain;margin-right:12px;">'

    # Barras clientes
    max_cli = por_cliente.max() if len(por_cliente) else 1
    barras_clientes = ""
    cores_cli = ['#27ae60','#2ecc71','#1abc9c','#16a085','#0d7a63']
    for i, (cli, val) in enumerate(por_cliente.items()):
        cor = cores_cli[i % len(cores_cli)]
        w   = val / max_cli * 100
        barras_clientes += f"""
        <div class="bar-row">
          <div class="bar-label">{cli}</div>
          <div class="bar-wrap">
            <div class="bar-fill" style="width:{w:.1f}%;background:{cor};"></div>
          </div>
          <div class="bar-val">{fmt(val)}</div>
        </div>"""

    # Barras meses
    max_mes = por_mes.max() if len(por_mes) else 1
    barras_meses = ""
    cores_mes = ['#27ae60','#f39c12','#e74c3c','#3498db','#9b59b6']
    for i, (mes, val) in enumerate(por_mes.items()):
        cor = cores_mes[i % len(cores_mes)]
        w   = val / max_mes * 100
        barras_meses += f"""
        <div class="bar-row">
          <div class="bar-label">{mes}</div>
          <div class="bar-wrap">
            <div class="bar-fill" style="width:{w:.1f}%;background:{cor};"></div>
          </div>
          <div class="bar-val">{fmt(val)}</div>
        </div>"""

    # Tabela registros
    status_cores = {
        'Aprovado':             ('rgba(39,174,96,.15)',  '#27ae60'),
        'Aguardando Aprovação': ('rgba(243,156,18,.15)', '#f39c12'),
        'Em medição':           ('rgba(52,152,219,.15)', '#3498db'),
    }
    rows_html = ""
    for _, r in df.iterrows():
        bg, fg = status_cores.get(r['STATUS'], ('rgba(255,255,255,.05)', '#aaa'))
        rows_html += f"""
        <tr>
          <td>{r['MÊS']}</td>
          <td><strong>{r['CLIENTE']}</strong></td>
          <td><span class="classif {'rec' if r['CLASSIFICAÇÃO']=='RECORRENTE' else 'avu'}">{r['CLASSIFICAÇÃO']}</span></td>
          <td class="val-col">{fmt(r['VALOR'])}</td>
          <td><span class="badge" style="background:{bg};color:{fg};">{r['STATUS']}</span></td>
          <td class="obs">{r['Observação']}</td>
        </tr>"""

    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Painel de Faturamento — Autodefesa Brasil</title>
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
.page-sub{{font-size:13px;color:var(--text2);margin-bottom:32px;}}

/* KPIs */
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px;}}
.kpi{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:22px 20px;position:relative;overflow:hidden;}}
.kpi::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:14px 14px 0 0;}}
.kpi.green::before{{background:var(--green);}}
.kpi.orange::before{{background:#f39c12;}}
.kpi.blue::before{{background:#3498db;}}
.kpi.gray::before{{background:#7f8c8d;}}
.kpi-label{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;}}
.kpi-value{{font-size:22px;font-weight:800;letter-spacing:-0.5px;}}
.kpi-sub{{font-size:11px;color:var(--text3);margin-top:6px;}}

/* Grid 2 colunas */
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;}}
.panel{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:24px;}}
.panel-title{{font-size:13px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:1px;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid var(--border);}}

/* Donut status */
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

/* Barras */
.bar-row{{display:flex;align-items:center;gap:10px;margin-bottom:10px;}}
.bar-label{{font-size:12px;color:var(--text2);width:140px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.bar-wrap{{flex:1;background:var(--border);border-radius:4px;height:8px;overflow:hidden;}}
.bar-fill{{height:8px;border-radius:4px;transition:width .6s ease;}}
.bar-val{{font-size:12px;font-weight:700;width:110px;text-align:right;flex-shrink:0;}}

/* Classificação */
.classif-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}
.classif-card{{border-radius:10px;padding:16px;text-align:center;}}
.classif-card.rec{{background:rgba(39,174,96,.1);border:1px solid rgba(39,174,96,.25);}}
.classif-card.avu{{background:rgba(52,152,219,.1);border:1px solid rgba(52,152,219,.25);}}
.classif-name{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;}}
.classif-card.rec .classif-name{{color:var(--green);}}
.classif-card.avu .classif-name{{color:#3498db;}}
.classif-val{{font-size:18px;font-weight:900;}}
.classif-pct{{font-size:11px;color:var(--text3);margin-top:4px;}}

/* Tabela */
.table-wrap{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:24px;margin-bottom:20px;}}
.table-scroll{{overflow-x:auto;}}
table{{width:100%;border-collapse:collapse;}}
th{{font-size:11px;color:var(--text2);text-transform:uppercase;letter-spacing:1px;padding:10px 12px;text-align:left;border-bottom:1px solid var(--border);}}
td{{font-size:13px;padding:11px 12px;border-bottom:1px solid #1a2740;vertical-align:middle;}}
tr:last-child td{{border-bottom:none;}}
tr:hover td{{background:rgba(39,174,96,.03);}}
.val-col{{font-weight:700;font-variant-numeric:tabular-nums;}}
.badge{{font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;white-space:nowrap;}}
.classif{{font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;}}
.classif.rec{{background:rgba(39,174,96,.15);color:var(--green);}}
.classif.avu{{background:rgba(52,152,219,.15);color:#3498db;}}
.obs{{font-size:11px;color:var(--text3);}}

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
      <a href="index.html" class="back-btn">← Central de Painéis</a>
    </div>
  </div>
</div>

<div class="content">
  <div class="page-title">Painel de <span>Faturamento</span></div>
  <div class="page-sub">{n_registros} registros · {n_clientes} clientes · Base: {', '.join(sorted(df['MÊS'].unique()))}</div>

  <!-- KPIs -->
  <div class="kpis">
    <div class="kpi green">
      <div class="kpi-label">💰 Total Faturado</div>
      <div class="kpi-value">{fmt(total)}</div>
      <div class="kpi-sub">{n_registros} registros · {n_clientes} clientes</div>
    </div>
    <div class="kpi green">
      <div class="kpi-label">✅ Aprovado</div>
      <div class="kpi-value">{fmt(aprovado)}</div>
      <div class="kpi-sub">{pct(aprovado, total)} do total</div>
    </div>
    <div class="kpi orange">
      <div class="kpi-label">⏳ Aguardando Aprovação</div>
      <div class="kpi-value">{fmt(aguardando)}</div>
      <div class="kpi-sub">{pct(aguardando, total)} do total</div>
    </div>
    <div class="kpi blue">
      <div class="kpi-label">📐 Em Medição</div>
      <div class="kpi-value">{fmt(em_medicao)}</div>
      <div class="kpi-sub">{pct(em_medicao, total)} do total</div>
    </div>
  </div>

  <!-- Grid principal -->
  <div class="grid2">
    <!-- Por cliente -->
    <div class="panel">
      <div class="panel-title">Faturamento por Cliente</div>
      {barras_clientes}
    </div>

    <!-- Status + Classificação -->
    <div style="display:flex;flex-direction:column;gap:20px;">
      <div class="panel">
        <div class="panel-title">Status dos Faturamentos</div>
        <div class="status-items">
          {"".join([f'''
          <div>
            <div class="status-row">
              <div class="status-left">
                <div class="status-dot" style="background:{'#27ae60' if s=='Aprovado' else '#f39c12' if s=='Aguardando Aprovação' else '#3498db'};"></div>
                <div class="status-name">{s}</div>
              </div>
              <div class="status-right">
                <div class="status-val">{fmt(v)}</div>
                <div class="status-pct">{pct(v,total)}</div>
              </div>
            </div>
            <div class="status-bar-bg">
              <div class="status-bar-fill" style="width:{pct(v,total)};background:{'#27ae60' if s=='Aprovado' else '#f39c12' if s=='Aguardando Aprovação' else '#3498db'};"></div>
            </div>
          </div>''' for s,v in por_status.items()])}
        </div>
      </div>

      <div class="panel">
        <div class="panel-title">Recorrente vs Avulso</div>
        <div class="classif-grid">
          <div class="classif-card rec">
            <div class="classif-name">Recorrente</div>
            <div class="classif-val">{fmt(recorrente)}</div>
            <div class="classif-pct">{pct(recorrente, total)} do total</div>
          </div>
          <div class="classif-card avu">
            <div class="classif-name">Avulso</div>
            <div class="classif-val">{fmt(avulso)}</div>
            <div class="classif-pct">{pct(avulso, total)} do total</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Por mês -->
  <div class="panel" style="margin-bottom:20px;">
    <div class="panel-title">Faturamento por Período</div>
    {barras_meses}
  </div>

  <!-- Tabela -->
  <div class="table-wrap">
    <div class="panel-title">Registros Detalhados</div>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Período</th><th>Cliente</th><th>Tipo</th>
            <th>Valor</th><th>Status</th><th>Observação</th>
          </tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>
    </div>
  </div>

</div>

<div class="footer">
  Autodefesa Brasil · Painel de Faturamento · Gerado em {data_hora}
</div>

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
