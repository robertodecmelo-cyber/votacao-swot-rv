import json

with open("/home/claude/votacao_unificada/logo_a.b64") as f:
    LOGO_A_B64 = f.read().strip()  # white-circle badge -> use on BLUE backgrounds
with open("/home/claude/votacao_unificada/logo_b.b64") as f:
    LOGO_B_B64 = f.read().strip()  # navy-circle badge -> use on WHITE backgrounds

# ============================================================================
# Site único (2 etapas) — RV Digital 2027.
# Saída: index.html (seletor de etapa+quadrante), voto.html (votação
# genérica, parametrizada por ?stage=&quad=) e admin.html (painel único,
# com aba de etapa no topo), gerados neste mesmo diretório.
# Rode com: python3 generate.py  (a partir de /home/claude/votacao_unificada)
# ============================================================================

OUT_DIR = "/home/claude/votacao_unificada"

# ============================================================================
# SHARED CSS (mesmo sistema visual das versões anteriores, + extensões para
# as abas de etapa, os chips de origem "Não Telecom"/"Telecom + Ambos", o
# selo de itens migrados e o seletor em duas etapas do index.html)
# ============================================================================
BASE_CSS = r"""
:root{
  --navy-dk:#0b2350; --navy:#0d2d5b; --navy-lt:#14548c;
  --ink:#0d2d5b; --ink-soft:#5c6c80; --paper:#f4f6fa; --surface:#ffffff; --surface-2:#eef1f6;
  --line:#dce2ea;
  --accent:#14548c; --accent-soft:#e4edf6;
  --gold:#f5a100; --yellow:#fde90e; --green:#00b554; --red:#d14343;
  --radius:14px;
  --shadow:0 1px 2px rgba(13,45,91,.06), 0 10px 30px -12px rgba(13,45,91,.16);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ink:#e9edf5; --ink-soft:#9aa8bd; --paper:#0c1220; --surface:#141b2b; --surface-2:#1a2336;
    --line:#28324a; --accent-soft:#1c2740;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -12px rgba(0,0,0,.6);
  }
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:var(--paper); color:var(--ink);
  font-family:"Ubuntu",system-ui,sans-serif; font-size:17px; line-height:1.55;
  -webkit-font-smoothing:antialiased;
}
.mono{font-family:"Ubuntu Mono",monospace;}
h1,h2,h3{font-family:"Ubuntu",sans-serif; font-weight:700; margin:0;}
a{color:var(--navy-lt)}

.rv-logo{flex:none; display:block;}
.rv-logo img{display:block; width:100%; height:100%; object-fit:contain;}

header.hero{
  background:linear-gradient(115deg, var(--navy-dk) 0%, var(--navy) 45%, var(--navy-lt) 100%);
  color:#fff; padding:20px 0 40px; position:relative; overflow:hidden;
}
header.hero::after{
  content:""; position:absolute; left:-40px; bottom:-60px; width:180px; height:220px;
  border:2px solid var(--yellow); border-radius:20px; opacity:.55;
}
.hero-inner{max-width:900px; margin:0 auto; padding:0 20px; display:flex; align-items:flex-start; gap:18px; position:relative; z-index:2;}
.hero-text{flex:1;}
.back-to-menu{
  position:fixed; top:14px; left:14px; z-index:999;
  display:inline-flex; align-items:center; gap:6px;
  color:#fff; background:var(--navy-dk); border:1px solid rgba(255,255,255,.25);
  border-radius:999px; padding:8px 15px 8px 13px; font-size:13px; font-weight:600;
  text-decoration:none; transition:.15s; box-shadow:0 2px 10px -2px rgba(0,0,0,.4);
}
.back-to-menu:hover{background:var(--navy);}
.hero-text{padding-top:40px;}
@media (max-width:600px){ .back-to-menu{ padding:7px 12px 7px 11px; font-size:12.5px; } }
.hero-eyebrow{font-size:13px; text-transform:uppercase; letter-spacing:.1em; color:#ffe27a; margin-bottom:10px; margin-top:2px; font-weight:700;}
.hero-title{font-size:29px; line-height:1.2;}
.hero-sub{font-size:15.5px; color:#f2f6fc; margin-top:10px; max-width:560px; line-height:1.5;}
.hero-logo{width:60px; height:60px;}

.top-tabs{display:flex; gap:6px; margin-top:18px; flex-wrap:wrap;}
.tab-btn{
  border:1px solid rgba(255,255,255,.35); background:rgba(255,255,255,.08); color:#fff;
  padding:8px 14px; border-radius:999px; font-size:13.5px; font-weight:500; cursor:pointer;
  transition:.15s;
}
.tab-btn.active{background:#fff; color:var(--navy); border-color:#fff; font-weight:700;}
.tab-btn:not(.active):hover{border-color:#fff;}
.stage-tabs{margin-top:14px; padding-bottom:12px; border-bottom:1px solid rgba(255,255,255,.22);}
.stage-tabs .tab-btn{font-size:14px; padding:9px 16px;}

main{max-width:900px; margin:0 auto; padding:26px 20px 90px;}
.view{display:none;}
.view.active{display:block;}

.intro{
  background:var(--surface); border:1px solid var(--line); border-radius:var(--radius);
  padding:20px 22px; box-shadow:var(--shadow); margin-bottom:20px;
}
.scale{display:grid; gap:8px; margin-top:10px;}
.scale-row{
  display:flex; gap:12px; align-items:flex-start; padding:10px 12px;
  border-radius:10px; background:var(--surface-2); border:1px solid var(--line);
}
.scale-num{
  font-family:"Ubuntu Mono",monospace; font-weight:700; font-size:15px;
  width:26px; height:26px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  color:#fff; flex:none;
}
.scale-row.s5 .scale-num{background:var(--green);}
.scale-row.s3 .scale-num{background:var(--gold);}
.scale-row.s1 .scale-num{background:var(--red);}
.scale-row p{margin:0; font-size:15px;}
.anon-note{
  margin-top:14px; font-size:14px; color:var(--ink-soft);
  padding:10px 14px; background:var(--accent-soft); border-radius:10px; line-height:1.5;
}
.anon-note .ic{margin-right:6px;}
.already-voted-note{
  margin-top:14px; font-size:13.5px; color:#1b4a8a;
  padding:10px 14px; background:#e4edf6; border:1px solid #bcd2e6; border-radius:10px; line-height:1.5;
}
.tag-legend{
  margin-top:14px; font-size:13.5px; color:var(--ink-soft); line-height:1.7;
  padding:10px 14px; background:var(--surface-2); border:1px solid var(--line); border-radius:10px;
}
.tag-legend .leg-row{display:flex; align-items:center; gap:8px; margin:3px 0;}
.tag-legend .chip{flex:none;}

.progress-wrap{ position:sticky; top:0; z-index:30; background:var(--paper); padding:10px 0 14px 185px; }
@media (max-width:600px){ .progress-wrap{ padding-left:150px; } }

.origin-filter{ display:flex; align-items:center; gap:7px; flex-wrap:wrap; margin:0 0 16px; }
.origin-filter-label{ font-size:13px; color:var(--ink-soft); font-weight:600; margin-right:2px; }
.origin-filter button{ border:1px solid var(--line); background:var(--surface); color:var(--ink-soft); padding:7px 14px; border-radius:999px; font-size:13px; font-weight:600; cursor:pointer; transition:.12s; }
.origin-filter button:hover{ border-color:var(--accent); }
.origin-filter button.active{ background:var(--accent); color:#fff; border-color:var(--accent); }
.origin-filter button .cnt{ opacity:.75; font-weight:500; margin-left:3px; }
.progress-track{ height:8px; border-radius:999px; background:var(--surface-2); border:1px solid var(--line); overflow:hidden; }
.progress-fill{height:100%; background:var(--accent); width:0%; transition:width .25s;}
.progress-label{display:flex; justify-content:space-between; font-size:12.5px; color:var(--ink-soft); margin-top:6px;}

.item{ background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); padding:16px 18px; margin-bottom:12px; box-shadow:var(--shadow); }
.item.voted{border-color:var(--accent);}
.item.is-migrated{border-style:dashed;}
.item-top{display:flex; gap:10px; align-items:flex-start;}
.item-idx{ font-family:"Ubuntu Mono",monospace; font-size:12.5px; color:var(--ink-soft); flex:none; padding-top:2px; width:30px; }
.item-title{font-size:16.5px; font-weight:500; flex:1;}
.item-meta{display:flex; gap:6px; flex-wrap:wrap; margin:8px 0 0 40px;}
.chip{ font-size:12px; padding:3px 9px; border-radius:999px; border:1px solid var(--line); color:var(--ink-soft); background:var(--surface-2); font-weight:500; }
.chip.type-c{color:var(--navy-lt); border-color:var(--navy-lt); background:var(--accent-soft);}
.chip.origin-telecom, .chip.tag-telecom{color:#8a5a00; border-color:#e3c07a; background:#fdf0dc;}
.chip.origin-ambos, .chip.tag-ambos{color:#5b3fa0; border-color:#c9bce8; background:#efeaf9;}
.chip.origin-naotelecom, .chip.tag-naotelecom{color:#0d6b4a; border-color:#9fd9c4; background:#e2f7ee;}
.chip.tag-telecomambos{color:#14548c; border-color:#bcd2e6; background:#e4edf6;}
.chip.migrated-chip{color:#5b3fa0; border-color:#c9bce8; background:#efeaf9; font-weight:700;}
details.orig{margin:8px 0 0 40px;}
details.orig summary{font-size:12.5px; color:var(--navy-lt); cursor:pointer; list-style:none; font-weight:500;}
details.orig summary::-webkit-details-marker{display:none;}
details.orig ol{margin:8px 0 0; padding-left:18px; font-size:13px; color:var(--ink-soft);}
details.orig ol li{margin-bottom:4px;}
details.orig .oi-origin{font-size:10.5px; font-weight:700; padding:1px 6px; border-radius:999px; margin-left:6px; white-space:nowrap;}
details.orig .oi-origin.t{color:#8a5a00; background:#fdf0dc;}
details.orig .oi-origin.a{color:#5b3fa0; background:#efeaf9;}
details.orig .oi-origin.nt{color:#0d6b4a; background:#e2f7ee;}
details.orig .reason{margin-top:6px; font-size:12.5px; color:var(--ink-soft); font-style:italic;}

.migrated-heading{ margin:26px 0 12px; font-size:14px; font-weight:700; color:var(--ink-soft); padding-top:14px; border-top:1px dashed var(--line); }

.vote-row{display:flex; gap:8px; margin:12px 0 0 40px; flex-wrap:wrap;}
.vote-btn{ flex:1; min-width:140px; border:1.5px solid var(--line); background:var(--surface); border-radius:10px; padding:9px 12px; cursor:pointer; text-align:left; display:flex; align-items:center; gap:9px; transition:.12s; }
.vote-btn .vnum{ font-family:"Ubuntu Mono",monospace; font-weight:700; font-size:14px; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#fff; flex:none; }
.vote-btn .vtxt{font-size:13.5px; color:var(--ink-soft); line-height:1.3; font-weight:500;}
.vote-btn[data-score="5"] .vnum{background:var(--green);}
.vote-btn[data-score="3"] .vnum{background:var(--gold);}
.vote-btn[data-score="1"] .vnum{background:var(--red);}
.vote-btn:hover{border-color:var(--accent);}
.vote-btn.sel{background:var(--accent); border-color:var(--accent);}
.vote-btn.sel .vtxt{color:#fff;}

.save-tag{ margin:8px 0 0 40px; font-size:12px; font-weight:600; min-height:16px; }
.save-tag span{display:none;}
.save-tag[data-state="pending"] .save-tag-pending{display:inline; color:var(--gold);}
.save-tag[data-state="saved"] .save-tag-saved{display:inline; color:var(--green);}

.save-bar{
  position:sticky; bottom:0; z-index:35; margin-top:16px;
  display:flex; align-items:center; gap:14px; flex-wrap:wrap;
  background:var(--surface); border:1px solid var(--line); border-radius:var(--radius);
  padding:16px 18px; box-shadow:0 -6px 24px -10px rgba(13,45,91,.25), var(--shadow);
}
.save-bar-text{flex:1; min-width:180px; font-size:14px; color:var(--ink-soft); line-height:1.45;}
.save-bar-text b{color:var(--ink); font-family:"Ubuntu Mono",monospace;}
.save-btn{
  border:none; border-radius:999px; padding:13px 26px; font-weight:700; font-size:14.5px;
  cursor:pointer; color:#fff; background:var(--accent); transition:.15s; flex:none;
  display:flex; align-items:center; gap:8px;
}
.save-btn:disabled{background:var(--surface-2); color:var(--ink-soft); cursor:default;}
.save-btn.state-saving{background:var(--ink-soft);}
.save-btn.state-saved{background:var(--green);}
.save-btn.state-error{background:var(--red);}
.save-flash{
  display:none; align-items:center; gap:10px; margin-top:10px;
  background:#e2f8ea; color:#0d6b3a; border:1px solid #b6e8ca; border-radius:10px;
  padding:10px 14px; font-size:13px; font-weight:600;
}
.save-flash.show{display:flex;}
.save-flash.error{background:#fbe6e6; color:#9c2222; border-color:#f0bcbc;}

.admin-toolbar{ display:flex; gap:18px; align-items:center; flex-wrap:wrap; margin-bottom:18px; background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); padding:14px 18px; box-shadow:var(--shadow); }
.stat{display:flex; flex-direction:column; gap:2px;}
.stat b{font-family:"Ubuntu Mono",monospace; font-size:20px;}
.stat span{font-size:11.5px; color:var(--ink-soft); text-transform:uppercase; letter-spacing:.06em;}
.toggle-btn{ margin-left:auto; border:none; border-radius:999px; padding:10px 18px; font-weight:700; font-size:13.5px; cursor:pointer; color:#fff; }
.toggle-btn.open{background:var(--green);}
.toggle-btn.closed{background:var(--red);}
.admin-item{ background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); padding:14px 18px; margin-bottom:10px; box-shadow:var(--shadow); }
.admin-item.is-migrated{border-style:dashed;}
.admin-item-top{display:flex; gap:10px; align-items:baseline; flex-wrap:wrap;}
.admin-item-top .item-title{font-size:14.5px;}
.avg-badge{ font-family:"Ubuntu Mono",monospace; font-weight:700; font-size:13px; padding:3px 10px; border-radius:999px; color:#fff; flex:none; }
.prioritize-ctrl{ display:flex; align-items:center; gap:6px; font-size:12px; color:var(--ink-soft); font-weight:600; flex:none; }
.prioritize-ctrl input{ width:16px; height:16px; cursor:pointer; }
.bars{display:flex; height:10px; border-radius:999px; overflow:hidden; margin:10px 0 6px 0; background:var(--surface-2);}
.bar-5{background:var(--green);} .bar-3{background:var(--gold);} .bar-1{background:var(--red);}
.bar-legend{display:flex; gap:14px; font-size:11.5px; color:var(--ink-soft); flex-wrap:wrap;}
.bar-legend b{color:var(--ink);}
.rank-toggle{display:flex; gap:6px; margin-bottom:14px;}
.rank-toggle button{ border:1px solid var(--line); background:var(--surface-2); color:var(--ink-soft); padding:7px 12px; border-radius:999px; font-size:12.5px; font-weight:500; cursor:pointer; }
.rank-toggle button.active{background:var(--accent); color:#fff; border-color:var(--accent);}

.view-toggle{display:flex; gap:6px; margin-bottom:16px; flex-wrap:wrap;}
.view-toggle button{ border:1px solid var(--line); background:var(--surface-2); color:var(--ink-soft); padding:8px 16px; border-radius:999px; font-size:13px; font-weight:600; cursor:pointer; }
.view-toggle button.active{background:var(--navy); color:#fff; border-color:var(--navy);}

.prio-summary{ background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); padding:12px 16px; margin-bottom:16px; box-shadow:var(--shadow); font-size:13.5px; color:var(--ink-soft); }
.prio-summary b{color:var(--ink);}

.top5-wrap{ background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); padding:16px 18px; margin-bottom:18px; box-shadow:var(--shadow); }
.top5-wrap h3{font-size:15px; margin:0 0 12px;}
.top5-table{width:100%; border-collapse:collapse; font-size:13.5px;}
.top5-table th{ text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--ink-soft); padding:6px 8px; border-bottom:1px solid var(--line); }
.top5-table td{ padding:9px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
.top5-table tr:last-child td{border-bottom:none;}
.top5-rank{ font-family:"Ubuntu Mono",monospace; font-weight:700; color:var(--ink-soft); width:26px; }
.top5-avg{ font-family:"Ubuntu Mono",monospace; font-weight:700; white-space:nowrap; }
.top5-tie{ font-size:10.5px; font-weight:700; color:var(--gold); margin-left:6px; }
.summary-quad{ margin-bottom:22px; }
.summary-quad h3{ font-size:16px; margin:0 0 10px; display:flex; align-items:center; gap:8px; }
.summary-quad h3 .dot{width:10px; height:10px; border-radius:50%; display:inline-block; flex:none;}
.empty-note{ color:var(--ink-soft); font-size:13px; padding:10px 2px; }

.edit-item textarea{ width:100%; border:1px solid var(--line); border-radius:8px; padding:9px 11px; font-family:"Ubuntu",sans-serif; font-size:13.5px; resize:vertical; color:var(--ink); background:var(--surface); }
.edit-item .edit-actions{display:flex; gap:8px; align-items:center; margin-top:9px; flex-wrap:wrap;}
.edit-item .edit-save{ border:none; border-radius:999px; padding:8px 16px; font-weight:700; font-size:12.5px; cursor:pointer; color:#fff; background:var(--accent); }
.edit-item .edit-reset{ border:1px solid var(--line); background:var(--surface-2); color:var(--ink-soft); border-radius:999px; padding:8px 16px; font-weight:600; font-size:12.5px; cursor:pointer; }
.edit-item .edit-status{font-size:12px; color:var(--green); font-weight:600;}
.edit-item .edit-status.err{color:var(--red);}

.topn-ctrl{ display:flex; align-items:center; gap:8px; margin-left:auto; font-size:12.5px; color:var(--ink-soft); }
.topn-ctrl input{ width:52px; border:1px solid var(--line); border-radius:8px; padding:5px 8px; font-family:"Ubuntu Mono",monospace; font-size:13px; text-align:center; color:var(--ink); background:var(--surface); }
.top5-wrap .top5-head{display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;}
.top5-wrap .top5-head h3{margin:0;}
.restore-order-btn{ border:1px solid var(--line); background:var(--surface-2); color:var(--ink-soft); border-radius:999px; padding:6px 13px; font-size:12px; font-weight:600; cursor:pointer; }
.export-bar{ display:flex; align-items:center; gap:9px; flex-wrap:wrap; background:var(--surface-2); border:1px solid var(--line); border-radius:12px; padding:11px 14px; margin-bottom:16px; }
.export-bar .export-label{ font-size:12.5px; font-weight:700; color:var(--ink-soft); margin-right:2px; }
.export-bar select.export-format{ border:1px solid var(--line); background:var(--surface); color:var(--ink); border-radius:8px; padding:7px 10px; font-size:12.5px; font-family:inherit; }
.export-bar button.export-btn{ border:1px solid var(--line); background:var(--surface); color:var(--ink); border-radius:999px; padding:8px 16px; font-size:12.5px; font-weight:700; cursor:pointer; }
.export-bar button.export-btn:hover{ border-color:var(--navy-lt); color:var(--navy-lt); }
.export-bar button.export-btn.export-total{ background:var(--navy); color:#fff; border-color:var(--navy); }
.export-bar button.export-btn.export-total:hover{ opacity:.88; color:#fff; }
.export-bar .export-status{ font-size:12px; color:var(--ink-soft); margin-left:2px; }
.export-bar .export-status.err{ color:var(--red); font-weight:600; }
.rank-arrows{display:flex; flex-direction:column; gap:2px;}
.rank-arrows button{ border:1px solid var(--line); background:var(--surface-2); color:var(--ink-soft); border-radius:5px; width:20px; height:16px; font-size:10px; line-height:1; cursor:pointer; display:flex; align-items:center; justify-content:center; padding:0; }
.rank-arrows button:disabled{opacity:.3; cursor:default;}
.rank-arrows button:not(:disabled):hover{background:var(--accent); color:#fff; border-color:var(--accent);}
.top5-table td.top5-rankcell{display:flex; align-items:center; gap:6px;}

.add-item-box{ background:var(--surface-2); border:1px dashed var(--line); border-radius:var(--radius); padding:14px 16px; margin-bottom:16px; }
.add-item-box h4{font-size:13.5px; margin:0 0 8px;}
.add-item-box textarea{ width:100%; border:1px solid var(--line); border-radius:8px; padding:9px 11px; font-family:"Ubuntu",sans-serif; font-size:13.5px; resize:vertical; color:var(--ink); background:var(--surface); }
.add-item-box .add-row{display:flex; gap:8px; align-items:center; margin-top:9px; flex-wrap:wrap;}
.add-item-box select{ border:1px solid var(--line); border-radius:8px; padding:8px 10px; font-size:13px; color:var(--ink); background:var(--surface); }
.add-item-btn{ border:none; border-radius:999px; padding:8px 16px; font-weight:700; font-size:12.5px; cursor:pointer; color:#fff; background:var(--green); }
.remove-item-btn{ border:1px solid #e0a0a0; background:#fbe9e9; color:#9c2222; border-radius:999px; padding:8px 16px; font-weight:600; font-size:12.5px; cursor:pointer; }
.added-badge{color:var(--green); font-weight:700;}
.migrated-badge{color:#5b3fa0; font-weight:700;}
.removed-panel{ background:var(--surface-2); border:1px solid var(--line); border-radius:var(--radius); padding:14px 16px; margin-top:18px; }
.removed-panel h4{font-size:13px; margin:0 0 10px; color:var(--ink-soft);}
.removed-row{ display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid var(--line); font-size:13px; }
.removed-row:last-child{border-bottom:none;}
.removed-row .rt{flex:1; color:var(--ink-soft);}
.restore-item-btn{ border:1px solid var(--line); background:var(--surface); color:var(--navy-lt); border-radius:999px; padding:6px 13px; font-size:12px; font-weight:600; cursor:pointer; flex:none; }
.reset-confirm{background:var(--red) !important;}

.menu-grid{ display:grid; gap:14px; margin-top:6px; }
.menu-card{
  display:flex; align-items:center; gap:16px; text-decoration:none;
  background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--mc-accent);
  border-radius:var(--radius); padding:18px 20px; box-shadow:var(--shadow); transition:.15s;
  position:relative;
}
.menu-card:hover{ transform:translateX(3px); box-shadow:0 4px 16px -4px rgba(13,45,91,.22), var(--shadow); }
.menu-card.is-voted{ opacity:.68; }
.menu-card-icon{
  width:46px; height:46px; border-radius:12px; background:var(--mc-soft); color:var(--mc-accent);
  display:flex; align-items:center; justify-content:center; font-size:21px; flex:none;
}
.menu-card-body{flex:1; min-width:0;}
.menu-card-title{font-size:18.5px; font-weight:700; color:var(--ink); margin-bottom:3px; display:flex; align-items:center; gap:8px;}
.menu-card-desc{font-size:13.5px; color:var(--ink-soft); line-height:1.4;}
.menu-card-arrow{font-size:18px; color:var(--ink-soft); flex:none; transition:.15s;}
.menu-card:hover .menu-card-arrow{color:var(--mc-accent); transform:translateX(2px);}
.voted-badge{ font-size:10.5px; font-weight:700; color:#0d6b3a; background:#e2f8ea; border:1px solid #b6e8ca; border-radius:999px; padding:2px 8px; white-space:nowrap; }
.admin-link-pill{
  display:inline-flex; align-items:center; gap:7px; text-decoration:none;
  color:var(--ink-soft); font-size:13px; font-weight:600; padding:10px 18px;
  border:1px solid var(--line); border-radius:999px; background:var(--surface); transition:.15s;
}
.admin-link-pill:hover{ color:var(--navy); border-color:var(--navy-lt); background:var(--surface-2); }
.index-footnote{ text-align:center; color:var(--ink-soft); font-size:12.5px; margin-top:14px; line-height:1.5; }

.stage-grid{ display:grid; gap:18px; margin-top:6px; grid-template-columns:1fr; }
@media (min-width:640px){ .stage-grid{ grid-template-columns:1fr 1fr; } }
.stage-card{
  display:block; text-decoration:none; text-align:left; cursor:pointer;
  background:var(--surface); border:1px solid var(--line); border-top:4px solid var(--mc-accent);
  border-radius:var(--radius); padding:26px 22px; box-shadow:var(--shadow); transition:.15s;
}
.stage-card:hover{ transform:translateY(-2px); box-shadow:0 8px 22px -8px rgba(13,45,91,.25), var(--shadow); }
.stage-card-icon{
  width:52px; height:52px; border-radius:14px; background:var(--mc-soft); color:var(--mc-accent);
  display:flex; align-items:center; justify-content:center; margin-bottom:14px;
}
.stage-card-title{font-size:20px; font-weight:700; color:var(--ink); margin-bottom:6px;}
.stage-card-desc{font-size:14px; color:var(--ink-soft); line-height:1.45;}
.stage-card-note{margin-top:12px; font-size:12.5px; color:var(--navy-lt); background:var(--accent-soft); border-radius:8px; padding:8px 10px; line-height:1.4;}
.step-back{ display:inline-flex; align-items:center; gap:6px; color:var(--ink-soft); font-size:13.5px; font-weight:600; text-decoration:none; margin-bottom:16px; cursor:pointer; border:none; background:none; padding:0; }
.step-back:hover{color:var(--navy);}
#step2-telecom, #step2-naotelecom{display:none;}

.gate{ max-width:420px; margin:60px auto; text-align:center; padding:30px; background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); box-shadow:var(--shadow); }
.gate .icon{font-size:34px; margin-bottom:10px;}
.gate input{ width:100%; padding:11px 14px; border-radius:10px; border:1px solid var(--line); margin-top:10px; font-size:14px; font-family:"Ubuntu",sans-serif; }
.gate button{ margin-top:14px; width:100%; border:none; border-radius:999px; padding:12px; font-weight:700; font-size:14.5px; cursor:pointer; color:#fff; background:var(--navy); }
.gate .err{ color:var(--red); font-size:12.5px; margin-top:10px; min-height:16px; }

footer.pagefoot{ background:var(--surface); border-top:1px solid var(--line); margin-top:30px; padding:22px 20px; }
.pagefoot-inner{max-width:900px; margin:0 auto; display:flex; align-items:center; gap:14px;}
.pagefoot-logo{width:32px; height:32px;}
.pagefoot-text{font-size:12px; color:var(--ink-soft); line-height:1.4;}

@media (max-width:600px){
  .vote-row{flex-direction:column;}
  .item-meta, details.orig, .vote-row{margin-left:0;}
  .hero-title{font-size:22px;}
}
"""

