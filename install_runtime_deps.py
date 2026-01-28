# -*- coding: utf-8 -*-
"""
Script para instalar dependencias em runtime no Android
"""
import subprocess
import sys

def install_packages():
    """Instala pacotes Python necessarios"""
    packages = ['pyjwt==2.8.0']
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} instalado")
        except:
            print(f"✗ Erro ao instalar {package}")

if __name__ == '__main__':
    install_packages()
