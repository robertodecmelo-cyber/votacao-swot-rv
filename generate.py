import json

with open("/home/claude/votacao_supabase/logo_a.b64") as f:
    LOGO_A_B64 = f.read().strip()  # white-circle badge -> use on BLUE backgrounds
with open("/home/claude/votacao_supabase/logo_b.b64") as f:
    LOGO_B_B64 = f.read().strip()  # navy-circle badge -> use on WHITE backgrounds

# ============================================================================
# SHARED CSS (same visual system as the Claude-artifact version)
# ============================================================================
BASE_CSS = r"""
:root{
  --navy-dk:#0b2350; --navy:#0d2d5b; --navy-lt:#14548c;
  --ink:#0d2d5b; --ink-soft:#5c6c80; --paper:#f4f6fa; --surface:#ffffff; --surface-2:#eef1f6;
  --line:#dce2ea;
  --accent:__ACCENT__; --accent-soft:__ACCENT_SOFT__;
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
  font-family:"Ubuntu",system-ui,sans-serif; font-size:16px; line-height:1.5;
  -webkit-font-smoothing:antialiased;
}
.mono{font-family:"Ubuntu Mono",monospace;}
h1,h2,h3{font-family:"Ubuntu",sans-serif; font-weight:700; margin:0;}
a{color:var(--navy-lt)}

.rv-logo{flex:none; display:block;}
.rv-logo img{display:block; width:100%; height:100%; object-fit:contain;}

header.hero{
  background:linear-gradient(115deg, var(--navy-dk) 0%, var(--navy) 45%, var(--navy-lt) 100%);
  color:#fff; padding:26px 0 34px; position:relative; overflow:hidden;
}
header.hero::after{
  content:""; position:absolute; left:-40px; bottom:-60px; width:180px; height:220px;
  border:2px solid var(--yellow); border-radius:20px; opacity:.55;
}
.hero-inner{max-width:900px; margin:0 auto; padding:0 20px; display:flex; align-items:flex-start; gap:18px; position:relative; z-index:2;}
.hero-text{flex:1;}
.hero-eyebrow{font-size:12.5px; text-transform:uppercase; letter-spacing:.12em; color:#cfe0f5; margin-bottom:8px; font-weight:500;}
.hero-title{font-size:28px; line-height:1.15;}
.hero-sub{font-size:14.5px; color:#d7e4f7; margin-top:8px; max-width:560px;}
.hero-logo{width:60px; height:60px;}

.top-tabs{display:flex; gap:6px; margin-top:18px;}
.tab-btn{
  border:1px solid rgba(255,255,255,.35); background:rgba(255,255,255,.08); color:#fff;
  padding:8px 14px; border-radius:999px; font-size:13.5px; font-weight:500; cursor:pointer;
  transition:.15s;
}
.tab-btn.active{background:#fff; color:var(--navy); border-color:#fff; font-weight:700;}
.tab-btn:not(.active):hover{border-color:#fff;}

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
.scale-row p{margin:0; font-size:14px;}
.anon-note{
  display:flex; gap:8px; align-items:center; margin-top:14px; font-size:13px; color:var(--ink-soft);
  padding:10px 12px; background:var(--accent-soft); border-radius:10px;
}

.progress-wrap{ position:sticky; top:0; z-index:30; background:var(--paper); padding:10px 0 14px; }
.progress-track{ height:8px; border-radius:999px; background:var(--surface-2); border:1px solid var(--line); overflow:hidden; }
.progress-fill{height:100%; background:var(--accent); width:0%; transition:width .25s;}
.progress-label{display:flex; justify-content:space-between; font-size:12.5px; color:var(--ink-soft); margin-top:6px;}

.item{ background:var(--surface); border:1px solid var(--line); border-radius:var(--radius); padding:16px 18px; margin-bottom:12px; box-shadow:var(--shadow); }
.item.voted{border-color:var(--accent);}
.item-top{display:flex; gap:10px; align-items:flex-start;}
.item-idx{ font-family:"Ubuntu Mono",monospace; font-size:12px; color:var(--ink-soft); flex:none; padding-top:2px; width:30px; }
.item-title{font-size:15.5px; font-weight:500; flex:1;}
.item-meta{display:flex; gap:6px; flex-wrap:wrap; margin:8px 0 0 40px;}
.chip{ font-size:11px; padding:2px 8px; border-radius:999px; border:1px solid var(--line); color:var(--ink-soft); background:var(--surface-2); font-weight:500; }
.chip.type-c{color:var(--navy-lt); border-color:var(--navy-lt); background:var(--accent-soft);}
.chip.origin-telecom{color:#8a5a00; border-color:#e3c07a; background:#fdf0dc;}
.chip.origin-ambos{color:#5b3fa0; border-color:#c9bce8; background:#efeaf9;}
details.orig{margin:8px 0 0 40px;}
details.orig summary{font-size:12.5px; color:var(--navy-lt); cursor:pointer; list-style:none; font-weight:500;}
details.orig summary::-webkit-details-marker{display:none;}
details.orig ol{margin:8px 0 0; padding-left:18px; font-size:13px; color:var(--ink-soft);}
details.orig ol li{margin-bottom:4px;}
details.orig .oi-origin{font-size:10.5px; font-weight:700; padding:1px 6px; border-radius:999px; margin-left:6px; white-space:nowrap;}
details.orig .oi-origin.t{color:#8a5a00; background:#fdf0dc;}
details.orig .oi-origin.a{color:#5b3fa0; background:#efeaf9;}
details.orig .reason{margin-top:6px; font-size:12.5px; color:var(--ink-soft); font-style:italic;}

.vote-row{display:flex; gap:8px; margin:12px 0 0 40px; flex-wrap:wrap;}
.vote-btn{ flex:1; min-width:140px; border:1.5px solid var(--line); background:var(--surface); border-radius:10px; padding:9px 12px; cursor:pointer; text-align:left; display:flex; align-items:center; gap:9px; transition:.12s; }
.vote-btn .vnum{ font-family:"Ubuntu Mono",monospace; font-weight:700; font-size:14px; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#fff; flex:none; }
.vote-btn .vtxt{font-size:12.5px; color:var(--ink-soft); line-height:1.25; font-weight:500;}
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
.save-bar-text{flex:1; min-width:180px; font-size:13px; color:var(--ink-soft); line-height:1.4;}
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
.admin-item-top{display:flex; gap:10px; align-items:baseline;}
.admin-item-top .item-title{font-size:14.5px;}
.avg-badge{ font-family:"Ubuntu Mono",monospace; font-weight:700; font-size:13px; padding:3px 10px; border-radius:999px; color:#fff; flex:none; }
.bars{display:flex; height:10px; border-radius:999px; overflow:hidden; margin:10px 0 6px 0; background:var(--surface-2);}
.bar-5{background:var(--green);} .bar-3{background:var(--gold);} .bar-1{background:var(--red);}
.bar-legend{display:flex; gap:14px; font-size:11.5px; color:var(--ink-soft); flex-wrap:wrap;}
.bar-legend b{color:var(--ink);}
.rank-toggle{display:flex; gap:6px; margin-bottom:14px;}
.rank-toggle button{ border:1px solid var(--line); background:var(--surface-2); color:var(--ink-soft); padding:7px 12px; border-radius:999px; font-size:12.5px; font-weight:500; cursor:pointer; }
.rank-toggle button.active{background:var(--accent); color:#fff; border-color:var(--accent);}

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
# VOTING PAGE TEMPLATE (no login, writes to Supabase with an anonymous key)
# ============================================================================
VOTE_TEMPLATE = HEAD + r"""
<body>