HEAD = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>__PAGE_TITLE__</title>
<meta name="description" content="__PAGE_DESC__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Ubuntu:wght@400;500;700&family=Ubuntu+Mono:wght@400;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="./supabase-config.js"></script>
<style>
__CSS__
</style>
</head>
"""

# ============================================================================
# QUADRANTS (idêntico nas duas etapas — cor/label por quadrante)
# ============================================================================
QUADRANTS = [
  {"key":"forcas", "label":"Forças", "accent":"#00b554", "accent_soft":"#e2f8ea"},
  {"key":"fraquezas", "label":"Fraquezas", "accent":"#d14343", "accent_soft":"#fbe6e6"},
  {"key":"oportunidades", "label":"Oportunidades", "accent":"#14548c", "accent_soft":"#e4edf6"},
  {"key":"ameacas", "label":"Ameaças", "accent":"#f5a100", "accent_soft":"#fdf0dc"},
]

STAGE_LABELS = {"telecom": "Telecom + Ambos", "naotelecom": "Não Telecom + Ambos"}

def build_items(convergences, solos, qkey):
    items = []
    for i, c in enumerate(convergences.get(qkey, []), start=1):
        origs = [{"text":o[0], "division":o[1], "origin":o[2]} for o in c["originals"]]
        divisions = sorted(set(o["division"] for o in origs))
        origins = sorted(set(o["origin"] for o in origs))
        items.append({
            "id": qkey + "_c" + str(i), "type": "convergencia", "title": c["title"],
            "divisions": divisions, "origins": origins, "n": len(origs),
            "originals": origs, "reason": c["reason"],
        })
    for i, s in enumerate(solos.get(qkey, []), start=1):
        items.append({
            "id": qkey + "_s" + str(i), "type": "isolada", "title": s[0],
            "divisions": [s[1]], "origins": [s[2]], "n": 1, "originals": None, "reason": None,
        })
    return items

# ============================================================================
# Data: Telecom + Ambos SWOT (copiado verbatim de votacao_supabase/generate.py)
# ============================================================================
CONVERGENCES_TELECOM = {
  "forcas": [
    {"title":"Capilaridade nacional e presença multicanal (físico e digital)", "reason":"Três propostas, de duas diretorias, descrevem a mesma força de alcance nacional, física e digital da RV.",
     "originals":[
       ["Capilaridade nacional","Marketing","Ambos"],
       ["Capilaridade e Venda no Varejo Físico Brasil","Operações","Ambos"],
       ["Presença em canais físico e digital","Operações","Ambos"]
     ]},
    {"title":"Relacionamento consolidado com clientes, parceiros, operadoras e pontos de venda", "reason":"Quatro propostas apontam o mesmo ativo relacional da RV sob ângulos complementares: financeiro/contratual com operadoras, comercial com clientes e parceiros, execução no PDV e contratos Telecom/Não Telecom.",
     "originals":[
       ["Relacionamento consolidado com operadoras e parceiros (Comercial/Financeiro/Contábil)","Financeira","Ambos"],
       ["Relacionamento consolidado com clientes e parceiros/B2B","Marketing","Ambos"],
       ["Relacionamento com pontos de venda e capacidade de execução na última milha","Operações","Ambos"],
       ["Relacionamento e contratos Telecom / Não Telecom","Operações","Ambos"]
     ]},
    {"title":"Plataforma tecnológica proprietária, flexível e escalável", "reason":"Duas propostas descrevem a mesma plataforma própria da RV, com ênfase em titularidade e em flexibilidade/escala.",
     "originals":[
       ["Plataforma tecnológica proprietária","Marketing","Ambos"],
       ["Plataforma flexível e escalável (recarga e verticais), tanto para o físico como para o digital","Operações","Ambos"]
     ]},
    {"title":"Modelo de gestão, governança e disciplina de resultados", "reason":"Três propostas, de três diretorias, destacam a maturidade do modelo de gestão, governança e disciplina de resultados da companhia.",
     "originals":[
       ["Modelo de gestão e governança","Financeira","Ambos"],
       ["Gestão de resultados","Marketing","Ambos"],
       ["Modelo de gestão do negócio","Operações","Ambos"]
     ]},
    {"title":"Estabilidade e resiliência das equipes e lideranças", "reason":"Duas propostas tratam da solidez do capital humano: adaptação das equipes e baixa rotatividade das lideranças se reforçam.",
     "originals":[
       ["Resiliência e adaptação das equipes","Marketing","Ambos"],
       ["Baixo turn over das lideranças","Operações","Ambos"]
     ]},
    {"title":"Capacidade operacional e tecnológica de execução (Telecom, delivery e canais de venda)", "reason":"Unificação dentro da mesma diretoria (Tecnologia): quatro propostas descrevem a maturidade operacional de execução, delivery e canais de venda da RV.",
     "originals":[
       ["Operações - Execução TELECOM","Tecnologia","Ambos"],
       ["Maturidade de Gestão de Delivery de Produtos suporta qualquer tipo de demanda (Colaboração: Produtos, Desenvolvimento, Infraestrutura, Segurança da Informação, SUPORTE, Operações, Jurídico)","Tecnologia","Ambos"],
       ["Disponibilidade dos Canais de Venda","Tecnologia","Ambos"],
       ["Temos um novo motor de crescimento exponencial na CIA (Máquina de Vendas)","Tecnologia","Ambos"]
     ]},
    {"title":"Cultura organizacional, atendimento humano e incentivo à inovação", "reason":"Três propostas da mesma diretoria (Marketing) descrevem a cultura, o atendimento humano e o incentivo dos sócios à inovação como diferenciais da RV.",
     "originals":[
       ["Atendimento humano","Marketing","Ambos"],
       ["Cultura organizacional","Marketing","Ambos"],
       ["Incentivo dos sócios à inovação","Marketing","Ambos"]
     ]},
    {"title":"Gestão de crédito, cobrança e modelo de venda consignada", "reason":"Unificação dentro da mesma diretoria (Operações): ambas descrevem competências da RV na gestão de crédito e nos modelos de venda do Telecom.",
     "originals":[
       ["Gestão de crédito e cobrança","Operações","Telecom"],
       ["Modelo de venda consignada","Operações","Telecom"]
     ]}
  ],
  "fraquezas": [
    {"title":"Fragilidade de estrutura de capital e baixa disponibilidade de caixa", "reason":"Três propostas, de três diretorias, apontam a mesma limitação financeira estrutural: capital insuficiente e baixa disponibilidade de caixa.",
     "originals":[
       ["Estrutura de capital (Risco restoque, Risco caixa, Falta garantias, Limite Crédito Teles)","Financeira","Ambos"],
       ["Estrutura de capital","Marketing","Ambos"],
       ["Baixa Disponibilidade de Caixa","Operações","Ambos"]
     ]},
    {"title":"Base cadastral de clientes desatualizada, incompleta ou pouco qualitativa", "reason":"Três propostas, dos dois arquivos, relatam o mesmo problema de dados: cadastro desatualizado, incompleto ou sem informações qualitativas.",
     "originals":[
       ["Base Cadastral desatualizada (Dificultando acesso e cobrança)","Financeira","Ambos"],
       ["Gestão de Cadastros dos Clientes","Marketing","Ambos"],
       ["Melhorar nossa base cadastral com mais dados qualitativos dos clientes","Operações","Telecom"]
     ]},
    {"title":"Dependência do canal físico e da força de vendas, limitando a escala de novos produtos", "reason":"Três propostas descrevem o mesmo gargalo comercial: dependência do canal físico e força de vendas sobrecarregada, sem capacidade de escalar novos produtos.",
     "originals":[
       ["Dependência relevante da operação tradicional e da força de vendas presencial","Marketing","Ambos"],
       ["Dependência do canal físico (equipe Telecom) para escalar produtos","Operações","Ambos"],
       ["A força comercial atual não tem a possibilidade de escalar novos produtos (muitas incumbências para os vendedores)","Tecnologia","Ambos"]
     ]},
    {"title":"Gestão de pessoas: turnover elevado e baixa atratividade de benefícios", "reason":"Três propostas, de três diretorias, descrevem facetas do mesmo problema de gestão de pessoas: gestão estratégica insuficiente, baixa atratividade de benefícios e alto turnover na equipe de vendas.",
     "originals":[
       ["Gestão Estratégica de Pessoas","Marketing","Ambos"],
       ["Atratividade dos benefícios","Tecnologia","Ambos"],
       ["Alto turn-over da equipe de vendas / lentidão na reposição das vagas","Operações","Ambos"]
     ]},
    {"title":"Integração sistêmica incompleta entre negócios e o ERP", "reason":"Unificação dentro da mesma diretoria (Financeira): ambas descrevem o mesmo gargalo de integração de sistemas com o ERP.",
     "originals":[
       ["Ausência de integração sistêmica de alguns negócios - energia, coban e adquirência","Financeira","Ambos"],
       ["Integração full do Cellcard/Rv Hub com o ERP (Ex. Contas a receber e Cobrança)","Financeira","Ambos"]
     ]}
  ],
  "oportunidades": [
    {"title":"Créditos tributários e benefícios fiscais (CBS, PIS/COFINS e incentivos estaduais)", "reason":"Cinco propostas da mesma diretoria (Financeira) tratam de facetas do mesmo tema: a captura de ganhos fiscais e tributários na transição para a CBS.",
     "originals":[
       ["Créditos Tributário em andamento para realização financeira (Perse R$ 431 MM / Tese do Século R$ 706 MM)","Financeira","Ambos"],
       ["Estudos e teses adicionais para recuperação e monetização de créditos diversos de PIS/COFINS, devido sua extinção a partir de jan27","Financeira","Ambos"],
       ["Não cumulatividade plena da CBS em quase todas as despesas/custos, aumentando os créditos e reduzindo a carga tributária efetiva","Financeira","Ambos"],
       ["Apuração Assistida (\"online\") da CBS entre contribuinte x Fisco, gerando um menor risco de autuações futuras","Financeira","Ambos"],
       ["Venda através de E-commerce para capturar benefícios fiscais (Ex: Estado SC para B2C)","Financeira","Ambos"]
     ]},
    {"title":"IA e automação como alavanca de produtividade, eficiência e escala", "reason":"Duas propostas, das diretorias Financeira e Marketing, enxergam a mesma tendência: IA e automação para ganhar produtividade, eficiência e escala.",
     "originals":[
       ["Automação e IA para reduzir esforço manual e melhorar eficiência operacional","Financeira","Ambos"],
       ["IA e automação como alavanca de produtividade e escala","Marketing","Ambos"]
     ]},
    {"title":"Consolidação e expansão do mercado Telecom (M&A, novos negócios, MVNO e novas áreas de distribuição)", "reason":"Maior cluster de oportunidades: seis propostas, dos dois arquivos, descrevem o mesmo movimento estratégico de crescer no Telecom via M&A, MVNO e novas áreas de distribuição.",
     "originals":[
       ["Novos negócios no mercado de Telecom","Marketing","Telecom"],
       ["Consolidação do mercado Telecom (fusões e aquisições)","Operações","Telecom"],
       ["Novos Negócios no mercado Telecom","Operações","Telecom"],
       ["MVNO RV","Operações","Telecom"],
       ["Aquisições e fusões","Marketing","Ambos"],
       ["Consolidação do mercado Telecom (novas áreas de distribuição)","Operações","Ambos"]
     ]},
    {"title":"Expansão de serviços financeiros, crédito e fintechs", "reason":"Três propostas convergem para a mesma janela de mercado: posicionar a RV como plataforma de crédito, meios de pagamento e fintechs.",
     "originals":[
       ["Demanda por crédito vinculado ao histórico transacional do PDV","Marketing","Telecom"],
       ["Expansão de serviços financeiros e meios de pagamento (BaaS)","Marketing","Ambos"],
       ["Integração de grandes Fintechs","Operações","Ambos"]
     ]},
    {"title":"Demanda de operadoras e empresas por distribuição no canal físico", "reason":"Ambas capturam a mesma demanda: empresas buscando o canal físico da RV para distribuir seus produtos.",
     "originals":[
       ["Estruturar modelo de distribuição pré-paga para a Brisanet","Operações","Telecom"],
       ["Busca das empresas por distribuição canal físico","Marketing","Ambos"]
     ]}
  ],
  "ameacas": [
    {"title":"Crimes cibernéticos, invasões e ataques hackers", "reason":"Quatro propostas, de quatro diretorias, apontam a mesma ameaça externa de crimes e ataques cibernéticos.",
     "originals":[
       ["Crimes Cibernéticos","Financeira","Ambos"],
       ["Invasões e ataques hackers","Marketing","Ambos"],
       ["Cenário de Cybersecurity no Brasil","Tecnologia","Ambos"],
       ["Aumento de ataques cibernéticos","Operações","Ambos"]
     ]},
    {"title":"Popularização do e-SIM no Brasil", "reason":"Três propostas, dos dois arquivos, citam a mesma ameaça tecnológica: a adoção do e-SIM, reduzindo a necessidade do chip físico.",
     "originals":[
       ["Popularização do E-sim","Operações","Telecom"],
       ["Popularização do e-SIM no Brasil","Marketing","Ambos"],
       ["E-sim","Tecnologia","Ambos"]
     ]},
    {"title":"Reforma Tributária/CBS: riscos regulatórios, fiscais e de fluxo de caixa", "reason":"Maior cluster de ameaças: oito propostas, das diretorias Financeira, Marketing e Operações, descrevem facetas do mesmo risco regulatório, fiscal e de fluxo de caixa na transição para a CBS/Reforma Tributária.",
     "originals":[
       ["Insegurança jurídica e regulamentação ainda em aberto da CBS, principalmente para o mercado de distribuição de telefonia","Financeira","Ambos"],
       ["Fisco exigir o faturamento específico da recarga por venda, extinguindo a NF-e Global, com risco do ERP não suportar as emissões diárias","Financeira","Ambos"],
       ["Incertezas quanto ao início do Split Payment/RAD, com possíveis descasamentos no fluxo de caixa nas operações B2B, devido à retenção antecipada da CBS pelo cliente","Financeira","Ambos"],
       ["Reflexo econômico/financeiro negativo da Reforma Tributária nos PDVs, podendo causar a descontinuidade operacional de alguns, com redução da capilaridade BMRV","Financeira","Ambos"],
       ["Fornecedores de produtos e serviços mantendo-se como optantes do SIMPLES, diminuindo o crédito da CBS pela BMRV","Financeira","Ambos"],
       ["Ausência de Documento legal para Fechamento fiscal (NF Teles dentro do Prazo)","Financeira","Ambos"],
       ["Riscos regulatórios e mudanças na legislação","Marketing","Ambos"],
       ["Início da implementação da reforma tributária","Operações","Ambos"]
     ]},
    {"title":"Condições comerciais e de serviço das operadoras/Teles", "reason":"Quatro propostas, dos dois arquivos, descrevem a mesma exposição às decisões comerciais e ao desempenho das operadoras/Teles, fora do controle da RV.",
     "originals":[
       ["Mudança da política comercial Teles (prazos, margens e garantias)","Operações","Telecom"],
       ["SLA dilatadado das Teles (Fragilidade Sistemas)","Financeira","Ambos"],
       ["Mudanças nas políticas comerciais de parceiros/operadoras","Marketing","Ambos"],
       ["Pressão dos parceiros (Telecom e etc) na redução contínua das margens","Tecnologia","Ambos"]
     ]},
    {"title":"Desintermediação: operadoras atendendo diretamente o varejo", "reason":"Ambas descrevem o mesmo risco estrutural: operadoras atendendo a rede de varejo diretamente.",
     "originals":[
       ["Atendimento direto nas redes de varejo pelas operadoras","Operações","Telecom"],
       ["Desintermediação da cadeia de negócio pelas operadoras","Marketing","Ambos"]
     ]},
    {"title":"Cenário macroeconômico: juros altos, endividamento e aversão a risco", "reason":"Quatro propostas, das diretorias Financeira e Marketing, descrevem o mesmo pano de fundo macroeconômico: juros altos, endividamento e aversão ao risco reduzindo o consumo do pequeno varejo.",
     "originals":[
       ["Maior aversão ao risco por parte dos bancos e fundos em relação ao setor varejista.","Financeira","Ambos"],
       ["Manutenção Selic em altos patamares (Incerteza do Mercado, Eleição, etc)","Financeira","Ambos"],
       ["Endividamento atual das empresas e pessoas físicas x poder de compra (< consumo, principalmente no varejo)","Financeira","Ambos"],
       ["Cenário macroeconômico desafiador, com capacidade financeira limitada do pequeno varejo brasileiro","Marketing","Ambos"]
     ]},
    {"title":"Migração do consumo para o digital e queda da recarga eletrônica no varejo físico", "reason":"Ambas descrevem o mesmo efeito: a queda da recarga eletrônica como consequência da migração do consumo para o digital.",
     "originals":[
       ["Migração do consumo para os canais digitais","Operações","Telecom"],
       ["Redução acelerada da demanda por recarga eletrônica no varejo físico (perda de base eletrônica)","Operações","Ambos"]
     ]},
    {"title":"Aumento da concorrência no canal pré-pago no Telecom", "reason":"Unificação dentro do arquivo Telecom, mesma diretoria (Operações): duas propostas descrevem o mesmo aumento de concorrência no canal pré-pago.",
     "originals":[
       ["Desregionalização do canal pré-pago (mercado aberto - todo mundo vende onde quiser)","Operações","Telecom"],
       ["Entrada de novos players no telecom (Aqui tem+, Martins, I2GO)","Operações","Telecom"]
     ]}
  ]
}

SOLOS_TELECOM = {
  "forcas": [
    ["ERP com fluxos integrados entre as áreas, facilitando novas implantações/atualizações e exigências legais (Ex. Reforma Tributária)","Financeira","Ambos"],
    ["Planejamento tributário com resultados comprovados de redução efetiva da carga tributária (ex.: ebook, migração de regime LR x LP)","Financeira","Ambos"],
    ["Portfólio amplo e diversificado","Marketing","Ambos"],
    ["Força de vendas com atendimento presencial","Operações","Ambos"]
  ],
  "fraquezas": [
    ["Concentração do resultado nos produtos telecom","Operações","Telecom"],
    ["Pouca interação com o cliente do Cliente","Operações","Telecom"],
    ["Ausência de auditoria presencial periódica dos estoques nas regionais","Financeira","Ambos"],
    ["Fragmentação dos sistemas e pouca diversificação dos canais de atendimento","Marketing","Ambos"],
    ["Arranjo de pagamento fechado","Marketing","Ambos"],
    ["Retenção no pós-venda e prospecção de clientes de baixa rentabilidade, sem análise de risco adequada","Marketing","Ambos"],
    ["Baixa renovação de equipamentos","Marketing","Ambos"],
    ["Ausência de camada digital de relacionamento sobre a força de vendas","Marketing","Ambos"],
    ["Processos operacionais recorrentes ainda manuais","Marketing","Ambos"],
    ["Baixa oferta de portfólio aos PDVs","Marketing","Ambos"],
    ["Sinergia entre as áreas","Marketing","Ambos"],
    ["Notoriedade de marca e presença digital insuficientes para sustentar a expansão de portfólio","Marketing","Ambos"],
    ["Capacidade de investimento devido a margem reduzida","Tecnologia","Ambos"],
    ["Limitação do nosso TI para desenvolvimento de ferramentas de inteligência de vendas","Operações","Ambos"]
  ],
  "oportunidades": [
    ["Parcerias com software house","Operações","Telecom"],
    ["Atuação no Cliente do Cliente (B2B e B2C)","Operações","Telecom"],
    ["Reduzir custo logístico na venda e entrega do chip","Operações","Telecom"],
    ["Benefício da compra a vista do Telecom","Operações","Telecom"],
    ["Crescimento via canais digitais e mudança no comportamento de compra","Marketing","Ambos"],
    ["Encontrar \"O Produto\" + \"Nicho\" para ser escalado na Máquina de Originação (B2B & B2C)","Tecnologia","Ambos"],
    ["Crescente demanda por produtos de automação de vendas e marketing (B2B)","Tecnologia","Ambos"],
    ["Expansão do Kiddle","Operações","Ambos"]
  ],
  "ameacas": [
    ["Perda de oportunidade de novos negócios/contratos devido à fragilidade de caixa","Operações","Telecom"],
    ["Obrigatoriedade do reconhecimento facial na ativação do chip","Operações","Telecom"],
    ["Mudanças no padrão de atendimento ao cliente","Marketing","Ambos"],
    ["Adquirência: Falta de competitividade (Mar Vermelho, Produto Comoditizado)","Tecnologia","Ambos"],
    ["Cenário Geopolítico incerto (política e guerras)","Operações","Ambos"]
  ]
}

# ============================================================================
# Data: Não Telecom + Ambos SWOT (copiado verbatim de votacao_ntelecom/generate.py)
# ============================================================================
CONVERGENCES_NTELECOM = {
  "forcas": [
  ],
  "fraquezas": [
    {"title":"Baixo foco e integração dos produtos não-telecom aos sistemas da RV", "reason":"Três propostas, de duas diretorias, apontam a mesma fragilidade: os produtos não-telecom (energia, serviços financeiros/coban) carecem de foco estratégico e de integração aos sistemas da RV.",
     "originals":[
       ["Produtos não telecom (energia, serviços financeiros etc.) sem integração aos sistemas RV","Marketing","Não Telecom"],
       ["Falta de foco nos produtos não-telecom","Marketing","Não Telecom"],
       ["Falta de integração sistêmica para os produtos de energia e coban","Operações","Não Telecom"]
     ]},
    {"title":"Fragilidades do produto e do modelo de receita de Adquirência", "reason":"Duas propostas da Diretoria de Marketing descrevem a mesma fragilidade competitiva do produto de Adquirência: falta de diferenciação e um modelo de receita desalinhado com as condições de adoção do mercado.",
     "originals":[
       ["Diferenciação do produto Adquirência","Marketing","Não Telecom"],
       ["Modelo de receita da adquirência em conflito com as condições de adoção do mercado","Marketing","Não Telecom"]
     ]},
    {"title":"Dependência do parceiro e baixa retenção do cliente de Adquirência", "reason":"Três propostas, de duas diretorias, tratam do mesmo problema: a experiência, a satisfação e a retenção do cliente de Adquirência dependem do parceiro adquirente, fragilizando o relacionamento direto com a RV.",
     "originals":[
       ["Experiência do cliente dependente do parceiro adquirente","Marketing","Não Telecom"],
       ["Reputação e satisfação do cliente de adquirência","Marketing","Não Telecom"],
       ["Retenção de clientes de adquirência","Operações","Não Telecom"]
     ]},
    {"title":"Parque de POS defasado e cobrança fora do padrão de mercado", "reason":"Duas propostas da Diretoria de Operações descrevem fragilidades relacionadas ao mesmo equipamento (POS): parque próprio defasado e modelo de cobrança do aluguel fora do padrão do mercado (boleto em vez de recebíveis).",
     "originals":[
       ["Parque de POS próprio defasado (Stone)","Operações","Não Telecom"],
       ["Cobrança do aluguel do POS em boleto (padrão de mercado é nos recebíveis)","Operações","Não Telecom"]
     ]},
    {"title":"Falta de estrutura logística e de gestão para produtos físicos (não-telecom)", "reason":"Duas propostas da Diretoria de Operações apontam a ausência da mesma estrutura de suporte — processo logístico e sistema de gestão (back office e front office) — para os produtos físicos não-telecom.",
     "originals":[
       ["Falta de um processo logístico para entrega de produtos físicos (acessórios, outros)","Operações","Não Telecom"],
       ["Falta de um sistema de gestão (back office e front office) especializado em produtos físicos (não telecom)","Operações","Não Telecom"]
     ]},
  ],
  "oportunidades": [
    {"title":"Abertura e expansão do mercado de energia (baixa tensão e modelo white label)", "reason":"Duas propostas, de duas diretorias, tratam da mesma oportunidade: a abertura do mercado livre de energia, seja pela migração para baixa tensão, seja por parcerias no modelo white label com geradoras.",
     "originals":[
       ["Migração do mercado livre de energia para baixa tensão","Marketing","Não Telecom"],
       ["Abertura do mercado livre de energia e desenvolver parcerias com geradoras de energia no modelo white label","Operações","Não Telecom"]
     ]},
    {"title":"Expansão de crédito e serviços financeiros para o varejo (PME)", "reason":"Três propostas, de duas diretorias, apontam a mesma oportunidade de crescimento em serviços financeiros e crédito, com destaque para a demanda dos varejistas (PME).",
     "originals":[
       ["Abertura do mercado de pagamentos/financeiro","Marketing","Não Telecom"],
       ["Crescimento da demanda por serviço de banking/crédito","Operações","Não Telecom"],
       ["Necessidade de crédito por parte dos varejistas (PME)","Operações","Não Telecom"]
     ]},
    {"title":"Novas parcerias comerciais com adquirentes e subadquirentes", "reason":"Duas propostas da Diretoria de Operações tratam da mesma oportunidade de ampliar parcerias comerciais com adquirentes/subadquirentes, inclusive por meio da liberação de vouchers.",
     "originals":[
       ["Desenvolver parcerias com novos adquirentes/subadquirente","Operações","Não Telecom"],
       ["Liberação de Vouchers para todos os adquirentes","Operações","Não Telecom"]
     ]},
    {"title":"Novos canais físicos por meio de parcerias com grandes marcas e empresas de produtos físicos", "reason":"Duas propostas da Diretoria de Operações descrevem a mesma oportunidade de expandir a rede de canais físicos por meio de parcerias com grandes marcas e empresas de produtos físicos.",
     "originals":[
       ["Grandes marcas buscando novos canais físicos de vendas e atendimento (PDVE Claro, Vivo, BB, Seguros, Energia etc)","Operações","Não Telecom"],
       ["Expansão de parcerias com empresas de produtos físicos","Operações","Não Telecom"]
     ]},
    {"title":"Ampliação da oferta de serviços de valor agregado e gestão de equipes especializadas", "reason":"Duas propostas da Diretoria de Operações tratam da mesma oportunidade de crescimento em serviços de valor agregado (telemedicina, jurídico etc.), que demandará gestão de equipes especializadas.",
     "originals":[
       ["Ampliação da oferta e procura por serviços como telemedicina, assessoria jurídica entre outros","Operações","Não Telecom"],
       ["Demanda crescente por gestão de equipes especializadas em serviços (PAP, varejo, promotores etc)","Operações","Não Telecom"]
     ]},
  ],
  "ameacas": [
    {"title":"Desintermediação do PDV pelo crescimento do PIX direto", "reason":"Duas propostas da Diretoria de Operações descrevem a mesma ameaça: o crescimento do consumo direto via PIX reduz a intermediação e a relevância do canal físico (PDV) e dos adquirentes.",
     "originals":[
       ["Descontinuidade de produtos Verticais para os canais físicos e digitais (consumo direto via pix)","Operações","Não Telecom"],
       ["Crescimento da utilização do PIX sem intermediação pelos adquirentes","Operações","Não Telecom"]
     ]},
    {"title":"Concorrência de novos players e dos próprios contratantes no atendimento do PDV", "reason":"Duas propostas, de duas diretorias, apontam o mesmo risco competitivo: novos entrantes e os próprios contratantes (adquirentes/operadoras) passando a atender o PDV diretamente, reduzindo o papel de intermediação da RV.",
     "originals":[
       ["Entrada de novos players no mercado de adquirência e produtos financeiros","Marketing","Não Telecom"],
       ["Atendimento direto do PDV através dos contratantes (Pagseguro, Stone, Operadoras, etc)","Operações","Não Telecom"]
     ]},
  ],
}

SOLOS_NTELECOM = {
  "forcas": [
    ["Portfólio diversificado de produtos","Operações","Não Telecom"]
  ],
  "fraquezas": [
    ["Concentração do resultado em um produto único (chip)","Marketing","Não Telecom"],
    ["Ausência de equipe especializada para venda de adquirência, serviços financeiros etc","Operações","Não Telecom"],
    ["Fragilidade cadastral / falta de CRM","Operações","Não Telecom"],
    ["Falta de plataforma segura/estável conversacional para Whatsapp/Atendimento via IA","Operações","Não Telecom"],
    ["Falta de uma oferta proprietária da RV de produtos financeiros (maquininha, conta, empréstimos, softwares etc)","Operações","Não Telecom"]
  ],
  "oportunidades": [
    ["Fusões e Aquisições","Operações","Não Telecom"],
    ["Aumento da utilização da IA para ganho de produtividade em vendas, atendimento, desenvolvimento de serviços etc","Operações","Não Telecom"],
    ["Novos Negócios no mercado Telecom fora Pré","Operações","Não Telecom"],
    ["Atuação no cliente do cliente (aproveitamento do tráfego de clientes do clientes físico e digital)","Operações","Não Telecom"]
  ],
  "ameacas": [
    ["Popularização do E-sim reduzindo capilaridade física da RV","Operações","Não Telecom"]
  ],
}

# ============================================================================
# ITEMS: todos os itens-base das duas etapas, por quadrante.
# ============================================================================
ITEMS = {
  "telecom": {q["key"]: build_items(CONVERGENCES_TELECOM, SOLOS_TELECOM, q["key"]) for q in QUADRANTS},
  "naotelecom": {q["key"]: build_items(CONVERGENCES_NTELECOM, SOLOS_NTELECOM, q["key"]) for q in QUADRANTS},
}

# ============================================================================
# VOTE_TEMPLATE — página única de votação, parametrizada por ?stage=&quad=
# (substitui os 8 arquivos estáticos das duas gerações anteriores)
# ============================================================================
VOTE_TEMPLATE = HEAD.replace("__PAGE_TITLE__", "Votação SWOT — RV Digital 2027").replace(
    "__PAGE_DESC__", "Votação anônima sobre as propostas do painel SWOT — RV Digital 2027."
) + r"""
<body>

