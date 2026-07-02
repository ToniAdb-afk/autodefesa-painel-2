HEAD_TPL = '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>Autodefesa Brasil — Indisponibilidade</title>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>\n<style>\n@import url(\'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap\');\n:root{--bg:#080b10;--bg2:#0e1420;--bg3:#141c2e;--border:#1e2d4a;--text:#e8edf5;--text2:#7a8ba8;--text3:#4a5f7a;--red:#e74c3c;--orange:#e67e22;--green:#2ecc71;--purple:#9b59b6;--blue:#3498db;}\n*{margin:0;padding:0;box-sizing:border-box;}\nbody{font-family:\'Inter\',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding-bottom:48px;}\n.header{background:linear-gradient(180deg,#0a0f1a,#080b10);border-bottom:1px solid #9b59b644;padding:0 40px;position:sticky;top:0;z-index:100;backdrop-filter:blur(10px);}\n.header-inner{max-width:1500px;margin:0 auto;display:flex;align-items:center;gap:20px;height:70px;}\n.back-btn{display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--text2);font-size:12px;font-weight:600;padding:6px 14px;border-radius:8px;border:1px solid var(--border);transition:all .15s;}\n.back-btn:hover{color:var(--text);border-color:var(--text2);}\n.logo-text strong{font-size:15px;font-weight:800;letter-spacing:1.5px;color:var(--text);}\n.logo-text span{font-size:10px;color:var(--text2);letter-spacing:2px;text-transform:uppercase;display:block;margin-top:3px;}\n.header-divider{width:1px;height:36px;background:var(--border);}\n.header-title{font-size:13px;font-weight:600;color:var(--text2);}\n.header-spacer{flex:1;}\n.header-meta{text-align:right;font-size:11px;color:var(--text2);line-height:1.7;}\n.header-meta strong{color:var(--text);}\n.live-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#e74c3c;animation:pulse 2s infinite;margin-right:5px;}\n@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.3)}}\n.nav{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 40px;}\n.nav-inner{max-width:1500px;margin:0 auto;display:flex;}\n.nav-tab{padding:14px 20px;font-size:12px;font-weight:600;color:var(--text2);cursor:pointer;border-bottom:2px solid transparent;transition:all .15s;white-space:nowrap;}\n.nav-tab:hover{color:var(--text);}.nav-tab.active{color:#9b59b6;border-bottom-color:#9b59b6;}\n.page{display:none;}.page.active{display:block;}\n.container{max-width:1500px;margin:0 auto;padding:28px 40px 0;}\n.stitle{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:var(--text3);margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;}\n.stitle-bar{width:18px;height:2px;border-radius:2px;flex-shrink:0;}\n.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:24px;}\n.kpi-card{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:20px;position:relative;overflow:hidden;transition:transform .2s,border-color .2s;}\n.kpi-card:hover{transform:translateY(-2px);}\n.kpi-glow{position:absolute;top:-30px;right:-30px;width:100px;height:100px;border-radius:50%;opacity:.07;filter:blur(20px);}\n.kpi-icon{font-size:20px;margin-bottom:10px;}\n.kpi-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:var(--text2);margin-bottom:8px;}\n.kpi-value{font-size:28px;font-weight:800;line-height:1;letter-spacing:-1px;}\n.kpi-sub{font-size:10px;color:var(--text2);margin-top:6px;}\n.kpi-bar{height:3px;border-radius:3px;margin-top:12px;background:var(--bg3);overflow:hidden;}\n.kpi-bar-fill{height:100%;border-radius:3px;}\n.kpi-red .kpi-value{color:var(--red);}.kpi-red .kpi-glow{background:var(--red);}.kpi-red:hover{border-color:#e74c3c44;}\n.kpi-orange .kpi-value{color:var(--orange);}.kpi-orange .kpi-glow{background:var(--orange);}.kpi-orange:hover{border-color:#e67e2244;}\n.kpi-green .kpi-value{color:var(--green);}.kpi-green .kpi-glow{background:var(--green);}.kpi-green:hover{border-color:#2ecc7144;}\n.kpi-purple .kpi-value{color:var(--purple);}.kpi-purple .kpi-glow{background:var(--purple);}.kpi-purple:hover{border-color:#9b59b644;}\n.kpi-blue .kpi-value{color:var(--blue);}.kpi-blue .kpi-glow{background:var(--blue);}.kpi-blue:hover{border-color:#3498db44;}\n.status-card{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:18px 22px;margin-bottom:24px;}\n.status-labels{display:flex;gap:20px;margin-bottom:10px;flex-wrap:wrap;}\n.slabel{display:flex;align-items:center;gap:7px;font-size:12px;color:var(--text2);}.slabel strong{color:var(--text);margin-left:3px;}\n.sdot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}\n.sbar{height:10px;border-radius:6px;background:var(--bg3);overflow:hidden;display:flex;}.sseg{height:100%;}\n.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px;}\n.chart-card{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:22px;}.chart-card.full{grid-column:1/-1;}\n.chart-title{font-size:13px;font-weight:700;margin-bottom:3px;}.chart-sub{font-size:11px;color:var(--text2);margin-bottom:18px;}\n.chart-wrap{position:relative;}.h220{height:220px;}.h260{height:260px;}.h300{height:300px;}\n.table-card{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:22px;margin-bottom:24px;overflow-x:auto;}\ntable{width:100%;border-collapse:collapse;font-size:12px;}\nth{text-align:left;padding:9px 14px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:var(--text2);border-bottom:1px solid var(--border);white-space:nowrap;}\ntd{padding:11px 14px;border-bottom:1px solid rgba(30,45,74,.5);vertical-align:middle;}tr:last-child td{border-bottom:none;}tr:hover td{background:rgba(255,255,255,.02);}\n.pill{display:inline-block;padding:2px 10px;border-radius:20px;font-size:10px;font-weight:700;}\n.pill-red{background:rgba(231,76,60,.12);color:#e74c3c;border:1px solid rgba(231,76,60,.25);}\n.pill-green{background:rgba(46,204,113,.12);color:#2ecc71;border:1px solid rgba(46,204,113,.25);}\n.pill-orange{background:rgba(230,126,34,.12);color:#e67e22;border:1px solid rgba(230,126,34,.25);}\n.pill-blue{background:rgba(52,152,219,.12);color:#3498db;border:1px solid rgba(52,152,219,.25);}\n.hist-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin-bottom:24px;}\n.hist-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px;transition:border-color .2s;}\n.hist-card:hover{border-color:#9b59b655;}\n.hist-data{font-size:11px;font-weight:700;color:var(--text2);margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px;}\n.hist-row{display:flex;justify-content:space-between;align-items:center;font-size:11px;margin-bottom:4px;}\n.hist-label{color:var(--text2);}\n.hist-val{font-weight:700;}\n.hist-val.red{color:var(--red);}.hist-val.orange{color:var(--orange);}.hist-val.green{color:var(--green);}\n.no-hist{text-align:center;padding:40px;color:var(--text2);font-size:13px;}\n.footer{text-align:center;color:var(--text3);font-size:11px;margin-top:16px;}\n</style>\n</head>\n<body>\n<div class="header"><div class="header-inner">\n  <a href="index.html" class="back-btn">← Voltar</a>\n  <div class="header-divider"></div>\n  <div class="logo-text"><strong>🛡️ AUTODEFESA BRASIL</strong><span>Indisponibilidade — Alarmes &amp; CFTV</span></div>\n  <div class="header-spacer"></div>\n  <div class="header-meta"><span class="live-dot"></span>Ref. CFTV: <strong id="hRef">—</strong><br>Emissão: <strong id="hEmissao">—</strong></div>\n</div></div>\n\n<div class="nav"><div class="nav-inner">\n  <div class="nav-tab active" onclick="showPage(\'visao\',this)">📊 Visão Geral</div>\n  <div class="nav-tab" onclick="showPage(\'alarmes\',this)">🚨 Alarmes</div>\n  <div class="nav-tab" onclick="showPage(\'cftv\',this)">📹 CFTV Offline</div>\n  <div class="nav-tab" onclick="showPage(\'historico\',this)">📅 Histórico</div>\n</div></div>\n\n<!-- VISÃO GERAL -->\n<div id="page-visao" class="page active"><div class="container">\n  <div class="stitle"><span class="stitle-bar" style="background:#9b59b6"></span>Resumo do Dia — <span id="titData"></span></div>\n  <div class="kpi-grid">\n    <div class="kpi-card kpi-red"><div class="kpi-glow"></div><div class="kpi-icon">🚨</div><div class="kpi-label">Alarmes Abertos</div><div class="kpi-value" id="kvAb">—</div><div class="kpi-sub">Aguardando resolução</div><div class="kpi-bar"><div class="kpi-bar-fill" id="kvAbBar" style="background:#e74c3c"></div></div></div>\n    <div class="kpi-card kpi-green"><div class="kpi-glow"></div><div class="kpi-icon">✅</div><div class="kpi-label">Alarmes Fechados</div><div class="kpi-value" id="kvFe">—</div><div class="kpi-sub">Resolvidos no dia</div><div class="kpi-bar"><div class="kpi-bar-fill" id="kvFeBar" style="background:#2ecc71"></div></div></div>\n    <div class="kpi-card kpi-red"><div class="kpi-glow"></div><div class="kpi-icon">📹</div><div class="kpi-label">CFTV Offline</div><div class="kpi-value" id="kvCOff">—</div><div class="kpi-sub" id="kvCOffSub">—</div><div class="kpi-bar"><div class="kpi-bar-fill" id="kvCOffBar" style="background:#e74c3c"></div></div></div>\n    <div class="kpi-card kpi-green"><div class="kpi-glow"></div><div class="kpi-icon">🟢</div><div class="kpi-label">CFTV Online</div><div class="kpi-value" id="kvCOn">—</div><div class="kpi-sub" id="kvCOnSub">—</div><div class="kpi-bar"><div class="kpi-bar-fill" id="kvCOnBar" style="background:#2ecc71"></div></div></div>\n    <div class="kpi-card kpi-purple"><div class="kpi-glow"></div><div class="kpi-icon">📡</div><div class="kpi-label">Total Gravadores</div><div class="kpi-value" id="kvTot">—</div><div class="kpi-sub">Monitorados</div><div class="kpi-bar"><div class="kpi-bar-fill" style="width:100%;background:#9b59b6"></div></div></div>\n  </div>\n\n  <div class="stitle"><span class="stitle-bar" style="background:#e74c3c"></span>Status Geral</div>\n  <div class="status-card">\n    <div class="status-labels">\n      <div class="slabel"><span class="sdot" style="background:#2ecc71"></span>CFTV Online<strong id="sbOn">—</strong></div>\n      <div class="slabel"><span class="sdot" style="background:#e74c3c"></span>CFTV Offline<strong id="sbOff">—</strong></div>\n      <div class="slabel"><span class="sdot" style="background:#f39c12"></span>Alarmes Abertos<strong id="sbAl">—</strong></div>\n      <div class="slabel"><span class="sdot" style="background:#2ecc71"></span>Alarmes Fechados<strong id="sbFe">—</strong></div>\n    </div>\n    <div class="sbar">\n      <div class="sseg" id="sbSegOn" style="background:#2ecc71"></div>\n      <div class="sseg" id="sbSegOff" style="background:#e74c3c"></div>\n    </div>\n  </div>\n\n  <div class="charts-grid">\n    <div class="chart-card"><div class="chart-title">Alarmes por Cliente</div><div class="chart-sub">Abertos vs. Fechados por empresa</div><div class="chart-wrap h260"><canvas id="cAlCli"></canvas></div></div>\n    <div class="chart-card"><div class="chart-title">CFTV Status Geral</div><div class="chart-sub">Online vs. Offline — proporção total</div><div class="chart-wrap h260"><canvas id="cCftvDonut"></canvas></div></div>\n    <div class="chart-card full"><div class="chart-title">Top Cidades com CFTV Offline</div><div class="chart-sub">Quantidade de gravadores offline por cidade</div><div class="chart-wrap h220"><canvas id="cCidOff"></canvas></div></div>\n  </div>\n  <div class="footer">Autodefesa Brasil · Indisponibilidade · Emissão: <span id="ftEmissao"></span></div>\n</div></div>\n\n<!-- ALARMES -->\n<div id="page-alarmes" class="page"><div class="container">\n  <div class="stitle"><span class="stitle-bar" style="background:#e74c3c"></span>Alarmes Abertos — Pendentes de Resolução</div>\n  <div class="table-card"><table><thead><tr><th>#</th><th>Conta</th><th>Cliente</th><th>Data Abertura</th><th>Atendimento</th><th>Status</th></tr></thead><tbody id="tbAbertas"></tbody></table></div>\n  <div class="stitle"><span class="stitle-bar" style="background:#2ecc71"></span>Alarmes Fechados — Resolvidos</div>\n  <div class="table-card"><table><thead><tr><th>#</th><th>Conta</th><th>Cliente</th><th>Data Abertura</th><th>Data Fechamento</th><th>SLA</th></tr></thead><tbody id="tbFechadas"></tbody></table></div>\n  <div class="footer">Autodefesa Brasil · Indisponibilidade · Emissão: <span id="ftEmissao2"></span></div>\n</div></div>\n\n<!-- CFTV -->\n<div id="page-cftv" class="page"><div class="container">\n  <div class="stitle"><span class="stitle-bar" style="background:#e74c3c"></span>Gravadores CFTV Offline — <span id="titCftv"></span></div>\n  <div class="table-card"><table><thead><tr><th>#</th><th>Cliente / Loja</th><th>Cidade</th><th>IP</th><th>Última Verificação</th><th>Status</th></tr></thead><tbody id="tbCftv"></tbody></table></div>\n  <div class="footer">Autodefesa Brasil · Indisponibilidade · Emissão: <span id="ftEmissao3"></span></div>\n</div></div>\n\n<!-- HISTÓRICO -->\n<div id="page-historico" class="page"><div class="container">\n  <div class="stitle"><span class="stitle-bar" style="background:#9b59b6"></span>Histórico de Indisponibilidade — Registro Diário</div>\n  <div style="background:rgba(155,89,182,.08);border:1px solid rgba(155,89,182,.25);border-radius:12px;padding:16px 20px;margin-bottom:20px;font-size:12px;color:var(--text2);line-height:1.7;">\n    📌 O histórico é acumulado automaticamente pelo GitHub Actions a cada atualização da planilha e fica salvo no repositório — é o mesmo para qualquer pessoa que abrir o painel, em qualquer navegador ou dispositivo.\n  </div>\n  <div class="hist-grid" id="histGrid"></div>\n  <div id="noHist" class="no-hist" style="display:none">📭 Nenhum histórico registrado ainda. As próximas atualizações da planilha vão começar a compor o mapa de indisponibilidade.</div>\n  <div class="charts-grid" id="histCharts" style="display:none">\n    <div class="chart-card full"><div class="chart-title">Evolução Histórica — CFTV Offline</div><div class="chart-sub">Quantidade de gravadores offline por dia</div><div class="chart-wrap h260"><canvas id="cHistCftv"></canvas></div></div>\n    <div class="chart-card full"><div class="chart-title">Evolução Histórica — Alarmes Abertos</div><div class="chart-sub">Quantidade de alarmes abertos por dia</div><div class="chart-wrap h260"><canvas id="cHistAl"></canvas></div></div>\n  </div>\n  <div class="footer">Autodefesa Brasil · Indisponibilidade · Emissão: <span id="ftEmissao4"></span></div>\n</div></div>\n\n<script>\n\n'