<header class="hero">
  <div class="hero-inner">
    <div class="hero-text">
      <div class="hero-eyebrow">RV Digital &middot; Planejamento Estrat&eacute;gico 2027 &middot; SWOT Telecom e Ambos</div>
      <h1 class="hero-title">Vota&ccedil;&atilde;o &mdash; __QUAD_LABEL__</h1>
      <div class="hero-sub">Vota&ccedil;&atilde;o an&ocirc;nima. Esta vota&ccedil;&atilde;o &eacute; exclusiva do quadrante __QUAD_LABEL_LOWER__ (__ITEM_COUNT__ itens).</div>
    </div>
    <div class="rv-logo hero-logo"><img src="data:image/png;base64,__LOGO_A_B64__" alt="RV Digital"></div>
  </div>
</header>

<main>
  <section class="view active" id="view-vote">
    <div class="intro">
      <p style="font-size:14.5px; margin:0 0 10px; font-weight:500;">Para cada item, avalie seu grau de concord&acirc;ncia com a prioriza&ccedil;&atilde;o da proposta:</p>
      <div class="scale">
        <div class="scale-row s5"><div class="scale-num">5</div><p><b>Concordo totalmente</b> &mdash; este item deve ser altamente priorizado.</p></div>
        <div class="scale-row s3"><div class="scale-num">3</div><p><b>Concordo parcialmente</b> &mdash; este item &eacute; relevante, mas n&atilde;o priorit&aacute;rio.</p></div>
        <div class="scale-row s1"><div class="scale-num">1</div><p><b>Discordo</b> &mdash; este item n&atilde;o deve ser priorizado.</p></div>
      </div>
      <div class="anon-note">&#128274; Sua vota&ccedil;&atilde;o &eacute; an&ocirc;nima: ningu&eacute;m vê quem votou o qu&ecirc; &mdash; apenas os totais agregados, e somente para os administradores autorizados. N&atilde;o &eacute; necess&aacute;rio fazer login.</div>
      <div class="anon-note" style="background:var(--surface-2);">&#128190; V&aacute; marcando suas respostas normalmente. Nada &eacute; enviado ainda &mdash; s&oacute; quando voc&ecirc; clicar em <b>"Salvar respostas"</b>, no final da p&aacute;gina, é que elas s&atilde;o gravadas. N&atilde;o atualize a p&aacute;gina antes de salvar, ou as marca&ccedil;&otilde;es ainda n&atilde;o salvas ser&atilde;o perdidas.</div>
    </div>

    <div class="progress-wrap">
      <div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="progress-label"><span id="progress-text">0 de __ITEM_COUNT__ respondidos</span><span id="vote-status-text"></span></div>
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
    <div class="pagefoot-text">Planejamento Estrat&eacute;gico RV Digital 2027 &mdash; Vota&ccedil;&atilde;o an&ocirc;nima do quadrante __QUAD_LABEL__ &middot; SWOT Telecom e Ambos</div>
  </div>
