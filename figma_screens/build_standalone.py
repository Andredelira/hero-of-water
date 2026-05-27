"""
Gera prototipo.html com todas as imagens embutidas em base64.
Resultado: arquivo HTML 100% autonomo, nao precisa de nada externo.
"""
import base64

# Carregar imagens
files = [
    '01_Dificuldade.jpg',
    '02_Menu_Principal.jpg',
    '03_Historia.jpg',
    '04_Instrucoes.jpg',
    '05_Selecao_Fases.jpg',
    '06_Gameplay_Fase1.jpg',
    '07_Vitoria.jpg',
    '08_Derrota.jpg',
]

imgs = {}
for fname in files:
    with open(fname, 'rb') as f:
        imgs[fname] = base64.b64encode(f.read()).decode()
    print(f"  {fname} -> {len(imgs[fname])} chars")

# Template HTML
screens_html = ""

screen_configs = [
    ("01", "Dificuldade", "01_Dificuldade.jpg", True, [
        ("hotspot-facil",   "goTo('02')", "left:35%;top:44%;width:30%;height:9%"),
        ("hotspot-media",   "goTo('02')", "left:35%;top:58%;width:30%;height:9%"),
        ("hotspot-dificil", "goTo('02')", "left:35%;top:73%;width:30%;height:9%"),
    ], None),
    ("02", "Menu Principal", "02_Menu_Principal.jpg", False, [
        ("hotspot-jogar",      "goTo('03')", "left:35%;top:62%;width:30%;height:8%"),
        ("hotspot-instrucoes", "goTo('04')", "left:35%;top:73%;width:30%;height:7%"),
    ], None),
    ("03", "Historia", "03_Historia.jpg", False, [
        ("hotspot-avancar", "goTo('05')", "left:0;top:0;width:100%;height:100%"),
    ], "Clique em qualquer lugar para continuar"),
    ("04", "Instrucoes", "04_Instrucoes.jpg", False, [
        ("hotspot-voltar", "goTo('02')", "left:35%;top:80%;width:30%;height:9%"),
    ], None),
    ("05", "Selecao de Fases", "05_Selecao_Fases.jpg", False, [
        ("hotspot-fase1",  "goTo('06')", "left:7%;top:34%;width:15%;height:32%"),
        ("hotspot-fase2",  "goTo('06')", "left:24%;top:34%;width:15%;height:32%"),
        ("hotspot-voltar", "goTo('02')", "left:5%;top:84%;width:15%;height:8%"),
    ], None),
    ("06", "Gameplay (Fase 1)", "06_Gameplay_Fase1.jpg", False, [
        ("hotspot-derrota", "goTo('08')", "left:0;top:0;width:50%;height:100%"),
        ("hotspot-vitoria", "goTo('07')", "left:50%;top:0;width:50%;height:100%"),
    ], "Esquerda = derrota | Direita = vitoria"),
    ("07", "Vitoria", "07_Vitoria.jpg", False, [
        ("hotspot-proxima", "goTo('05')", "left:35%;top:78%;width:30%;height:9%"),
    ], None),
    ("08", "Derrota", "08_Derrota.jpg", False, [
        ("hotspot-recomecar", "goTo('05')", "left:35%;top:64%;width:30%;height:9%"),
    ], None),
]