TAIL_TPL = '\nconst CO={responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:\'#7a8ba8\',font:{size:10},padding:8,boxWidth:10}}}};\nconst sc=(s=false)=>({x:{stacked:s,grid:{color:\'rgba(30,45,74,.5)\'},ticks:{color:\'#7a8ba8\',font:{size:10}}},y:{stacked:s,grid:{color:\'rgba(30,45,74,.5)\'},ticks:{color:\'#7a8ba8\',font:{size:10}}}});\nconst scH=()=>({x:{grid:{color:\'rgba(30,45,74,.5)\'},ticks:{color:\'#7a8ba8\',font:{size:10}}},y:{grid:{color:\'rgba(30,45,74,.5)\'},ticks:{color:\'#7a8ba8\',font:{size:10}}}});\nfunction showPage(id,tab){document.querySelectorAll(\'.page\').forEach(p=>p.classList.remove(\'active\'));document.querySelectorAll(\'.nav-tab\').forEach(t=>t.classList.remove(\'active\'));document.getElementById(\'page-\'+id).classList.add(\'active\');tab.classList.add(\'active\');}\n\n// KPIs\ndocument.getElementById(\'hRef\').textContent=DATA_REF;\ndocument.getElementById(\'hEmissao\').textContent=EMISSAO;\ndocument.getElementById(\'titData\').textContent=DATA_REF;\ndocument.getElementById(\'titCftv\').textContent=OFFLINE_CFTV+\' unidades offline\';\n[\'ftEmissao\',\'ftEmissao2\',\'ftEmissao3\',\'ftEmissao4\'].forEach(id=>document.getElementById(id).textContent=EMISSAO);\n\ndocument.getElementById(\'kvAb\').textContent=ABERTAS_AL;\ndocument.getElementById(\'kvAbBar\').style.width=Math.round(ABERTAS_AL/TOTAL_AL*100)+\'%\';\ndocument.getElementById(\'kvFe\').textContent=FECHADAS_AL;\ndocument.getElementById(\'kvFeBar\').style.width=Math.round(FECHADAS_AL/TOTAL_AL*100)+\'%\';\ndocument.getElementById(\'kvCOff\').textContent=OFFLINE_CFTV;\ndocument.getElementById(\'kvCOffSub\').textContent=PCT_OFF+\'% do total monitorado\';\ndocument.getElementById(\'kvCOffBar\').style.width=PCT_OFF+\'%\';\ndocument.getElementById(\'kvCOn\').textContent=ONLINE_CFTV;\ndocument.getElementById(\'kvCOnSub\').textContent=(100-PCT_OFF).toFixed(1)+\'% do total monitorado\';\ndocument.getElementById(\'kvCOnBar\').style.width=(100-PCT_OFF)+\'%\';\ndocument.getElementById(\'kvTot\').textContent=TOTAL_CFTV;\n\ndocument.getElementById(\'sbOn\').textContent=ONLINE_CFTV;\ndocument.getElementById(\'sbOff\').textContent=OFFLINE_CFTV;\ndocument.getElementById(\'sbAl\').textContent=ABERTAS_AL;\ndocument.getElementById(\'sbFe\').textContent=FECHADAS_AL;\ndocument.getElementById(\'sbSegOn\').style.width=(ONLINE_CFTV/TOTAL_CFTV*100).toFixed(1)+\'%\';\ndocument.getElementById(\'sbSegOff\').style.width=(OFFLINE_CFTV/TOTAL_CFTV*100).toFixed(1)+\'%\';\n\n// Charts Geral\nnew Chart(document.getElementById(\'cAlCli\'),{type:\'bar\',data:{labels:AL_CLI.map(x=>x.c),datasets:[{label:\'Abertos\',data:AL_CLI.map(x=>x.ab),backgroundColor:\'rgba(231,76,60,.75)\',borderRadius:4,stack:\'a\'},{label:\'Fechados\',data:AL_CLI.map(x=>x.fe),backgroundColor:\'rgba(46,204,113,.7)\',borderRadius:4,stack:\'a\'}]},options:{...CO,scales:sc(true),plugins:{...CO.plugins,legend:{position:\'bottom\',labels:{color:\'#7a8ba8\',font:{size:10},padding:10,boxWidth:10}}}}});\nnew Chart(document.getElementById(\'cCftvDonut\'),{type:\'doughnut\',data:{labels:[\'Online\',\'Offline\'],datasets:[{data:[ONLINE_CFTV,OFFLINE_CFTV],backgroundColor:[\'#2ecc71\',\'#e74c3c\'],borderColor:\'#0e1420\',borderWidth:3}]},options:{...CO,cutout:\'65%\',plugins:{legend:{position:\'right\',labels:{color:\'#7a8ba8\',font:{size:11},padding:12,boxWidth:10}},tooltip:{callbacks:{label:ctx=>` ${ctx.label}: ${ctx.parsed} (${(ctx.parsed/TOTAL_CFTV*100).toFixed(1)}%)`}}}}});\nnew Chart(document.getElementById(\'cCidOff\'),{type:\'bar\',indexAxis:\'y\',data:{labels:CFTV_CID.map(x=>x.c),datasets:[{label:\'Offline\',data:CFTV_CID.map(x=>x.q),backgroundColor:CFTV_CID.map((_,i)=>`hsl(${350-i*6},70%,${55-i*1}%)`),borderRadius:4,borderSkipped:false}]},options:{...CO,plugins:{...CO.plugins,legend:{display:false}},scales:scH()}});\n\n// Tabela alarmes abertos\nconst tbAb=document.getElementById(\'tbAbertas\');\nAL_AB.forEach((r,i)=>{tbAb.innerHTML+=`<tr><td style="color:var(--text3);font-weight:700">${i+1}</td><td style="font-size:11px;max-width:300px;word-break:break-word">${r.conta}</td><td><span class="pill pill-blue">${r.cli}</span></td><td>${r.dt}</td><td>${r.at}</td><td><span class="pill pill-red">Aberta</span></td></tr>`;});\nif(AL_AB.length===0) tbAb.innerHTML=\'<tr><td colspan="6" style="text-align:center;color:var(--text2);padding:20px">✅ Nenhum alarme aberto</td></tr>\';\n\n// Tabela alarmes fechados\nconst tbFe=document.getElementById(\'tbFechadas\');\nAL_FE.forEach((r,i)=>{tbFe.innerHTML+=`<tr><td style="color:var(--text3);font-weight:700">${i+1}</td><td style="font-size:11px;max-width:280px;word-break:break-word">${r.conta}</td><td><span class="pill pill-blue">${r.cli}</span></td><td>${r.dt}</td><td>${r.dtf}</td><td><span class="pill pill-green">${r.sla}</span></td></tr>`;});\n\n// Tabela CFTV offline\nconst tbC=document.getElementById(\'tbCftv\');\nCFTV_OFF.forEach((r,i)=>{tbC.innerHTML+=`<tr><td style="color:var(--text3);font-weight:700">${i+1}</td><td style="font-size:11px">${r.Cliente}</td><td>${r.Cidade}</td><td style="font-family:monospace;font-size:11px;color:var(--text2)">${r.IP}</td><td style="font-size:11px">${r[\'Última Verificação\']}</td><td><span class="pill pill-red">OFFLINE</span></td></tr>`;});\n\n// ── HISTÓRICO ─────────────────────────────────────────────────────────\n// O histórico agora vem pronto do servidor (historico_indisponibilidade.json,\n// versionado no repositório e atualizado pelo próprio workflow a cada\n// execução). Todos os usuários veem o mesmo histórico, em qualquer\n// navegador ou dispositivo — não depende mais de localStorage.\n\nfunction renderHistorico(){\n  const hist=HIST_SERVIDOR;\n  const grid=document.getElementById(\'histGrid\');\n  const noHist=document.getElementById(\'noHist\');\n  const charts=document.getElementById(\'histCharts\');\n\n  if(hist.length===0){\n    noHist.style.display=\'block\';\n    charts.style.display=\'none\';\n    return;\n  }\n  noHist.style.display=\'none\';\n  charts.style.display=\'grid\';\n\n  const sorted=[...hist].sort((a,b)=>b.data.localeCompare(a.data));\n  sorted.forEach(h=>{\n    const d=new Date(h.data+\'T12:00:00\');\n    const label=d.toLocaleDateString(\'pt-BR\',{weekday:\'short\',day:\'2-digit\',month:\'short\'});\n    const pctOff=h.cftv_total>0?(h.cftv_offline/h.cftv_total*100).toFixed(1):0;\n    grid.innerHTML+=`<div class="hist-card">\n      <div class="hist-data">${label}</div>\n      <div class="hist-row"><span class="hist-label">🚨 Alarmes abertos</span><span class="hist-val red">${h.alarmes_abertas}</span></div>\n      <div class="hist-row"><span class="hist-label">✅ Alarmes fechados</span><span class="hist-val green">${h.alarmes_fechadas}</span></div>\n      <div class="hist-row"><span class="hist-label">📹 CFTV offline</span><span class="hist-val red">${h.cftv_offline}</span></div>\n      <div class="hist-row"><span class="hist-label">🟢 CFTV online</span><span class="hist-val green">${h.cftv_online}</span></div>\n      <div class="hist-row"><span class="hist-label">% offline</span><span class="hist-val orange">${pctOff}%</span></div>\n    </div>`;\n  });\n\n  // Gráficos histórico (ordem cronológica)\n  const chrono=[...hist].sort((a,b)=>a.data.localeCompare(b.data));\n  const labels=chrono.map(h=>{const d=new Date(h.data+\'T12:00:00\');return d.toLocaleDateString(\'pt-BR\',{day:\'2-digit\',month:\'short\'});});\n\n  new Chart(document.getElementById(\'cHistCftv\'),{type:\'line\',data:{labels,datasets:[{label:\'CFTV Offline\',data:chrono.map(h=>h.cftv_offline),borderColor:\'#e74c3c\',backgroundColor:\'rgba(231,76,60,.15)\',pointRadius:5,pointHoverRadius:8,tension:.3,fill:true,borderWidth:2}]},options:{...CO,scales:sc(),plugins:{...CO.plugins,legend:{display:false}}}});\n  new Chart(document.getElementById(\'cHistAl\'),{type:\'line\',data:{labels,datasets:[{label:\'Alarmes Abertos\',data:chrono.map(h=>h.alarmes_abertas),borderColor:\'#f39c12\',backgroundColor:\'rgba(243,156,18,.15)\',pointRadius:5,pointHoverRadius:8,tension:.3,fill:true,borderWidth:2}]},options:{...CO,scales:sc(),plugins:{...CO.plugins,legend:{display:false}}}});\n}\n\nrenderHistorico();\n</script></body></html>'

