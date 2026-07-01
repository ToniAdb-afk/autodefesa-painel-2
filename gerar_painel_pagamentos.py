#!/usr/bin/env python3
"""
gerar_painel_pagamentos.py - Gerador do Painel Financeiro Autodefesa Brasil
Uso: python gerar_painel_pagamentos.py [arquivo.xlsx]
Requisito: pip install pandas openpyxl
"""
import pandas as pd
import json, sys, os, base64
from datetime import datetime

ARQUIVO = sys.argv[1] if len(sys.argv) > 1 else "BASE_DE_DADOS_SANKHYA_-_PAGAMENTOS.xlsx"
LOGO    = sys.argv[2] if len(sys.argv) > 2 else "OIP__1_.webp"
SAIDA   = "painel_pagamentos.html"

if not os.path.exists(ARQUIVO):
    print(f"❌ Arquivo '{ARQUIVO}' não encontrado.")
    print(f"   Uso: python gerar_painel_pagamentos.py [planilha.xlsx] [logo.webp]")
    sys.exit(1)

print(f"📂 Lendo {ARQUIVO}...")

# ── Validação: verifica se é realmente a planilha financeira ──────────
try:
    df_check = pd.read_excel(ARQUIVO, header=2, nrows=2)
    if 'Dt. Negociação' not in df_check.columns and 'Valor Nota/Financ.' not in df_check.columns:
        print(f"⚠️  Arquivo '{ARQUIVO}' não parece ser a planilha financeira (colunas não encontradas).")
        print(f"   Pulando geração do painel financeiro.")
        sys.exit(0)
except Exception as e:
    print(f"⚠️  Erro ao verificar arquivo: {e}")
    sys.exit(0)