</footer>

<script>
var QUAD_KEY = "__QUAD_KEY__";
var ITEMS = __ITEMS_JSON__;

var sb = window.supabase.createClient(window.RV_SUPABASE_URL, window.RV_SUPABASE_ANON_KEY);

function getClientId(){
  var k = "rv_swot_client_id";
  var id = localStorage.getItem(k);
  if(!id){
    id = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : ("id-" + Date.now() + "-" + Math.random().toString(16).slice(2));
    localStorage.setItem(k, id);
  }
  return id;
}
var myId = getClientId();
var myVotes = {};
var savedVotes = {};
var votingOpen = true, saving = false;

function origLabel(o){ return o === "Telecom" ? "Telecom" : "Ambos"; }
function origClass(o){ return o === "Telecom" ? "t" : "a"; }
function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}

function renderItems(){
  var mount = document.getElementById("items-mount");
  var html = "";
  ITEMS.forEach(function(it, i){ html += renderItem(it, i+1); });
  mount.innerHTML = html;
}
function renderItem(it, idx){
  var typeChip = it.type === "convergencia"
    ? '<span class="chip type-c">Convergência · '+it.n+' propostas</span>'
    : '<span class="chip">Proposta isolada</span>';
  var divisionChips = (it.divisions || []).map(function(a){ return '<span class="chip">'+escapeHtml(a)+'</span>'; }).join("");
  var originChips = (it.origins || []).map(function(o){
    return '<span class="chip origin-'+(o==="Telecom"?"telecom":"ambos")+'">'+o+'</span>';
  }).join("");
  var details = "";
  if(it.type === "convergencia" && it.originals){
    var origLis = it.originals.map(function(o){
      return "<li>"+escapeHtml(o.text)+' <span class="oi-origin '+origClass(o.origin)+'">'+origLabel(o.origin)+'</span></li>';
    }).join("");
    details = '<details class="orig"><summary>Ver as '+it.originals.length+' propostas originais e o motivo da unifica&ccedil;&atilde;o</summary>'
      + '<ol>'+origLis+'</ol>'
      + '<div class="reason">'+escapeHtml(it.reason)+'</div>'
      + '</details>';
  }
  return '<div class="item" id="item-'+it.id+'" data-id="'+it.id+'">'
    + '<div class="item-top"><div class="item-idx mono">#'+idx+'</div><div class="item-title">'+escapeHtml(it.title)+'</div></div>'
    + '<div class="item-meta">'+typeChip+originChips+divisionChips+'</div>'
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
  document.getElementById("progress-fill").style.width = Math.round(voted/ITEMS.length*100) + "%";
  document.getElementById("progress-text").textContent = voted + " de " + ITEMS.length + " respondidos";
  document.getElementById("vote-status-text").textContent = votingOpen ? "" : "Vota&ccedil;&atilde;o encerrada pelo administrador";
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
function updateSaveBar(){
  var text = document.getElementById("save-bar-text");
  var btn = document.getElementById("save-btn");
  if(!text || !btn) return;
  var dirty = countDirty();
  var answered = Object.keys(myVotes).length;
  if(saving){
    text.textContent = "Salvando suas respostas&hellip;";
    btn.textContent = "Salvando&hellip;"; btn.disabled = true; btn.className = "save-btn state-saving";
    return;
  }
  if(!votingOpen){
    text.textContent = "Vota&ccedil;&atilde;o encerrada pelo administrador &mdash; n&atilde;o &eacute; mais poss&iacute;vel salvar.";
    btn.disabled = true; btn.className = "save-btn"; btn.textContent = "Salvar respostas";
    return;
  }
  if(answered === 0){ text.textContent = "Nenhuma resposta selecionada ainda."; }
  else if(dirty === 0){ text.textContent = answered + " de " + ITEMS.length + " respondidos &mdash; tudo salvo."; }
  else { text.textContent = answered + " de " + ITEMS.length + " respondidos &mdash; " + dirty + " altera&ccedil;&atilde;o(&otilde;es) ainda n&atilde;o salva(s)."; }
  btn.disabled = dirty === 0;
  btn.className = "save-btn" + (dirty === 0 && answered > 0 ? " state-saved" : "");
  btn.textContent = dirty > 0 ? ("Salvar respostas (" + dirty + ")") : "Salvar respostas";
}
function showFlash(msg, isError){
  var flash = document.getElementById("save-flash");
  if(!flash) return;
  flash.textContent = (isError ? "&#9888; " : "&#10003; ") + msg;
  flash.className = "save-flash show" + (isError ? " error" : "");
  clearTimeout(flash._t);
  flash._t = setTimeout(function(){ flash.className = "save-flash"; }, 5000);
}
function castVote(itemId, score){
  if(!votingOpen || saving) return;
  myVotes[itemId] = score;
  paintMyVotes();
}
async function saveAllVotes(){
  if(!votingOpen || saving) return;
  if(countDirty() === 0) return;
  saving = true; updateSaveBar();
  try{
    var payload = { quadrant: QUAD_KEY, client_id: myId, scores: Object.assign({}, myVotes), updated_at: new Date().toISOString() };
    var res = await sb.from("votes").upsert(payload, { onConflict: "quadrant,client_id" });
    if(res.error) throw res.error;
    savedVotes = Object.assign({}, myVotes);
    saving = false; paintMyVotes();
    showFlash("Respostas salvas com sucesso &mdash; registradas anonimamente.", false);
  }catch(e){
    console.warn("save failed", e);
    saving = false; paintMyVotes();
    showFlash("N&atilde;o foi poss&iacute;vel salvar agora. Verifique sua conex&atilde;o e clique em \"Salvar respostas\" novamente.", true);
  }
}
document.getElementById("save-btn").addEventListener("click", saveAllVotes);
window.addEventListener("beforeunload", function(e){
  if(countDirty() > 0){ e.preventDefault(); e.returnValue = ""; }
});

async function loadConfig(){
  try{
    var res = await sb.from("voting_config").select("is_open").eq("quadrant", QUAD_KEY).maybeSingle();
    if(!res.error && res.data) votingOpen = !!res.data.is_open;
  }catch(e){ console.warn("config load failed", e); }
  paintMyVotes();
}

renderItems();
paintMyVotes();
loadConfig();
setInterval(loadConfig, 20000);
</script>
</body>
</html>
"""

# ============================================================================
# ADMIN TEMPLATE (login-gated dashboard, all 4 quadrants)
# ============================================================================
ADMIN_TEMPLATE = HEAD.replace("__PAGE_TITLE__", "Painel Administrativo &mdash; Vota&ccedil;&atilde;o SWOT &mdash; RV Digital 2027").replace("__PAGE_DESC__", "Painel de resultados ao vivo da vota&ccedil;&atilde;o SWOT, restrito aos administradores.") + r"""
<body>

<header class="hero">
  <div class="hero-inner">
    <div class="hero-text">
      <div class="hero-eyebrow">RV Digital &middot; Planejamento Estrat&eacute;gico 2027</div>
      <h1 class="hero-title">Painel Administrativo &mdash; Vota&ccedil;&atilde;o SWOT</h1>
      <div class="hero-sub">Acompanhamento ao vivo, restrito aos administradores. SWOT Telecom e Ambos.</div>
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
      <button class="toggle-btn" style="background:var(--ink-soft);" id="logout-btn">Sair</button>
    </div>
    <div class="rank-toggle">
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
    <div class="pagefoot-text">Planejamento Estrat&eacute;gico RV Digital 2027 &mdash; Painel administrativo &middot; SWOT Telecom e Ambos</div>
  </div>
</footer>

<script>
var ALL_ITEMS = __ALL_ITEMS_JSON__;   // { forcas: [...], fraquezas: [...], ... }
var sb = window.supabase.createClient(window.RV_SUPABASE_URL, window.RV_SUPABASE_ANON_KEY);
var currentQuad = "forcas";
var votingOpenByQuad = {};
var rowsByQuad = {};
var adminOrder = "original";

function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}

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
    err.textContent = "E-mail ou senha incorretos, ou esta conta n&atilde;o &eacute; administradora.";
  }
});
document.getElementById("logout-btn").addEventListener("click", async function(){
  await sb.auth.signOut();
  location.reload();
});