#!/usr/bin/env python3
"""
gerar_painel_indisponibilidade.py - Gerador do Painel de Indisponibilidade Autodefesa Brasil
Uso: python gerar_painel_indisponibilidade.py [alarmes.xlsx] [cftv.xlsx] [historico.json]
Requisito: pip install pandas openpyxl

Lê duas planilhas:
  1) Base de alarmes (Observação de Abertura, Conta, Empresa, Data de Abertura,
     Status da OS, Atendimento, Data de fechamento, SLA, ...)
  2) Base de CFTV/gravadores (Cliente, Categoria, Cidade, Gravador, IP, Porta,
     Status [ONLINE/OFFLINE], Última Verificação)

Histórico:
  O snapshot do dia é acumulado em um arquivo JSON versionado no repositório
  (historico_indisponibilidade.json, por padrão). Esse arquivo deve ser
  commitado junto com o HTML pelo workflow, para que o histórico persista
  entre execuções e seja igual para todos os usuários (sem depender de
  localStorage do navegador).
"""
import pandas as pd
import json, sys, os, re
from datetime import datetime

ARQ_ALARMES = sys.argv[1] if len(sys.argv) > 1 else "Base_de_indisponibilidade.xlsx"
ARQ_CFTV    = sys.argv[2] if len(sys.argv) > 2 else "Base_de_indisponibilidade_imvictos.xlsx"
ARQ_HIST    = sys.argv[3] if len(sys.argv) > 3 else "historico_indisponibilidade.json"
SAIDA       = "painel_indisponibilidade.html"
MAX_DIAS    = 90