<header class="hero">
  <div class="hero-inner">
    <div class="hero-text">
      <a class="back-to-menu" href="./index.html">&larr; Voltar ao menu</a>
      <div class="hero-eyebrow" id="hero-eyebrow">RV Digital &middot; Planejamento Estrat&eacute;gico 2027</div>
      <h1 class="hero-title">Vota&ccedil;&atilde;o &mdash; <span id="quad-label-span">&hellip;</span></h1>
      <div class="hero-sub" id="hero-sub">Carregando&hellip;</div>
    </div>
    <div class="rv-logo hero-logo"><img src="data:image/png;base64,__LOGO_A_B64__" alt="RV Digital"></div>
  </div>
</header>

<main>
  <div id="view-error" style="display:none;">
    <div class="intro">
      <h2 style="font-size:17px; margin-bottom:8px; color:var(--red);">N&atilde;o foi poss&iacute;vel abrir esta vota&ccedil;&atilde;o</h2>
      <p style="font-size:14.5px; color:var(--ink-soft);" id="error-text">Par&acirc;metros inv&aacute;lidos na URL.</p>
      <p style="margin-top:14px;"><a href="./index.html">&larr; Voltar ao menu e escolher novamente</a></p>
    </div>
  </div>

  <section class="view" id="view-vote">
    <div class="intro">
      <p style="font-size:14.5px; margin:0 0 10px; font-weight:500;">Para cada item, avalie seu grau de concord&acirc;ncia com a prioriza&ccedil;&atilde;o da proposta:</p>
      <div class="scale">
        <div class="scale-row s5"><div class="scale-num">5</div><p><b>Concordo totalmente</b> &mdash; este item deve ser altamente priorizado.</p></div>
        <div class="scale-row s3"><div class="scale-num">3</div><p><b>Concordo parcialmente</b> &mdash; este item &eacute; relevante, mas n&atilde;o priorit&aacute;rio.</p></div>
        <div class="scale-row s1"><div class="scale-num">1</div><p><b>Discordo</b> &mdash; este item n&atilde;o deve ser priorizado.</p></div>
      </div>
      <div class="anon-note"><span class="ic">&#128274;</span>Sua vota&ccedil;&atilde;o &eacute; an&ocirc;nima: ningu&eacute;m vê quem votou o qu&ecirc; &mdash; apenas os totais agregados, e somente para os administradores autorizados. N&atilde;o &eacute; necess&aacute;rio fazer login.</div>
      <div class="anon-note" style="background:var(--surface-2);"><span class="ic">&#128190;</span>V&aacute; marcando suas respostas normalmente. Nada &eacute; enviado ainda &mdash; s&oacute; quando voc&ecirc; clicar em <b>"Salvar respostas"</b>, no final da p&aacute;gina, é que elas s&atilde;o gravadas. N&atilde;o atualize a p&aacute;gina antes de salvar, ou as marca&ccedil;&otilde;es ainda n&atilde;o salvas ser&atilde;o perdidas.</div>
      <div id="already-voted-note" class="already-voted-note" style="display:none;"></div>
      <div class="tag-legend" id="tag-legend"></div>
    </div>

    <div class="progress-wrap">
      <div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="progress-label"><span id="progress-text">Carregando&hellip;</span><span id="vote-status-text"></span></div>
    </div>

    <div class="origin-filter" id="origin-filter" style="display:none;">
      <span class="origin-filter-label">Mostrar:</span>
    </div>

    <div id="items-mount"></div>

    <div class="save-bar">
      <div class="save-bar-text" id="save-bar-text">Carregando&hellip;</div>
      <button class="save-btn" id="save-btn" disabled>Salvar respostas</button>
    </div>
    <div class="save-flash" id="save-flash"></div>
  </section>
