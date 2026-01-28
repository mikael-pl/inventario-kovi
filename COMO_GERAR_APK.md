# 🚀 GUIA RÁPIDO - Como Gerar o APK

## Jeito Mais Fácil (Recomendado)

### ☁️ Opção 1: Google Colab (Online, Grátis)

**Vantagens:**
- ✅ Não precisa instalar nada no seu computador
- ✅ Funciona no Windows, Mac, Linux
- ✅ Grátis
- ✅ Rápido (15-20 minutos)

**Passo a passo:**

1. **Compactar o projeto**
   - Compacte a pasta `APK inventario` em um arquivo `.zip`
   - Ou suba para um repositório GitHub

2. **Abrir Google Colab**
   - Acesse: https://colab.research.google.com
   - Faça login com sua conta Google
   - Clique em **+ New Notebook**

3. **Cole e execute este código** (célula por célula):

```python
# Célula 1: Instalar ferramentas
!apt-get update
!apt-get install -y zip unzip
!pip install buildozer cython==0.29.33

# Célula 2: Fazer upload do projeto
from google.colab import files
uploaded = files.upload()  # Selecione seu arquivo .zip

# Célula 3: Descompactar
!unzip -q "*.zip"
%cd "APK inventario"

# Célula 4: Instalar dependências Android
!buildozer android debug

# Célula 5: Baixar o APK gerado
from google.colab import files
import glob
apk_files = glob.glob('bin/*.apk')
if apk_files:
    files.download(apk_files[0])
    print(f"✅ APK pronto: {apk_files[0]}")
else:
    print("❌ Nenhum APK foi gerado")
```

4. **Aguarde**
   - Primeira compilação demora ~20 minutos
   - O APK será baixado automaticamente quando pronto

---

## Outras Opções

### 💻 Opção 2: Linux/Mac Local

```bash
# Instalar Buildozer
pip3 install buildozer

# Instalar dependências (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3 python3-pip git zip unzip \
    openjdk-11-jdk wget libssl-dev autoconf libtool \
    build-essential ccache git libncurses5:i386 libstdc++6:i386 \
    libgtk2.0-0:i386 libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 \
    libidn11:i386 python3.8 python3-pip openjdk-8-jdk unzip zlib1g-dev \
    libltdl-dev libffi-dev libssl-dev autoconf automake

# Gerar APK
cd "APK inventario"
buildozer android debug
```

### 🪟 Opção 3: Windows (WSL2)

```bash
# 1. Instalar WSL2
# No PowerShell como Administrador:
wsl --install

# 2. Reiniciar o computador

# 3. Abrir Ubuntu (procure "Ubuntu" no menu Iniciar)

# 4. Seguir os passos da Opção 2 (Linux)
```

### 🤖 Opção 4: Android Studio (Modo Tradicional)

Se você quiser usar Android Studio:

1. Reescrever o app em Java/Kotlin (mais trabalhoso)
2. Ou usar o Chaquopy para rodar Python no Android Studio

**Não recomendado** - Kivy/Buildozer é muito mais simples para apps Python!

---

## 📦 Resultado

Você terá um arquivo `.apk` do tipo:
```
inventariokovi-1.0.0-arm64-v8a-debug.apk
```

## 📱 Instalar no Tablet

1. **Transferir o APK**
   - Via USB, email, Google Drive, ou AirDrop

2. **Configurar o Android**
   - Vá em **Configurações**
   - **Segurança** ou **Privacidade**
   - Habilite **Fontes Desconhecidas** ou **Instalar apps desconhecidos**

3. **Instalar**
   - Abra o arquivo `.apk` no tablet
   - Clique em **Instalar**
   - Clique em **Abrir**

## ⚠️ Troubleshooting

### Erro: "Command failed: ./distribute.sh"
- Limpe o cache: `buildozer android clean`
- Tente novamente: `buildozer android debug`

### Erro: "No such file or directory: 'buildozer'"
- Instale: `pip3 install --upgrade buildozer`

### Erro: "NDK not found"
- O Buildozer baixa automaticamente
- Se falhar, edite `buildozer.spec` e comente a linha `android.ndk`

### Erro: "Out of memory"
- Use Google Colab (tem mais RAM)
- Ou feche outros programas

## 🎯 Dica Pro

Para gerar um APK **release** (para produção):

```bash
# Gerar keystore (primeira vez)
keytool -genkey -v -keystore inventario.keystore -alias inventario \
    -keyalg RSA -keysize 2048 -validity 10000

# Gerar APK release
buildozer android release

# Assinar o APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
    -keystore inventario.keystore \
    bin/inventariokovi-1.0.0-arm64-v8a-release-unsigned.apk inventario
```

---

## ❓ Precisa de Ajuda?

1. Verifique o arquivo `README.md` completo
2. Consulte a documentação do Kivy: https://kivy.org
3. Consulte a documentação do Buildozer: https://buildozer.readthedocs.io

---

**💡 Recomendação:** Use a **Opção 1 (Google Colab)** - é de longe a mais fácil!