# ── Logo base64 ───────────────────────────────────────────────────────
logo_b64 = ""
if os.path.exists(LOGO):
    with open(LOGO, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    print(f"🖼️  Logo carregado: {LOGO}")
else:
    print(f"⚠️  Logo '{LOGO}' não encontrado — painel gerado sem logo.")

# ── Leitura ───────────────────────────────────────────────────────────
df = pd.read_excel(ARQUIVO, header=2)
df['Dt. Negociação']     = pd.to_datetime(df['Dt. Negociação'], errors='coerce')
df['Prim.Dt.Venc']       = pd.to_datetime(df['Prim.Dt.Venc'], errors='coerce')
df['Valor Nota/Financ.'] = pd.to_numeric(df['Valor Nota/Financ.'], errors='coerce').fillna(0)
df['Mes'] = df['Dt. Negociação'].dt.to_period('M').astype(str)

emissao        = datetime.now().strftime('%d/%m/%Y %H:%M')
total_registros = len(df)
total_valor     = df['Valor Nota/Financ.'].sum()
total_fin       = int((df['Status Nota'] == 'L').sum())
total_agu       = int((df['Status Nota'] == 'A').sum())

data_min = df['Dt. Negociação'].min()
data_max = df['Dt. Negociação'].max()
periodo  = f"{data_min.strftime('%b/%Y')} – {data_max.strftime('%b/%Y')}" if pd.notna(data_min) else ''

# ── Cliente ───────────────────────────────────────────────────────────
def extract_client(nome):
    if pd.isna(nome): return 'Sem Cliente'
    s = str(nome).upper()
    for k in ['AGIBANK','WESTERN UNION','SICOOB','MERCANTIL','CREFISA']:
        if k in s: return k
    return s.split('-')[0].strip()

# ── Pivôs ──────────────────────────────────────────────────────────────
MES_MAP = {'01':'Jan','02':'Fev','03':'Mar','04':'Abr','05':'Mai','06':'Jun',
           '07':'Jul','08':'Ago','09':'Set','10':'Out','11':'Nov','12':'Dez'}

def mes_label(m):
    return MES_MAP.get(str(m)[-2:], str(m))

# Mensal
monthly_raw = df.groupby('Mes')['Valor Nota/Financ.'].sum().reset_index()
monthly_raw['label'] = monthly_raw['Mes'].apply(mes_label)
monthly = [{"mes": r['label'], "valor": round(r['Valor Nota/Financ.'], 2)} for _, r in monthly_raw.iterrows()]

# Mensal por status
ms_raw = df.groupby(['Mes','Status Nota'])['Valor Nota/Financ.'].sum().unstack(fill_value=0).reset_index()
if 'L' not in ms_raw.columns: ms_raw['L'] = 0
if 'A' not in ms_raw.columns: ms_raw['A'] = 0
monthly_status = [{"mes": mes_label(r['Mes']), "L": round(r['L'],2), "A": round(r['A'],2)} for _, r in ms_raw.iterrows()]

# Solicitantes
sol_raw = df.groupby('Nome (Solicitante)')['Valor Nota/Financ.'].agg(['sum','count']).reset_index()
sol_raw.columns = ['nome','valor','qtd']
sol_raw = sol_raw.sort_values('valor', ascending=False).head(15)
solicitantes = sol_raw.to_dict(orient='records')
for s in solicitantes: s['valor'] = round(s['valor'], 2)

# Sol status
ss_raw = df.groupby(['Nome (Solicitante)','Status Nota'])['Valor Nota/Financ.'].sum().unstack(fill_value=0).reset_index()
if 'L' not in ss_raw.columns: ss_raw['L'] = 0
if 'A' not in ss_raw.columns: ss_raw['A'] = 0
sol_status = [{"n": r['Nome (Solicitante)'], "L": round(r['L'],2), "A": round(r['A'],2)} for _, r in ss_raw.iterrows() if r['L']+r['A'] > 0]

# Top 5 solicitantes por mes
top5 = sol_raw.head(5)['nome'].tolist()
ms_sol_raw = df[df['Nome (Solicitante)'].isin(top5)].groupby(['Mes','Nome (Solicitante)'])['Valor Nota/Financ.'].sum().unstack(fill_value=0).reset_index()
monthly_sol = []
for _, r in ms_sol_raw.iterrows():
    rec = {"mes": mes_label(r['Mes'])}
    for n in top5:
        rec[n] = round(r.get(n, 0), 2)
    monthly_sol.append(rec)

# Natureza
nat_raw = df.groupby('Descrição (Natureza)')['Valor Nota/Financ.'].agg(['sum','count']).reset_index()
nat_raw.columns = ['n','v','q']
nat_raw = nat_raw.sort_values('v', ascending=False).head(8)
natureza = [{"n": r['n'][:35], "v": round(r['v'],2), "q": int(r['q'])} for _, r in nat_raw.iterrows()]

# Tipo operação
tipo_raw = df.groupby('Descrição (Tipo de Operação)')['Valor Nota/Financ.'].agg(['sum','count']).reset_index()
tipo_raw.columns = ['t','v','q']
tipo_raw = tipo_raw.sort_values('v', ascending=False)
tipo_op = [{"t": r['t'][:35], "v": round(r['v'],2), "q": int(r['q'])} for _, r in tipo_raw.iterrows()]

# Cidades
cid_raw = df.groupby('Nome (Cidade)')['Valor Nota/Financ.'].agg(['sum','count']).reset_index()
cid_raw.columns = ['c','v','q']
cid_raw = cid_raw.sort_values('v', ascending=False).head(15)
cidades = [{"c": r['c'], "v": round(r['v'],2), "q": int(r['q'])} for _, r in cid_raw.iterrows()]

# Parceiros
parc_raw = df.groupby('Nome Parceiro (Parceiro)')['Valor Nota/Financ.'].agg(['sum','count']).reset_index()
parc_raw.columns = ['p','v','q']
parc_raw = parc_raw.sort_values('v', ascending=False).head(10)
def clean_parc(s):
    s = str(s)
    for sub in [' CPF:','CPF:',' CNPJ:','CNPJ:']:
        if sub in s: s = s[:s.index(sub)]
    return s.strip()
parceiros = [{"p": clean_parc(r['p']), "v": round(r['v'],2), "q": int(r['q'])} for _, r in parc_raw.iterrows()]

# Áreas
areas_raw = df.groupby('Descrição (Centro de Resultado)')['Valor Nota/Financ.'].agg(['sum','count']).reset_index()
areas_raw.columns = ['a','v','q']
areas = [{"a": r['a'], "v": round(r['v'],2), "q": int(r['q'])} for _, r in areas_raw.iterrows()]

# Vencimentos próximos 60 dias
hoje = pd.Timestamp.now().normalize()
venc_raw = df[(df['Prim.Dt.Venc'] >= hoje) & (df['Prim.Dt.Venc'] <= hoje + pd.Timedelta(days=60))]
venc_g = venc_raw.groupby('Prim.Dt.Venc')['Valor Nota/Financ.'].sum().reset_index()
venc_g.columns = ['d','v']
venc_g['d'] = venc_g['d'].dt.strftime('%Y-%m-%d')
vencimentos = [{"d": r['d'], "v": round(r['v'],2)} for _, r in venc_g.iterrows()]

total_venc = sum(v['v'] for v in vencimentos)

# Serializar
JS = f"""
const EMISSAO="{emissao}";
const PERIODO="{periodo}";
const TOTAL={total_registros};
const TOTAL_VALOR={round(total_valor,2)};
const TOTAL_FIN={total_fin};
const TOTAL_AGU={total_agu};
const TOTAL_VENC={round(total_venc,2)};
const MONTHLY={json.dumps(monthly, ensure_ascii=False)};
const MONTHLY_STATUS={json.dumps(monthly_status, ensure_ascii=False)};
const SOLICITANTES={json.dumps(solicitantes, ensure_ascii=False)};
const SOL_STATUS={json.dumps(sol_status, ensure_ascii=False)};
const MONTHLY_SOL={json.dumps(monthly_sol, ensure_ascii=False)};
const TOP5={json.dumps(top5, ensure_ascii=False)};
const NATUREZA={json.dumps(natureza, ensure_ascii=False)};
const TIPO_OP={json.dumps(tipo_op, ensure_ascii=False)};
const CIDADES={json.dumps(cidades, ensure_ascii=False)};
const PARCEIROS={json.dumps(parceiros, ensure_ascii=False)};
const AREAS={json.dumps(areas, ensure_ascii=False)};
const VENCIMENTOS={json.dumps(vencimentos, ensure_ascii=False)};
"""

fmtK_val = round(total_valor/1e6, 2)
logo_src = f"data:image/webp;base64,{logo_b64}" if logo_b64 else ""
logo_tag = f'<img class="logo-img" src="{logo_src}" alt="Autodefesa Brasil">' if logo_b64 else '<div class="logo-fallback">ADB</div>'

HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Autodefesa Brasil — Painel de Pagamentos</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
:root{{--bg:#080b10;--bg2:#0e1420;--bg3:#141c2e;--border:#1e2d4a;--text:#e8edf5;--text2:#7a8ba8;--text3:#4a5f7a;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;}}
.header{{background:linear-gradient(180deg,#0a0f1a,#080b10);border-bottom:1px solid #c0392b44;padding:0 40px;position:sticky;top:0;z-index:100;backdrop-filter:blur(10px);}}
.header-inner{{max-width:1500px;margin:0 auto;display:flex;align-items:center;gap:20px;height:70px;}}
.logo-wrap{{display:flex;align-items:center;gap:14px;}}
.logo-img{{width:44px;height:44px;border-radius:8px;object-fit:cover;}}
.logo-fallback{{width:44px;height:44px;border-radius:8px;background:#c0392b;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:13px;letter-spacing:1px;}}
.logo-text strong{{font-size:15px;font-weight:800;letter-spacing:1.5px;color:var(--text);}}
.logo-text span{{font-size:10px;color:var(--text2);letter-spacing:2px;text-transform:uppercase;display:block;margin-top:3px;}}
.header-divider{{width:1px;height:36px;background:var(--border);}}
.header-title{{font-size:13px;font-weight:600;color:var(--text2);}}
.header-spacer{{flex:1;}}
.header-meta{{text-align:right;font-size:11px;color:var(--text2);line-height:1.7;}}
.header-meta strong{{color:var(--text);}}
.live-dot{{display:inline-block;width:7px;height:7px;border-radius:50%;background:#e74c3c;animation:pulse 2s infinite;margin-right:5px;}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.5;transform:scale(1.3)}}}}
.nav{{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 40px;}}
.nav-inner{{max-width:1500px;margin:0 auto;display:flex;}}
.nav-tab{{padding:14px 20px;font-size:12px;font-weight:600;color:var(--text2);cursor:pointer;border-bottom:2px solid transparent;transition:all .15s;letter-spacing:.3px;white-space:nowrap;}}
.nav-tab:hover{{color:var(--text);}}.nav-tab.active{{color:#e74c3c;border-bottom-color:#e74c3c;}}
.page{{display:none;}}.page.active{{display:block;}}
.container{{max-width:1500px;margin:0 auto;padding:28px 40px 40px;}}
.stitle{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:var(--text3);margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;}}
.stitle-bar{{width:18px;height:2px;border-radius:2px;flex-shrink:0;}}
.kpi-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;}}
.kpi-card{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:22px;position:relative;overflow:hidden;transition:transform .2s,border-color .2s;}}
.kpi-card:hover{{transform:translateY(-2px);}}
.kpi-glow{{position:absolute;top:-30px;right:-30px;width:100px;height:100px;border-radius:50%;opacity:.07;filter:blur(20px);}}
.kpi-icon{{font-size:22px;margin-bottom:10px;}}
.kpi-label{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:var(--text2);margin-bottom:8px;}}
.kpi-value{{font-size:28px;font-weight:800;line-height:1;letter-spacing:-1px;}}
.kpi-sub{{font-size:11px;color:var(--text2);margin-top:8px;}}
.kpi-bar{{height:3px;border-radius:3px;margin-top:14px;background:var(--bg3);overflow:hidden;}}
.kpi-bar-fill{{height:100%;border-radius:3px;}}
.kpi-red .kpi-value{{color:#e74c3c;}}.kpi-red .kpi-glow{{background:#e74c3c;}}.kpi-red:hover{{border-color:#e74c3c44;}}
.kpi-gold .kpi-value{{color:#f39c12;}}.kpi-gold .kpi-glow{{background:#f39c12;}}.kpi-gold:hover{{border-color:#f39c1244;}}
.kpi-green .kpi-value{{color:#2ecc71;}}.kpi-green .kpi-glow{{background:#2ecc71;}}.kpi-green:hover{{border-color:#2ecc7144;}}
.kpi-blue .kpi-value{{color:#3498db;}}.kpi-blue .kpi-glow{{background:#3498db;}}.kpi-blue:hover{{border-color:#3498db44;}}
.status-card{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:20px 24px;margin-bottom:24px;}}
.status-labels{{display:flex;gap:24px;margin-bottom:12px;flex-wrap:wrap;}}
.slabel{{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--text2);}}.slabel strong{{color:var(--text);margin-left:3px;}}
.sdot{{width:8px;height:8px;border-radius:50%;flex-shrink:0;}}
.sbar{{height:10px;border-radius:6px;background:var(--bg3);overflow:hidden;display:flex;}}.sseg{{height:100%;}}
.charts-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px;}}
.chart-card{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:22px;}}.chart-card.full{{grid-column:1/-1;}}
.chart-title{{font-size:13px;font-weight:700;margin-bottom:3px;}}.chart-sub{{font-size:11px;color:var(--text2);margin-bottom:18px;}}
.chart-wrap{{position:relative;}}.h180{{height:180px;}}.h220{{height:220px;}}.h280{{height:280px;}}.h340{{height:340px;}}
.table-card{{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:22px;margin-bottom:24px;overflow-x:auto;}}
table{{width:100%;border-collapse:collapse;font-size:12px;}}
th{{text-align:left;padding:9px 14px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--text2);border-bottom:1px solid var(--border);white-space:nowrap;}}
td{{padding:12px 14px;border-bottom:1px solid rgba(30,45,74,.5);vertical-align:middle;}}tr:last-child td{{border-bottom:none;}}tr:hover td{{background:rgba(255,255,255,.02);}}
.rank-num{{font-size:12px;font-weight:800;color:var(--text3);}}.name-cell{{font-weight:600;font-size:12px;}}.val-cell{{font-weight:700;font-size:13px;}}
.avatar{{width:30px;height:30px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;margin-right:9px;vertical-align:middle;}}
.pill{{display:inline-block;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:700;}}
.pill-green{{background:rgba(46,204,113,.12);color:#2ecc71;border:1px solid rgba(46,204,113,.25);}}.pill-gold{{background:rgba(243,156,18,.12);color:#f39c12;border:1px solid rgba(243,156,18,.25);}}
.mini-bar-wrap{{display:flex;align-items:center;gap:8px;}}.mini-bar{{flex:1;height:4px;background:var(--bg3);border-radius:3px;overflow:hidden;max-width:100px;}}.mini-bar-fill{{height:100%;border-radius:3px;}}.mval{{font-size:11px;font-weight:600;min-width:30px;}}
.venc-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px;}}
.venc-card{{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center;transition:border-color .2s,transform .2s;}}.venc-card:hover{{transform:translateY(-2px);}}.venc-card.urgent{{border-color:rgba(231,76,60,.4);}}
.venc-data{{font-size:11px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;}}
.venc-val{{font-size:20px;font-weight:800;color:#f39c12;}}.venc-val.urgent{{color:#e74c3c;}}
.no-venc{{text-align:center;padding:40px;color:var(--text2);font-size:13px;}}
.footer{{text-align:center;color:var(--text3);font-size:11px;margin-top:16px;padding-bottom:8px;}}
</style>
</head>
<body>
<div class="header"><div class="header-inner">
  <div class="logo-wrap">
    {logo_tag}
    <div class="logo-text"><strong>AUTODEFESA BRASIL</strong><span>Gestão &amp; Tecnologia em Segurança</span></div>
  </div>
  <div class="header-divider"></div>
  <div class="header-title">Painel de Pagamentos — Sankhya</div>
  <div class="header-spacer"></div>
  <a href="index.html" style="color:var(--text2);text-decoration:none;font-size:12px;border:1px solid var(--border);padding:6px 14px;border-radius:8px;">&#8592; Hub</a>
  <div class="header-meta"><span class="live-dot"></span>Emissão: <strong>{emissao}</strong><br>Período: {periodo}</div>
</div></div>

<div class="nav"><div class="nav-inner">
  <div class="nav-tab active" onclick="showPage('visao',this)">📊 Visão Geral</div>
  <div class="nav-tab" onclick="showPage('solicitantes',this)">👥 Solicitantes</div>
  <div class="nav-tab" onclick="showPage('natureza',this)">📁 Natureza &amp; Tipo</div>
  <div class="nav-tab" onclick="showPage('parceiros',this)">🤝 Parceiros</div>
  <div class="nav-tab" onclick="showPage('vencimentos',this)">📅 Vencimentos</div>
</div></div>

<div id="page-visao" class="page active"><div class="container">
  <div class="stitle"><span class="stitle-bar" style="background:#e74c3c"></span>Resumo Executivo — <span id="titPeriodo"></span></div>
  <div class="kpi-grid">
    <div class="kpi-card kpi-red"><div class="kpi-glow"></div><div class="kpi-icon">💰</div><div class="kpi-label">Volume Total</div><div class="kpi-value" id="kvTotal">—</div><div class="kpi-sub" id="kvTotalSub">—</div><div class="kpi-bar"><div class="kpi-bar-fill" style="width:100%;background:#e74c3c"></div></div></div>
    <div class="kpi-card kpi-green"><div class="kpi-glow"></div><div class="kpi-icon">✅</div><div class="kpi-label">Notas Liberadas</div><div class="kpi-value" id="kvFin">—</div><div class="kpi-sub" id="kvFinSub">—</div><div class="kpi-bar"><div class="kpi-bar-fill" id="kvFinBar" style="background:#2ecc71"></div></div></div>
    <div class="kpi-card kpi-gold"><div class="kpi-glow"></div><div class="kpi-icon">⏳</div><div class="kpi-label">Aguardando</div><div class="kpi-value" id="kvAgu">—</div><div class="kpi-sub" id="kvAguSub">—</div><div class="kpi-bar"><div class="kpi-bar-fill" id="kvAguBar" style="background:#f39c12"></div></div></div>
    <div class="kpi-card kpi-blue"><div class="kpi-glow"></div><div class="kpi-icon">📅</div><div class="kpi-label">Vence em 60 dias</div><div class="kpi-value" id="kvVenc">—</div><div class="kpi-sub" id="kvVencSub">—</div><div class="kpi-bar"><div class="kpi-bar-fill" id="kvVencBar" style="background:#3498db"></div></div></div>
  </div>
  <div class="stitle"><span class="stitle-bar" style="background:#f39c12"></span>Status das Notas</div>
  <div class="status-card">
    <div class="status-labels">
      <div class="slabel"><span class="sdot" style="background:#2ecc71"></span>Liberadas (L) <strong id="sbFin">—</strong></div>
      <div class="slabel"><span class="sdot" style="background:#f39c12"></span>Aguardando (A) <strong id="sbAgu">—</strong></div>
    </div>
    <div class="sbar"><div class="sseg" id="sbSegFin" style="background:linear-gradient(90deg,#2ecc71,#27ae60)"></div><div class="sseg" id="sbSegAgu" style="background:#f39c12"></div></div>
  </div>
  <div class="stitle"><span class="stitle-bar" style="background:#3498db"></span>Evolução Mensal</div>
  <div class="charts-grid">
    <div class="chart-card full"><div class="chart-title">Volume Financeiro por Mês</div><div class="chart-sub">Valor total negociado (R$)</div><div class="chart-wrap h280"><canvas id="cMensal"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Liberadas vs. Aguardando</div><div class="chart-sub">Status por mês</div><div class="chart-wrap h280"><canvas id="cStatusMensal"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Distribuição por Área</div><div class="chart-sub">Centro de resultado — valor total</div><div class="chart-wrap h280"><canvas id="cAreas"></canvas></div></div>
  </div>
  <div class="footer">Autodefesa Brasil — Painel Sankhya · Gerado em {emissao} · {total_registros:,} registros</div>
</div></div>

<div id="page-solicitantes" class="page"><div class="container">
  <div class="stitle"><span class="stitle-bar" style="background:#e74c3c"></span>Análise por Solicitante</div>
  <div class="charts-grid">
    <div class="chart-card"><div class="chart-title">Volume por Solicitante (Top 8)</div><div class="chart-sub">Valor total solicitado</div><div class="chart-wrap h340"><canvas id="cSolBar"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Evolução Mensal — Top 5</div><div class="chart-sub">Volume por mês por operador</div><div class="chart-wrap h340"><canvas id="cSolMensal"></canvas></div></div>
    <div class="chart-card full"><div class="chart-title">Liberado vs. Aguardando por Solicitante</div><div class="chart-sub">Composição de status</div><div class="chart-wrap h220"><canvas id="cSolStatus"></canvas></div></div>
  </div>
  <div class="stitle"><span class="stitle-bar" style="background:#f39c12"></span>Detalhamento</div>
  <div class="table-card"><table><thead><tr><th>#</th><th>Solicitante</th><th>Qtd.</th><th>Valor Total</th><th>Liberado</th><th>Aguardando</th><th>% Lib.</th></tr></thead><tbody id="solTableBody"></tbody></table></div>
  <div class="footer">Autodefesa Brasil — Painel Sankhya · Gerado em {emissao}</div>
</div></div>

<div id="page-natureza" class="page"><div class="container">
  <div class="stitle"><span class="stitle-bar" style="background:#e74c3c"></span>Por Natureza do Serviço</div>
  <div class="charts-grid">
    <div class="chart-card"><div class="chart-title">Volume por Natureza</div><div class="chart-sub">Valor financeiro por categoria</div><div class="chart-wrap h340"><canvas id="cNatBar"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Participação por Natureza</div><div class="chart-sub">Proporção no total</div><div class="chart-wrap h340"><canvas id="cNatDonut"></canvas></div></div>
  </div>
  <div class="stitle"><span class="stitle-bar" style="background:#3498db"></span>Por Tipo de Operação &amp; Cidades</div>
  <div class="charts-grid">
    <div class="chart-card"><div class="chart-title">Volume por Tipo de Operação</div><div class="chart-sub">Valor e quantidade</div><div class="chart-wrap h280"><canvas id="cTipoBar"></canvas></div></div>
    <div class="chart-card"><div class="chart-title">Top 15 Cidades</div><div class="chart-sub">Maior volume negociado</div><div class="chart-wrap h280"><canvas id="cCidades"></canvas></div></div>
  </div>
  <div class="footer">Autodefesa Brasil — Painel Sankhya · Gerado em {emissao}</div>
</div></div>

<div id="page-parceiros" class="page"><div class="container">
  <div class="stitle"><span class="stitle-bar" style="background:#e74c3c"></span>Top Parceiros</div>
  <div class="charts-grid">
    <div class="chart-card full"><div class="chart-title">Volume — Top 10 Parceiros</div><div class="chart-sub">Valor total por parceiro (R$)</div><div class="chart-wrap h280"><canvas id="cParcBar"></canvas></div></div>
  </div>
  <div class="stitle"><span class="stitle-bar" style="background:#f39c12"></span>Detalhamento</div>
  <div class="table-card"><table><thead><tr><th>#</th><th>Parceiro</th><th>Qtd.</th><th>Valor Total</th><th>Participação</th></tr></thead><tbody id="parcTableBody"></tbody></table></div>
  <div class="footer">Autodefesa Brasil — Painel Sankhya · Gerado em {emissao}</div>
</div></div>

<div id="page-vencimentos" class="page"><div class="container">
  <div class="stitle"><span class="stitle-bar" style="background:#e74c3c"></span>Vencimentos nos Próximos 60 Dias</div>
  <div class="venc-grid" id="vencCards"></div>
  <div id="noVenc" class="no-venc" style="display:none">✅ Nenhum vencimento nos próximos 60 dias.</div>
  <div class="chart-card" style="margin-bottom:24px"><div class="chart-title">Cronograma de Vencimentos</div><div class="chart-sub">Valor a vencer por data</div><div class="chart-wrap h280"><canvas id="cVenc"></canvas></div></div>
  <div class="footer">Autodefesa Brasil — Painel Sankhya · Gerado em {emissao}</div>
</div></div>

<script>
{JS}
const fmt=v=>'R$ '+v.toLocaleString('pt-BR',{{minimumFractionDigits:2,maximumFractionDigits:2}});
const fmtK=v=>v>=1e6?'R$ '+(v/1e6).toFixed(2).replace('.',',')+'M':v>=1e3?'R$ '+(v/1e3).toFixed(1).replace('.',',')+'K':fmt(v);
const sn=s=>{{const p=s.split('.');return p[0][0].toUpperCase()+p[0].slice(1).toLowerCase()+(p[1]?' '+p[1][0].toUpperCase()+'.':'');}};
const AVC=['#e74c3c','#e67e22','#f1c40f','#2ecc71','#1abc9c','#3498db','#9b59b6','#e91e63','#ff5722','#607d8b'];
const CO={{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{labels:{{color:'#7a8ba8',font:{{size:10}},padding:10,boxWidth:10}}}}}}}};
const sc=(s=false)=>{{return {{x:{{stacked:s,grid:{{color:'rgba(30,45,74,.5)'}},ticks:{{color:'#7a8ba8',font:{{size:10}}}}}},y:{{stacked:s,grid:{{color:'rgba(30,45,74,.5)'}},ticks:{{color:'#7a8ba8',font:{{size:10}},callback:v=>fmtK(v)}}}}}}}};
const scH=()=>{{return {{x:{{grid:{{color:'rgba(30,45,74,.5)'}},ticks:{{color:'#7a8ba8',font:{{size:10}},callback:v=>fmtK(v)}}}},y:{{grid:{{color:'rgba(30,45,74,.5)'}},ticks:{{color:'#7a8ba8',font:{{size:10}}}}}}}}}};
function showPage(id,tab){{document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));document.getElementById('page-'+id).classList.add('active');tab.classList.add('active');}}

// KPIs
document.getElementById('titPeriodo').textContent=PERIODO;
document.getElementById('kvTotal').textContent=fmtK(TOTAL_VALOR);
document.getElementById('kvTotalSub').textContent=TOTAL.toLocaleString('pt-BR')+' registros · ADB Matriz';
document.getElementById('kvFin').textContent=TOTAL_FIN.toLocaleString('pt-BR');
const finPct=TOTAL>0?(TOTAL_FIN/TOTAL*100).toFixed(1):0;
document.getElementById('kvFinSub').textContent=finPct+'% do total de registros';
document.getElementById('kvFinBar').style.width=finPct+'%';
document.getElementById('kvAgu').textContent=TOTAL_AGU.toLocaleString('pt-BR');
const aguPct=TOTAL>0?(TOTAL_AGU/TOTAL*100).toFixed(1):0;
document.getElementById('kvAguSub').textContent=aguPct+'% · pendentes de aprovação';
document.getElementById('kvAguBar').style.width=aguPct+'%';
document.getElementById('kvVenc').textContent=fmtK(TOTAL_VENC);
document.getElementById('kvVencSub').textContent=VENCIMENTOS.length+' datas de vencimento';
document.getElementById('kvVencBar').style.width=Math.min(TOTAL_VENC/TOTAL_VALOR*100,100)+'%';
document.getElementById('sbFin').textContent=TOTAL_FIN.toLocaleString('pt-BR');
document.getElementById('sbAgu').textContent=TOTAL_AGU.toLocaleString('pt-BR');
document.getElementById('sbSegFin').style.width=finPct+'%';
document.getElementById('sbSegAgu').style.width=aguPct+'%';

// Charts Geral
const mesL=MONTHLY.map(m=>m.mes);
new Chart(document.getElementById('cMensal'),{{type:'bar',data:{{labels:mesL,datasets:[{{label:'Volume (R$)',data:MONTHLY.map(m=>m.valor),backgroundColor:MONTHLY.map((_,i)=>i===MONTHLY.length-1?'#e74c3c':'rgba(231,76,60,.35)'),borderRadius:8,borderSkipped:false}}]}},options:{{...CO,plugins:{{...CO.plugins,legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>` ${{fmt(ctx.parsed.y)}}`}}}}}},scales:sc()}}}});
new Chart(document.getElementById('cStatusMensal'),{{type:'bar',data:{{labels:mesL,datasets:[{{label:'Liberadas',data:MONTHLY_STATUS.map(m=>m.L),backgroundColor:'rgba(46,204,113,.7)',borderRadius:4,stack:'a'}},{{label:'Aguardando',data:MONTHLY_STATUS.map(m=>m.A),backgroundColor:'rgba(243,156,18,.8)',stack:'a'}}]}},options:{{...CO,scales:sc(true),plugins:{{...CO.plugins,legend:{{position:'bottom',labels:{{color:'#7a8ba8',font:{{size:10}},padding:8,boxWidth:10}}}}}}}}}});
new Chart(document.getElementById('cAreas'),{{type:'doughnut',data:{{labels:AREAS.map(a=>a.a),datasets:[{{data:AREAS.map(a=>a.v),backgroundColor:['#e74c3c','#3498db','#f39c12','#9b59b6','#1abc9c'],borderColor:'#0e1420',borderWidth:3}}]}},options:{{...CO,cutout:'65%',plugins:{{legend:{{position:'right',labels:{{color:'#7a8ba8',font:{{size:10}},padding:8,boxWidth:8}}}},tooltip:{{callbacks:{{label:ctx=>` ${{ctx.label}}: ${{fmtK(ctx.parsed)}}`}}}}}}}}}});

// Solicitantes
const top8=SOLICITANTES.slice(0,8);
new Chart(document.getElementById('cSolBar'),{{type:'bar',indexAxis:'y',data:{{labels:top8.map(s=>sn(s.nome)),datasets:[{{label:'Valor',data:top8.map(s=>s.valor),backgroundColor:top8.map((_,i)=>AVC[i]),borderRadius:5,borderSkipped:false}}]}},options:{{...CO,plugins:{{...CO.plugins,legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>` ${{fmt(ctx.parsed.x)}}`}}}}}},scales:scH()}}}});
const t5c=['#e74c3c','#3498db','#f39c12','#2ecc71','#9b59b6'];
new Chart(document.getElementById('cSolMensal'),{{type:'line',data:{{labels:mesL,datasets:TOP5.map((n,i)=>{{return {{label:sn(n),data:MONTHLY_SOL.map(m=>m[n]||0),borderColor:t5c[i],backgroundColor:t5c[i]+'22',pointRadius:4,tension:.4,fill:false,borderWidth:2}}}})}},options:{{...CO,scales:sc(),plugins:{{...CO.plugins,legend:{{position:'bottom',labels:{{color:'#7a8ba8',font:{{size:10}},padding:8,boxWidth:10}}}}}}}}}});
new Chart(document.getElementById('cSolStatus'),{{type:'bar',data:{{labels:SOL_STATUS.map(s=>sn(s.n)),datasets:[{{label:'Liberado',data:SOL_STATUS.map(s=>s.L),backgroundColor:'rgba(46,204,113,.75)',borderRadius:4,stack:'a'}},{{label:'Aguardando',data:SOL_STATUS.map(s=>s.A),backgroundColor:'rgba(243,156,18,.8)',stack:'a'}}]}},options:{{...CO,scales:sc(true),plugins:{{...CO.plugins,legend:{{position:'bottom',labels:{{color:'#7a8ba8',font:{{size:10}},padding:8,boxWidth:10}}}}}}}}}});