</main>

<footer class="pagefoot">
  <div class="pagefoot-inner">
    <div class="rv-logo pagefoot-logo"><img src="data:image/png;base64,__LOGO_B_B64__" alt="RV Digital"></div>
    <div class="pagefoot-text" id="pagefoot-text">Planejamento Estrat&eacute;gico RV Digital 2027</div>
  </div>
</footer>

<script>
function fatalConfigError(e){
  var msg = "Erro de configura&ccedil;&atilde;o do site: " + (e && e.message ? e.message : String(e));
  var mount = document.getElementById("items-mount");
  if(mount){
    mount.innerHTML = '<div style="background:#fbe9e9;border:1px solid #e0a0a0;border-radius:10px;padding:18px 20px;color:#7a1f1f;font-size:14px;line-height:1.5;">'
      + '<b>&#9888; ' + msg + '</b><br><br>'
      + 'Isso normalmente significa que o arquivo <code>supabase-config.js</code> n&atilde;o foi preenchido corretamente '
      + '(URL ou chave ausente, incorreta, ou colada com quebra de linha no meio). Avise o administrador do site para revisar o Passo 5 do manual.'
      + '</div>';
  }
  var bar = document.getElementById("save-bar-text");
  if(bar) bar.textContent = "Não foi possível carregar a votação.";
  var btn = document.getElementById("save-btn");
  if(btn) btn.disabled = true;
  console.error("Config/init error:", e);
}

function showFatalParamError(msg){
  document.getElementById("view-vote").classList.remove("active");
  document.getElementById("view-vote").style.display = "none";
  document.getElementById("view-error").style.display = "block";
  document.getElementById("error-text").textContent = msg;
}

try{

var QUADS_META = __QUADS_META_JSON__;      // { forcas:{label,accent,accent_soft}, ... }
var ITEMS_ALL = __ITEMS_ALL_JSON__;        // { telecom:{forcas:[...],...}, naotelecom:{...} }
var STAGE_LABELS = { telecom: "Telecom + Ambos", naotelecom: "Não Telecom + Ambos" };

var params = new URLSearchParams(location.search);
var STAGE = params.get("stage");
var QUAD = params.get("quad");
var validStage = (STAGE === "telecom" || STAGE === "naotelecom");
var validQuad = QUAD && Object.prototype.hasOwnProperty.call(QUADS_META, QUAD);

if(!validStage || !validQuad){
  var problems = [];
  if(!validStage) problems.push('a etapa ("stage") precisa ser "telecom" ou "naotelecom"');
  if(!validQuad) problems.push('o quadrante ("quad") precisa ser um dos 4 quadrantes do SWOT');
  showFatalParamError("O link usado não tem os parâmetros corretos na URL: " + problems.join(" e ") + ". Volte ao menu e escolha novamente.");
  throw new Error("parâmetros inválidos (stage=" + STAGE + ", quad=" + QUAD + ")");
}

document.getElementById("view-vote").classList.add("active");
document.getElementById("view-vote").style.display = "block";

var qmeta = QUADS_META[QUAD];
document.documentElement.style.setProperty("--accent", qmeta.accent);
document.documentElement.style.setProperty("--accent-soft", qmeta.accent_soft);
document.title = "Votação SWOT — " + qmeta.label + " — " + STAGE_LABELS[STAGE] + " — RV Digital 2027";
document.getElementById("quad-label-span").textContent = qmeta.label;
document.getElementById("hero-eyebrow").textContent = "RV Digital · Planejamento Estratégico 2027 · SWOT " + STAGE_LABELS[STAGE];
document.getElementById("pagefoot-text").textContent = "Planejamento Estratégico RV Digital 2027 — Votação anônima do quadrante " + qmeta.label + " · SWOT " + STAGE_LABELS[STAGE];

var BASE_ITEMS = ITEMS_ALL[STAGE][QUAD];
var ITEMS = JSON.parse(JSON.stringify(BASE_ITEMS));
updateHeroSub();

// A conexão com o Supabase é inicializada só mais abaixo (depois da lista de
// itens já estar na tela): assim, mesmo se a biblioteca do Supabase não
// carregar (ex.: sem internet) ou supabase-config.js estiver incompleto, a
// pessoa ainda vê a lista de propostas e o formulário — só não consegue
// salvar, com um aviso claro em vez de uma tela em branco.
var sb = null;
var sbConfigError = null;

function initSupabaseClient(){
  if(!window.RV_SUPABASE_URL || !window.RV_SUPABASE_ANON_KEY || window.RV_SUPABASE_URL.indexOf("COLOQUE_AQUI") !== -1){
    sbConfigError = new Error("supabase-config.js não está preenchido (URL ou chave ausente).");
    return;
  }
  if(!window.supabase || !window.supabase.createClient){
    sbConfigError = new Error("Não foi possível carregar a biblioteca do Supabase (verifique sua conexão com a internet).");
    return;
  }
  try{
    sb = window.supabase.createClient(window.RV_SUPABASE_URL, window.RV_SUPABASE_ANON_KEY);
  }catch(e){
    sbConfigError = e;
  }
}

function getClientId(){
  var k = "rv_swot_client_id";
  var id = localStorage.getItem(k);
  if(!id){
    id = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : ("id-" + Date.now() + "-" + Math.random().toString(16).slice(2));
    try{ localStorage.setItem(k, id); }catch(e){}
  }
  return id;
}
var myId = getClientId();
var myVotes = {};
var savedVotes = {};
var votingOpen = true, saving = false;
var currentFilter = "all";

function updateHeroSub(){
  var sub = document.getElementById("hero-sub");
  if(sub) sub.textContent = "Votação anônima. Esta votação é exclusiva do quadrante " + qmeta.label.toLowerCase() + " (" + ITEMS.length + " itens).";
}

function origSlug(o){
  if(o === "Telecom") return "telecom";
  if(o === "Não Telecom") return "naotelecom";
  return "ambos";
}
function origClass(o){
  if(o === "Telecom") return "t";
  if(o === "Não Telecom") return "nt";
  return "a";
}
function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}
function tagLabelFromOrigins(origins){
  var has = {};
  (origins || []).forEach(function(o){ has[o] = true; });
  if(has["Não Telecom"]) return "Não Telecom";
  if(has["Telecom"] && has["Ambos"]) return "Telecom + Ambos";
  if(has["Telecom"]) return "Telecom";
  return "Ambos";
}

function distinctOrigins(){
  var set = {};
  ITEMS.forEach(function(it){ (it.origins||[]).forEach(function(o){ set[o]=true; }); });
  return Object.keys(set);
}

function itemMatchesFilter(it){
  if(currentFilter === "all") return true;
  return (it.origins || []).indexOf(currentFilter) !== -1;
}

function renderOriginFilterAndLegend(){
  var wrap = document.getElementById("origin-filter");
  var legend = document.getElementById("tag-legend");
  var origins = distinctOrigins();
  if(origins.length <= 1){
    wrap.style.display = "none";
    legend.innerHTML = "";
    currentFilter = "all";
    return;
  }
  wrap.style.display = "flex";
  var order = ["Telecom","Ambos","Não Telecom"].filter(function(o){ return origins.indexOf(o) !== -1; });
  var html = '<span class="origin-filter-label">Mostrar:</span><button data-filter="all" class="' + (currentFilter==="all"?"active":"") + '">Todas <span class="cnt">(' + ITEMS.length + ')</span></button>';
  order.forEach(function(o){
    var n = ITEMS.filter(function(it){ return (it.origins||[]).indexOf(o) !== -1; }).length;
    html += '<button data-filter="' + escapeHtml(o) + '" class="' + (currentFilter===o?"active":"") + '">' + escapeHtml(o) + ' <span class="cnt">(' + n + ')</span></button>';
  });
  wrap.innerHTML = html;

  var legendDescs = {
    "Ambos": "proposta relevante tanto para o negócio <b>Telecom</b> quanto para o <b>Não Telecom</b>.",
    "Telecom": "proposta específica do negócio <b>Telecom</b>.",
    "Não Telecom": "proposta específica do negócio <b>Não Telecom</b> (inclui propostas migradas da etapa Telecom + Ambos com tag Ambos, já priorizadas lá)."
  };
  var legHtml = "";
  order.forEach(function(o){
    legHtml += '<div class="leg-row"><span class="chip origin-' + origSlug(o) + '">' + escapeHtml(o) + '</span><span>' + (legendDescs[o] || "") + '</span></div>';
  });
  legend.innerHTML = legHtml;
}

function renderItems(){
  var mount = document.getElementById("items-mount");
  var native = ITEMS.filter(function(it){ return !it.migrated; });
  var migrated = ITEMS.filter(function(it){ return it.migrated; });
  var idx = 0;
  var html = "";
  // Numeração (#N) segue a posição no conjunto completo de itens (incluindo
  // migrados), mesmo com o filtro ativo, para o número de cada proposta não
  // mudar dependendo do filtro.
  native.forEach(function(it){ idx++; if(itemMatchesFilter(it)) html += renderItem(it, idx); });
  if(!html) html = '<div class="empty-note">Nenhuma proposta nesta categoria.</div>';
  if(STAGE === "naotelecom"){
    var migHtml = "";
    migrated.forEach(function(it){ idx++; if(itemMatchesFilter(it)) migHtml += renderItem(it, idx); });
    html += '<div class="migrated-heading">Também priorizadas em Telecom + Ambos (tag Ambos)</div>';
    html += migHtml || '<div class="empty-note">Nenhum item com tag Ambos foi priorizado ainda na etapa Telecom + Ambos.</div>';
  }
  mount.innerHTML = html;
  renderOriginFilterAndLegend();
}

function renderItem(it, idx){
  var typeChip = it.type === "convergencia"
    ? '<span class="chip type-c">Convergência · '+it.n+' propostas</span>'
    : '<span class="chip">Proposta isolada</span>';
  var divisionChips = (it.divisions || []).map(function(a){ return '<span class="chip">'+escapeHtml(a)+'</span>'; }).join("");
  var originChips = (it.origins || []).map(function(o){
    return '<span class="chip origin-'+origSlug(o)+'">'+escapeHtml(o)+'</span>';
  }).join("");
  var migChip = it.migrated ? '<span class="chip migrated-chip">Ambos · já priorizada em Telecom + Ambos</span>' : "";
  var details = "";
  if(it.type === "convergencia" && it.originals){
    var origLis = it.originals.map(function(o){
      return "<li>"+escapeHtml(o.text)+' <span class="oi-origin '+origClass(o.origin)+'">'+escapeHtml(o.origin)+'</span></li>';
    }).join("");
    details = '<details class="orig"><summary>Ver as '+it.originals.length+' propostas originais e o motivo da unifica&ccedil;&atilde;o</summary>'
      + '<ol>'+origLis+'</ol>'
      + '<div class="reason">'+escapeHtml(it.reason)+'</div>'
      + '</details>';
  }
  return '<div class="item'+(it.migrated?' is-migrated':'')+'" id="item-'+it.id+'" data-id="'+it.id+'">'
    + '<div class="item-top"><div class="item-idx mono">#'+idx+'</div><div class="item-title">'+escapeHtml(it.title)+'</div></div>'
    + '<div class="item-meta">'+migChip+typeChip+originChips+divisionChips+'</div>'
    + details
    + '<div class="vote-row">'
    +   voteBtn(it.id,5,"Concordo totalmente")
    +   voteBtn(it.id,3,"Concordo parcialmente")
    +   voteBtn(it.id,1,"Discordo")
    + '</div>'
    + '<div class="save-tag" id="save-'+it.id+'"><span class="save-tag-pending">&#9679; Selecionado &mdash; ainda n&atilde;o salvo</span><span class="save-tag-saved">&#10003; Salvo</span></div>'
    + '</div>';
}
function voteBtn(itemId, score, label){
  return '<button class="vote-btn" data-score="'+score+'" onclick="castVote(\''+itemId+'\','+score+')">'
    + '<span class="vnum">'+score+'</span><span class="vtxt"><b>'+label+'</b></span>'
    + '</button>';
}

function isDirty(itemId){ return myVotes[itemId] !== savedVotes[itemId]; }
function countDirty(){ var n=0; ITEMS.forEach(function(it){ if(isDirty(it.id)) n++; }); return n; }

function updateProgress(){
  var voted = Object.keys(myVotes).length;
  document.getElementById("progress-fill").style.width = (ITEMS.length ? Math.round(voted/ITEMS.length*100) : 0) + "%";
  document.getElementById("progress-text").textContent = voted + " de " + ITEMS.length + " respondidos";
  document.getElementById("vote-status-text").textContent = votingOpen ? "" : "Votação encerrada pelo administrador";
}
function paintMyVotes(){
  ITEMS.forEach(function(it){
    var card = document.getElementById("item-"+it.id);
    if(!card) return;
    var score = myVotes[it.id];
    card.classList.toggle("voted", score !== undefined);
    card.querySelectorAll(".vote-btn").forEach(function(b){
      b.classList.toggle("sel", score !== undefined && String(score) === b.getAttribute("data-score"));
      b.disabled = !votingOpen;
      b.style.opacity = votingOpen ? "1" : ".55";
      b.style.cursor = votingOpen ? "pointer" : "not-allowed";
    });
    var tag = document.getElementById("save-"+it.id);
    if(tag){ tag.dataset.state = score === undefined ? "" : (isDirty(it.id) ? "pending" : "saved"); }
  });
  updateProgress();
  updateSaveBar();
}
function allAnswered(){ return ITEMS.length > 0 && Object.keys(myVotes).length === ITEMS.length; }
function updateSaveBar(){
  var text = document.getElementById("save-bar-text");
  var btn = document.getElementById("save-btn");
  if(!text || !btn) return;
  var dirty = countDirty();
  var answered = Object.keys(myVotes).length;
  var missing = ITEMS.length - answered;
  if(saving){
    text.textContent = "Salvando suas respostas…";
    btn.textContent = "Salvando…"; btn.disabled = true; btn.className = "save-btn state-saving";
    return;
  }
  if(!votingOpen){
    text.textContent = "Votação encerrada pelo administrador — não é mais possível salvar.";
    btn.disabled = true; btn.className = "save-btn"; btn.textContent = "Salvar respostas";
    return;
  }
  if(answered === 0){
    text.textContent = "Nenhuma resposta selecionada ainda. Responda todos os " + ITEMS.length + " itens para poder salvar.";
  } else if(missing > 0){
    text.textContent = answered + " de " + ITEMS.length + " respondidos — faltam " + missing + " item" + (missing === 1 ? "" : "s") + " para poder salvar.";
  } else if(dirty === 0){
    text.textContent = answered + " de " + ITEMS.length + " respondidos — tudo salvo.";
  } else {
    text.textContent = answered + " de " + ITEMS.length + " respondidos — " + dirty + " alteração(ões) ainda não salva(s).";
  }
  var canSave = allAnswered() && dirty > 0;
  btn.disabled = !canSave;
  btn.className = "save-btn" + (dirty === 0 && answered > 0 ? " state-saved" : "");
  btn.textContent = missing > 0 ? ("Responda todos para salvar (" + missing + " restante" + (missing === 1 ? "" : "s") + ")") : (dirty > 0 ? ("Salvar respostas (" + dirty + ")") : "Salvar respostas");
}
function showFlash(msg, isError){
  var flash = document.getElementById("save-flash");
  if(!flash) return;
  flash.textContent = (isError ? "⚠ " : "✓ ") + msg;
  flash.className = "save-flash show" + (isError ? " error" : "");
  clearTimeout(flash._t);
  flash._t = setTimeout(function(){ flash.className = "save-flash"; }, 5000);
}
function castVote(itemId, score){
  if(!votingOpen || saving) return;
  myVotes[itemId] = score;
  paintMyVotes();
}

