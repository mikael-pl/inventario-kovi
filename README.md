# Invent?rio Kovi - APK Android

Aplicativo de invent?rio para tablets Android.

## ?? Download do APK

O APK ? gerado automaticamente pelo GitHub Actions.

### Como baixar:
1. Acesse a aba **Actions** deste reposit?rio
2. Clique no workflow **Build Android APK** mais recente
3. Baixe o arquivo **inventario-kovi-apk** em Artifacts

## ??? Build Local (Linux/Ubuntu recomendado)

```bash
# Instalar depend?ncias
sudo apt-get install -y python3-pip build-essential git zlib1g-dev \
  libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev \
  libffi-dev wget libbz2-dev libsqlite3-dev

# Instalar Buildozer
pip3 install buildozer cython==0.29.36

# Gerar APK
buildozer android debug
```

## ?? Funcionalidades

- Login com 8 analistas pr?-configurados
- Busca de ativos por patrim?nio
- Inventariar ativos (atualizar status)
- Enviar termo de responsabilidade via DocuSign
- Hist?rico de a??es com busca/filtro
- Timeout de inatividade (45 segundos)

## ?? Credenciais

Analistas: Mikael, Richard, Sergio, Arthur, Nicolas, Guilherme, Mateus, Gaby

Senha definida no primeiro acesso.
