#!/usr/bin/env python3
"""Reemplaza el Koopa por versión canvas pixel art en todas las páginas."""

from pathlib import Path
import re

OLD_KOOPA_STYLE = '''<style>
#koopa {
  position: fixed;
  bottom: 20px;
  left: -60px;
  font-size: 36px;
  z-index: 9999;
  animation: correr 12s linear infinite;
  cursor: pointer;
  filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.5));
}
@keyframes correr {
  0% { left: -60px; transform: scaleX(1); }
  49% { left: calc(100vw + 60px); transform: scaleX(1); }
  50% { left: calc(100vw + 60px); transform: scaleX(-1); }
  99% { left: -60px; transform: scaleX(-1); }
  100% { left: -60px; transform: scaleX(1); }
}
#koopa:hover {
  animation-play-state: paused;
  font-size: 48px;
}
</style>'''

NEW_KOOPA_STYLE = '''<style>
#koopa {
  position: fixed;
  bottom: 20px;
  left: -80px;
  z-index: 9999;
  cursor: pointer;
  animation: koopa-run 12s linear infinite;
  image-rendering: pixelated;
}
@keyframes koopa-run {
  0% { left: -80px; transform: scaleX(1); }
  49% { left: calc(100vw + 80px); transform: scaleX(1); }
  50% { left: calc(100vw + 80px); transform: scaleX(-1); }
  99% { left: -80px; transform: scaleX(-1); }
  100% { left: -80px; transform: scaleX(1); }
}
#koopa:hover {
  animation-play-state: paused;
}
#koopa canvas {
  width: 64px;
  height: 64px;
}
</style>'''

NEW_KOOPA_HTML = '''<div id="koopa" title="¡Mamma mia!">
  <canvas id="koopa-canvas" width="16" height="16"></canvas>
</div>
<script>
(function(){
  const c = document.getElementById('koopa-canvas');
  if(!c) return;
  const ctx = c.getContext('2d');
  const p = ['','#1a1a1a','#2d6a2d','#4caf50','#ffeb3b','#e53935','#ffffff','#ffcc80'];
  const px = [
    [0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
    [0,0,1,5,5,5,5,5,5,1,0,0,0,0,0,0],
    [0,1,5,5,5,5,5,5,5,5,1,0,0,0,0,0],
    [0,1,4,4,4,1,4,4,1,4,1,0,0,0,0,0],
    [0,1,4,4,4,1,4,4,1,4,1,0,0,0,0,0],
    [0,1,5,5,5,5,5,5,5,5,1,0,0,0,0,0],
    [0,0,1,2,2,2,2,2,2,1,0,0,0,0,0,0],
    [0,1,2,2,3,2,2,3,2,2,1,0,0,0,0,0],
    [1,2,2,3,3,2,2,3,3,2,2,1,0,0,0,0],
    [1,2,2,2,2,2,2,2,2,2,2,1,0,0,0,0],
    [1,2,3,2,2,2,2,2,2,3,2,1,0,0,0,0],
    [0,1,2,2,2,2,2,2,2,2,1,0,0,0,0,0],
    [0,0,1,7,7,1,0,1,7,7,1,0,0,0,0,0],
    [0,1,7,7,7,1,0,1,7,7,7,1,0,0,0,0],
    [1,4,4,7,7,1,0,1,7,7,4,4,1,0,0,0],
    [1,4,4,1,0,0,0,0,1,4,4,1,0,0,0,0],
  ];
  px.forEach((row,y) => row.forEach((col,x) => {
    if(col===0) return;
    ctx.fillStyle = p[col];
    ctx.fillRect(x,y,1,1);
  }));
  let frame = 0;
  setInterval(()=>{
    ctx.clearRect(0,12,16,4);
    if(frame % 2 === 0){
      [[1,4,4,7,1,0,0,0,1,7,4,4,1],[1,4,4,1,0,0,0,0,0,1,4,1,0]].forEach((row,y) => row.forEach((col,x) => {
        if(col) { ctx.fillStyle=p[col]; ctx.fillRect(x,13+y,1,1); }
      }));
    } else {
      [[0,1,4,4,7,1,0,1,7,4,4,1,0],[0,0,1,4,4,1,0,1,4,4,1,0,0]].forEach((row,y) => row.forEach((col,x) => {
        if(col) { ctx.fillStyle=p[col]; ctx.fillRect(x,13+y,1,1); }
      }));
    }
    frame++;
  }, 200);
})();
</script>'''

def replace_koopa_in_file(filepath):
    """Reemplaza el Koopa antiguo por la versión canvas."""
    content = filepath.read_text(encoding='utf-8')
    
    # Verificar si ya tiene el nuevo Koopa
    if 'koopa-canvas' in content:
        print(f"   ⏭️  {filepath.name} ya tiene Canvas Koopa")
        return
    
    # Buscar y reemplazar el estilo anterior
    if '#koopa {' in content:
        # Reemplazar el bloque de estilo completo
        content = re.sub(
            r'<style>\s*#koopa\s*\{[^}]*\}[^<]*</style>',
            NEW_KOOPA_STYLE,
            content,
            flags=re.DOTALL
        )
    else:
        # Si no hay estilo, añadirlo antes del div#koopa
        content = content.replace(
            '<div id="koopa"',
            NEW_KOOPA_STYLE + '\n<div id="koopa"'
        )
    
    # Reemplazar el div#koopa
    old_patterns = [
        r'<div id="koopa"[^>]*>[^<]*</div>',
        r'<div id="koopa"[^>]*><img[^>]*></div>',
    ]
    
    for pattern in old_patterns:
        content = re.sub(pattern, NEW_KOOPA_HTML, content, flags=re.DOTALL)
    
    filepath.write_text(content, encoding='utf-8')
    print(f"   ✅ {filepath.name}")

def main():
    print("🐢 Reemplazando Koopa por versión Canvas pixel art...")
    
    # Archivos raíz
    root_files = ['index.html', 'sobre-nosotros.html']
    for filename in root_files:
        filepath = Path(filename)
        if filepath.exists():
            replace_koopa_in_file(filepath)
    
    # Posts individuales
    posts_dir = Path('posts')
    count = 0
    if posts_dir.exists():
        for post_dir in posts_dir.iterdir():
            if post_dir.is_dir():
                index_file = post_dir / 'index.html'
                if index_file.exists():
                    replace_koopa_in_file(index_file)
                    count += 1
        print(f"\n   📁 {count} posts actualizados")
    
    print("\n🎉 ¡Koopa ahora es Canvas pixel art animado!")

if __name__ == "__main__":
    main()
