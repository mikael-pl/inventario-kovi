# -*- coding: utf-8 -*-
"""
API do Fresh Service
Funcoes para buscar, inventariar e enviar termos
"""

import requests
import base64
import urllib.parse

# Configuracao do Fresh Service
DOMAIN = "kovitec.freshservice.com"
BASE_URL = f"https://{DOMAIN}/api/v2"

class FreshAPI:
    def __init__(self, api_key):
        """Inicializa a API com a chave do usuario"""
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self._get_auth_header()
        }
    
    def _get_auth_header(self):
        """Retorna o header de autorizacao"""
        auth_string = f"{self.api_key}:X"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        return f"Basic {auth_b64}"
    
    def buscar_ativo_por_patrimonio(self, patrimonio):
        """Busca um ativo pelo patrimonio (asset_tag)"""
        try:
            # Busca direta
            query = f'"asset_tag:\'{patrimonio}\'"'
            url = f"{BASE_URL}/assets?search={query}&include=type_fields"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get('assets') and len(json_data['assets']) > 0:
                    return self._processar_ativo(json_data['assets'][0])
            
            # Se nao encontrou, tenta com zeros a esquerda
            if patrimonio.isdigit():
                patrimonio_com_zeros = patrimonio.zfill(6)
                query = f'"asset_tag:\'{patrimonio_com_zeros}\'"'
                url = f"{BASE_URL}/assets?search={query}&include=type_fields"
                
                response = requests.get(url, headers=self.headers, timeout=30)
                
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data.get('assets') and len(json_data['assets']) > 0:
                        return self._processar_ativo(json_data['assets'][0])
            
            return None
            
        except Exception as e:
            raise Exception(f"Erro na busca: {str(e)}")
    
    def _processar_ativo(self, ativo):
        """Processa os dados do ativo"""
        type_fields = ativo.get('type_fields', {})
        produto_id = type_fields.get("product_22001045183")
        nome_ativo = ativo.get('name', '')
        tag_ativo = ativo.get('asset_tag', '')
        
        # Detecta o tipo
        produto = self._detectar_tipo_por_nome(nome_ativo, tag_ativo)
        
        # Se tem produto_id, tenta buscar o nome
        if produto_id:
            nome_produto = self._buscar_nome_produto(produto_id)
            if nome_produto and nome_produto != "N/A":
                produto = nome_produto
        
        # Regra especifica para KOVIMAC (MacBook)
        if produto == "Desconhecido" and nome_ativo.upper().startswith('KOVIMAC'):
            produto = "Notebook"
        
        # Busca informacoes do usuario atual
        user_id = ativo.get('user_id')
        usuario_atual = None
        if user_id:
            usuario_atual = self._buscar_info_usuario(user_id)
        
        return {
            'display_id': ativo.get('display_id'),
            'nome': nome_ativo,
            'patrimonio': tag_ativo,
            'tipo': produto,
            'serial': type_fields.get("serial_number_22001045183", ""),
            'status_atual': type_fields.get("asset_state_22001045183", "N/A"),
            'user_id': user_id,
            'usuario_atual': usuario_atual
        }
    
    def _mapear_tipo_para_docusign(self, tipo_ativo):
        """Mapeia o tipo do Fresh para o tipo do DocuSign"""
        tipo_lower = tipo_ativo.lower()
        
        # Detecta MacBook
        if 'macbook' in tipo_lower or 'mac' in tipo_lower:
            return 'mac'
        
        # Detecta Notebook Windows
        if any(palavra in tipo_lower for palavra in ['notebook', 'laptop', 'thinkpad', 'lenovo', 'dell', 'hp', 'windows']):
            return 'windows'
        
        # Detecta HeadSet/Fone
        if any(palavra in tipo_lower for palavra in ['headset', 'fone', 'headphone', 'audio']):
            return 'fone'
        
        # Detecta Celular
        if any(palavra in tipo_lower for palavra in ['celular', 'mobile', 'phone', 'iphone', 'samsung']):
            return 'celular'
        
        # Default para notebook windows se nao detectar
        return 'windows'
    
    def _buscar_info_usuario(self, user_id):
        """Busca informacoes do usuario pelo ID"""
        try:
            # Tenta em requesters
            url = f"{BASE_URL}/requesters/{user_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                user = response.json().get('requester', {})
                return {
                    'nome': user.get('first_name', 'N/A'),
                    'email': user.get('primary_email', 'N/A')
                }
            
            # Se nao encontrou, tenta em agents
            url = f"{BASE_URL}/agents/{user_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                user = response.json().get('agent', {})
                return {
                    'nome': user.get('first_name', 'N/A'),
                    'email': user.get('email', 'N/A')
                }
            
            return None
        except:
            return None
    
    def _detectar_tipo_por_nome(self, nome_ativo, tag_ativo=None):
        """Detecta o tipo do ativo pelo nome"""
        if not nome_ativo:
            return "Desconhecido"
        
        nome_upper = nome_ativo.upper()
        tag_upper = (tag_ativo or "").upper()
        
        # Regras especificas
        if nome_upper.startswith('CLINFO') or nome_upper.startswith('CLK'):
            return "Celular"
        
        if nome_upper.startswith('INFOTOUCH'):
            return "Notebook"
        
        if tag_upper.startswith('HSCX') or tag_upper.startswith('HSVD'):
            return "HeadSet"
        
        # Regras genericas
        nome_lower = nome_ativo.lower()
        
        if any(p in nome_lower for p in ['pe', 'lenovo', 'dell', 'hp', 'macbook', 'laptop', 'notebook']):
            return "Notebook"
        elif any(p in nome_lower for p in ['headset', 'fone', 'headphone', 'audio']):
            return "HeadSet"
        elif any(p in nome_lower for p in ['celular', 'mobile', 'phone', 'iphone', 'samsung', 'redmi']):
            return "Celular"
        
        return "Desconhecido"
    
    def _buscar_nome_produto(self, produto_id):
        """Busca o nome do produto pelo ID"""
        try:
            url = f"{BASE_URL}/products/{produto_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                produto = response.json().get('product', {})
                return produto.get('name', 'N/A')
            
            return "N/A"
        except:
            return "N/A"
    
    def buscar_user_id_por_email(self, email):
        """Busca o user_id pelo email"""
        try:
            # Tenta em requesters
            url = f"{BASE_URL}/requesters?email={urllib.parse.quote(email)}"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                dados = response.json()
                if dados.get("requesters") and len(dados["requesters"]) > 0:
                    return dados["requesters"][0]["id"]
            
            # Tenta em agents
            url = f"{BASE_URL}/agents?email={urllib.parse.quote(email)}"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                dados = response.json()
                if dados.get("agents") and len(dados["agents"]) > 0:
                    return dados["agents"][0]["id"]
            
            return None
        except:
            return None
    
    def inventariar_ativo(self, display_id, email, status="In Use"):
        """Inventaria o ativo (atualiza status e atribui ao usuario)"""
        try:
            # Busca o user_id se tiver email
            user_id = None
            if email:
                user_id = self.buscar_user_id_por_email(email)
                if not user_id:
                    return {
                        'sucesso': False,
                        'mensagem': f'Usuario nao encontrado: {email}'
                    }
            
            # Atualiza o ativo
            url = f"{BASE_URL}/assets/{display_id}"
            
            # O Fresh Service precisa do status dentro de type_fields
            payload = {
                "asset": {
                    "type_fields": {
                        "asset_state_22001045183": status
                    }
                }
            }
            
            # Adiciona user_id apenas se tiver
            if user_id:
                payload["asset"]["user_id"] = user_id
            else:
                # Se nao tem user_id, remove o usuario atual
                payload["asset"]["user_id"] = None
            
            response = requests.put(url, json=payload, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                return {
                    'sucesso': True,
                    'mensagem': 'Ativo atualizado com sucesso'
                }
            else:
                # Retorna o erro da API para debug
                error_detail = ""
                try:
                    error_detail = response.json()
                except:
                    pass
                return {
                    'sucesso': False,
                    'mensagem': f'Erro {response.status_code}: {error_detail}'
                }
        
        except Exception as e:
            return {
                'sucesso': False,
                'mensagem': f'Erro: {str(e)}'
            }
    
    def enviar_termo(self, email, tipo_ativo, patrimonio, serial):
        """Envia o termo de responsabilidade via DocuSign"""
        # Verifica se o tipo requer termo (busca por palavras-chave)
        tipo_lower = tipo_ativo.lower()
        
        # Palavras-chave que indicam que precisa de termo
        palavras_notebook = ['notebook', 'laptop', 'macbook', 'thinkpad', 'lenovo', 'dell', 'hp', 'windows', 'mac']
        palavras_headset = ['headset', 'fone', 'headphone', 'audio']
        palavras_celular = ['celular', 'mobile', 'phone', 'iphone', 'samsung']
        
        requer_termo = (
            any(palavra in tipo_lower for palavra in palavras_notebook) or
            any(palavra in tipo_lower for palavra in palavras_headset) or
            any(palavra in tipo_lower for palavra in palavras_celular)
        )
        
        if not requer_termo:
            return {
                'sucesso': False,
                'mensagem': f'Tipo "{tipo_ativo}" nao requer termo'
            }
        
        try:
            # Mapeia o tipo para o formato do DocuSign
            tipo_docusign = self._mapear_tipo_para_docusign(tipo_ativo)
            
            # Importa e usa a funcao de envio
            from utils.docusign_helper import enviar_termo_completo
            
            # Envia o termo
            sucesso = enviar_termo_completo(email, tipo_docusign, patrimonio, serial)
            
            if sucesso:
                return {
                    'sucesso': True,
                    'mensagem': 'Termo enviado com sucesso via DocuSign!'
                }
            else:
                return {
                    'sucesso': False,
                    'mensagem': 'Erro ao enviar termo. Verifique os logs.'
                }
        
        except Exception as e:
            return {
                'sucesso': False,
                'mensagem': f'Erro ao enviar termo: {str(e)}'
            }