const stb=document.getElementById('solTableBody');
SOLICITANTES.forEach((s,i)=>{{
  const ss=SOL_STATUS.find(x=>x.n===s.nome)||{{A:0,L:0}};
  const pct=s.valor>0?Math.round((ss.L/s.valor)*100):100;
  const clr=AVC[i%AVC.length];
  const ini=s.nome.split('.').map(p=>p[0]).join('').slice(0,2).toUpperCase();
  const medal=i===0?'🥇':i===1?'🥈':i===2?'🥉':i+1;
  stb.innerHTML+=`<tr><td class="rank-num">${{medal}}</td><td><span class="avatar" style="background:${{clr}}22;color:${{clr}};border:1px solid ${{clr}}44">${{ini}}</span><span class="name-cell">${{sn(s.nome)}}</span></td><td>${{s.qtd.toLocaleString('pt-BR')}}</td><td class="val-cell" style="color:${{clr}}">${{fmt(s.valor)}}</td><td><span class="pill pill-green">${{fmtK(ss.L||0)}}</span></td><td>${{ss.A>0?`<span class="pill pill-gold">${{fmtK(ss.A)}}</span>`:'<span style="color:var(--text3)">—</span>'}}</td><td><div class="mini-bar-wrap"><div class="mini-bar"><div class="mini-bar-fill" style="width:${{pct}}%;background:${{pct>90?'#2ecc71':'#f39c12'}}"></div></div><span class="mval" style="color:${{pct>90?'#2ecc71':'#f39c12'}}">${{pct}}%</span></div></td></tr>`;
}});

