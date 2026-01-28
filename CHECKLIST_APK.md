# ✅ CHECKLIST FINAL - ANTES DE GERAR O APK

## 📋 Verificações Importantes

### 1. Credenciais Corretas
- [ ] API Key do Fresh Service está correta em `utils/fresh_config.py`
- [ ] Credenciais DocuSign estão corretas em `utils/docusign_config.py`
- [ ] PDF do termo está em `assets/Termo de Responsabilidade (11).pdf`

### 2. Testes no Mac
- [ ] Login funciona para todos os usuários
- [ ] Busca de ativos funciona
- [ ] Inventariar funciona (muda status)
- [ ] Enviar termo funciona (termo chega preenchido)
- [ ] Histórico salva as ações
- [ ] Busca no histórico funciona
- [ ] Timeout de 45s funciona (testado?)

### 3. Configurações
- [ ] Lista de usuários está completa (8 analistas)
- [ ] Opções de status estão corretas
- [ ] Timeout de 45 segundos está ok (ajustar se necessário)

### 4. Build
- [ ] Buildozer instalado
- [ ] Dependências do sistema instaladas
- [ ] Java configurado

---

## 🚀 COMANDOS PARA GERAR APK

### Instalar Buildozer (se ainda não instalou)
```bash
pip3 install buildozer
brew install autoconf automake libtool pkg-config zlib openjdk@11
```

### Gerar APK
```bash
~/gerar_apk.sh
```

OU manualmente:

```bash
cd "/Users/mikael.lourenco/Server/server 25.11/APK inventario"
buildozer -v android debug
```

---

## 📱 INSTALAR NO TABLET

### Via ADB (USB)
```bash
adb install "bin/inventariokovi-1.1.0-arm64-v8a-debug.apk"
```

### Manual
1. Copie o APK para o tablet (USB/Drive/Email)
2. Ative "Fontes desconhecidas" nas configurações
3. Abra o APK e instale

---

## 🧪 TESTES NO TABLET

Após instalar, teste:

1. **Login**
   - [ ] Mikael consegue logar com sua senha
   - [ ] API key já está configurada para Mikael
   - [ ] Outros usuários definem senha no primeiro acesso

2. **Buscar Ativo**
   - [ ] Busca por patrimônio funciona
   - [ ] Mostra informações corretas
   - [ ] Mostra usuário atual do ativo

3. **Inventariar**
   - [ ] Consegue mudar status
   - [ ] Email é obrigatório para "In Use"
   - [ ] Atualiza no Fresh Service

4. **Enviar Termo**
   - [ ] Termo é enviado via DocuSign
   - [ ] Termo chega preenchido (nome, email, patrimônio, etc.)
   - [ ] Email de assinatura chega ao destinatário

5. **Histórico**
   - [ ] Ações são salvas
   - [ ] Busca funciona
   - [ ] Mostra autor, patrimônio, ação e data

6. **Timeout**
   - [ ] Após 45s sem tocar, faz logout
   - [ ] Mostra mensagem de sessão expirada

7. **Rotação de Tela**
   - [ ] Interface se adapta ao girar o tablet
   - [ ] Landscape e Portrait funcionam

---

## 🔧 AJUSTES FINAIS DISPONÍVEIS

Se precisar mudar algo antes de gerar o APK:

### Mudar tempo de timeout
```python
# main.py, linha 37
self.inactivity_timeout = 45  # segundos
```

### Adicionar/remover usuários
```python
# utils/database.py, linhas 40-48
users_config = {
    "Mikael": "9hc8kzd8dg2goabyOGCD",
    "Richard": None,
    # ...
}
```

### Mudar opções de status
```python
# screens/inventory_screen.py, linhas 171-178
self.status_options = [
    "In Use",
    "In Stock",
    "Retired",
    "Missing",
    "Repair",
    "Reserved"
]
```

---

## 📊 ARQUIVOS IMPORTANTES

```
APK inventario/
├── main.py                    # App principal (timeout)
├── test_app.py                # Para testar no Mac
├── buildozer.spec             # Configuração do APK
├── requirements.txt           # Dependências Python
│
├── screens/
│   ├── login_screen.py        # Tela de login
│   ├── inventory_screen.py    # Tela principal
│   └── history_screen.py      # Tela de histórico
│
├── utils/
│   ├── database.py            # SQLite (usuários, histórico)
│   ├── api_fresh.py           # Fresh Service API
│   ├── fresh_config.py        # Credenciais Fresh
│   ├── docusign_helper.py     # DocuSign API
│   └── docusign_config.py     # Credenciais DocuSign
│
└── assets/
    └── Termo de Responsabilidade (11).pdf
```

---

## ⚠️ ATENÇÃO

1. **Não commitar credenciais no Git!**
   - API Keys
   - Private Keys
   - Passwords

2. **APK de Debug vs Release**
   - O script gera APK de debug (para testes)
   - Para produção, use `buildozer android release`
   - APK release precisa ser assinado

3. **Backup do banco de dados**
   - No tablet: `/data/data/com.kovi.inventariokovi/files/inventario.db`
   - Fazer backup periodicamente se necessário

---

## 📞 TROUBLESHOOTING

### Buildozer falha
```bash
# Limpar e tentar novamente
buildozer android clean
rm -rf .buildozer/
buildozer -v android debug
```

### APK não instala
- Verificar se Android é 5.0+ (API 21+)
- Ativar "Fontes desconhecidas"
- Baixar APK correto (arm64-v8a para tablets modernos)

### App fecha ao abrir
```bash
# Ver logs
adb logcat | grep -i python
```

### APIs não funcionam no tablet
- Verificar conexão com internet
- Verificar se credenciais estão corretas
- Testar APIs manualmente (Postman)

---

**Pronto para gerar o APK?** 🚀

Execute: `~/gerar_apk.sh`