if not os.path.exists(ARQ_ALARMES):
    print(f"❌ Arquivo de alarmes '{ARQ_ALARMES}' não encontrado.")
    sys.exit(1)
if not os.path.exists(ARQ_CFTV):
    print(f"❌ Arquivo de CFTV '{ARQ_CFTV}' não encontrado.")
    sys.exit(1)

print(f"📂 Lendo {ARQ_ALARMES}...")
print(f"📂 Lendo {ARQ_CFTV}...")

# ── Heurística de simplificação de nome de cliente ─────────────────────
# Remove numerais romanos finais (AGIBANK I / AGIBANK II -> AGIBANK) e
# palavras genéricas no início (BANCO, S.A., LTDA...) para agrupar por
# marca/cliente em vez de razão social completa.
_STOPWORDS = {"BANCO", "S.A.", "S/A", "SA", "LTDA", "LTDA."}
_ROMAN = {"I", "II", "III", "IV", "V", "VI"}

def simplificar_cliente(nome):
    if not isinstance(nome, str) or not nome.strip():
        return "OUTROS"
    tokens = nome.upper().split()
    while tokens and tokens[-1] in _ROMAN:
        tokens.pop()
    while tokens and tokens[0] in _STOPWORDS:
        tokens.pop(0)
    return tokens[0] if tokens else nome.upper()