// Natureza
new Chart(document.getElementById('cNatBar'),{{type:'bar',indexAxis:'y',data:{{labels:NATUREZA.map(n=>n.n),datasets:[{{label:'Valor',data:NATUREZA.map(n=>n.v),backgroundColor:AVC,borderRadius:5,borderSkipped:false}}]}},options:{{...CO,plugins:{{...CO.plugins,legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>` ${{fmt(ctx.parsed.x)}}`}}}}}},scales:scH()}}}});
new Chart(document.getElementById('cNatDonut'),{{type:'doughnut',data:{{labels:NATUREZA.map(n=>n.n),datasets:[{{data:NATUREZA.map(n=>n.v),backgroundColor:AVC,borderColor:'#0e1420',borderWidth:3}}]}},options:{{...CO,cutout:'60%',plugins:{{legend:{{position:'bottom',labels:{{color:'#7a8ba8',font:{{size:9}},padding:8,boxWidth:8}}}},tooltip:{{callbacks:{{label:ctx=>` ${{fmtK(ctx.parsed)}}`}}}}}}}}}});
new Chart(document.getElementById('cTipoBar'),{{type:'bar',data:{{labels:TIPO_OP.map(t=>t.t),datasets:[{{label:'Valor (R$)',data:TIPO_OP.map(t=>t.v),backgroundColor:'rgba(231,76,60,.7)',borderRadius:5,yAxisID:'y'}},{{label:'Qtd.',data:TIPO_OP.map(t=>t.q),backgroundColor:'rgba(52,152,219,.5)',borderRadius:5,yAxisID:'y2'}}]}},options:{{...CO,scales:{{x:{{grid:{{color:'rgba(30,45,74,.5)'}},ticks:{{color:'#7a8ba8',font:{{size:9}}}}}},y:{{grid:{{color:'rgba(30,45,74,.5)'}},ticks:{{color:'#e74c3c',font:{{size:9}},callback:v=>fmtK(v)}},position:'left'}},y2:{{ticks:{{color:'#3498db',font:{{size:9}}}},position:'right',grid:{{drawOnChartArea:false}}}}}},plugins:{{...CO.plugins,legend:{{position:'bottom',labels:{{color:'#7a8ba8',font:{{size:10}},padding:10,boxWidth:10}}}}}}}}}});
new Chart(document.getElementById('cCidades'),{{type:'bar',indexAxis:'y',data:{{labels:CIDADES.map(c=>c.c),datasets:[{{label:'Valor',data:CIDADES.map(c=>c.v),backgroundColor:CIDADES.map((_,i)=>`hsl(${{350-i*8}},70%,${{58-i*1.5}}%)`),borderRadius:4,borderSkipped:false}}]}},options:{{...CO,plugins:{{...CO.plugins,legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>` ${{fmt(ctx.parsed.x)}} (${{CIDADES[ctx.dataIndex].q}} notas)`}}}}}},scales:scH()}}}});