function showAlreadyVotedNoteIfAny(){
  try{
    var key = "rv_voted_" + STAGE + "_" + QUAD;
    var ts = localStorage.getItem(key);
    if(!ts) return;
    var d = new Date(ts);
    var formatted = isNaN(d.getTime()) ? ts : d.toLocaleString("pt-BR");
    var note = document.getElementById("already-voted-note");
    note.style.display = "block";
    note.textContent = "Você já registrou respostas para este quadrante em " + formatted + " — você pode revisar e alterar suas respostas abaixo.";
  }catch(e){ /* localStorage indisponível — apenas não mostra o aviso */ }
}
function markVotedInLocalStorage(){
  try{ localStorage.setItem("rv_voted_" + STAGE + "_" + QUAD, new Date().toISOString()); }catch(e){}
}

async function saveAllVotes(){
  if(!votingOpen || saving) return;
  if(!sb){
    showFlash("Sem conexão com o servidor de votação. Verifique sua internet e recarregue a página.", true);
    return;
  }
  if(!allAnswered()){
    var missing = ITEMS.length - Object.keys(myVotes).length;
    showFlash("Responda todos os " + ITEMS.length + " itens antes de salvar (faltam " + missing + ").", true);
    return;
  }
  if(countDirty() === 0) return;
  saving = true; updateSaveBar();
  try{
    // Grava o voto chamando a função save_vote_v2 (ver schema.sql), já com a
    // etapa (stage) — substitui a antiga save_vote de etapa única.
    var res = await sb.rpc("save_vote_v2", { p_stage: STAGE, p_quadrant: QUAD, p_client_id: myId, p_scores: Object.assign({}, myVotes) });
    if(res.error) throw res.error;
    savedVotes = Object.assign({}, myVotes);
    saving = false; paintMyVotes();
    markVotedInLocalStorage();
    showFlash("Respostas salvas com sucesso — registradas anonimamente.", false);
  }catch(e){
    console.warn("save failed", e);
    saving = false; paintMyVotes();
    var detail = (e && (e.message || e.msg || e.hint || e.details)) ? (e.message || e.msg || e.hint || e.details) : "erro desconhecido";
    showFlash("Não foi possível salvar agora (" + detail + "). Verifique sua conexão e clique em \"Salvar respostas\" novamente.", true);
  }
}
document.getElementById("save-btn").addEventListener("click", saveAllVotes);
window.addEventListener("beforeunload", function(e){
  if(countDirty() > 0){ e.preventDefault(); e.returnValue = ""; }
});
document.getElementById("origin-filter").addEventListener("click", function(e){
  var b = e.target.closest("button");
  if(!b) return;
  currentFilter = b.getAttribute("data-filter");
  renderItems();
  paintMyVotes();
});

async function loadConfig(){
  try{
    var res = await sb.from("voting_config").select("is_open").eq("stage", STAGE).eq("quadrant", QUAD).maybeSingle();
    if(!res.error && res.data) votingOpen = !!res.data.is_open;
  }catch(e){ console.warn("config load failed", e); }
  paintMyVotes();
}

function applyChanges(baseItems, editMap, addedList, removedSet){
  // Junta 3 fontes por cima de um conjunto-base de itens: item_edits (textos
  // corrigidos), item_added (propostas criadas pelo admin) e item_removed
  // (propostas ocultadas pelo admin). Usada tanto para a etapa atual quanto
  // para reconstruir a etapa Telecom + Ambos (migração de itens "Ambos").
  var next = baseItems.filter(function(it){ return !removedSet[it.id]; }).map(function(it){
    var clone = JSON.parse(JSON.stringify(it));
    if(editMap[clone.id] !== undefined) clone.title = editMap[clone.id];
    return clone;
  });
  (addedList || []).forEach(function(r){
    if(removedSet[r.item_id]) return;
    next.push({
      id: r.item_id, type: "isolada",
      title: (editMap[r.item_id] !== undefined) ? editMap[r.item_id] : r.title,
      divisions: r.division ? [r.division] : [],
      origins: r.origin ? [r.origin] : ["Ambos"],
      n: 1, originals: null, reason: null
    });
  });
  return next;
}

async function computeMigratedItems(){
  // Só se aplica à etapa Não Telecom: migra para lá, de forma DINÂMICA (nunca
  // uma foto congelada), todo item da etapa Telecom + Ambos deste mesmo
  // quadrante que (a) já foi marcado como priorizado pelo admin na etapa
  // Telecom + Ambos (tabela item_prioritized) e (b) tem tag EXATAMENTE
  // "Ambos" (não "Telecom", nem "Telecom + Ambos", nem "Não Telecom").
  if(STAGE !== "naotelecom") return [];
  try{
    var prioRes = await sb.from("item_prioritized").select("item_id").eq("quadrant", QUAD);
    if(prioRes.error || !prioRes.data || !prioRes.data.length) return [];
    var prioSet = {};
    prioRes.data.forEach(function(r){ prioSet[r.item_id] = true; });

    var tEditsRes = await sb.from("item_edits").select("item_id,title").eq("stage","telecom").eq("quadrant", QUAD);
    var tAddedRes = await sb.from("item_added").select("item_id,title,origin,division").eq("stage","telecom").eq("quadrant", QUAD);
    var tRemovedRes = await sb.from("item_removed").select("item_id").eq("stage","telecom").eq("quadrant", QUAD);
    var tEditMap = {}; if(!tEditsRes.error) (tEditsRes.data||[]).forEach(function(r){ tEditMap[r.item_id] = r.title; });
    var tRemovedSet = {}; if(!tRemovedRes.error) (tRemovedRes.data||[]).forEach(function(r){ tRemovedSet[r.item_id] = true; });
    var tAddedList = (!tAddedRes.error && tAddedRes.data) ? tAddedRes.data : [];

    var telecomItems = applyChanges(ITEMS_ALL["telecom"][QUAD], tEditMap, tAddedList, tRemovedSet);

    var survivors = telecomItems.filter(function(it){
      return prioSet[it.id] && tagLabelFromOrigins(it.origins) === "Ambos";
    });
    var migratedBase = survivors.map(function(it){
      var clone = JSON.parse(JSON.stringify(it));
      clone.id = "mig_" + it.id;
      clone.migrated = true;
      clone.migratedFrom = it.id;
      return clone;
    });

    // Aplica edições/remoções feitas na própria etapa Não Telecom sobre os
    // itens migrados (identificados pelo prefixo "mig_"), sem afetar o item
    // original na etapa Telecom + Ambos.
    var mEditsRes = await sb.from("item_edits").select("item_id,title").eq("stage","naotelecom").eq("quadrant", QUAD);
    var mRemovedRes = await sb.from("item_removed").select("item_id").eq("stage","naotelecom").eq("quadrant", QUAD);
    var mEditMap = {}; if(!mEditsRes.error) (mEditsRes.data||[]).forEach(function(r){ if(r.item_id.indexOf("mig_") === 0) mEditMap[r.item_id] = r.title; });
    var mRemovedSet = {}; if(!mRemovedRes.error) (mRemovedRes.data||[]).forEach(function(r){ if(r.item_id.indexOf("mig_") === 0) mRemovedSet[r.item_id] = true; });

    return migratedBase.filter(function(it){ return !mRemovedSet[it.id]; }).map(function(it){
      var clone = JSON.parse(JSON.stringify(it));
      if(mEditMap[clone.id] !== undefined) clone.title = mEditMap[clone.id];
      return clone;
    });
  }catch(e){ console.warn("migration compute failed", e); return []; }
}

async function loadItemChanges(){
  // Sempre recalcula a partir de BASE_ITEMS (nunca acumula em cima do ITEMS
  // anterior), assim uma remoção desfeita ou uma edição revertida também
  // aparece certo aqui, sem precisar recarregar a página.
  try{
    var editsRes = await sb.from("item_edits").select("item_id,title").eq("stage", STAGE).eq("quadrant", QUAD);
    var addedRes = await sb.from("item_added").select("item_id,title,origin,division").eq("stage", STAGE).eq("quadrant", QUAD);
    var removedRes = await sb.from("item_removed").select("item_id").eq("stage", STAGE).eq("quadrant", QUAD);
    var editMap = {};
    if(!editsRes.error) (editsRes.data || []).forEach(function(r){ editMap[r.item_id] = r.title; });
    var removedSet = {};
    if(!removedRes.error) (removedRes.data || []).forEach(function(r){ removedSet[r.item_id] = true; });
    var addedList = (!addedRes.error && addedRes.data) ? addedRes.data : [];

    var nativeNext = applyChanges(BASE_ITEMS, editMap, addedList, removedSet);
    var migratedNext = await computeMigratedItems();
    var next = nativeNext.concat(migratedNext);

    var prevIds = ITEMS.map(function(i){ return i.id; }).join("|");
    var nextIds = next.map(function(i){ return i.id; }).join("|");
    var titlesChanged = next.some(function(it){
      var prev = ITEMS.filter(function(p){ return p.id === it.id; })[0];
      return !prev || prev.title !== it.title;
    });
    if(prevIds !== nextIds || titlesChanged){
      ITEMS = next;
      renderItems();
      paintMyVotes();
      updateHeroSub();
    }
  }catch(e){ console.warn("item changes load failed", e); }
}

renderItems();
paintMyVotes();
showAlreadyVotedNoteIfAny();

initSupabaseClient();
if(!sb){
  // Lista de itens e formulário continuam visíveis; só o salvamento fica
  // indisponível, com uma mensagem clara (sem tela em branco).
  var bar = document.getElementById("save-bar-text");
  if(bar) bar.textContent = "Sem conexão com o servidor de votação — não é possível salvar agora.";
  var btn = document.getElementById("save-btn");
  if(btn) btn.disabled = true;
  console.warn("Supabase indisponível:", sbConfigError);
} else {
  loadConfig();
  loadItemChanges();
  setInterval(loadConfig, 20000);
  setInterval(loadItemChanges, 20000);
}

}catch(e){ fatalConfigError(e); }
</script>
</body>
</html>
"""

# ============================================================================
# INDEX_TEMPLATE — seletor em duas etapas: 1) etapa, 2) quadrante.
# Nenhum recarregamento de página entre as duas etapas.
# ============================================================================
INDEX_TEMPLATE = HEAD.replace("__PAGE_TITLE__", "Votação SWOT — RV Digital 2027").replace(
    "__PAGE_DESC__", "Escolha a etapa e o quadrante do SWOT que deseja avaliar. Votação anônima, sem necessidade de login."
) + r"""
<body>

<header class="hero" style="padding-bottom:36px;">
  <div class="hero-inner" style="align-items:center;">
    <div class="hero-text" style="padding-top:0;">
      <div class="hero-eyebrow">RV Digital &middot; Planejamento Estrat&eacute;gico 2027</div>
      <h1 class="hero-title">Vota&ccedil;&atilde;o SWOT</h1>
      <div class="hero-sub">Escolha a etapa e o quadrante que deseja avaliar. A vota&ccedil;&atilde;o &eacute; an&ocirc;nima e n&atilde;o exige login.</div>
    </div>
    <div class="rv-logo hero-logo"><img src="data:image/png;base64,__LOGO_A_B64__" alt="RV Digital"></div>
  </div>
</header>

<main style="max-width:680px;">

  <div id="step1">
    <div class="stage-grid">
      <div class="stage-card" data-stage="telecom" style="--mc-accent:#14548c; --mc-soft:#e4edf6;" tabindex="0" role="button">
        <div class="stage-card-icon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div>
        <div class="stage-card-title">Telecom + Ambos</div>
        <div class="stage-card-desc">Votação sobre as propostas SWOT do negócio Telecom e das propostas que valem para os dois negócios.</div>
      </div>
      <div class="stage-card" data-stage="naotelecom" style="--mc-accent:#0d6b4a; --mc-soft:#e2f7ee;" tabindex="0" role="button">
        <div class="stage-card-icon"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg></div>
        <div class="stage-card-title">N&atilde;o Telecom + Ambos</div>
        <div class="stage-card-desc">Votação sobre as propostas SWOT do negócio Não Telecom e das propostas "Ambos" já priorizadas na etapa Telecom.</div>
        <div class="stage-card-note" id="naotelecom-note" style="display:none;">Dispon&iacute;vel ap&oacute;s a prioriza&ccedil;&atilde;o da etapa Telecom + Ambos.</div>
      </div>
    </div>
    <div style="text-align:center; margin-top:30px;">
      <a href="admin.html" class="admin-link-pill">&#128274; Acesso administrativo (resultados)</a>
    </div>
    <div class="index-footnote">Sua vota&ccedil;&atilde;o &eacute; an&ocirc;nima: apenas os totais agregados ficam vis&iacute;veis, e somente para os administradores autorizados.</div>
  </div>

  <div id="step2-telecom">
    <button class="step-back" data-back="1">&larr; voltar</button>
    <div class="menu-grid" data-stage-grid="telecom">
      __MENU_CARDS_TELECOM__
    </div>
  </div>

  <div id="step2-naotelecom">
    <button class="step-back" data-back="1">&larr; voltar</button>
    <div class="menu-grid" data-stage-grid="naotelecom">
      __MENU_CARDS_NAOTELECOM__
    </div>
  </div>

</main>

<footer class="pagefoot">
  <div class="pagefoot-inner">
    <div class="rv-logo pagefoot-logo"><img src="data:image/png;base64,__LOGO_B_B64__" alt="RV Digital"></div>
    <div class="pagefoot-text">Planejamento Estrat&eacute;gico RV Digital 2027</div>
  </div>
</footer>

<script>
try{

var sb = null;
try{
  if(window.RV_SUPABASE_URL && window.RV_SUPABASE_ANON_KEY && window.RV_SUPABASE_URL.indexOf("COLOQUE_AQUI") === -1){
    sb = window.supabase.createClient(window.RV_SUPABASE_URL, window.RV_SUPABASE_ANON_KEY);
  }
}catch(e){ console.warn("supabase init failed on index", e); }

function showStep2(stage){
  document.getElementById("step1").style.display = "none";
  document.getElementById("step2-telecom").style.display = (stage === "telecom") ? "block" : "none";
  document.getElementById("step2-naotelecom").style.display = (stage === "naotelecom") ? "block" : "none";
  paintVotedBadges();
}
function showStep1(){
  document.getElementById("step1").style.display = "block";
  document.getElementById("step2-telecom").style.display = "none";
  document.getElementById("step2-naotelecom").style.display = "none";
}
document.querySelectorAll(".stage-card").forEach(function(card){
  card.addEventListener("click", function(){ showStep2(card.getAttribute("data-stage")); });
  card.addEventListener("keydown", function(e){ if(e.key === "Enter" || e.key === " "){ e.preventDefault(); showStep2(card.getAttribute("data-stage")); } });
});
document.querySelectorAll(".step-back").forEach(function(b){
  b.addEventListener("click", showStep1);
});

function paintVotedBadges(){
  try{
    document.querySelectorAll(".menu-card[data-stage][data-quad]").forEach(function(card){
      var stage = card.getAttribute("data-stage");
      var quad = card.getAttribute("data-quad");
      var key = "rv_voted_" + stage + "_" + quad;
      var voted = !!localStorage.getItem(key);
      card.classList.toggle("is-voted", voted);
      var badgeSlot = card.querySelector(".voted-badge-slot");
      if(badgeSlot) badgeSlot.innerHTML = voted ? '<span class="voted-badge">J&aacute; votado</span>' : "";
    });
  }catch(e){ /* localStorage indisponível — apenas não mostra os selos */ }
}
paintVotedBadges();

(async function checkNaoTelecomStatus(){
  if(!sb) return;
  try{
    var res = await sb.from("voting_config").select("is_open").eq("stage", "naotelecom");
    if(res.error || !res.data || res.data.length < 4) return;
    var allClosed = res.data.every(function(r){ return !r.is_open; });
    if(allClosed){ document.getElementById("naotelecom-note").style.display = "block"; }
  }catch(e){ /* falha de rede/RLS — ignora silenciosamente, nunca quebra o seletor */ }
})();

}catch(e){ console.error("index init error", e); }
</script>
</body>
</html>
"""

def menu_card_html(stage, q):
    return (
        '<a class="menu-card" href="voto.html?stage=' + stage + '&quad=' + q["key"] + '" '
        'data-stage="' + stage + '" data-quad="' + q["key"] + '" '
        'style="--mc-accent:' + q["accent"] + '; --mc-soft:' + q["accent_soft"] + ';">'
        '<div class="menu-card-icon">' + MENU_ICONS[q["key"]] + '</div>'
        '<div class="menu-card-body"><div class="menu-card-title">' + q["label"] + '<span class="voted-badge-slot"></span></div>'
        '<div class="menu-card-desc">Vote nas propostas de ' + q["label"] + ' do painel SWOT.</div></div>'
        '<div class="menu-card-arrow">&rarr;</div>'
        '</a>'
    )

MENU_ICONS = {
    "forcas": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "fraquezas": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></svg>',
    "oportunidades": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    "ameacas": '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>',
}

# ============================================================================
# ADMIN_TEMPLATE — painel único, com aba de ETAPA no topo (Telecom + Ambos /
# Não Telecom + Ambos) por cima das 4 abas de quadrante já existentes.
# ============================================================================
ADMIN_TEMPLATE = HEAD.replace("__PAGE_TITLE__", "Painel Administrativo &mdash; Vota&ccedil;&atilde;o SWOT &mdash; RV Digital 2027").replace("__PAGE_DESC__", "Painel de resultados ao vivo da vota&ccedil;&atilde;o SWOT, restrito aos administradores.") + r"""
<body>