async function onLoggedIn(){
  document.getElementById("login-gate").style.display = "none";
  document.getElementById("dash").style.display = "block";
  document.getElementById("tabs").style.display = "flex";
  await refreshAll();
  sb.channel("votes-changes")
    .on("postgres_changes", { event: "*", schema: "public", table: "votes" }, function(){ refreshAll(); })
    .subscribe();
}

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
document.getElementById("toggle-voting").addEventListener("click", async function(){
  var newState = !votingOpenByQuad[currentQuad];
  try{
    await sb.from("voting_config").update({ is_open: newState }).eq("quadrant", currentQuad);
    votingOpenByQuad[currentQuad] = newState;
    paintToggle();
  }catch(e){ console.warn("toggle failed", e); }
});
function paintToggle(){
  var open = !!votingOpenByQuad[currentQuad];
  var tb = document.getElementById("toggle-voting");
  tb.textContent = open ? "Vota&ccedil;&atilde;o aberta" : "Vota&ccedil;&atilde;o encerrada";
  tb.classList.toggle("open", open);
  tb.classList.toggle("closed", !open);
}

async function refreshAll(){
  try{
    var votesRes = await sb.from("votes").select("quadrant,scores");
    if(!votesRes.error){
      rowsByQuad = { forcas: [], fraquezas: [], oportunidades: [], ameacas: [] };
      (votesRes.data || []).forEach(function(r){ if(rowsByQuad[r.quadrant]) rowsByQuad[r.quadrant].push(r.scores || {}); });
    }
    var cfgRes = await sb.from("voting_config").select("quadrant,is_open");
    if(!cfgRes.error){
      (cfgRes.data || []).forEach(function(r){ votingOpenByQuad[r.quadrant] = r.is_open; });
    }
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

function renderDash(){
  paintToggle();
  var mount = document.getElementById("admin-mount");
  var items = (ALL_ITEMS[currentQuad] || []).slice();
  var agg = computeAgg(currentQuad);
  var voters = (rowsByQuad[currentQuad] || []).length;
  var totalVotes = 0, sumAll = 0;
  Object.keys(agg).forEach(function(id){ totalVotes += agg[id].total; sumAll += agg[id].sum; });
  document.getElementById("admin-voters").textContent = voters;
  document.getElementById("admin-total-votes").textContent = totalVotes;
  document.getElementById("admin-avg").textContent = totalVotes ? (sumAll/totalVotes).toFixed(2) : "&mdash;";

  if(adminOrder === "rank-desc" || adminOrder === "rank-asc"){
    items.sort(function(a,b){
      var aa = agg[a.id], bb = agg[b.id];
      var avA = aa.total ? aa.sum/aa.total : -1;
      var avB = bb.total ? bb.sum/bb.total : -1;
      return adminOrder === "rank-desc" ? (avB-avA) : (avA-avB);
    });
  }

  var html = "";
  items.forEach(function(it){
    var a = agg[it.id];
    var avg = a.total ? (a.sum/a.total) : null;
    var avgColor = avg===null ? "var(--ink-soft)" : (avg>=4 ? "var(--green)" : (avg>=2.2 ? "var(--gold)" : "var(--red)"));
    var pct5 = a.total ? (a.c5/a.total*100) : 0;
    var pct3 = a.total ? (a.c3/a.total*100) : 0;
    var pct1 = a.total ? (a.c1/a.total*100) : 0;
    html += '<div class="admin-item">'
      + '<div class="admin-item-top"><div class="item-title" style="flex:1">'+escapeHtml(it.title)+'</div>'
      + '<span class="avg-badge" style="background:'+avgColor+'">'+(avg===null?"sem votos":avg.toFixed(1))+'</span></div>'
      + '<div class="bars"><div class="bar-5" style="width:'+pct5+'%"></div><div class="bar-3" style="width:'+pct3+'%"></div><div class="bar-1" style="width:'+pct1+'%"></div></div>'
      + '<div class="bar-legend"><span><b>'+a.c5+'</b> concordam totalmente</span><span><b>'+a.c3+'</b> concordam parcialmente</span><span><b>'+a.c1+'</b> discordam</span><span><b>'+a.total+'</b> votos</span></div>'
      + '</div>';
  });
  mount.innerHTML = html;
}

(async function init(){
  var sess = await sb.auth.getSession();
  if(sess.data && sess.data.session){ onLoggedIn(); }
})();
</script>
</body>
</html>
"""

# ============================================================================
# Data: Telecom + Ambos SWOT — same content already validated in the Claude version
# ============================================================================
CONVERGENCES = {
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

SOLOS = {
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

QUADRANTS = [
  {"key":"forcas", "label":"Forças", "accent":"#00b554", "accent_soft":"#e2f8ea"},
  {"key":"fraquezas", "label":"Fraquezas", "accent":"#d14343", "accent_soft":"#fbe6e6"},
  {"key":"oportunidades", "label":"Oportunidades", "accent":"#14548c", "accent_soft":"#e4edf6"},
  {"key":"ameacas", "label":"Ameaças", "accent":"#f5a100", "accent_soft":"#fdf0dc"},
]

def build_items(qkey):
    items = []
    for i, c in enumerate(CONVERGENCES[qkey], start=1):
        origs = [{"text":o[0], "division":o[1], "origin":o[2]} for o in c["originals"]]
        divisions = sorted(set(o["division"] for o in origs))
        origins = sorted(set(o["origin"] for o in origs))
        items.append({
            "id": qkey + "_c" + str(i), "type": "convergencia", "title": c["title"],
            "divisions": divisions, "origins": origins, "n": len(origs),
            "originals": origs, "reason": c["reason"],
        })
    for i, s in enumerate(SOLOS[qkey], start=1):
        items.append({
            "id": qkey + "_s" + str(i), "type": "isolada", "title": s[0],
            "divisions": [s[1]], "origins": [s[2]], "n": 1, "originals": None, "reason": None,
        })
    return items

OUT_DIR = "/home/claude/votacao_supabase"

for q in QUADRANTS:
    items = build_items(q["key"])
    html = VOTE_TEMPLATE
    html = html.replace("__CSS__", BASE_CSS.replace("__ACCENT_SOFT__", q["accent_soft"]).replace("__ACCENT__", q["accent"]))
    html = html.replace("__PAGE_TITLE__", "Votação SWOT — " + q["label"] + " — RV Digital 2027")
    html = html.replace("__PAGE_DESC__", "Votação anônima sobre as propostas do quadrante " + q["label"] + " — SWOT Telecom e Ambos, RV Digital 2027.")
    html = html.replace("__QUAD_LABEL_LOWER__", q["label"].lower())
    html = html.replace("__QUAD_LABEL__", q["label"])
    html = html.replace("__QUAD_KEY__", q["key"])
    html = html.replace("__ITEM_COUNT__", str(len(items)))
    html = html.replace("__ITEMS_JSON__", json.dumps(items, ensure_ascii=False))
    html = html.replace("__LOGO_A_B64__", LOGO_A_B64)
    html = html.replace("__LOGO_B_B64__", LOGO_B_B64)
    fname = OUT_DIR + "/" + q["key"] + ".html"
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname, len(items), "items")

# Admin page (all 4 quadrants)
all_items = {q["key"]: build_items(q["key"]) for q in QUADRANTS}
admin_html = ADMIN_TEMPLATE
admin_html = admin_html.replace("__CSS__", BASE_CSS.replace("__ACCENT_SOFT__", "#e4edf6").replace("__ACCENT__", "#14548c"))
admin_html = admin_html.replace("__ALL_ITEMS_JSON__", json.dumps(all_items, ensure_ascii=False))
admin_html = admin_html.replace("__LOGO_A_B64__", LOGO_A_B64)
admin_html = admin_html.replace("__LOGO_B_B64__", LOGO_B_B64)
with open(OUT_DIR + "/admin.html", "w", encoding="utf-8") as f:
    f.write(admin_html)
print("wrote", OUT_DIR + "/admin.html")