// Parceiros
new Chart(document.getElementById('cParcBar'),{{type:'bar',data:{{labels:PARCEIROS.map(p=>p.p.split(' ').slice(0,3).join(' ')),datasets:[{{label:'Valor',data:PARCEIROS.map(p=>p.v),backgroundColor:PARCEIROS.map((_,i)=>AVC[i%AVC.length]),borderRadius:6,borderSkipped:false}}]}},options:{{...CO,plugins:{{...CO.plugins,legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>` ${{fmt(ctx.parsed.y)}} (${{PARCEIROS[ctx.dataIndex].q}} notas)`}}}}}},scales:sc()}}}});
const ptb=document.getElementById('parcTableBody');
PARCEIROS.forEach((p,i)=>{{
  const clr=AVC[i%AVC.length];const medal=i===0?'🥇':i===1?'🥈':i===2?'🥉':i+1;
  ptb.innerHTML+=`<tr><td class="rank-num">${{medal}}</td><td class="name-cell" style="color:${{clr}}">${{p.p}}</td><td>${{p.q.toLocaleString('pt-BR')}}</td><td class="val-cell">${{fmt(p.v)}}</td><td><div class="mini-bar-wrap"><div class="mini-bar" style="max-width:120px"><div class="mini-bar-fill" style="width:${{Math.round(p.v/PARCEIROS[0].v*100)}}%;background:${{clr}}"></div></div><span class="mval" style="color:${{clr}}">${{(p.v/PARCEIROS[0].v*100).toFixed(0)}}%</span></div></td></tr>`;
}});