<header class="hero">
  <div class="hero-inner">
    <div class="hero-text">
      <a class="back-to-menu" href="./index.html">&larr; Voltar ao menu</a>
      <div class="hero-eyebrow">RV Digital &middot; Planejamento Estrat&eacute;gico 2027</div>
      <h1 class="hero-title">Painel Administrativo &mdash; Vota&ccedil;&atilde;o SWOT</h1>
      <div class="hero-sub">Acompanhamento ao vivo, restrito aos administradores.</div>
      <div class="top-tabs stage-tabs" id="stage-tabs" style="display:none;">
        <button class="tab-btn active" data-stage="telecom">Telecom + Ambos</button>
        <button class="tab-btn" data-stage="naotelecom">N&atilde;o Telecom + Ambos</button>
      </div>
      <div class="top-tabs" id="tabs" style="display:none;">
        <button class="tab-btn active" data-q="forcas">For&ccedil;as</button>
        <button class="tab-btn" data-q="fraquezas">Fraquezas</button>
        <button class="tab-btn" data-q="oportunidades">Oportunidades</button>
        <button class="tab-btn" data-q="ameacas">Amea&ccedil;as</button>
      </div>
    </div>
    <div class="rv-logo hero-logo"><img src="data:image/png;base64,__LOGO_A_B64__" alt="RV Digital"></div>
  </div>
</header>

<main>
  <div id="login-gate" class="gate">
    <div class="icon">&#128274;</div>
    <h2 style="font-size:18px; margin-bottom:8px;">Acesso restrito</h2>
    <p style="color:var(--ink-soft); font-size:13.5px;">Entre com a conta de administrador para acompanhar os resultados.</p>
    <input type="email" id="login-email" placeholder="E-mail">
    <input type="password" id="login-pass" placeholder="Senha">
    <button id="login-btn">Entrar</button>
    <div class="err" id="login-err"></div>
  </div>

  <div id="dash" style="display:none;">
    <div class="admin-toolbar">
      <div class="stat"><b id="admin-voters">0</b><span>diretores votaram</span></div>
      <div class="stat"><b id="admin-total-votes">0</b><span>votos registrados</span></div>
      <div class="stat"><b id="admin-avg">&mdash;</b><span>m&eacute;dia geral</span></div>
      <button class="toggle-btn open" id="toggle-voting">Vota&ccedil;&atilde;o aberta</button>
      <button class="toggle-btn" style="background:#b23b3b;" id="reset-votes-btn" title="Apaga todos os votos deste quadrante">Reiniciar vota&ccedil;&atilde;o</button>
      <button class="toggle-btn" style="background:var(--ink-soft);" id="logout-btn">Sair</button>
    </div>
    <div class="view-toggle" id="view-toggle">
      <button class="active" data-view="results">Resultados</button>
      <button data-view="summary">Resumo Top 5 (todos os quadrantes)</button>
      <button data-view="edit">Editar textos</button>
    </div>
    <div class="rank-toggle" id="rank-toggle">
      <button class="active" data-order="original">Ordem do painel</button>
      <button data-order="rank-desc">Maior prioridade primeiro</button>
      <button data-order="rank-asc">Menor prioridade primeiro</button>
    </div>
    <div id="admin-mount"></div>
  </div>
</main>

<footer class="pagefoot">
  <div class="pagefoot-inner">
    <div class="rv-logo pagefoot-logo"><img src="data:image/png;base64,__LOGO_B_B64__" alt="RV Digital"></div>
    <div class="pagefoot-text">Planejamento Estrat&eacute;gico RV Digital 2027 &mdash; Painel administrativo</div>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<script>
function fatalConfigError(e){
  var msg = "Erro de configura&ccedil;&atilde;o do site: " + (e && e.message ? e.message : String(e));
  var gate = document.getElementById("login-gate");
  if(gate){
    gate.innerHTML = '<div style="background:#fbe9e9;border:1px solid #e0a0a0;border-radius:10px;padding:18px 20px;color:#7a1f1f;font-size:14px;line-height:1.5;text-align:left;">'
      + '<b>&#9888; ' + msg + '</b><br><br>'
      + 'Verifique o arquivo <code>supabase-config.js</code> (Passo 5 do manual): a URL e a chave anon precisam estar preenchidas, cada uma em uma &uacute;nica linha, sem quebras.'
      + '</div>';
  }
  console.error("Config/init error:", e);
}

try{

var BASE_ALL_ITEMS = __ALL_ITEMS_JSON__;   // { telecom:{forcas:[...],...}, naotelecom:{...} } — nunca é alterado
var ALL_ITEMS = { forcas:[], fraquezas:[], oportunidades:[], ameacas:[] }; // recalculado a cada refreshAll(), para a etapa atual
if(!window.RV_SUPABASE_URL || !window.RV_SUPABASE_ANON_KEY || window.RV_SUPABASE_URL.indexOf("COLOQUE_AQUI") !== -1){
  throw new Error("supabase-config.js não está preenchido (URL ou chave ausente).");
}
var sb = window.supabase.createClient(window.RV_SUPABASE_URL, window.RV_SUPABASE_ANON_KEY);
var currentStage = "telecom";
var currentQuad = "forcas";
var votingOpenByQuad = {};
var rowsByQuad = {};
var itemEditsByQuad = { forcas:{}, fraquezas:{}, oportunidades:{}, ameacas:{} };
var itemAddedByQuad = { forcas:[], fraquezas:[], oportunidades:[], ameacas:[] };
var itemRemovedByQuad = { forcas:{}, fraquezas:{}, oportunidades:{}, ameacas:{} };
var rankOverridesByQuad = { forcas:{}, fraquezas:{}, oportunidades:{}, ameacas:{} };
var prioritizedSet = { forcas:{}, fraquezas:{}, oportunidades:{}, ameacas:{} }; // nunca é escopado por etapa — é sempre relativo à etapa Telecom + Ambos
var adminOrder = "original";
var adminView = "results";
var topN = 5;
var resetArmed = false, resetArmTimer = null;
var QUAD_LABELS = { forcas:"Forças", fraquezas:"Fraquezas", oportunidades:"Oportunidades", ameacas:"Ameaças" };
var QUAD_COLORS = { forcas:"var(--green)", fraquezas:"var(--gold)", oportunidades:"var(--navy-lt)", ameacas:"var(--red)" };
var STAGE_LABELS = { telecom: "Telecom + Ambos", naotelecom: "Não Telecom + Ambos" };

function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}
function tagLabelFromOrigins(origins){
  var has = {};
  (origins || []).forEach(function(o){ has[o] = true; });
  if(has["Não Telecom"]) return "Não Telecom";
  if(has["Telecom"] && has["Ambos"]) return "Telecom + Ambos";
  if(has["Telecom"]) return "Telecom";
  return "Ambos";
}
function tagSlug(tag){
  if(tag === "Não Telecom") return "naotelecom";
  if(tag === "Telecom + Ambos") return "telecomambos";
  if(tag === "Telecom") return "telecom";
  return "ambos";
}
function tagChipHtml(tag){
  return '<span class="chip tag-' + tagSlug(tag) + '">' + escapeHtml(tag) + '</span>';
}

function applyChanges(baseItems, editMap, addedList, removedSet){
  var next = (baseItems || []).filter(function(it){ return !removedSet[it.id]; }).map(function(it){
    var clone = JSON.parse(JSON.stringify(it));
    if(editMap[clone.id] !== undefined) clone.title = editMap[clone.id];
    return clone;
  });
  (addedList || []).forEach(function(r){
    if(removedSet[r.item_id]) return;
    next.push({
      id: r.item_id, type: "isolada",
      title: (editMap[r.item_id] !== undefined) ? editMap[r.item_id] : r.title,
      divisions: r.division ? [r.division] : [],
      origins: r.origin ? [r.origin] : ["Ambos"],
      n: 1, originals: null, reason: null
    });
  });
  return next;
}

async function fetchStageState(stage){
  // Busca item_edits/item_added/item_removed de UMA etapa, agrupados por
  // quadrante — usada tanto para a etapa atualmente selecionada quanto
  // (quando a etapa atual é "naotelecom") para reconstruir a etapa Telecom +
  // Ambos e calcular quais itens migram por já estarem priorizados e com
  // tag "Ambos".
  var out = {
    editsByQuad: { forcas:{}, fraquezas:{}, oportunidades:{}, ameacas:{} },
    addedByQuad: { forcas:[], fraquezas:[], oportunidades:[], ameacas:[] },
    removedByQuad: { forcas:{}, fraquezas:{}, oportunidades:{}, ameacas:{} }
  };
  try{
    var editsRes = await sb.from("item_edits").select("quadrant,item_id,title").eq("stage", stage);
    if(!editsRes.error) (editsRes.data || []).forEach(function(r){ if(out.editsByQuad[r.quadrant]) out.editsByQuad[r.quadrant][r.item_id] = r.title; });
    var addedRes = await sb.from("item_added").select("quadrant,item_id,title,origin,division").eq("stage", stage);
    if(!addedRes.error) (addedRes.data || []).forEach(function(r){ if(out.addedByQuad[r.quadrant]) out.addedByQuad[r.quadrant].push(r); });
    var removedRes = await sb.from("item_removed").select("quadrant,item_id").eq("stage", stage);
    if(!removedRes.error) (removedRes.data || []).forEach(function(r){ if(out.removedByQuad[r.quadrant]) out.removedByQuad[r.quadrant][r.item_id] = true; });
  }catch(e){ console.warn("fetchStageState failed for", stage, e); }
  return out;
}

async function onLoggedIn(){
  document.getElementById("login-gate").style.display = "none";
  document.getElementById("dash").style.display = "block";
  document.getElementById("stage-tabs").style.display = "flex";
  document.getElementById("tabs").style.display = "flex";
  await refreshAll();
  sb.channel("votes-changes")
    .on("postgres_changes", { event: "*", schema: "public", table: "votes" }, function(){ refreshAll(); })
    .subscribe();
}

document.getElementById("stage-tabs").addEventListener("click", function(e){
  var b = e.target.closest(".tab-btn");
  if(!b) return;
  document.querySelectorAll("#stage-tabs .tab-btn").forEach(function(x){ x.classList.remove("active"); });
  b.classList.add("active");
  currentStage = b.getAttribute("data-stage");
  refreshAll();
});
document.getElementById("tabs").addEventListener("click", function(e){
  var b = e.target.closest(".tab-btn");
  if(!b) return;
  document.querySelectorAll("#tabs .tab-btn").forEach(function(x){ x.classList.remove("active"); });
  b.classList.add("active");
  currentQuad = b.getAttribute("data-q");
  renderDash();
});
document.querySelector(".rank-toggle").addEventListener("click", function(e){
  var b = e.target.closest("button");
  if(!b) return;
  document.querySelectorAll(".rank-toggle button").forEach(function(x){ x.classList.remove("active"); });
  b.classList.add("active");
  adminOrder = b.getAttribute("data-order");
  renderDash();
});
document.getElementById("view-toggle").addEventListener("click", function(e){
  var b = e.target.closest("button");
  if(!b) return;
  document.querySelectorAll("#view-toggle button").forEach(function(x){ x.classList.remove("active"); });
  b.classList.add("active");
  adminView = b.getAttribute("data-view");
  document.getElementById("rank-toggle").style.display = (adminView === "results") ? "flex" : "none";
  renderDash();
});
document.getElementById("admin-mount").addEventListener("click", async function(e){
  var saveBtn = e.target.closest(".edit-save");
  var resetBtn = e.target.closest(".edit-reset");
  var removeBtn = e.target.closest(".remove-item-btn");
  var restoreItemBtn = e.target.closest(".restore-item-btn");
  var addBtn = e.target.closest(".add-item-btn");
  var restoreOrderBtn = e.target.closest(".restore-order-btn");
  var rankUpBtn = e.target.closest(".rank-up");
  var rankDownBtn = e.target.closest(".rank-down");
  var exportBtn = e.target.closest(".export-btn");

  if(exportBtn){
    var quadExp = exportBtn.getAttribute("data-quad");
    var fmtSel = document.getElementById("export-format-select");
    var fmt = fmtSel ? fmtSel.value : "pdf";
    var statusEl = document.getElementById("export-status");
    if(statusEl){ statusEl.textContent = "Gerando arquivo…"; statusEl.className = "export-status"; }
    try{
      if(quadExp === "total"){
        if(fmt === "pdf") exportTotalPDF(); else exportTotalXLSB();
      } else {
        if(fmt === "pdf") exportQuadPDF(quadExp); else exportQuadXLSB(quadExp);
      }
      if(statusEl){ statusEl.textContent = "Arquivo gerado."; setTimeout(function(){ if(statusEl) statusEl.textContent = ""; }, 3000); }
    }catch(exErr){
      console.warn("export failed", exErr);
      if(statusEl){ statusEl.textContent = "Erro ao exportar (" + (exErr && exErr.message ? exErr.message : "desconhecido") + ")."; statusEl.className = "export-status err"; }
    }
    return;
  }

  if(addBtn){
    var box = addBtn.closest(".add-item-box");
    var ta = box.querySelector(".new-item-title");
    var selOrigin = box.querySelector(".new-item-origin");
    var status0 = box.querySelector(".edit-status");
    var title0 = ta.value.trim();
    if(!title0){ status0.textContent = "Escreva o texto da proposta."; status0.className = "edit-status err"; return; }
    status0.textContent = "Adicionando…"; status0.className = "edit-status";
    try{
      var newId = "add_" + currentQuad + "_" + Date.now().toString(36) + Math.random().toString(36).slice(2,6);
      // Correção do bug antigo do site Não Telecom (que gravava sempre "Ambos"
      // mesmo criando a proposta dentro da etapa Não Telecom): quando a etapa
      // atual é "naotelecom", a origem é sempre "Não Telecom"; na etapa
      // "telecom" o admin continua podendo escolher Ambos/Telecom.
      var originValue = (currentStage === "naotelecom") ? "Não Telecom" : (selOrigin ? selOrigin.value : "Ambos");
      var resA = await sb.from("item_added").insert({ stage: currentStage, quadrant: currentQuad, item_id: newId, title: title0, origin: originValue, division: null });
      if(resA.error) throw resA.error;
      ta.value = "";
      await refreshAll();
    }catch(errA){
      status0.textContent = "Erro ao adicionar (" + (errA && errA.message ? errA.message : "desconhecido") + ").";
      status0.className = "edit-status err";
    }
    return;
  }

  if(restoreOrderBtn){
    try{
      await sb.from("rank_overrides").delete().eq("stage", currentStage).eq("quadrant", currentQuad);
      rankOverridesByQuad[currentQuad] = {};
      renderDash();
    }catch(errR){ console.warn("restore order failed", errR); }
    return;
  }

  if(rankUpBtn || rankDownBtn){
    var quadForRank = rankUpBtn ? rankUpBtn.getAttribute("data-quad") : rankDownBtn.getAttribute("data-quad");
    var idForRank = rankUpBtn ? rankUpBtn.getAttribute("data-id") : rankDownBtn.getAttribute("data-id");
    var dir = rankUpBtn ? -1 : 1;
    await moveRank(quadForRank, idForRank, dir);
    return;
  }

  if(removeBtn){
    var rcard = e.target.closest(".edit-item");
    var rid = rcard.getAttribute("data-id");
    var rstatus = rcard.querySelector(".edit-status");
    var isAdded = rid.indexOf("add_") === 0;
    if(rstatus){ rstatus.textContent = "Removendo…"; rstatus.className = "edit-status"; }
    try{
      if(isAdded){
        var resD = await sb.from("item_added").delete().eq("stage", currentStage).eq("quadrant", currentQuad).eq("item_id", rid);
        if(resD.error) throw resD.error;
      } else {
        var resD2 = await sb.from("item_removed").upsert(
          { stage: currentStage, quadrant: currentQuad, item_id: rid },
          { onConflict: "stage,quadrant,item_id" }
        );
        if(resD2.error) throw resD2.error;
      }
      await refreshAll();
    }catch(errD){
      if(rstatus){ rstatus.textContent = "Erro ao remover (" + (errD && errD.message ? errD.message : "desconhecido") + ")."; rstatus.className = "edit-status err"; }
    }
    return;
  }

  if(restoreItemBtn){
    var rrid = restoreItemBtn.getAttribute("data-id");
    try{
      await sb.from("item_removed").delete().eq("stage", currentStage).eq("quadrant", currentQuad).eq("item_id", rrid);
      await refreshAll();
    }catch(errRR){ console.warn("restore item failed", errRR); }
    return;
  }

  if(!saveBtn && !resetBtn) return;
  var card = e.target.closest(".edit-item");
  if(!card) return;
  var id = card.getAttribute("data-id");
  var status = card.querySelector(".edit-status");
  if(saveBtn){
    var textarea = card.querySelector(".edit-title-input");
    var newTitle = textarea.value.trim();
    if(!newTitle){ status.textContent = "O texto não pode ficar vazio."; status.className = "edit-status err"; return; }
    status.textContent = "Salvando…"; status.className = "edit-status";
    try{
      var res = await sb.from("item_edits").upsert(
        { stage: currentStage, quadrant: currentQuad, item_id: id, title: newTitle, updated_at: new Date().toISOString() },
        { onConflict: "stage,quadrant,item_id" }
      );
      if(res.error) throw res.error;
      await refreshAll();
    }catch(err){
      status.textContent = "Erro ao salvar (" + (err && err.message ? err.message : "desconhecido") + ").";
      status.className = "edit-status err";
    }
  } else if(resetBtn){
    status.textContent = "Restaurando…"; status.className = "edit-status";
    try{
      var res2 = await sb.from("item_edits").delete().eq("stage", currentStage).eq("quadrant", currentQuad).eq("item_id", id);
      if(res2.error) throw res2.error;
      await refreshAll();
    }catch(err2){
      status.textContent = "Erro ao restaurar (" + (err2 && err2.message ? err2.message : "desconhecido") + ").";
      status.className = "edit-status err";
    }
  }
});

// Campo de "top N" (afeta a tabela de ranking tanto em Resultados quanto em Resumo)
// e checkbox de "Priorizar" (só existe na etapa Telecom + Ambos, view Resultados).
document.getElementById("admin-mount").addEventListener("change", function(e){
  var input = e.target.closest(".topn-input");
  if(input){
    var v = parseInt(input.value, 10);
    if(!v || v < 1) v = 5;
    if(v > 50) v = 50;
    topN = v;
    renderDash();
    return;
  }
  var pri = e.target.closest(".prioritize-checkbox");
  if(pri){
    var id = pri.getAttribute("data-id");
    var checked = pri.checked;
    pri.disabled = true;
    (async function(){
      try{
        if(checked){
          var r = await sb.from("item_prioritized").insert({ quadrant: currentQuad, item_id: id });
          if(r.error) throw r.error;
          if(!prioritizedSet[currentQuad]) prioritizedSet[currentQuad] = {};
          prioritizedSet[currentQuad][id] = true;
        } else {
          var r2 = await sb.from("item_prioritized").delete().eq("quadrant", currentQuad).eq("item_id", id);
          if(r2.error) throw r2.error;
          if(prioritizedSet[currentQuad]) delete prioritizedSet[currentQuad][id];
        }
        renderDash();
      }catch(err){
        console.warn("prioritize toggle failed", err);
        pri.checked = !checked;
        pri.disabled = false;
        alert("Não foi possível salvar a priorização (" + (err && err.message ? err.message : "erro desconhecido") + ").");
      }
    })();
    return;
  }
});

