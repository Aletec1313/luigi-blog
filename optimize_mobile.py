#!/usr/bin/env python3
"""Optimiza el blog para móvil: añade viewport y actualiza CSS."""

from pathlib import Path
import re

VIEWPORT_META = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'

def add_viewport_to_file(filepath):
    """Añade el viewport meta si no existe."""
    content = filepath.read_text(encoding='utf-8')
    
    # Verificar si ya tiene viewport
    if 'viewport' in content.lower():
        # Verificar si tiene el correcto
        if 'width=device-width' in content and 'initial-scale=1.0' in content:
            print(f"   ⏭️  {filepath.name} ya tiene viewport correcto")
            return
        # Si tiene viewport pero con valorees diferentes, actualizar
        content = re.sub(
            r'<meta[^>]*viewport[^>]*>',
            VIEWPORT_META,
            content,
            flags=re.IGNORECASE
        )
        filepath.write_text(content, encoding='utf-8')
        print(f"   ✅ {filepath.name} (viewport actualizado)")
        return
    
    # Añadir viewport después del primer <meta charset...>
    content = re.sub(
        r'(<meta[^>]*charset[^>]*>)',
        r'\1\n  ' + VIEWPORT_META,
        content,
        flags=re.IGNORECASE
    )
    
    filepath.write_text(content, encoding='utf-8')
    print(f"   ✅ {filepath.name} (viewport añadido)")

def add_mobile_css_to_file(filepath):
    """Añade estilos responsive al final del CSS."""
    content = filepath.read_text(encoding='utf-8')
    
    # Verificar si ya tiene los estilos móviles
    if '@media (max-width: 768px)' in content:
        print(f"   ⏭️  {filepath.name} ya tiene estilos móviles")
        return
    
    mobile_styles = '''

/* ============================================
   ESTILOS RESPONSIVOS PARA MÓVIL
   ============================================ */

@media (max-width: 768px) {
  /* Header y navegación */
  .header-inner {
    flex-direction: column;
    text-align: center;
    padding: 12px 16px;
  }
  
  nav {
    flex-direction: column;
    text-align: center;
    padding: 8px;
    gap: 4px;
  }
  
  nav a {
    display: block;
    width: 100%;
    margin: 2px 0;
  }
  
  /* Hero */
  .hero {
    padding: 24px 16px;
  }
  
  .hero-img {
    max-width: 90%;
  }
  
  .hero h1, .hero-title {
    font-size: 16px;
  }
  
  .hero-emojis {
    font-size: 32px;
  }
  
  /* Posts */
  .container {
    padding: 0 12px 40px;
  }
  
  .post-card {
    margin: 8px 0;
    border-radius: 8px;
  }
  
  .post-card-inner {
    padding: 16px;
  }
  
  .post-card h2 {
    font-size: 16px;
  }
  
  .post-excerpt {
    font-size: 14px;
  }
  
  /* Sobre Nosotros */
  .profiles-grid {
    grid-template-columns: 1fr !important;
    gap: 16px;
  }
  
  .profile-card {
    padding: 24px;
  }
  
  .profile-emoji {
    font-size: 48px;
  }
  
  .profile-name {
    font-size: 20px;
  }
  
  /* Suscripción */
  .subscribe-section {
    padding: 24px 16px;
    margin: 24px 0 40px;
  }
  
  .subscribe-form {
    flex-direction: column;
  }
  
  .subscribe-form input[type="email"],
  .subscribe-form button {
    width: 100%;
    margin: 4px 0;
  }
  
  /* Koopa más pequeño en móvil */
  #koopa {
    font-size: 24px !important;
  }
  
  /* Footer */
  footer {
    padding-bottom: 50px;
  }
}

/* Para pantallas muy pequeñas */
@media (max-width: 480px) {
  .site-title {
    font-size: 8px;
  }
  
  .hero-tagline {
    font-size: 12px;
    padding: 8px 16px;
  }
  
  .post-card h2 {
    font-size: 15px;
  }
  
  .section-title {
    font-size: 8px;
  }
}
'''
    
    filepath.write_text(content + mobile_styles, encoding='utf-8')
    print(f"   ✅ {filepath.name} (estilos móviles añadidos)")

def main():
    print("📱 Optimizando para móvil...\n")
    
    # 1. Añadir viewport a todas las páginas HTML
    print("📝 Paso 1: Añadiendo viewport meta...")
    
    # Archivos raíz
    root_files = ['index.html', 'sobre-nosotros.html']
    for filename in root_files:
        filepath = Path(filename)
        if filepath.exists():
            add_viewport_to_file(filepath)
    
    # Posts individuales
    posts_dir = Path('posts')
    post_count = 0
    if posts_dir.exists():
        for post_dir in posts_dir.iterdir():
            if post_dir.is_dir():
                index_file = post_dir / 'index.html'
                if index_file.exists():
                    add_viewport_to_file(index_file)
                    post_count += 1
        print(f"   📁 {post_count} posts actualizados")
    
    # 2. Añadir estilos responsive al CSS
    print("\n📝 Paso 2: Añadiendo estilos responsive al CSS...")
    css_file = Path('css/style.css')
    if css_file.exists():
        add_mobile_css_to_file(css_file)
    else:
        print("   ⚠️  No se encontró css/style.css")
    
    print("\n🎉 ¡Blog optimizado para móvil!")
    print("\n📱 Cambios realizados:")
    print(f"   - Viewport añadido a {len(root_files) + post_count} páginas")
    print(f"   - Estilos responsive añadidos a CSS")
    print("\n✨ El blog ahora se ve bien en móviles y tablets")

if __name__ == "__main__":
    main()
