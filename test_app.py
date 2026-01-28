#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste - Roda o app localmente no computador
Útil para testar antes de gerar o APK
"""

import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

# Importa e roda o app
from main import InventarioApp

if __name__ == '__main__':
    print("="*60)
    print("MODO DE TESTE - Rodando app localmente")
    print("="*60)
    print()
    print("Dicas:")
    print("- Use o mouse para navegar")
    print("- Pressione ESC para sair")
    print("- Pressione F1 para inspector (debug)")
    print()
    print("="*60)
    print()
    
    try:
        InventarioApp().run()
    except KeyboardInterrupt:
        print("\n\nApp fechado pelo usuário.")
    except Exception as e:
        print(f"\n\nErro ao executar app: {e}")
        import traceback
        traceback.print_exc()