async function moveRank(quad, id, dir){
  // Move o item "id" uma posição para cima (dir=-1) ou para baixo (dir=1)
  // dentro da lista atualmente exibida (já com empates resolvidos), e
  // grava a nova ordem inteira na tabela rank_overrides (escopada por etapa).
  var list = getDisplayTop(quad, topN).slice();
  var idx = list.findIndex(function(x){ return x.it.id === id; });
  var swapIdx = idx + dir;
  if(idx === -1 || swapIdx < 0 || swapIdx >= list.length) return;
  var tmp = list[idx]; list[idx] = list[swapIdx]; list[swapIdx] = tmp;

  var overrides = {};
  list.forEach(function(x, i){ overrides[x.it.id] = i; });
  rankOverridesByQuad[quad] = overrides;
  renderDash();

  try{
    var rows = list.map(function(x, i){ return { stage: currentStage, quadrant: quad, item_id: x.it.id, position: i, updated_at: new Date().toISOString() }; });
    var res = await sb.from("rank_overrides").upsert(rows, { onConflict: "stage,quadrant,item_id" });
    if(res.error) throw res.error;
  }catch(e){ console.warn("save rank order failed", e); }
}
document.getElementById("toggle-voting").addEventListener("click", async function(){
  var newState = !votingOpenByQuad[currentQuad];
  try{
    await sb.from("voting_config").update({ is_open: newState }).eq("stage", currentStage).eq("quadrant", currentQuad);
    votingOpenByQuad[currentQuad] = newState;
    paintToggle();
  }catch(e){ console.warn("toggle failed", e); }
});
function paintToggle(){
  var open = !!votingOpenByQuad[currentQuad];
  var tb = document.getElementById("toggle-voting");
  tb.textContent = open ? "Votação aberta" : "Votação encerrada";
  tb.classList.toggle("open", open);
  tb.classList.toggle("closed", !open);
}
document.getElementById("reset-votes-btn").addEventListener("click", async function(){
  var btn = this;
  if(!resetArmed){
    resetArmed = true;
    btn.textContent = "Confirmar: apagar todos os votos de " + QUAD_LABELS[currentQuad] + " (" + STAGE_LABELS[currentStage] + ")?";
    btn.classList.add("reset-confirm");
    clearTimeout(resetArmTimer);
    resetArmTimer = setTimeout(function(){ resetArmed = false; btn.textContent = "Reiniciar votação"; btn.classList.remove("reset-confirm"); }, 5000);
    return;
  }
  clearTimeout(resetArmTimer);
  resetArmed = false;
  btn.classList.remove("reset-confirm");
  btn.disabled = true;
  btn.textContent = "Reiniciando…";
  try{
    var res = await sb.from("votes").delete().eq("stage", currentStage).eq("quadrant", currentQuad);
    if(res.error) throw res.error;
    await refreshAll();
  }catch(e){
    console.warn("reset votes failed", e);
    alert("Não foi possível reiniciar a votação (" + (e && e.message ? e.message : "erro desconhecido") + ").");
  }
  btn.textContent = "Reiniciar votação";
  btn.disabled = false;
});

async function refreshAll(){
  try{
    var votesRes = await sb.from("votes").select("quadrant,scores").eq("stage", currentStage);
    if(!votesRes.error){
      rowsByQuad = { forcas: [], fraquezas: [], oportunidades: [], ameacas: [] };
      (votesRes.data || []).forEach(function(r){ if(rowsByQuad[r.quadrant]) rowsByQuad[r.quadrant].push(r.scores || {}); });
    }
    var cfgRes = await sb.from("voting_config").select("quadrant,is_open").eq("stage", currentStage);
    if(!cfgRes.error){
      votingOpenByQuad = {};
      (cfgRes.data || []).forEach(function(r){ votingOpenByQuad[r.quadrant] = r.is_open; });
    }

    var curState = await fetchStageState(currentStage);
    itemEditsByQuad = curState.editsByQuad;
    itemAddedByQuad = curState.addedByQuad;
    itemRemovedByQuad = curState.removedByQuad;

    var rankRes = await sb.from("rank_overrides").select("quadrant,item_id,position").eq("stage", currentStage);
    rankOverridesByQuad = { forcas:{}, fraquezas:{}, oportunidades:{}, ameacas:{} };
    if(!rankRes.error){
      (rankRes.data || []).forEach(function(r){ if(rankOverridesByQuad[r.quadrant]) rankOverridesByQuad[r.quadrant][r.item_id] = r.position; });
    }

    // item_prioritized nunca é escopado por etapa: é sempre relativo à etapa
    // Telecom + Ambos (ver schema.sql). É usado aqui tanto para desenhar o
    // checkbox (etapa Telecom) quanto para calcular a migração (etapa Não
    // Telecom), então é sempre buscado, independentemente da etapa atual.
    var prioRes = await sb.from("item_prioritized").select("quadrant,item_id");
    prioritizedSet = { forcas:{}, fraquezas:{}, oportunidades:{}, ameacas:{} };
    if(!prioRes.error){
      (prioRes.data || []).forEach(function(r){ if(prioritizedSet[r.quadrant]) prioritizedSet[r.quadrant][r.item_id] = true; });
    }

    var telecomState = null;
    if(currentStage === "naotelecom"){
      telecomState = await fetchStageState("telecom");
    }

    var next = {};
    ["forcas","fraquezas","oportunidades","ameacas"].forEach(function(q){
      var native = applyChanges(BASE_ALL_ITEMS[currentStage][q], itemEditsByQuad[q], itemAddedByQuad[q], itemRemovedByQuad[q]);
      var list = native;
      if(currentStage === "naotelecom" && telecomState){
        var telecomNative = applyChanges(BASE_ALL_ITEMS.telecom[q], telecomState.editsByQuad[q], telecomState.addedByQuad[q], telecomState.removedByQuad[q]);
        var survivors = telecomNative.filter(function(it){
          return (prioritizedSet[q] && prioritizedSet[q][it.id]) && tagLabelFromOrigins(it.origins) === "Ambos";
        });
        var migBase = survivors.map(function(it){
          var c = JSON.parse(JSON.stringify(it));
          c.id = "mig_" + it.id; c.migrated = true; c.migratedFrom = it.id;
          return c;
        });
        // aplica edições/remoções da própria etapa Não Telecom, já escopadas
        // pelo prefixo "mig_" (itemEditsByQuad/itemRemovedByQuad acima já são
        // da etapa atual, naotelecom).
        var migFinal = migBase.filter(function(it){ return !itemRemovedByQuad[q][it.id]; }).map(function(it){
          var c = JSON.parse(JSON.stringify(it));
          if(itemEditsByQuad[q][it.id] !== undefined) c.title = itemEditsByQuad[q][it.id];
          return c;
        });
        list = native.concat(migFinal);
      }
      next[q] = list;
    });
    ALL_ITEMS = next;
  }catch(e){ console.warn("refresh failed", e); }
  paintToggle();
  renderDash();
}

function computeAgg(quad){
  var items = ALL_ITEMS[quad] || [];
  var agg = {};
  items.forEach(function(it){ agg[it.id] = {c5:0,c3:0,c1:0,total:0,sum:0}; });
  (rowsByQuad[quad] || []).forEach(function(scores){
    Object.keys(scores || {}).forEach(function(itemId){
      if(!agg[itemId]) return;
      var score = scores[itemId];
      if(score === 5) agg[itemId].c5++;
      else if(score === 3) agg[itemId].c3++;
      else if(score === 1) agg[itemId].c1++;
      else return;
      agg[itemId].total++; agg[itemId].sum += score;
    });
  });
  return agg;
}

function computeTopWithTies(quad, n){
  var items = ALL_ITEMS[quad] || [];
  var agg = computeAgg(quad);
  var scored = [];
  items.forEach(function(it){
    var a = agg[it.id];
    if(a && a.total > 0){ scored.push({ it: it, avg: a.sum/a.total, total: a.total }); }
  });
  scored.sort(function(a,b){ return b.avg - a.avg; });
  if(scored.length <= n) return scored;
  var cutoffKey = Math.round(scored[n-1].avg * 1000);
  var cut = n;
  while(cut < scored.length && Math.round(scored[cut].avg * 1000) >= cutoffKey) cut++;
  return scored.slice(0, cut);
}

function getDisplayTop(quad, n){
  var auto = computeTopWithTies(quad, n);
  var overrides = rankOverridesByQuad[quad];
  if(!overrides || !Object.keys(overrides).length) return auto;
  var withPos = auto.map(function(x, i){
    var p = overrides[x.it.id];
    return { x: x, pos: (p !== undefined) ? p : (1000 + i) };
  });
  withPos.sort(function(a,b){ return a.pos - b.pos; });
  return withPos.map(function(w){ return w.x; });
}

function topNHead(quad, title, allowReorder){
  var hasOverride = rankOverridesByQuad[quad] && Object.keys(rankOverridesByQuad[quad]).length > 0;
  return '<div class="top5-head">'
    + '<h3>&#127942; '+title+'</h3>'
    + '<div class="topn-ctrl">Mostrar top <input type="number" min="1" max="50" class="topn-input" value="'+topN+'"> itens</div>'
    + (allowReorder && hasOverride ? '<button class="restore-order-btn">Restaurar ordem autom&aacute;tica</button>' : '')
    + '</div>';
}

function renderTopNTable(quad, allowReorder, head){
  var top = getDisplayTop(quad, topN);
  var hasOverride = rankOverridesByQuad[quad] && Object.keys(rankOverridesByQuad[quad]).length > 0;
  if(head === undefined) head = topNHead(quad, "Top "+topN+" mais priorizados &mdash; "+QUAD_LABELS[quad], allowReorder);
  if(!top.length) return head + '<div class="empty-note">Ainda sem votos suficientes neste quadrante.</div>';
  var rowsHtml = "";
  var lastKey = null, lastRank = 0;
  top.forEach(function(x, i){
    var key = Math.round(x.avg * 1000);
    var rank;
    if(hasOverride){
      rank = i + 1;
    } else if(key === lastKey){
      rank = lastRank;
    } else { rank = i + 1; lastRank = rank; lastKey = key; }
    var shareCount = hasOverride ? 1 : top.filter(function(y){ return Math.round(y.avg * 1000) === key; }).length;
    var tie = shareCount > 1 ? '<span class="top5-tie">EMPATE</span>' : '';
    var avgColor = x.avg >= 4 ? "var(--green)" : (x.avg >= 2.2 ? "var(--gold)" : "var(--red)");
    var rankCell = '#'+rank;
    if(allowReorder){
      rankCell = '<div class="top5-rankcell"><span>#'+rank+'</span><div class="rank-arrows">'
        + '<button class="rank-up" data-quad="'+quad+'" data-id="'+x.it.id+'" '+(i===0?'disabled':'')+'>&#9650;</button>'
        + '<button class="rank-down" data-quad="'+quad+'" data-id="'+x.it.id+'" '+(i===top.length-1?'disabled':'')+'>&#9660;</button>'
        + '</div></div>';
    }
    var migTag = x.it.migrated ? ' <span class="migrated-badge" title="Migrada de Telecom + Ambos">&#9671;</span>' : '';
    rowsHtml += '<tr><td class="top5-rank">'+rankCell+'</td><td>'+escapeHtml(x.it.title)+migTag+tie+'</td>'
      + '<td class="top5-avg" style="color:'+avgColor+'">'+x.avg.toFixed(2)+'</td>'
      + '<td style="color:var(--ink-soft); white-space:nowrap;">'+x.total+' voto'+(x.total===1?'':'s')+'</td></tr>';
  });
  return head + '<table class="top5-table"><thead><tr><th>#</th><th>Item</th><th>M&eacute;dia</th><th>Votos</th></tr></thead><tbody>'+rowsHtml+'</tbody></table>';
}

function renderDash(){
  paintToggle();
  if(adminView === "summary"){ renderSummaryView(); return; }
  if(adminView === "edit"){ renderEditView(); return; }
  renderResultsView();
}

function renderResultsView(){
  var mount = document.getElementById("admin-mount");
  var items = (ALL_ITEMS[currentQuad] || []).slice();
  var agg = computeAgg(currentQuad);
  var voters = (rowsByQuad[currentQuad] || []).length;
  var totalVotes = 0, sumAll = 0;
  Object.keys(agg).forEach(function(id){ totalVotes += agg[id].total; sumAll += agg[id].sum; });
  document.getElementById("admin-voters").textContent = voters;
  document.getElementById("admin-total-votes").textContent = totalVotes;
  document.getElementById("admin-avg").textContent = totalVotes ? (sumAll/totalVotes).toFixed(2) : "—";

  if(adminOrder === "rank-desc" || adminOrder === "rank-asc"){
    items.sort(function(a,b){
      var aa = agg[a.id], bb = agg[b.id];
      var avA = aa.total ? aa.sum/aa.total : -1;
      var avB = bb.total ? bb.sum/bb.total : -1;
      return adminOrder === "rank-desc" ? (avB-avA) : (avA-avB);
    });
  }

  var html = "";
  if(currentStage === "telecom"){
    var prioCount = items.filter(function(it){ return prioritizedSet[currentQuad] && prioritizedSet[currentQuad][it.id]; }).length;
    var ambosPrioCount = items.filter(function(it){ return prioritizedSet[currentQuad] && prioritizedSet[currentQuad][it.id] && tagLabelFromOrigins(it.origins) === "Ambos"; }).length;
    html += '<div class="prio-summary"><b>'+prioCount+'</b> item'+(prioCount===1?"":"s")+' priorizado'+(prioCount===1?"":"s")+' neste quadrante'
      + ' (<b>'+ambosPrioCount+'</b> com tag Ambos &mdash; ser'+(ambosPrioCount===1?"á":"ão")+' migrado'+(ambosPrioCount===1?"":"s")+' para N&atilde;o Telecom + Ambos).</div>';
  }
  html += '<div class="top5-wrap">'+renderTopNTable(currentQuad, true)+'</div>';
  items.forEach(function(it){
    var a = agg[it.id];
    var avg = a.total ? (a.sum/a.total) : null;
    var avgColor = avg===null ? "var(--ink-soft)" : (avg>=4 ? "var(--green)" : (avg>=2.2 ? "var(--gold)" : "var(--red)"));
    var pct5 = a.total ? (a.c5/a.total*100) : 0;
    var pct3 = a.total ? (a.c3/a.total*100) : 0;
    var pct1 = a.total ? (a.c1/a.total*100) : 0;
    var tag = tagLabelFromOrigins(it.origins);
    var prioCtrl = "";
    if(currentStage === "telecom"){
      var isChecked = !!(prioritizedSet[currentQuad] && prioritizedSet[currentQuad][it.id]);
      prioCtrl = '<label class="prioritize-ctrl"><input type="checkbox" class="prioritize-checkbox" data-id="'+it.id+'" '+(isChecked?'checked':'')+'> Priorizar</label>';
    }
    var migBadge = (currentStage === "naotelecom" && it.migrated) ? '<span class="chip migrated-chip">Migrada de Telecom + Ambos</span>' : "";
    html += '<div class="admin-item'+(it.migrated?' is-migrated':'')+'">'
      + '<div class="admin-item-top"><div class="item-title" style="flex:1">'+escapeHtml(it.title)+' '+tagChipHtml(tag)+' '+migBadge+'</div>'
      + prioCtrl
      + '<span class="avg-badge" style="background:'+avgColor+'">'+(avg===null?"sem votos":avg.toFixed(1))+'</span></div>'
      + '<div class="bars"><div class="bar-5" style="width:'+pct5+'%"></div><div class="bar-3" style="width:'+pct3+'%"></div><div class="bar-1" style="width:'+pct1+'%"></div></div>'
      + '<div class="bar-legend"><span><b>'+a.c5+'</b> concordam totalmente</span><span><b>'+a.c3+'</b> concordam parcialmente</span><span><b>'+a.c1+'</b> discordam</span><span><b>'+a.total+'</b> votos</span></div>'
      + '</div>';
  });
  mount.innerHTML = html;
}

function renderSummaryView(){
  var mount = document.getElementById("admin-mount");
  document.getElementById("admin-voters").textContent = "—";
  document.getElementById("admin-total-votes").textContent = "—";
  document.getElementById("admin-avg").textContent = "—";
  var order = ["forcas","fraquezas","oportunidades","ameacas"];
  var html = '<div class="top5-wrap" style="margin-bottom:8px;"><div class="top5-head">'
    + '<h3>&#127942; Resumo Top '+topN+' &mdash; '+STAGE_LABELS[currentStage]+' &mdash; todos os quadrantes</h3>'
    + '<div class="topn-ctrl">Mostrar top <input type="number" min="1" max="50" class="topn-input" value="'+topN+'"> itens</div>'
    + '</div></div>';
  html += '<div class="export-bar">'
    + '<span class="export-label">Exportar Top '+topN+' ('+STAGE_LABELS[currentStage]+'):</span>'
    + '<select class="export-format" id="export-format-select">'
    +   '<option value="pdf">PDF</option>'
    +   '<option value="xlsb">Excel (.xlsb)</option>'
    + '</select>'
    + '<button class="export-btn" data-quad="forcas">For&ccedil;as</button>'
    + '<button class="export-btn" data-quad="fraquezas">Fraquezas</button>'
    + '<button class="export-btn" data-quad="oportunidades">Oportunidades</button>'
    + '<button class="export-btn" data-quad="ameacas">Amea&ccedil;as</button>'
    + '<button class="export-btn export-total" data-quad="total">Total (todos os quadrantes)</button>'
    + '<span class="export-status" id="export-status"></span>'
    + '</div>';
  order.forEach(function(q){
    html += '<div class="summary-quad"><h3><span class="dot" style="background:'+QUAD_COLORS[q]+'"></span>'+QUAD_LABELS[q]+'</h3>'
      + renderTopNTable(q, false, "") + '</div>';
  });
  mount.innerHTML = html;
}

