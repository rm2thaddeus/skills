import base64
from pathlib import Path


def to_data_uri(png_path: Path) -> str:
    data = png_path.read_bytes()
    b64 = base64.b64encode(data).decode('ascii')
    return f"data:image/png;base64,{b64}"


def main() -> None:
    op_dir = Path('artifacts/operations/20251105-102650-104666')
    slides_dir = op_dir / 'html' / 'slides'
    persona = op_dir / 'output' / 'assets' / 'persona_banner.png'
    mindmap = op_dir / 'output' / 'assets' / 'mindmap_system.png'

    persona_uri = to_data_uri(persona)
    mindmap_uri = to_data_uri(mindmap)

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html {{ background: #2c2c2c; }}
  body {{ width: 720pt; height: 405pt; margin: 0; padding: 0; background: #2c2c2c; font-family: Arial, Helvetica, sans-serif; }}
  h2 {{ color: #f4f6f6; font-size: 24pt; margin: 24pt 48pt 0 48pt; }}
  .left {{ position: absolute; left: 48pt; top: 90pt; width: 300pt; height: 240pt; }}
  .right{{ position: absolute; right: 48pt; top: 90pt; width: 300pt; height: 240pt; }}
  img {{ width: 100%; height: 100%; object-fit: contain; border: 1pt solid #aab7b8; border-radius: 8pt; background: #202020; }}
  
</style>
</head>
<body>
  <h2>Qui je suis — et comment j’y suis arrivé</h2>
  <div class="left">
    <img src="{persona_uri}" alt="Scientifique → Architecte LLM" />
  </div>
  <div class="right">
    <img src="{mindmap_uri}" alt="Mindmap du système de candidatures IA" />
  </div>
</body>
</html>
'''
    out = slides_dir / '00_intro_fr_embed.html'
    out.write_text(html, encoding='utf-8')
    print(str(out))


if __name__ == '__main__':
    main()