# ── Leitura: Alarmes ────────────────────────────────────────────────────
df_al = pd.read_excel(ARQ_ALARMES)
df_al.columns = [str(c).strip() for c in df_al.columns]
df_al['Data de Abertura']  = pd.to_datetime(df_al['Data de Abertura'], errors='coerce')
df_al['Data de fechamento'] = pd.to_datetime(df_al['Data de fechamento'], errors='coerce')
df_al['ClienteSimpl'] = df_al['Empresa'].apply(simplificar_cliente)

abertas_df  = df_al[df_al['Status da OS'].str.upper() == 'ABERTA']
fechadas_df = df_al[df_al['Status da OS'].str.upper() == 'FECHADA']

total_al    = len(df_al)
abertas_al  = len(abertas_df)
fechadas_al = len(fechadas_df)

al_cli = (
    df_al.groupby('ClienteSimpl')
    .apply(lambda g: {
        "c": g.name,
        "ab": int((g['Status da OS'].str.upper() == 'ABERTA').sum()),
        "fe": int((g['Status da OS'].str.upper() == 'FECHADA').sum()),
    }, include_groups=False)
    .tolist()
)
al_cli.sort(key=lambda x: x['ab'] + x['fe'], reverse=True)

al_ab = [
    {
        "conta": str(r['Conta'])[:64],
        "cli": r['ClienteSimpl'],
        "dt": r['Data de Abertura'].strftime('%d/%m/%Y') if pd.notna(r['Data de Abertura']) else '',
        "at": str(r.get('Atendimento', '') or ''),
    }
    for _, r in abertas_df.iterrows()
]

