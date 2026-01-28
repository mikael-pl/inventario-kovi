# -*- coding: utf-8 -*-
"""
Gerenciamento de banco de dados local (SQLite)
Armazena usuarios, senhas e chaves de API
"""

import sqlite3
import hashlib
import os

class Database:
    def __init__(self, db_path='inventario.db'):
        """Inicializa o banco de dados"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Cria as tabelas se nao existirem"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                api_key TEXT,
                first_access INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de historico
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autor TEXT NOT NULL,
                patrimonio TEXT NOT NULL,
                acao TEXT NOT NULL,
                detalhes TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def initialize_users(self):
        """Inicializa os usuarios do sistema se nao existirem"""
        # Usuarios com suas API keys padrao (se tiverem)
        users_config = {
            "Mikael": "9hc8kzd8dg2goabyOGCD",  # API key do Mikael
            "Richard": None,
            "Sergio": None,
            "Arthur": None,
            "Nicolas": None,
            "Guilherme": None,
            "Mateus": None,
            "Gaby": None
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for username, api_key in users_config.items():
            # Verifica se o usuario ja existe
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if not cursor.fetchone():
                # Insere o usuario sem senha (primeiro acesso)
                cursor.execute(
                    'INSERT INTO users (username, first_access, api_key) VALUES (?, 1, ?)',
                    (username, api_key)
                )
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Gera hash SHA256 da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def is_first_access(self, username):
        """Verifica se e o primeiro acesso do usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT first_access FROM users WHERE username = ?',
            (username,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0] == 1
        return False
    
    def set_password(self, username, password):
        """Define a senha do usuario no primeiro acesso"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute(
            'UPDATE users SET password_hash = ?, first_access = 0 WHERE username = ?',
            (password_hash, username)
        )
        
        conn.commit()
        conn.close()
    
    def verify_user(self, username, password):
        """Verifica as credenciais do usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute(
            'SELECT api_key FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'success': True,
                'api_key': result[0]
            }
        
        return {'success': False}
    
    def update_api_key(self, username, api_key):
        """Atualiza a chave de API do usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE users SET api_key = ? WHERE username = ?',
            (api_key, username)
        )
        
        conn.commit()
        conn.close()
    
    def get_user_api_key(self, username):
        """Retorna a chave de API do usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT api_key FROM users WHERE username = ?',
            (username,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None
    
    def add_history(self, autor, patrimonio, acao, detalhes=''):
        """Adiciona um registro no historico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO history (autor, patrimonio, acao, detalhes) VALUES (?, ?, ?, ?)',
            (autor, patrimonio, acao, detalhes)
        )
        
        conn.commit()
        conn.close()
    
    def get_history(self, limit=100):
        """Retorna o historico de acoes (mais recentes primeiro)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT autor, patrimonio, acao, detalhes, data FROM history ORDER BY data DESC LIMIT ?',
            (limit,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return results