function renderEditView(){
  var mount = document.getElementById("admin-mount");
  document.getElementById("admin-voters").textContent = "—";
  document.getElementById("admin-total-votes").textContent = "—";
  document.getElementById("admin-avg").textContent = "—";
  var items = (ALL_ITEMS[currentQuad] || []).slice();

  var originSelectHtml = (currentStage === "telecom")
    ? '<select class="new-item-origin"><option value="Ambos">Ambos</option><option value="Telecom">Telecom</option></select>'
    : '<span style="font-size:12.5px; color:var(--ink-soft);">Origem: <b>N&atilde;o Telecom</b></span>';

  var html = '<div class="add-item-box">'
    + '<h4>&#10133; Adicionar nova proposta &mdash; '+QUAD_LABELS[currentQuad]+' ('+STAGE_LABELS[currentStage]+')</h4>'
    + '<textarea class="new-item-title" rows="2" placeholder="Texto da nova proposta a ser votada..."></textarea>'
    + '<div class="add-row">'
    +   originSelectHtml
    +   '<button class="add-item-btn">Adicionar</button>'
    +   '<span class="edit-status"></span>'
    + '</div></div>';

  html += '<div class="top5-wrap"><h3>&#9999;&#65039; Editar textos &mdash; '+QUAD_LABELS[currentQuad]+'</h3>'
    + '<p style="font-size:12.5px; color:var(--ink-soft); margin:-4px 0 4px;">Altere o texto de um item e clique em Salvar, ou remova uma proposta. A mudan&ccedil;a aparece na tela de vota&ccedil;&atilde;o de quem est&aacute; votando em at&eacute; 20 segundos, sem precisar reenviar nenhum arquivo. Itens migrados (identificados pelo prefixo <code>mig_</code>) podem ser editados/ocultados aqui sem afetar o item original na etapa Telecom + Ambos.</p></div>';
  items.forEach(function(it, i){
    var isEdited = !!(itemEditsByQuad[currentQuad] && itemEditsByQuad[currentQuad][it.id] !== undefined);
    var isAdded = it.id.indexOf("add_") === 0;
    html += '<div class="admin-item edit-item'+(it.migrated?' is-migrated':'')+'" data-id="'+it.id+'">'
      + '<div style="font-size:11.5px; color:var(--ink-soft); margin-bottom:6px;">#'+(i+1)
      +   (isAdded ? ' &middot; <span class="added-badge">proposta adicionada</span>' : '')
      +   (it.migrated ? ' &middot; <span class="migrated-badge">migrada de Telecom + Ambos</span>' : '')
      +   (isEdited ? ' &middot; <span style="color:var(--gold); font-weight:700;">texto editado</span>' : '')
      + '</div>'
      + '<textarea class="edit-title-input" rows="2">'+escapeHtml(it.title)+'</textarea>'
      + '<div class="edit-actions">'
      +   '<button class="edit-save">Salvar</button>'
      +   (isEdited ? '<button class="edit-reset">Restaurar original</button>' : '')
      +   '<button class="remove-item-btn">Remover proposta</button>'
      +   '<span class="edit-status"></span>'
      + '</div></div>';
  });

  var removedIds = Object.keys(itemRemovedByQuad[currentQuad] || {});
  if(removedIds.length){
    var rowsHtml = "";
    removedIds.forEach(function(rid){
      var orig = (BASE_ALL_ITEMS[currentStage][currentQuad] || []).filter(function(o){ return o.id === rid; })[0];
      if(!orig) return; // era um item adicionado (ou migrado) que já foi excluído de vez — não aparece aqui
      rowsHtml += '<div class="removed-row"><span class="rt">'+escapeHtml(orig.title)+'</span>'
        + '<button class="restore-item-btn" data-id="'+rid+'">Restaurar</button></div>';
    });
    if(rowsHtml){
      html += '<div class="removed-panel"><h4>Propostas ocultadas neste quadrante</h4>'+rowsHtml+'</div>';
    }
  }

  mount.innerHTML = html;
}

var EXPORT_TAG_COLORS = {
  "Não Telecom":     { fill:[91,62,150],  text:[255,255,255] },
  "Telecom":         { fill:[201,162,75], text:[27,42,74] },
  "Telecom + Ambos": { fill:[138,109,31], text:[255,255,255] },
  "Ambos":           { fill:[27,42,74],   text:[255,255,255] }
};
var EXPORT_QUAD_META = {
  forcas:        { label:"Forças",        bar:[220,243,227], text:[30,122,61] },
  fraquezas:     { label:"Fraquezas",     bar:[251,225,225], text:[178,59,59] },
  oportunidades: { label:"Oportunidades", bar:[220,233,247], text:[21,90,150] },
  ameacas:       { label:"Ameaças",       bar:[253,235,208], text:[179,105,10] }
};
var LOGO_A_DATAURL = "data:image/png;base64,__LOGO_A_B64__";

function buildExportRows(quad){
  var top = getDisplayTop(quad, topN);
  return top.map(function(x, i){
    return { rank: i+1, title: x.it.title, tag: tagLabelFromOrigins(x.it.origins), avg: x.avg, votes: x.total };
  });
}

function safeFileLabel(s){
  return String(s).replace(/[^A-Za-z0-9]+/g, "_");
}

function drawExportHeader(doc, pageWidth, subtitle){
  try{ doc.addImage(LOGO_A_DATAURL, "PNG", 40, 26, 72, 23); }catch(e){}
  doc.setFont("helvetica", "bold"); doc.setFontSize(18); doc.setTextColor(27,42,74);
  doc.text("Painel SWOT Consolidado", pageWidth/2, 42, { align:"center" });
  doc.setFont("helvetica", "normal"); doc.setFontSize(11); doc.setTextColor(85,85,85);
  doc.text("Plano Estratégico: Planejamento Estratégico RV Digital 2027 · " + subtitle, pageWidth/2, 58, { align:"center" });
  doc.setDrawColor(220,220,220); doc.setLineWidth(1);
  doc.line(40, 74, pageWidth-40, 74);
}

function drawExportFooter(doc, pageWidth, pageHeight, rightText){
  doc.setDrawColor(221,221,221); doc.setLineWidth(1);
  doc.line(40, pageHeight-34, pageWidth-40, pageHeight-34);
  doc.setFont("helvetica", "normal"); doc.setFontSize(9); doc.setTextColor(120,120,120);
  doc.text("Planejamento Estratégico RV Digital 2027", 40, pageHeight-20);
  doc.text(rightText || "", pageWidth-40, pageHeight-20, { align:"right" });
}

function drawQuadTable(doc, quad, x, y, w){
  var meta = EXPORT_QUAD_META[quad];
  var rows = buildExportRows(quad);
  var barH = 22;
  doc.setFillColor.apply(doc, meta.bar);
  doc.rect(x, y, w, barH, "F");
  doc.setFont("helvetica", "bold"); doc.setFontSize(12);
  doc.setTextColor.apply(doc, meta.text);
  doc.text(meta.label, x+10, y+15);
  y += barH + 16;

  var colRank = 26, colTag = 108, colAvg = 50, colVotes = 50;
  var colTitle = w - colRank - colTag - colAvg - colVotes;

  doc.setDrawColor(51,51,51); doc.setLineWidth(1);
  doc.line(x, y, x+w, y);
  doc.setFont("helvetica", "bold"); doc.setFontSize(9); doc.setTextColor(30,30,30);
  var hx = x;
  doc.text("#", hx+3, y-5); hx += colRank;
  doc.text("Proposta", hx+3, y-5); hx += colTitle;
  doc.text("Tipo", hx+3, y-5); hx += colTag;
  doc.text("Média", hx+3, y-5); hx += colAvg;
  doc.text("Votos", hx+3, y-5);
  y += 4;

  if(!rows.length){
    doc.setFont("helvetica", "normal"); doc.setFontSize(9.5); doc.setTextColor(120,120,120);
    doc.text("Ainda sem votos suficientes neste quadrante.", x+4, y+14);
    y += 22;
  }

  doc.setFont("helvetica", "normal"); doc.setFontSize(9);
  rows.forEach(function(r, i){
    var lines = doc.splitTextToSize(r.title, colTitle - 8);
    var rh = Math.max(16, lines.length * 10.5 + 6);
    if(i % 2 === 1){ doc.setFillColor(250,250,250); doc.rect(x, y, w, rh, "F"); }
    var cy = y + 11;
    var cx = x;
    doc.setTextColor(40,40,40);
    doc.text(String(r.rank), cx+3, cy); cx += colRank;
    doc.text(lines, cx+3, cy); cx += colTitle;
    var tagStyle = EXPORT_TAG_COLORS[r.tag] || { fill:[150,150,150], text:[255,255,255] };
    var pillW = Math.min(colTag - 6, 8 + r.tag.length * 4.4);
    doc.setFillColor.apply(doc, tagStyle.fill);
    doc.roundedRect(cx, y + (rh-14)/2, pillW, 14, 4, 4, "F");
    doc.setFontSize(7.6);
    doc.setTextColor.apply(doc, tagStyle.text);
    doc.text(r.tag, cx + pillW/2, y + rh/2 + 2.6, { align:"center" });
    doc.setFontSize(9); doc.setTextColor(40,40,40);
    cx += colTag;
    doc.text(r.avg.toFixed(2), cx+3, cy); cx += colAvg;
    doc.text(String(r.votes), cx+3, cy);
    doc.setDrawColor(228,228,228); doc.setLineWidth(0.5);
    doc.line(x, y+rh, x+w, y+rh);
    y += rh;
  });

  var totalVotes = rows.reduce(function(s,r){ return s + r.votes; }, 0);
  doc.setDrawColor(51,51,51); doc.setLineWidth(1);
  doc.line(x, y, x+w, y);
  y += 13;
  doc.setFont("helvetica", "bold"); doc.setFontSize(9.5); doc.setTextColor(20,20,20);
  doc.text("Total de votos no Top " + rows.length, x+3, y);
  doc.text(String(totalVotes), x+w-3, y, { align:"right" });
  return y + 12;
}

function getJsPDFCtor(){
  if(window.jspdf && window.jspdf.jsPDF) return window.jspdf.jsPDF;
  if(window.jsPDF) return window.jsPDF;
  throw new Error("Biblioteca de PDF não carregou (verifique sua conexão).");
}

function exportQuadPDF(quad){
  var JsPDF = getJsPDFCtor();
  var pageW = 620, pageH = 760;
  var doc = new JsPDF({ unit:"pt", format:[pageW, pageH] });
  drawExportHeader(doc, pageW, STAGE_LABELS[currentStage] + " — Top " + topN + " — " + EXPORT_QUAD_META[quad].label);
  drawQuadTable(doc, quad, 40, 96, pageW-80);
  drawExportFooter(doc, pageW, pageH, "Tipos: Não Telecom · Telecom · Telecom + Ambos · Ambos");
  doc.save("Top" + topN + "_" + safeFileLabel(EXPORT_QUAD_META[quad].label) + "_" + safeFileLabel(STAGE_LABELS[currentStage]) + "_RV_Digital_2027.pdf");
}

function exportTotalPDF(){
  var JsPDF = getJsPDFCtor();
  var pageW = 1000, pageH = 700;
  var doc = new JsPDF({ unit:"pt", format:[pageW, pageH] });
  var pairs = [["forcas","fraquezas"], ["oportunidades","ameacas"]];
  pairs.forEach(function(pair, idx){
    if(idx > 0) doc.addPage([pageW, pageH]);
    var subtitle = STAGE_LABELS[currentStage] + " — Top " + topN + " — " + EXPORT_QUAD_META[pair[0]].label + " e " + EXPORT_QUAD_META[pair[1]].label;
    drawExportHeader(doc, pageW, subtitle);
    var colW = (pageW - 80 - 30) / 2;
    drawQuadTable(doc, pair[0], 40, 96, colW);
    drawQuadTable(doc, pair[1], 40 + colW + 30, 96, colW);
    drawExportFooter(doc, pageW, pageH, "Tipos: Não Telecom · Telecom · Telecom + Ambos · Ambos");
  });
  doc.save("Top" + topN + "_Total_" + safeFileLabel(STAGE_LABELS[currentStage]) + "_RV_Digital_2027.pdf");
}

function buildQuadAoa(quad){
  var meta = EXPORT_QUAD_META[quad];
  var rows = buildExportRows(quad);
  var aoa = [
    ["Painel SWOT Consolidado"],
    ["Planejamento Estratégico RV Digital 2027 — " + STAGE_LABELS[currentStage] + " — Top " + topN + " — " + meta.label],
    [],
    [meta.label.toUpperCase()],
    ["#", "Proposta", "Tipo", "Média", "Votos"]
  ];
  rows.forEach(function(r){ aoa.push([r.rank, r.title, r.tag, Number(r.avg.toFixed(2)), r.votes]); });
  var totalVotes = rows.reduce(function(s,r){ return s + r.votes; }, 0);
  aoa.push(["", "", "Total", "", totalVotes]);
  return aoa;
}

function quadSheet(quad){
  var ws = XLSX.utils.aoa_to_sheet(buildQuadAoa(quad));
  ws["!cols"] = [{wch:5},{wch:62},{wch:18},{wch:9},{wch:9}];
  ws["!merges"] = [
    { s:{r:0,c:0}, e:{r:0,c:4} },
    { s:{r:1,c:0}, e:{r:1,c:4} },
    { s:{r:3,c:0}, e:{r:3,c:4} }
  ];
  return ws;
}

function exportQuadXLSB(quad){
  if(typeof XLSX === "undefined"){ alert("Biblioteca de planilha não carregou (verifique sua conexão)."); return; }
  var wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, quadSheet(quad), EXPORT_QUAD_META[quad].label.slice(0,31));
  XLSX.writeFile(wb, "Top" + topN + "_" + safeFileLabel(EXPORT_QUAD_META[quad].label) + "_" + safeFileLabel(STAGE_LABELS[currentStage]) + "_RV_Digital_2027.xlsb", { bookType:"xlsb" });
}

function exportTotalXLSB(){
  if(typeof XLSX === "undefined"){ alert("Biblioteca de planilha não carregou (verifique sua conexão)."); return; }
  var wb = XLSX.utils.book_new();
  var order = ["forcas","fraquezas","oportunidades","ameacas"];
  var summaryAoa = [
    ["Painel SWOT Consolidado"],
    ["Planejamento Estratégico RV Digital 2027 — " + STAGE_LABELS[currentStage] + " — Resumo Top " + topN],
    [],
    ["Quadrante", "Itens no Top", "Total de votos"]
  ];
  order.forEach(function(quad){
    var rows = buildExportRows(quad);
    var totalVotes = rows.reduce(function(s,r){ return s + r.votes; }, 0);
    summaryAoa.push([EXPORT_QUAD_META[quad].label, rows.length, totalVotes]);
  });
  var wsSummary = XLSX.utils.aoa_to_sheet(summaryAoa);
  wsSummary["!cols"] = [{wch:18},{wch:14},{wch:16}];
  wsSummary["!merges"] = [{ s:{r:0,c:0}, e:{r:0,c:2} }, { s:{r:1,c:0}, e:{r:1,c:2} }];
  XLSX.utils.book_append_sheet(wb, wsSummary, "Resumo");
  order.forEach(function(quad){
    XLSX.utils.book_append_sheet(wb, quadSheet(quad), EXPORT_QUAD_META[quad].label.slice(0,31));
  });
  XLSX.writeFile(wb, "Top" + topN + "_Total_" + safeFileLabel(STAGE_LABELS[currentStage]) + "_RV_Digital_2027.xlsb", { bookType:"xlsb" });
}


(async function init(){
  var sess = await sb.auth.getSession();
  if(sess.data && sess.data.session){ onLoggedIn(); }
})();

document.getElementById("login-btn").addEventListener("click", async function(){
  var email = document.getElementById("login-email").value.trim();
  var pass = document.getElementById("login-pass").value;
  var err = document.getElementById("login-err");
  err.textContent = "";
  try{
    var res = await sb.auth.signInWithPassword({ email: email, password: pass });
    if(res.error) throw res.error;
    onLoggedIn();
  }catch(e){
    err.textContent = "E-mail ou senha incorretos, ou esta conta não é administradora.";
  }
});
document.getElementById("logout-btn").addEventListener("click", async function(){
  await sb.auth.signOut();
  location.reload();
});

}catch(e){ fatalConfigError(e); }
</script>
</body>
</html>
"""

# ============================================================================
# DRIVER — gera voto.html, index.html e admin.html neste mesmo diretório.
# ============================================================================
QUADS_META = {q["key"]: {"label": q["label"], "accent": q["accent"], "accent_soft": q["accent_soft"]} for q in QUADRANTS}

# ---- voto.html ----------------------------------------------------------
voto_html = VOTE_TEMPLATE
voto_html = voto_html.replace("__CSS__", BASE_CSS)
voto_html = voto_html.replace("__QUADS_META_JSON__", json.dumps(QUADS_META, ensure_ascii=False))
voto_html = voto_html.replace("__ITEMS_ALL_JSON__", json.dumps(ITEMS, ensure_ascii=False))
voto_html = voto_html.replace("__LOGO_A_B64__", LOGO_A_B64)
voto_html = voto_html.replace("__LOGO_B_B64__", LOGO_B_B64)
with open(OUT_DIR + "/voto.html", "w", encoding="utf-8") as f:
    f.write(voto_html)
print("wrote", OUT_DIR + "/voto.html")

# ---- admin.html -----------------------------------------------------------
admin_html = ADMIN_TEMPLATE
admin_html = admin_html.replace("__CSS__", BASE_CSS)
admin_html = admin_html.replace("__ALL_ITEMS_JSON__", json.dumps(ITEMS, ensure_ascii=False))
admin_html = admin_html.replace("__LOGO_A_B64__", LOGO_A_B64)
admin_html = admin_html.replace("__LOGO_B_B64__", LOGO_B_B64)
with open(OUT_DIR + "/admin.html", "w", encoding="utf-8") as f:
    f.write(admin_html)
print("wrote", OUT_DIR + "/admin.html")

# ---- index.html -----------------------------------------------------------
menu_telecom = "\n      ".join(menu_card_html("telecom", q) for q in QUADRANTS)
menu_naotelecom = "\n      ".join(menu_card_html("naotelecom", q) for q in QUADRANTS)

index_html = INDEX_TEMPLATE
index_html = index_html.replace("__CSS__", BASE_CSS)
index_html = index_html.replace("__MENU_CARDS_TELECOM__", menu_telecom)
index_html = index_html.replace("__MENU_CARDS_NAOTELECOM__", menu_naotelecom)
index_html = index_html.replace("__LOGO_A_B64__", LOGO_A_B64)
index_html = index_html.replace("__LOGO_B_B64__", LOGO_B_B64)
with open(OUT_DIR + "/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print("wrote", OUT_DIR + "/index.html")

for stage in ["telecom", "naotelecom"]:
    for q in QUADRANTS:
        print("  items", stage, q["key"], len(ITEMS[stage][q["key"]]))