al_fe = [
    {
        "conta": str(r['Conta'])[:64],
        "cli": r['ClienteSimpl'],
        "dt": r['Data de Abertura'].strftime('%d/%m/%Y') if pd.notna(r['Data de Abertura']) else '',
        "dtf": r['Data de fechamento'].strftime('%d/%m/%Y') if pd.notna(r['Data de fechamento']) else '',
        "sla": str(r.get('SLA', '') or '') if pd.notna(r.get('SLA')) else '',
    }
    for _, r in fechadas_df.iterrows()
]

# ── Leitura: CFTV ────────────────────────────────────────────────────────
df_c = pd.read_excel(ARQ_CFTV)
df_c.columns = [str(c).strip() for c in df_c.columns]
df_c['Status'] = df_c['Status'].astype(str).str.upper().str.strip()

total_cftv   = len(df_c)
online_cftv  = int((df_c['Status'] == 'ONLINE').sum())
offline_cftv = int((df_c['Status'] == 'OFFLINE').sum())
pct_off      = round(offline_cftv / total_cftv * 100, 1) if total_cftv else 0.0

df_off = df_c[df_c['Status'] == 'OFFLINE'].copy()

cftv_cid = (
    df_off.groupby('Cidade').size().sort_values(ascending=False)
    .reset_index(name='q').rename(columns={'Cidade': 'c'})
    .to_dict(orient='records')
)
cftv_cid = [{"c": str(r['c']), "q": int(r['q'])} for r in cftv_cid][:20]

