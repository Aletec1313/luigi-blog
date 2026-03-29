#!/usr/bin/env python3
"""Añade el Koopa a todos los archivos HTML del blog."""

from pathlib import Path

KOOPA_CODE = '''<style>
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
</style>
<div id="koopa" title="¡Mamma mia!">🐢</div>'''

def add_koopa_to_file(filepath):
    """Añade el Koopa antes del </body> en un archivo HTML."""
    content = filepath.read_text(encoding='utf-8')
    
    # Verificar si ya tiene el koopa
    if 'id="koopa"' in content:
        print(f"   ⏭️  {filepath.name} ya tiene Koopa")
        return
    
    # Reemplazar </body> con Koopa + </body>
    new_content = content.replace('</body>', f'{KOOPA_CODE}\n</body>')
    
    filepath.write_text(new_content, encoding='utf-8')
    print(f"   ✅ {filepath.name}")

def main():
    print("🐢 Añadiendo Koopa a todas las páginas...\n")
    
    # Archivos raíz
    root_files = ['index.html', 'sobre-nosotros.html']
    for filename in root_files:
        filepath = Path(filename)
        if filepath.exists():
            add_koopa_to_file(filepath)
    
    # Posts individuales
    posts_dir = Path('posts')
    if posts_dir.exists():
        post_count = 0
        for post_dir in posts_dir.iterdir():
            if post_dir.is_dir():
                index_file = post_dir / 'index.html'
                if index_file.exists():
                    add_koopa_to_file(index_file)
                    post_count += 1
        print(f"\n   📁 {post_count} posts actualizados")
    
    print("\n🎉 ¡Koopa listo para correr!")

if __name__ == "__main__":
    main()
