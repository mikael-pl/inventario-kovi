# 🚀 INÍCIO RÁPIDO

## O que é este projeto?

**App de Inventário Kovi** - Aplicativo Android em Python para controle de ativos usando Fresh Service.

## 📋 Resumo

- **8 usuários**: Mikael, Richard, Sergio, Arthur, Nicolas, Guilherme, Mateus, Gaby
- **Senha no 1º acesso**: Cada um define sua senha
- **API Key individual**: Cada analista tem sua chave do Fresh
- **Busca ativos**: Por número de patrimônio
- **Inventaria**: Atribui ao usuário + status "In Use"
- **Envia termo**: DocuSign automático (para Notebook/HeadSet/Celular)

## 🎯 Para Usar no Tablet

1. **Instale o APK** (quando estiver pronto)
2. **Primeiro acesso:**
   - Selecione seu nome
   - Defina uma senha
   - Configure sua API Key do Fresh
3. **Use:**
   - Digite o patrimônio
   - Digite o email do colaborador
   - Clique em INVENTARIAR ou INVENTARIAR + TERMO

## 💻 Para Desenvolvedores

### Testar Localmente (no computador)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar o app
python test_app.py
```

### Gerar o APK

**Jeito mais fácil: Google Colab**

Veja o arquivo: `COMO_GERAR_APK.md`

## 📁 Estrutura do Projeto

```
APK inventario/
│
├── 📱 main.py                      # App principal
│
├── 🖥️  screens/                     # Telas
│   ├── login_screen.py            # Login com dropdown de usuários
│   └── inventory_screen.py        # Busca e inventário de ativos
│
├── 🔧 utils/                        # Utilitários
│   ├── database.py                # SQLite (usuários/senhas/API keys)
│   └── api_fresh.py               # Fresh Service API
│
├── ⚙️  buildozer.spec               # Config para gerar APK
├── 📦 requirements.txt             # Dependências Python
│
├── 📖 README.md                    # Documentação completa
├── 🚀 COMO_GERAR_APK.md            # Guia para gerar APK
├── ⚡ INICIO_RAPIDO.md             # Este arquivo
│
├── 🧪 test_app.py                  # Testar localmente
└── 🛠️  setup.sh                     # Script de instalação

```

## 🔑 Onde Pegar API Key do Fresh

1. Acesse: https://kovitec.freshservice.com/
2. Clique no seu perfil (canto superior direito)
3. **Profile Settings**
4. **View API Key**
5. Copie e cole no app

## ❓ Perguntas Frequentes

### Como funciona diferente do Android Studio?

- **Android Studio**: Java/Kotlin (complexo)
- **Este app**: Python com Kivy (simples)
- **Vantagem**: Aproveita código Python do servidor!

### Preciso instalar Android Studio?

**NÃO!** Use o Buildozer (compila Python para APK).

### Posso testar sem tablet?

**SIM!** Rode `python test_app.py` no seu computador.

### Quanto tempo demora para gerar o APK?

- Primeira vez: ~20 minutos
- Próximas vezes: ~5 minutos

### O APK funciona em qualquer Android?

Sim! Android 5.0 (API 21) ou superior.

## 🎨 Capturas de Tela

### Tela de Login
- Dropdown com 8 usuários
- Campo de senha
- Primeiro acesso define senha

### Tela de Inventário
- Buscar por patrimônio
- Visualiza: Nome, Tipo, Serial, Status
- Campo de email
- Botões: INVENTARIAR | INVENTARIAR + TERMO

## 📞 Suporte

Veja a documentação completa em `README.md`

---

**Desenvolvido para Kovi** 🚗