for sid, label, imgfile, is_active, hotspots, hint in screen_configs:
    active = ' active' if is_active else ''
    n = int(sid)
    b64 = imgs[imgfile]

    hotspots_html = ""
    for cls, onclick, style in hotspots:
        hotspots_html += f'    <div class="hotspot" onclick="{onclick}" style="position:absolute;{style};cursor:pointer;background:transparent;z-index:10;border-radius:6px" onmouseover="this.style.background=\'rgba(255,255,255,0.12)\'" onmouseout="this.style.background=\'transparent\'"></div>\n'

    hint_html = ""
    if hint:
        hint_html = f'    <span style="position:absolute;bottom:5%;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.65);color:#fff;padding:8px 20px;border-radius:20px;font-size:13px;pointer-events:none;z-index:20">{hint}</span>\n'

    screens_html += f'''  <div class="screen{active}" id="screen-{sid}">
    <span style="position:absolute;top:8px;left:8px;background:rgba(0,0,0,0.65);color:#fff;padding:4px 10px;border-radius:4px;font-size:11px;z-index:30;pointer-events:none">{n}/8 — {label}</span>
    <img src="data:image/jpeg;base64,{b64}" alt="{label}" style="width:100%;height:100%;object-fit:cover;display:block">
{hotspots_html}{hint_html}  </div>

'''

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hero of the Water v5.0 — Prototipo Interativo</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0a0a0a;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Segoe UI', Arial, sans-serif;
    overflow: hidden;
  }}
  .screen-container {{
    position: relative;
    width: 960px;
    height: 540px;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 0 40px rgba(0,0,0,0.6);
  }}
  .screen {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
  }}
  .screen.active {{
    opacity: 1;
    pointer-events: auto;
  }}
  .nav-bar {{
    display: flex;
    justify-content: center;
    gap: 4px;
    padding: 12px 10px 8px;
    flex-wrap: wrap;
  }}
  .nav-btn {{
    background: #222;
    color: #888;
    border: 1px solid #444;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 11px;
    cursor: pointer;
    transition: all 0.2s;
  }}
  .nav-btn:hover {{ background: #444; color: #fff; }}
  .nav-btn.active {{ background: #4CAF50; color: #fff; border-color: #4CAF50; }}
  .proto-title {{
    color: #555;
    font-size: 11px;
    padding: 8px 0 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}
  @media (max-width: 980px) {{
    .screen-container {{ width: 96vw; height: calc(96vw * 9 / 16); }}
  }}
  @media (max-height: 650px) {{
    .screen-container {{ height: calc(100vh - 90px); width: calc((100vh - 90px) * 16 / 9); }}
  }}
</style>
</head>
<body>

<div class="screen-container" id="container">
{screens_html}</div>

<div class="nav-bar">
  <button class="nav-btn active" onclick="goTo('01')">1. Dificuldade</button>
  <button class="nav-btn" onclick="goTo('02')">2. Menu</button>
  <button class="nav-btn" onclick="goTo('03')">3. Historia</button>
  <button class="nav-btn" onclick="goTo('04')">4. Instrucoes</button>
  <button class="nav-btn" onclick="goTo('05')">5. Fases</button>
  <button class="nav-btn" onclick="goTo('06')">6. Gameplay</button>
  <button class="nav-btn" onclick="goTo('07')">7. Vitoria</button>
  <button class="nav-btn" onclick="goTo('08')">8. Derrota</button>
</div>
<div class="proto-title">Hero of the Water v5.0 — ODS 6 — ADS 2026</div>

<script>
  let currentScreen = '01';
  const screenNames = ['01','02','03','04','05','06','07','08'];

  function goTo(id) {{
    if (id === currentScreen) return;
    const prev = document.getElementById('screen-' + currentScreen);
    const next = document.getElementById('screen-' + id);
    if (prev) prev.classList.remove('active');
    if (next) next.classList.add('active');
    currentScreen = id;
    document.querySelectorAll('.nav-btn').forEach((btn, i) => {{
      btn.classList.toggle('active', screenNames[i] === id);
    }});
  }}

  document.addEventListener('keydown', (e) => {{
    const num = parseInt(e.key);
    if (num >= 1 && num <= 8) goTo(String(num).padStart(2, '0'));
    if (e.key === 'Escape') goTo('01');
    if (e.key === 'ArrowRight') {{
      const idx = screenNames.indexOf(currentScreen);
      if (idx < screenNames.length - 1) goTo(screenNames[idx + 1]);
    }}
    if (e.key === 'ArrowLeft') {{
      const idx = screenNames.indexOf(currentScreen);
      if (idx > 0) goTo(screenNames[idx - 1]);
    }}
  }});
</script>
</body>
</html>'''

with open('prototipo.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os
size = os.path.getsize('prototipo.html')
print(f"\nprototipo.html gerado: {size/1024:.0f} KB (autonomo)")
print("Abra direto no navegador — nao precisa de nenhum outro arquivo.")
