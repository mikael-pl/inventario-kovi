#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App de Inventario - Kovi
Aplicativo Android para controle de inventario de ativos
"""

# Adicionar libs ao path (para pyjwt empacotado)
import sys
import os
libs_path = os.path.join(os.path.dirname(__file__), 'libs')
if os.path.exists(libs_path) and libs_path not in sys.path:
    sys.path.insert(0, libs_path)

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from screens.login_screen import LoginScreen
from screens.inventory_screen import InventoryScreen
from screens.history_screen import HistoryScreen
from utils.database import Database

# KV String para o layout
KV = '''
ScreenManager:
    LoginScreen:
        name: 'login'
    InventoryScreen:
        name: 'inventory'
    HistoryScreen:
        name: 'history'
'''

class InventarioApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.current_user = None
        self.user_api_key = None
        self.dialog = None
        self.inactivity_timer = None
        self.inactivity_timeout = 45  # segundos
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
        
        # Carrega o layout
        root = Builder.load_string(KV)
        
        # Adiciona listener de toque para resetar timer
        from kivy.core.window import Window
        Window.bind(on_touch_down=self.reset_inactivity_timer)
        Window.bind(on_key_down=self.reset_inactivity_timer)
        
        return root
    
    def on_start(self):
        """Executado quando o app inicia"""
        # Inicializa o banco de dados com os usuarios
        self.db.initialize_users()
    
    def show_dialog(self, title, text, close_callback=None):
        """Mostra um dialog de alerta"""
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.close_dialog(close_callback)
                    )
                ]
            )
        else:
            self.dialog.title = title
            self.dialog.text = text
        self.dialog.open()
    
    def close_dialog(self, callback=None):
        """Fecha o dialog"""
        if self.dialog:
            self.dialog.dismiss()
        if callback:
            callback()
    
    def show_snackbar(self, text):
        """Mostra uma snackbar (mensagem rapida na parte inferior)"""
        from kivymd.uix.snackbar import MDSnackbar
        from kivymd.uix.label import MDLabel
        
        snackbar = MDSnackbar(
            MDLabel(
                text=text,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
            ),
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5}
        )
        snackbar.open()
    
    def login(self, username, password):
        """Realiza o login do usuario"""
        result = self.db.verify_user(username, password)
        
        if result['success']:
            self.current_user = username
            self.user_api_key = result['api_key']
            
            # Inicia o timer de inatividade
            self.start_inactivity_timer()
            
            return True
        return False
    
    def logout(self):
        """Faz logout do usuario"""
        # Cancela o timer de inatividade
        self.stop_inactivity_timer()
        
        self.current_user = None
        self.user_api_key = None
        self.root.current = 'login'
    
    def start_inactivity_timer(self):
        """Inicia o timer de inatividade"""
        from kivy.clock import Clock
        
        # Cancela timer anterior se existir
        self.stop_inactivity_timer()
        
        # Cria novo timer
        self.inactivity_timer = Clock.schedule_once(
            self.on_inactivity_timeout, 
            self.inactivity_timeout
        )
    
    def stop_inactivity_timer(self):
        """Para o timer de inatividade"""
        from kivy.clock import Clock
        
        if self.inactivity_timer:
            Clock.unschedule(self.inactivity_timer)
            self.inactivity_timer = None
    
    def reset_inactivity_timer(self, *args):
        """Reseta o timer de inatividade ao detectar interacao"""
        # So reseta se estiver logado e nao estiver na tela de login
        if self.current_user and self.root and self.root.current != 'login':
            self.start_inactivity_timer()
    
    def on_inactivity_timeout(self, dt):
        """Chamado quando o tempo de inatividade expira"""
        if self.current_user:
            self.show_snackbar("Sessao expirada por inatividade")
            self.logout()
    
    def update_api_key(self, api_key):
        """Atualiza a chave API do usuario"""
        if self.current_user:
            self.db.update_api_key(self.current_user, api_key)
            self.user_api_key = api_key
            return True
        return False

if __name__ == '__main__':
    InventarioApp().run()