// Vencimentos
const vcEl=document.getElementById('vencCards');
if(VENCIMENTOS.length===0){{
  document.getElementById('noVenc').style.display='block';
  vcEl.style.display='none';
}} else {{
  VENCIMENTOS.forEach((v,i)=>{{
    const d=new Date(v.d+'T12:00:00');
    const lb=d.toLocaleDateString('pt-BR',{{day:'2-digit',month:'short',weekday:'short'}});
    const urg=i<2;
    vcEl.innerHTML+=`<div class="venc-card${{urg?' urgent':''}}"><div class="venc-data">${{lb}}</div><div class="venc-val${{urg?' urgent':''}}">${{fmtK(v.v)}}</div></div>`;
  }});
}}
if(VENCIMENTOS.length>0){{
  new Chart(document.getElementById('cVenc'),{{type:'bar',data:{{labels:VENCIMENTOS.map(v=>{{const d=new Date(v.d+'T12:00:00');return d.toLocaleDateString('pt-BR',{{day:'2-digit',month:'short'}})}}),datasets:[{{label:'Valor a Vencer',data:VENCIMENTOS.map(v=>v.v),backgroundColor:VENCIMENTOS.map((_,i)=>i<2?'rgba(231,76,60,.85)':'rgba(243,156,18,.7)'),borderRadius:8,borderSkipped:false}}]}},options:{{...CO,plugins:{{...CO.plugins,legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>` ${{fmt(ctx.parsed.y)}}`}}}}}},scales:sc()}}}});
}}
</script></body></html>"""

with open(SAIDA, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"✅ Painel gerado: {SAIDA}")
print(f"   Volume total : R$ {total_valor:,.2f}")
print(f"   Registros    : {total_registros:,}")
print(f"   Liberadas    : {total_fin:,} ({total_fin/total_registros*100:.1f}%)")
print(f"   Aguardando   : {total_agu:,}")
print(f"   Vencimentos  : {len(vencimentos)} datas · R$ {total_venc:,.2f}")
print(f"   Período      : {periodo}")
print(f"\n📂 Abra '{SAIDA}' no navegador ou suba no Netlify via GitHub.")