def _fmt_dt(v):
    if pd.isna(v):
        return ''
    return pd.to_datetime(v).strftime('%d/%m/%Y %H:%M')

cftv_off = [
    {
        "Cliente": str(r['Cliente']),
        "Cidade": str(r['Cidade']),
        "IP": str(r['IP']),
        "Última Verificação": _fmt_dt(r['Última Verificação']),
    }
    for _, r in df_off.iterrows()
]

# ── Datas de referência ──────────────────────────────────────────────────
emissao = datetime.now().strftime('%d/%m/%Y %H:%M')

ref_candidates = []
if df_c['Última Verificação'].notna().any():
    ref_candidates.append(pd.to_datetime(df_c['Última Verificação']).max())
if df_al['Data de Abertura'].notna().any():
    ref_candidates.append(df_al['Data de Abertura'].max())
data_ref_dt = max(ref_candidates) if ref_candidates else datetime.now()
data_ref    = data_ref_dt.strftime('%d/%m/%Y %H:%M')
data_snapshot = data_ref_dt.strftime('%Y-%m-%d')

snapshot_hoje = {
    "data": data_snapshot,
    "alarmes_abertas": abertas_al,
    "alarmes_fechadas": fechadas_al,
    "cftv_offline": offline_cftv,
    "cftv_online": online_cftv,
    "cftv_total": total_cftv,
}

