# -*- coding: utf-8 -*-
"""
Tela de Historico
Mostra todas as acoes realizadas no sistema
"""

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App

# KV Layout
Builder.load_string('''
<HistoryScreen>:
    name: 'history'
    
    MDBoxLayout:
        orientation: 'vertical'
        
        # Toolbar
        MDTopAppBar:
            title: "Historico de Acoes"
            left_action_items: [["arrow-left", lambda x: root.voltar()]]
            elevation: 2
        
        # Campo de busca
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(70)
            padding: dp(10)
            spacing: dp(10)
            
            MDTextField:
                id: search_field
                hint_text: "Buscar por autor, patrimonio ou acao..."
                icon_right: "magnify"
                mode: "rectangle"
                on_text: root.filtrar_historico(self.text)
            
            MDIconButton:
                icon: "refresh"
                on_release: root.atualizar_historico()
                pos_hint: {"center_y": 0.5}
        
        MDSeparator:
        
        # Lista de historico
        ScrollView:
            MDBoxLayout:
                id: history_list
                orientation: 'vertical'
                spacing: "10dp"
                padding: "10dp"
                adaptive_height: True
''')

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.historico_completo = []
    
    def on_enter(self):
        """Carrega o historico ao entrar na tela"""
        Clock.schedule_once(self._carregar_historico, 0.1)
    
    def _carregar_historico(self, dt):
        """Carrega os registros do historico"""
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivy.metrics import dp
        
        app = App.get_running_app()
        history_list = self.ids.history_list
        history_list.clear_widgets()
        
        # Limpa campo de busca
        if hasattr(self, 'ids') and 'search_field' in self.ids:
            self.ids.search_field.text = ""
        
        # Buscar historico do banco
        self.historico_completo = app.db.get_history(limit=100)
        
        if not self.historico_completo:
            # Mensagem vazia
            label = MDLabel(
                text="Nenhuma acao registrada ainda",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(50)
            )
            history_list.add_widget(label)
            return
        
        # Mostrar todos os registros
        self._mostrar_registros(self.historico_completo)
    
    def _mostrar_registros(self, registros):
        """Mostra os registros na tela"""
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivy.metrics import dp
        
        history_list = self.ids.history_list
        history_list.clear_widgets()
        
        if not registros:
            # Mensagem vazia
            label = MDLabel(
                text="Nenhum resultado encontrado",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(50)
            )
            history_list.add_widget(label)
            return
        
        # Criar cards para cada registro
        for registro in registros:
            autor, patrimonio, acao, detalhes, data = registro
            
            # Formatar data
            data_formatada = self._formatar_data(data)
            
            # Card do registro
            card = MDCard(
                orientation='vertical',
                size_hint_y=None,
                height=dp(120),
                padding=dp(15),
                radius=[10],
                elevation=2
            )
            
            # Autor e data
            header = MDLabel(
                text=f"[b]{autor}[/b] - {data_formatada}",
                markup=True,
                font_style="Body1",
                size_hint_y=None,
                height=dp(20)
            )
            card.add_widget(header)
            
            # Patrimonio
            patrimonio_label = MDLabel(
                text=f"Patrimonio: [b]{patrimonio}[/b]",
                markup=True,
                font_style="Body2",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(20)
            )
            card.add_widget(patrimonio_label)
            
            # Acao
            acao_label = MDLabel(
                text=f"Acao: {acao}",
                font_style="Body2",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(20)
            )
            card.add_widget(acao_label)
            
            # Detalhes (se houver)
            if detalhes:
                detalhes_label = MDLabel(
                    text=f"{detalhes}",
                    font_style="Caption",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=dp(20)
                )
                card.add_widget(detalhes_label)
            
            history_list.add_widget(card)
    
    def _formatar_data(self, data_str):
        """Formata a data para exibicao"""
        try:
            from datetime import datetime
            
            # Converter string para datetime
            dt = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
            
            # Formatar para brasileiro
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return data_str
    
    def filtrar_historico(self, texto_busca):
        """Filtra o historico com base no texto de busca"""
        if not texto_busca:
            # Sem filtro, mostra tudo
            self._mostrar_registros(self.historico_completo)
            return
        
        # Filtrar por autor, patrimonio ou acao (case-insensitive)
        texto_lower = texto_busca.lower()
        registros_filtrados = [
            reg for reg in self.historico_completo
            if (texto_lower in reg[0].lower() or  # autor
                texto_lower in reg[1].lower() or  # patrimonio
                texto_lower in reg[2].lower())    # acao
        ]
        
        self._mostrar_registros(registros_filtrados)
    
    def atualizar_historico(self):
        """Atualiza o historico (recarrega do banco)"""
        self._carregar_historico(0)
    
    def voltar(self):
        """Volta para a tela de inventario"""
        self.manager.current = 'inventory'
