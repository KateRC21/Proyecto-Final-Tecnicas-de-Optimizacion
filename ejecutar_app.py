"""
Script para ejecutar la aplicación Streamlit
"""

import subprocess
import sys
from pathlib import Path

def main():
    # Ruta a la aplicación
    app_path = Path(__file__).parent / "gui" / "app.py"
    
    # Comando para ejecutar Streamlit
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port=8501",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false"
    ]
    
    print("="*70)
    print("🚑 Iniciando Sistema de Optimización de Rutas de Ambulancias")
    print("="*70)
    print(f"\n📍 Aplicación: {app_path}")
    print(f"🌐 URL: http://localhost:8501")
    print("\n⚠️  Para detener: Presiona Ctrl+C")
    print("="*70)
    print()
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n✓ Aplicación detenida")
        print("="*70)

if __name__ == "__main__":
    main()

