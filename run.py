import os
import sys

# Adiciona o diretório atual ao path para garantir que os imports funcionem
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Ponto de entrada principal da aplicação."""
    from src.app import create_app

    # Criar a aplicação Flask
    app = create_app()

    # Configurações do servidor
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("ENVIRONMENT", "development") == "development"
    host = os.environ.get("HOST", "0.0.0.0")

    # Mensagem de inicialização
    print("\n" + "=" * 50)
    print("🚀 DioBank API - Inicializando...")
    print("=" * 50)
    print(f"📦 Ambiente: {os.environ.get('ENVIRONMENT', 'development')}")
    print(f"🌐 Host: {host}")
    print(f"🔌 Porta: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"📚 URL: http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print("=" * 50 + "\n")

    # Iniciar servidor
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
