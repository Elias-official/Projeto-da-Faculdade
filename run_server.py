#!/usr/bin/env python
"""
EntryPoint para rodar o servidor Flask da aplicação de inventário.

Uso:
    python run_server.py          # Roda em modo desenvolvimento
    python run_server.py --host 0.0.0.0  # Roda em todas as interfaces
"""
import sys
import os

# Adiciona a raiz do projeto ao path (apenas uma vez, no entry point)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.app import create_app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '127.0.0.1')
    app.run(host=host, port=port, debug=True)
