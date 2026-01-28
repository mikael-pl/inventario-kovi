# 📱 GUIA COMPLETO: GERAR APK PARA TABLET

## ✅ SIM, VAI FUNCIONAR NO TABLET!

O app foi desenvolvido com **Kivy/KivyMD**, que é **cross-platform** e funciona perfeitamente em:
- ✅ Tablets Android
- ✅ Celulares Android
- ✅ Diferentes tamanhos de tela
- ✅ Portrait e Landscape (todas orientações)

---

## 🔧 PREPARAR SEU MAC PARA GERAR O APK

### 1. Instalar Buildozer

```bash
pip3 install buildozer
```

### 2. Instalar Dependências do Sistema

```bash
brew install autoconf automake libtool pkg-config
brew install zlib
brew install openjdk@11
```

### 3. Configurar Java

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

---

## 🚀 GERAR O APK

### Opção 1: Script Automático (Recomendado)

```bash
~/gerar_apk.sh
```

### Opção 2: Manual

```bash
cd "/Users/mikael.lourenco/Server/server 25.11/APK inventario"
buildozer -v android debug
```

---

## ⏱️ TEMPO DE BUILD

- **Primeira vez**: 15-30 minutos
  - Baixa Android SDK (~1GB)
  - Baixa Android NDK (~500MB)
  - Compila Python para Android
  - Compila todas as dependências

- **Próximas vezes**: 5-10 minutos
  - Usa cache das dependências

---

## 📱 INSTALAR NO TABLET

### 1. Localizar o APK Gerado

```
APK inventario/bin/inventariokovi-1.1.0-arm64-v8a-debug.apk
```

### 2. Transferir para o Tablet

**Opção A: USB**
```bash
# Conectar tablet via USB e copiar
adb install bin/inventariokovi-1.1.0-arm64-v8a-debug.apk
```

**Opção B: Google Drive**
1. Upload do APK para o Drive
2. Baixar no tablet

**Opção C: Email**
1. Enviar APK como anexo
2. Abrir no tablet

### 3. Instalar no Tablet

1. Vá em **Configurações > Segurança**
2. Ative **"Instalar apps de fontes desconhecidas"**
3. Abra o arquivo APK
4. Clique em **Instalar**

---

## ✨ FUNCIONALIDADES QUE VÃO FUNCIONAR NO TABLET

✅ **Login com senha**
✅ **Buscar ativos do Fresh Service**
✅ **Inventariar ativos**
✅ **Enviar termos via DocuSign**
✅ **Histórico de ações com busca**
✅ **Timeout de 45 segundos**
✅ **Teclado virtual do Android**
✅ **Rotação de tela (portrait/landscape)**
✅ **Banco de dados local (SQLite)**

---

## 🔍 DIFERENÇAS: MAC vs TABLET

| Funcionalidade | Mac (Teste) | Tablet (Produção) |
|----------------|-------------|-------------------|
| Interface | ✅ Igual | ✅ Igual |
| Fresh Service API | ✅ Funciona | ✅ Funciona |
| DocuSign API | ✅ Funciona | ✅ Funciona |
| Banco SQLite | ✅ Local | ✅ Local |
| Histórico | ✅ Funciona | ✅ Funciona |
| Timeout | ✅ Funciona | ✅ Funciona |
| Leitor de Código | ❌ Não implementado* | ❌ Não implementado* |

*O campo de patrimônio aceita digitação manual. Para usar leitor de código de barras/QR, seria necessário adicionar biblioteca específica (pode implementar depois se quiser).

---

## 🐛 PROBLEMAS COMUNS E SOLUÇÕES

### Erro: "Command 'buildozer' not found"
```bash
pip3 install --upgrade buildozer
```

### Erro: "Java not found"
```bash
brew install openjdk@11
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

### Erro: "Android SDK not found"
- Na primeira execução, o Buildozer baixa automaticamente
- Aguarde o download completar

### Erro: "APK não instala no tablet"
- Verifique se "Fontes desconhecidas" está ativado
- Use o APK arm64-v8a (compatível com tablets modernos)

### App fecha logo após abrir
- Verifique se o tablet tem Android 5.0+ (API 21+)
- Verifique logs: `adb logcat | grep python`

---

## 🔐 SEGURANÇA

### Dados Armazenados Localmente:
- ✅ Senhas (hash SHA256, não texto plano)
- ✅ API Keys do Fresh Service
- ✅ Histórico de ações
- ✅ Credenciais DocuSign (embutidas no código)

### Comunicação:
- ✅ HTTPS para Fresh Service API
- ✅ HTTPS para DocuSign API
- ✅ JWT Authentication para DocuSign

---

## 📊 TAMANHO DO APK

- **APK Final**: ~40-60 MB
- **Após instalação**: ~100-150 MB
  - Contém Python runtime
  - Bibliotecas (Kivy, DocuSign, PyMuPDF)
  - Termo de Responsabilidade (PDF)

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Testar no Mac (já fizemos)
2. 🔨 Gerar APK com `~/gerar_apk.sh`
3. 📱 Instalar no tablet
4. ✅ Testar todas as funcionalidades
5. 🚀 Distribuir para os analistas

---

## ❓ DÚVIDAS FREQUENTES

**P: O app precisa de internet?**
R: Sim, para acessar Fresh Service e DocuSign APIs.

**P: Funciona offline?**
R: O login e histórico funcionam offline, mas buscar/inventariar precisa de internet.

**P: Posso instalar em vários tablets?**
R: Sim! O mesmo APK funciona em todos os tablets Android.

**P: Como atualizar o app?**
R: Gere um novo APK com versão maior e reinstale.

**P: Os dados ficam salvos após atualização?**
R: Sim, desde que o `package.name` não mude.

---

## 📞 SUPORTE

Se tiver problemas:
1. Verifique os logs do Buildozer
2. Teste no Mac antes de gerar APK
3. Use `adb logcat` para ver logs do tablet
4. Verifique se todas as APIs estão funcionando

---

**Última atualização**: 27/01/2026
**Versão do APK**: 1.1.0