# ── Histórico server-side ─────────────────────────────────────────────────
# Carrega o histórico já acumulado no repositório, adiciona/atualiza o
# snapshot de hoje (se já existir um registro para a mesma data, ele é
# substituído — assim reprocessar o mesmo dia não duplica linha), ordena
# cronologicamente e mantém só os últimos MAX_DIAS.
historico = []
if os.path.exists(ARQ_HIST):
    try:
        with open(ARQ_HIST, encoding='utf-8') as f:
            historico = json.load(f)
        if not isinstance(historico, list):
            historico = []
    except Exception as e:
        print(f"⚠️  Não consegui ler '{ARQ_HIST}' ({e}); começando histórico novo.")
        historico = []

historico = [h for h in historico if h.get('data') != data_snapshot]
historico.append(snapshot_hoje)
historico.sort(key=lambda h: h.get('data', ''))
historico = historico[-MAX_DIAS:]

with open(ARQ_HIST, 'w', encoding='utf-8') as f:
    json.dump(historico, f, ensure_ascii=False, indent=2)
print(f"🗂️  Histórico atualizado: {ARQ_HIST} ({len(historico)} dia(s) registrados)")

# ── Bloco de constantes JS (substitui o antigo, mantém o restante do template) ──
consts = f"""const EMISSAO="{emissao}";
const DATA_REF="{data_ref}";
const TOTAL_AL={total_al};
const ABERTAS_AL={abertas_al};
const FECHADAS_AL={fechadas_al};
const AL_CLI={json.dumps(al_cli, ensure_ascii=False)};
const AL_AB={json.dumps(al_ab, ensure_ascii=False)};
const AL_FE={json.dumps(al_fe, ensure_ascii=False)};
const TOTAL_CFTV={total_cftv};
const OFFLINE_CFTV={offline_cftv};
const ONLINE_CFTV={online_cftv};
const PCT_OFF={pct_off};
const CFTV_CID={json.dumps(cftv_cid, ensure_ascii=False)};
const CFTV_OFF={json.dumps(cftv_off, ensure_ascii=False)};
const SNAPSHOT_HOJE={json.dumps(snapshot_hoje, ensure_ascii=False)};
const HIST_SERVIDOR={json.dumps(historico, ensure_ascii=False)};
"""

HTML = HEAD_TPL + consts + "\n" + TAIL_TPL

with open(SAIDA, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"✅ Painel gerado: {SAIDA}")
print(f"   Alarmes total : {total_al}  (abertos: {abertas_al} · fechados: {fechadas_al})")
print(f"   CFTV total    : {total_cftv}  (offline: {offline_cftv} · online: {online_cftv} · {pct_off}%)")
print(f"   Data de ref.  : {data_ref}")
