# -*- coding: utf-8 -*-
"""
Helper DocuSign - SOLUÇÃO FINAL
Preenche campos usando DocuSign Tabs (sem PyMuPDF)
"""

import os
import base64
import requests
import jwt
from datetime import datetime, timedelta
from utils.docusign_config import DOCUSIGN_ACCOUNT_ID, DOCUSIGN_INTEGRATION_KEY, DOCUSIGN_USER_ID, DOCUSIGN_PRIVATE_KEY

class DocuSignSender:
    def __init__(self):
        self.access_token = None
        self.base_url = "https://na2.docusign.net/restapi"
        self.account_id = DOCUSIGN_ACCOUNT_ID
        
    def autenticar(self):
        """Autentica usando JWT - PRODUCAO"""
        try:
            print("Autenticando com DocuSign...")
            
            # Converter chave privada para bytes
            private_key_bytes = DOCUSIGN_PRIVATE_KEY.encode('utf-8')
            
            # Criar JWT - PRODUCAO (sem -d)
            now = datetime.utcnow()
            claim = {
                "iss": DOCUSIGN_INTEGRATION_KEY,
                "sub": DOCUSIGN_USER_ID,
                "aud": "account.docusign.com",  # PRODUCAO (SEM -d!)
                "iat": now,
                "exp": now + timedelta(hours=1),
                "scope": "signature impersonation"
            }
            
            # Assinar JWT com chave em bytes
            token = jwt.encode(claim, private_key_bytes, algorithm='RS256')
            
            # Trocar por access token - PRODUCAO
            url = "https://account.docusign.com/oauth/token"  # PRODUCAO (SEM -d!)
            data = {
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": token
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                self.access_token = response.json()['access_token']
                print("Autenticado!")
                return True
            else:
                print(f"Erro: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Erro na autenticacao: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def criar_tabs_preenchidas(self, dados):
        """Cria tabs do DocuSign com dados PRE-PREENCHIDOS nas posições CORRETAS"""
        tabs = {
            "signHereTabs": [
                {
                    "documentId": "1",
                    "pageNumber": "2",
                    "xPosition": "100",
                    "yPosition": "650"
                }
            ],
            "textTabs": []
        }
        
        # Posições REAIS detectadas no PDF
        campos_posicoes = {
            'Nome': {'page': 1, 'x': 79, 'y': 158, 'width': 200, 'height': 12},
            'Email': {'page': 1, 'x': 93, 'y': 227, 'width': 250, 'height': 11},
            'patrimonionotebook': {'page': 2, 'x': 260, 'y': 286, 'width': 112, 'height': 11},
            'serialnotebook': {'page': 2, 'x': 260, 'y': 320, 'width': 150, 'height': 11},  # Logo abaixo do patrimonio
            'modelomaquina': {'page': 2, 'x': 433, 'y': 286, 'width': 150, 'height': 11},
            'Data': {'page': 1, 'x': 93, 'y': 400, 'width': 100, 'height': 11},
        }
        
        # Criar tab para cada campo
        for campo, valor in dados.items():
            if campo in campos_posicoes and valor:
                pos = campos_posicoes[campo]
                tabs['textTabs'].append({
                    "documentId": "1",
                    "pageNumber": str(pos['page']),
                    "xPosition": str(pos['x']),
                    "yPosition": str(pos['y']),
                    "width": str(pos['width']),
                    "height": str(pos['height']),
                    "value": str(valor),
                    "locked": "true",
                    "required": "false",
                    "bold": "false",
                    "fontSize": "Size10",
                    "font": "Arial",
                    "tabLabel": campo
                })
        
        print(f"Criadas {len(tabs['textTabs'])} tabs com dados preenchidos")
        return tabs
    
    def enviar_envelope(self, email_destinatario, nome_destinatario, pdf_base64, dados):
        """Envia envelope com TABS PRE-PREENCHIDAS"""
        try:
            print("Criando envelope com dados preenchidos...")
            
            # Criar tabs com dados
            tabs = self.criar_tabs_preenchidas(dados)
            
            # Mostrar o que será preenchido
            print("\nDADOS QUE SERAO PREENCHIDOS NO PDF:")
            for campo, valor in dados.items():
                print(f"  {campo}: {valor}")
            
            # Payload do envelope
            envelope_data = {
                "emailSubject": "Termo de Responsabilidade - Kovi",
                "emailBlurb": "Por favor, revise e assine este termo de responsabilidade.",
                "status": "sent",
                "documents": [
                    {
                        "documentBase64": pdf_base64,
                        "name": "Termo de Responsabilidade",
                        "fileExtension": "pdf",
                        "documentId": "1"
                    }
                ],
                "recipients": {
                    "signers": [
                        {
                            "email": email_destinatario,
                            "name": nome_destinatario,
                            "recipientId": "1",
                            "routingOrder": "1",
                            "tabs": tabs
                        }
                    ]
                }
            }
            
            # Enviar
            url = f"{self.base_url}/v2.1/accounts/{self.account_id}/envelopes"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            print("\nEnviando envelope para DocuSign...")
            response = requests.post(url, json=envelope_data, headers=headers)
            
            if response.status_code in [200, 201]:
                result = response.json()
                envelope_id = result.get('envelopeId')
                print(f"\n✅ TERMO ENVIADO COM SUCESSO!")
                print(f"📧 Email: {email_destinatario}")
                print(f"📋 Envelope ID: {envelope_id}")
                print(f"✨ PDF foi preenchido com todos os dados!")
                return envelope_id
            else:
                print(f"❌ Erro: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"Erro: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def enviar_termo(self, email_destinatario, nome_destinatario, pdf_path, dados):
        """Envia termo com dados preenchidos"""
        try:
            # Ler PDF original
            print(f"Lendo PDF: {pdf_path}")
            with open(pdf_path, 'rb') as file:
                pdf_bytes = file.read()
            
            pdf_base64 = base64.b64encode(pdf_bytes).decode('ascii')
            print(f"PDF convertido: {len(pdf_bytes)} bytes")
            
            # Enviar com tabs preenchidas
            return self.enviar_envelope(email_destinatario, nome_destinatario, pdf_base64, dados)
            
        except Exception as e:
            print(f"Erro: {e}")
            return False


def enviar_termo_completo(email, tipo_ativo, patrimonio="", serial=""):
    """Envia termo completo via DocuSign com TABS preenchidas"""
    try:
        print(f"\n{'='*50}")
        print(f"ENVIANDO TERMO VIA DOCUSIGN")
        print(f"{'='*50}")
        print(f"📧 Email: {email}")
        print(f"📦 Tipo: {tipo_ativo}")
        print(f"🏷️  Patrimonio: {patrimonio}")
        print(f"🔢 Serial: {serial}")
        print(f"{'='*50}\n")
        
        # Extrair nome
        nome = email.split('@')[0].replace('.', ' ').title()
        
        # PDF LIMPO (sem {{}})
        pdf_original = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'assets',
            'Termo_Limpo.pdf'  # PDF sem placeholders
        )
        
        if not os.path.exists(pdf_original):
            print(f"❌ PDF nao encontrado: {pdf_original}")
            return False
        
        # Criar sender
        sender = DocuSignSender()
        
        # Autenticar
        if not sender.autenticar():
            return False
        
        # Dados para preencher
        dados = {
            'Nome': nome,
            'Email': email,
            'patrimonionotebook': patrimonio,
            'serialnotebook': serial,
            'modelomaquina': tipo_ativo,
            'Data': datetime.now().strftime('%d/%m/%Y')
        }
        
        # Enviar
        sucesso = sender.enviar_termo(email, nome, pdf_original, dados)
        
        if sucesso:
            print(f"\n{'='*50}")
            print("✅ SUCESSO! TERMO ENVIADO E PREENCHIDO!")
            print(f"{'='*50}\n")
            return True
        else:
            print(f"\n{'='*50}")
            print("❌ ERRO ao enviar termo")
            print(f"{'='*50}\n")
            return False
            
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False
