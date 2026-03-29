#!/usr/bin/env python3
"""Añade a Mario persiguiendo al Koopa en todas las páginas."""

from pathlib import Path
import re

OLD_KOOPA_BLOCK = '''<style>
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

NEW_DUO_BLOCK = '''<style>
.personaje {
  position: fixed;
  bottom: 20px;
  z-index: 9999;
  cursor: pointer;
  image-rendering: pixelated;
}
#koopa {
  animation: correr 12s linear infinite;
}
#mario {
  animation: correr 12s linear infinite;
  animation-delay: -2s;
}
@keyframes correr {
  0% { left: -80px; transform: scaleX(1); }
  49% { left: calc(100vw + 80px); transform: scaleX(1); }
  50% { left: calc(100vw + 80px); transform: scaleX(-1); }
  99% { left: -80px; transform: scaleX(-1); }
  100% { left: -80px; transform: scaleX(1); }
}
#koopa:hover, #mario:hover {
  animation-play-state: paused;
}
</style>
<canvas class="personaje" id="mario" width="16" height="16" style="width:56px;height:56px" title="¡It's-a me!"></canvas>
<canvas class="personaje" id="koopa" width="16" height="16" style="width:56px;height:56px" title="¡Mamma mia!"></canvas>
<script>
// MARIO pixel art
(function(){
  const c = document.getElementById('mario').getContext('2d');
  const p = ['','#1a1a1a','#e53935','#ffcc80','#1565c0','#ffeb3b','#795548'];
  const px = [
    [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,1,2,2,2,2,2,2,2,1,0,0,0,0,0],
    [0,1,2,2,2,3,3,2,3,2,1,0,0,0,0,0],
    [0,1,2,3,2,3,3,3,3,3,1,0,0,0,0,0],
    [0,1,2,3,3,3,3,3,3,3,1,0,0,0,0,0],
    [0,0,1,3,3,3,2,2,1,0,0,0,0,0,0,0],
    [0,1,4,4,2,4,4,4,4,1,0,0,0,0,0,0],
    [1,4,4,4,2,4,4,2,4,4,4,1,0,0,0,0],
    [1,4,4,4,4,4,4,4,4,4,4,1,0,0,0,0],
    [0,1,4,4,5,5,4,4,5,4,1,0,0,0,0,0],
    [0,1,3,3,5,5,5,5,5,3,1,0,0,0,0,0],
    [1,3,3,3,5,5,5,5,5,3,3,1,0,0,0,0],
    [1,3,3,5,5,5,5,5,5,5,3,1,0,0,0,0],
    [0,0,1,5,5,1,0,1,5,5,1,0,0,0,0,0],
    [0,1,6,6,6,1,0,1,6,6,6,1,0,0,0,0],
    [1,6,6,6,0,0,0,0,0,6,6,6,1,0,0,0],
  ];
  px.forEach((row,y)=>row.forEach((col,x)=>{
    if(!col)return;
    ctx.fillStyle=p[col];
    ctx.fillRect(x,y,1,1);
  }));
  let f=0;
  setInterval(()=>{
    ctx.clearRect(0,12,16,4);
    const legs = f%2===0 ? [[0,1,6,6,1,0,0,1,6,6,6,1],[1,6,6,0,0,0,0,0,0,6,6,6,1]] : [[0,0,1,6,6,1,0,1,6,6,1,0],[0,0,0,1,6,6,0,1,6,6,0,0,0]];
    legs.forEach((row,y)=>row.forEach((col,x)=>{
      if(!col)return;
      ctx.fillStyle=p[col];
      ctx.fillRect(x,13+y,1,1);
    }));
    f++;
  },180);
})();
// KOOPA pixel art
(function(){
  const c = document.getElementById('koopa').getContext('2d');
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
  px.forEach((row,y)=>row.forEach((col,x)=>{
    if(!col)return;
    ctx.fillStyle=p[col];
    ctx.fillRect(x,y,1,1);
  }));
  let f=0;
  setInterval(()=>{
    ctx.clearRect(0,12,16,4);
    const legs = f%2===0 ? [[1,4,4,7,1,0,0,0,1,7,4,4,1],[1,4,4,1,0,0,0,0,0,1,4,1,0]] : [[0,1,4,4,7,1,0,1,7,4,4,1,0],[0,0,1,4,4,1,0,1,4,4,1,0,0]];
    legs.forEach((row,y)=>row.forEach((col,x)=>{
      if(!col)return;
      ctx.fillStyle=p[col];
      ctx.fillRect(x,13+y,1,1);
    }));
    f++;
  },200);
})();
</script>'''

def replace_with_duo(filepath):
    """Reemplaza el Koopa por el dúo Mario+Koopa."""
    content = filepath.read_text(encoding='utf-8')
    
    # Verificar si ya tiene el dúo
    if 'id="mario"' in content:
        print(f"   ⏭️  {filepath.name} ya tiene el dúo")
        return
    
    # Reemplazar el bloque de estilo
    content = content.replace(OLD_KOOPA_BLOCK, NEW_DUO_BLOCK)
    
    # Si no se reemplazó, buscar otros patrones del Koopa canvas anterior
    if 'id="mario"' not in content:
        # Buscar y eliminar el viejo div#koopa y canvas#koopa-canvas
        content = re.sub(
            r'<canvas[^>]*id="koopa-canvas"[^>]*>[^<]*</canvas>',
            '',
            content
        )
        content = re.sub(
            r'<div[^>]*id="koopa"[^>]*>[^<]*</div>',
            '',
            content
        )
        
        # Eliminar el viejo script del Koopa
        content = re.sub(
            r'\(function\(\)\{[^}]*koopa-canvas[^}]*\}\)\(\);',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Añadir el nuevo bloque antes de </body>
        content = content.replace(
            '</body>',
            NEW_DUO_BLOCK + '\n</body>'
        )
    
    filepath.write_text(content, encoding='utf-8')
    print(f"   ✅ {filepath.name}")

def main():
    print("🔴🐢 Añadiendo a Mario persiguiendo al Koopa...")
    
    # Archivos raíz
    root_files = ['index.html', 'sobre-nosotros.html']
    for filename in root_files:
        filepath = Path(filename)
        if filepath.exists():
            replace_with_duo(filepath)
    
    # Posts individuales
    posts_dir = Path('posts')
    count = 0
    if posts_dir.exists():
        for post_dir in posts_dir.iterdir():
            if post_dir.is_dir():
                index_file = post_dir / 'index.html'
                if index_file.exists():
                    replace_with_duo(index_file)
                    count += 1
        print(f"\n   📁 {count} posts actualizados")
    
    print("\n🎉 ¡Mario persigue al Koopa en todas las páginas!")

if __name__ == "__main__":
    main()
