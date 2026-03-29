#!/usr/bin/env python3
"""Actualiza el Koopa a usar sprite en lugar de emoji en todas las páginas."""

from pathlib import Path

OLD_KOOPA = '<div id="koopa" title="¡Mamma mia!">🐢</div>'
NEW_KOOPA = '<div id="koopa" title="¡Mamma mia!"><img src="assets/koopa.png" alt="Koopa" style="width:48px;height:auto;image-rendering:pixelated;"></div>'

def update_koopa_in_file(filepath):
    """Reemplaza el emoji Koopa por la imagen."""
    content = filepath.read_text(encoding='utf-8')
    
    if '🐢' not in content and 'koopa.png' in content:
        print(f"   ⏭️  {filepath.name} ya tiene sprite")
        return
    
    new_content = content.replace(OLD_KOOPA, NEW_KOOPA)
    
    if new_content != content:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"   ✅ {filepath.name}")
    else:
        print(f"   ⚠️  {filepath.name} - no se encontró emoji")

def main():
    print("🐢 Actualizando Koopa a sprite...")
    
    posts_dir = Path('posts')
    count = 0
    if posts_dir.exists():
        for post_dir in posts_dir.iterdir():
            if post_dir.is_dir():
                index_file = post_dir / 'index.html'
                if index_file.exists():
                    update_koopa_in_file(index_file)
                    count += 1
        print(f"\n   📁 {count} posts actualizados")
    
    print("🎉 ¡Koopa ahora es pixel art!")

if __name__ == "__main__":
    main()
