# -*- coding: utf-8 -*-
"""
Tela de Inventario
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
import threading
from utils.api_fresh import FreshAPI

Builder.load_string('''
<InventoryScreen>:
    name: 'inventory'
    
    MDBoxLayout:
        orientation: 'vertical'
        
        # Top Bar
        MDTopAppBar:
            title: "Inventario de Ativos"
            elevation: 10
            left_action_items: [["menu", lambda x: root.show_menu()]]
            right_action_items: [["account", lambda x: root.show_user_info()]]
        
        # Content
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(15)
                padding: dp(20)
                adaptive_height: True
                
                # Card de busca
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(200)
                    padding: dp(20)
                    spacing: dp(15)
                    elevation: 5
                    
                    MDLabel:
                        text: "Buscar Ativo"
                        font_style: "H6"
                        size_hint_y: None
                        height: dp(30)
                    
                    MDTextField:
                        id: patrimonio_field
                        hint_text: "Numero do Patrimonio"
                        icon_right: "barcode-scan"
                        mode: "rectangle"
                        on_text_validate: root.buscar_ativo()
                    
                    MDRaisedButton:
                        text: "BUSCAR ATIVO"
                        size_hint_x: 1
                        md_bg_color: app.theme_cls.primary_color
                        on_release: root.buscar_ativo()
                
                # Card de resultado
                MDCard:
                    id: result_card
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 0
                    opacity: 0
                    padding: dp(20)
                    spacing: dp(10)
                    elevation: 5
                    
                    MDLabel:
                        id: result_title
                        text: "Informacoes do Ativo"
                        font_style: "H6"
                        size_hint_y: None
                        height: dp(30)
                    
                    MDSeparator:
                    
                    MDLabel:
                        id: ativo_nome
                        text: ""
                        size_hint_y: None
                        height: dp(25)
                    
                    MDLabel:
                        id: ativo_patrimonio
                        text: ""
                        size_hint_y: None
                        height: dp(25)
                    
                    MDLabel:
                        id: ativo_tipo
                        text: ""
                        size_hint_y: None
                        height: dp(25)
                    
                    MDLabel:
                        id: ativo_serial
                        text: ""
                        size_hint_y: None
                        height: dp(25)
                    
                    MDLabel:
                        id: ativo_status
                        text: ""
                        size_hint_y: None
                        height: dp(25)
                    
                    MDLabel:
                        id: ativo_usuario_atual
                        text: ""
                        size_hint_y: None
                        height: dp(25)
                        theme_text_color: "Custom"
                        text_color: 0.2, 0.6, 0.8, 1
                    
                    MDSeparator:
                    
                    MDTextField:
                        id: status_field
                        hint_text: "Novo Status"
                        icon_right: "arrow-down-drop-circle"
                        mode: "rectangle"
                        readonly: True
                        on_focus: root.show_status_menu(self) if self.focus else None
                    
                    MDTextField:
                        id: email_field
                        hint_text: "Email do usuario (opcional para alguns status)"
                        icon_right: "email"
                        mode: "rectangle"
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(10)
                        size_hint_y: None
                        height: dp(50)
                        
                        MDRaisedButton:
                            text: "INVENTARIAR"
                            size_hint_x: 0.5
                            md_bg_color: app.theme_cls.primary_color
                            on_release: root.inventariar_ativo()
                        
                        MDRaisedButton:
                            text: "INVENTARIAR + TERMO"
                            size_hint_x: 0.5
                            md_bg_color: 0.2, 0.6, 0.2, 1
                            on_release: root.inventariar_e_enviar_termo()
                
                Widget:
                    size_hint_y: None
                    height: dp(20)
''')

class InventoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_asset = None
        self.api = None
        self.loading_dialog = None
        self.status_menu = None
        self.status_options = [
            "In Use",
            "In Stock",
            "Retired",
            "Missing",
            "Repair",
            "Reserved"
        ]
    
    def on_enter(self):
        """Executado quando entra na tela"""
        from kivy.clock import Clock
        Clock.schedule_once(self._setup_screen, 0.1)
    
    def _setup_screen(self, dt):
        """Configura a tela apos widgets estarem prontos"""
        from kivy.app import App
        app = App.get_running_app()
        
        # Verifica se tem API key configurada
        if not app.user_api_key:
            self.show_api_key_dialog()
        else:
            # Inicializa a API
            self.api = FreshAPI(app.user_api_key)
        
        # Limpa campos
        if hasattr(self, 'ids') and 'patrimonio_field' in self.ids:
            self.ids.patrimonio_field.text = ""
            self.hide_result_card()
    
    def show_menu(self):
        """Mostra menu lateral"""
        from kivymd.uix.list import OneLineListItem
        from kivymd.uix.menu import MDDropdownMenu
        
        menu_items = [
            {
                "text": "Ver Historico",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.ver_historico(),
            },
            {
                "text": "Configurar API Key",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.show_api_key_dialog(),
            },
            {
                "text": "Sair",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.do_logout(),
            },
        ]
        
        MDDropdownMenu(
            caller=self,
            items=menu_items,
            width_mult=4,
        ).open()
    
    def show_user_info(self):
        """Mostra informacoes do usuario"""
        from kivy.app import App
        app = App.get_running_app()
        api_status = "Configurada" if app.user_api_key else "Nao configurada"
        
        app.show_dialog(
            f"Usuario: {app.current_user}",
            f"API Key: {api_status}\n\nClique no menu para configurar."
        )
    
    def show_api_key_dialog(self):
        """Mostra dialog para configurar API Key"""
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(100)
        )
        
        api_field = MDTextField(
            hint_text="Chave de API do Fresh",
            mode="rectangle"
        )
        content.add_widget(api_field)
        
        dialog = MDDialog(
            title="Configurar API Key",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SALVAR",
                    on_release=lambda x: self.save_api_key(api_field.text, dialog)
                ),
            ],
        )
        dialog.open()
    
    def save_api_key(self, api_key, dialog):
        """Salva a API Key"""
        from kivy.app import App
        
        if not api_key:
            app = App.get_running_app()
            app.show_snackbar("Por favor, digite a chave de API")
            return
        
        app = App.get_running_app()
        if app.update_api_key(api_key):
            self.api = FreshAPI(api_key)
            app.show_snackbar("API Key configurada com sucesso!")
            dialog.dismiss()
        else:
            app.show_snackbar("Erro ao salvar API Key")
    
    def do_logout(self):
        """Faz logout"""
        from kivy.app import App
        app = App.get_running_app()
        app.logout()
    
    def ver_historico(self):
        """Abre a tela de historico"""
        self.manager.current = 'history'
    
    def buscar_ativo(self):
        """Busca o ativo pelo patrimonio"""
        from kivy.app import App
        
        patrimonio = self.ids.patrimonio_field.text.strip()
        
        if not patrimonio:
            app = App.get_running_app()
            app.show_snackbar("Digite o numero do patrimonio")
            return
        
        if not self.api:
            app = App.get_running_app()
            app.show_snackbar("Configure sua API Key primeiro")
            self.show_api_key_dialog()
            return
        
        # Mostra loading
        self.show_loading("Buscando ativo...")
        
        # Busca em thread separada
        thread = threading.Thread(target=self._buscar_ativo_thread, args=(patrimonio,))
        thread.start()
    
    def _buscar_ativo_thread(self, patrimonio):
        """Busca o ativo em thread separada"""
        try:
            ativo = self.api.buscar_ativo_por_patrimonio(patrimonio)
            
            # Atualiza UI na thread principal
            Clock.schedule_once(lambda dt: self._on_ativo_found(ativo), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_error(str(e)), 0)
    
    def _on_ativo_found(self, ativo):
        """Callback quando o ativo e encontrado"""
        from kivy.app import App
        
        self.hide_loading()
        
        if ativo:
            self.current_asset = ativo
            self.show_asset_info(ativo)
        else:
            app = App.get_running_app()
            app.show_snackbar("Ativo nao encontrado")
            self.hide_result_card()
    
    def _on_error(self, error_msg):
        """Callback quando ocorre erro"""
        from kivy.app import App
        
        self.hide_loading()
        app = App.get_running_app()
        app.show_snackbar(f"Erro: {error_msg}")
    
    def show_asset_info(self, ativo):
        """Mostra as informacoes do ativo"""
        self.ids.ativo_nome.text = f"Nome: {ativo.get('nome', 'N/A')}"
        self.ids.ativo_patrimonio.text = f"Patrimonio: {ativo.get('patrimonio', 'N/A')}"
        self.ids.ativo_tipo.text = f"Tipo: {ativo.get('tipo', 'N/A')}"
        self.ids.ativo_serial.text = f"Serial: {ativo.get('serial', 'N/A')}"
        self.ids.ativo_status.text = f"Status: {ativo.get('status_atual', 'N/A')}"
        
        # Mostra usuario atual
        usuario_atual = ativo.get('usuario_atual')
        if usuario_atual:
            nome = usuario_atual.get('nome', 'N/A')
            email = usuario_atual.get('email', 'N/A')
            self.ids.ativo_usuario_atual.text = f"Com: {nome} - {email}"
        else:
            self.ids.ativo_usuario_atual.text = "Com: Ninguem (disponivel)"
        
        # Pre-seleciona o status atual
        status_atual = ativo.get('status_atual', 'In Use')
        self.ids.status_field.text = status_atual
        
        # Mostra o card de resultado
        self.show_result_card()
    
    def show_status_menu(self, text_field):
        """Mostra o menu dropdown com os status"""
        from kivymd.uix.menu import MDDropdownMenu
        
        menu_items = [
            {
                "text": status,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=status: self.select_status(x),
            } for status in self.status_options
        ]
        
        self.status_menu = MDDropdownMenu(
            caller=text_field,
            items=menu_items,
            width_mult=4,
        )
        self.status_menu.open()
    
    def select_status(self, status):
        """Seleciona um status do dropdown"""
        self.ids.status_field.text = status
        self.status_menu.dismiss()
    
    def show_result_card(self):
        """Mostra o card de resultado com animacao"""
        from kivy.animation import Animation
        
        card = self.ids.result_card
        card.height = dp(530)
        Animation(opacity=1, duration=0.3).start(card)
    
    def hide_result_card(self):
        """Esconde o card de resultado"""
        card = self.ids.result_card
        card.height = 0
        card.opacity = 0
    
    def inventariar_ativo(self):
        """Inventaria o ativo"""
        self._processar_ativo(enviar_termo=False)
    
    def inventariar_e_enviar_termo(self):
        """Inventaria o ativo e envia o termo"""
        self._processar_ativo(enviar_termo=True)
    
    def _processar_ativo(self, enviar_termo=False):
        """Processa o ativo (inventaria e opcionalmente envia termo)"""
        from kivy.app import App
        
        email = self.ids.email_field.text.strip()
        status = self.ids.status_field.text.strip()
        
        if not status:
            app = App.get_running_app()
            app.show_snackbar("Selecione um status")
            return
        
        # Email e obrigatorio apenas para "In Use"
        if status == "In Use" and (not email or '@' not in email):
            app = App.get_running_app()
            app.show_snackbar("Email e obrigatorio para status 'In Use'")
            return
        
        if not self.current_asset:
            app = App.get_running_app()
            app.show_snackbar("Busque um ativo primeiro")
            return
        
        # Mostra loading
        action = "Inventariando e enviando termo..." if enviar_termo else "Inventariando..."
        self.show_loading(action)
        
        # Processa em thread separada
        thread = threading.Thread(
            target=self._processar_ativo_thread,
            args=(email, enviar_termo)
        )
        thread.start()
    
    def _processar_ativo_thread(self, email, enviar_termo):
        """Processa o ativo em thread separada"""
        from kivy.app import App
        
        try:
            app = App.get_running_app()
            display_id = self.current_asset.get('display_id')
            status = self.ids.status_field.text.strip()
            patrimonio = self.current_asset.get('patrimonio', '')
            
            # Atualiza o ativo com o status selecionado
            resultado_inv = self.api.inventariar_ativo(display_id, email, status)
            
            if not resultado_inv.get('sucesso'):
                Clock.schedule_once(
                    lambda dt: self._on_error(resultado_inv.get('mensagem', 'Erro ao inventariar')),
                    0
                )
                return
            
            # Registra no historico
            detalhes = f"Status: {status}"
            if email:
                detalhes += f" | Usuario: {email}"
            
            app.db.add_history(
                autor=app.current_user,
                patrimonio=patrimonio,
                acao="Inventariado",
                detalhes=detalhes
            )
            
            # Envia termo se solicitado
            if enviar_termo:
                tipo = self.current_asset.get('tipo', '')
                serial = self.current_asset.get('serial', '')
                
                resultado_termo = self.api.enviar_termo(email, tipo, patrimonio, serial)
                
                if resultado_termo.get('sucesso'):
                    # Registra envio do termo no historico
                    app.db.add_history(
                        autor=app.current_user,
                        patrimonio=patrimonio,
                        acao="Termo enviado",
                        detalhes=f"Email: {email}"
                    )
                    
                    Clock.schedule_once(
                        lambda dt: self._on_success("Ativo inventariado e termo enviado com sucesso!"),
                        0
                    )
                else:
                    # Termo nao enviado, mas ativo foi inventariado
                    mensagem_erro = resultado_termo.get('mensagem', 'Erro desconhecido')
                    Clock.schedule_once(
                        lambda dt: self._on_success(
                            f"Ativo inventariado com sucesso!\n\nOBS: Termo nao enviado automaticamente.\nMotivo: {mensagem_erro}\n\nEnvie manualmente se necessario."
                        ),
                        0
                    )
            else:
                Clock.schedule_once(
                    lambda dt: self._on_success("Ativo inventariado com sucesso!"),
                    0
                )
        
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_error(str(e)), 0)
    
    def _on_success(self, message):
        """Callback de sucesso"""
        from kivy.app import App
        
        self.hide_loading()
        app = App.get_running_app()
        app.show_dialog("Sucesso", message)
        
        # Limpa os campos
        self.ids.patrimonio_field.text = ""
        self.ids.email_field.text = ""
        self.ids.status_field.text = ""
        self.hide_result_card()
        self.current_asset = None
    
    def show_loading(self, text="Processando..."):
        """Mostra dialog de loading"""
        if not self.loading_dialog:
            from kivymd.uix.spinner import MDSpinner
            
            content = MDBoxLayout(
                orientation='vertical',
                spacing=dp(20),
                size_hint_y=None,
                height=dp(100)
            )
            
            spinner = MDSpinner(
                size_hint=(None, None),
                size=(dp(46), dp(46)),
                pos_hint={'center_x': .5, 'center_y': .5}
            )
            content.add_widget(spinner)
            
            self.loading_dialog = MDDialog(
                text=text,
                type="custom",
                content_cls=content,
                auto_dismiss=False
            )
        else:
            self.loading_dialog.text = text
        
        self.loading_dialog.open()
    
    def hide_loading(self):
        """Esconde dialog de loading"""
        if self.loading_dialog:
            self.loading_dialog.dismiss()
