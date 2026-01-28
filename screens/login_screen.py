# -*- coding: utf-8 -*-
"""
Tela de Login
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

Builder.load_string('''
<LoginScreen>:
    name: 'login'
    
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.primary_color
        
        # Header
        MDBoxLayout:
            size_hint_y: 0.3
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(10)
            
            Widget:
                size_hint_y: 0.3
            
            MDLabel:
                text: "Inventario Kovi"
                font_style: "H4"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            
            MDLabel:
                text: "Sistema de Controle de Ativos"
                font_style: "Body1"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.8
            
            Widget:
                size_hint_y: 0.3
        
        # Login Form
        MDCard:
            size_hint: 0.9, 0.7
            pos_hint: {"center_x": 0.5}
            elevation: 10
            padding: dp(25)
            spacing: dp(25)
            radius: [25, 25, 0, 0]
            
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                padding: dp(10)
                
                MDLabel:
                    text: "Login"
                    font_style: "H5"
                    halign: "center"
                    size_hint_y: None
                    height: dp(40)
                
                # Dropdown de usuarios
                MDTextField:
                    id: username_field
                    hint_text: "Selecione o usuario"
                    icon_right: "account"
                    mode: "rectangle"
                    readonly: True
                    on_focus: root.show_user_menu(self) if self.focus else None
                
                # Campo de senha
                MDTextField:
                    id: password_field
                    hint_text: "Senha"
                    icon_right: "lock"
                    password: True
                    mode: "rectangle"
                    on_text_validate: root.do_login()
                
                Widget:
                    size_hint_y: None
                    height: dp(10)
                
                # Botao de login
                MDRaisedButton:
                    text: "ENTRAR"
                    size_hint_x: 1
                    pos_hint: {"center_x": 0.5}
                    md_bg_color: app.theme_cls.primary_color
                    on_release: root.do_login()
                
                Widget:
''')

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_menu = None
        self.users = [
            "Mikael",
            "Richard",
            "Sergio",
            "Arthur",
            "Nicolas",
            "Guilherme",
            "Mateus",
            "Gaby"
        ]
    
    def on_enter(self):
        """Executado quando entra na tela"""
        # Limpa os campos (com delay para garantir que widgets estejam prontos)
        from kivy.clock import Clock
        Clock.schedule_once(self._clear_fields, 0.1)
    
    def _clear_fields(self, dt):
        """Limpa os campos de texto"""
        if hasattr(self, 'ids') and 'username_field' in self.ids:
            self.ids.username_field.text = ""
            self.ids.password_field.text = ""
    
    def show_user_menu(self, text_field):
        """Mostra o menu dropdown com os usuarios"""
        menu_items = [
            {
                "text": user,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=user: self.select_user(x),
            } for user in self.users
        ]
        
        self.user_menu = MDDropdownMenu(
            caller=text_field,
            items=menu_items,
            width_mult=4,
        )
        self.user_menu.open()
    
    def select_user(self, username):
        """Seleciona um usuario do dropdown"""
        self.ids.username_field.text = username
        self.user_menu.dismiss()
        # Foca no campo de senha
        self.ids.password_field.focus = True
    
    def do_login(self):
        """Realiza o login"""
        from kivy.app import App
        
        username = self.ids.username_field.text.strip()
        password = self.ids.password_field.text.strip()
        
        if not username:
            self.show_error("Por favor, selecione um usuario")
            return
        
        if not password:
            self.show_error("Por favor, digite a senha")
            return
        
        # Tenta fazer login
        app = App.get_running_app()
        
        # Verifica se e primeiro acesso (senha padrao)
        db = app.db
        is_first_access = db.is_first_access(username)
        
        if is_first_access:
            # Primeiro acesso - define a senha
            if len(password) < 4:
                self.show_error("A senha deve ter pelo menos 4 caracteres")
                return
            
            db.set_password(username, password)
            app.current_user = username
            
            # Carrega a API key se ja estiver pre-configurada
            api_key = db.get_user_api_key(username)
            app.user_api_key = api_key
            
            if api_key:
                # Ja tem API key configurada
                app.show_dialog(
                    "Senha Definida",
                    f"Senha definida com sucesso para {username}!\n\nSua API key ja esta configurada.",
                    self.go_to_inventory
                )
            else:
                # Precisa configurar API key
                app.show_dialog(
                    "Senha Definida",
                    f"Senha definida com sucesso para {username}!\n\nAgora voce precisa configurar sua chave de API do Fresh.",
                    self.go_to_inventory
                )
        else:
            # Login normal
            if app.login(username, password):
                self.go_to_inventory()
            else:
                self.show_error("Senha incorreta")
    
    def show_error(self, message):
        """Mostra mensagem de erro"""
        from kivy.app import App
        app = App.get_running_app()
        app.show_snackbar(message)
    
    def go_to_inventory(self):
        """Vai para a tela de inventario"""
        self.manager.current = 'inventory'
