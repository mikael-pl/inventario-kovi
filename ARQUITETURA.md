# 🏗️ Arquitetura do App - Inventário Kovi

## 📊 Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│                     TABLET ANDROID                           │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │          App Inventário (Python/Kivy)              │     │
│  │                                                     │     │
│  │  ┌──────────────┐        ┌──────────────┐         │     │
│  │  │ Tela Login   │───────▶│ Tela         │         │     │
│  │  │              │        │ Inventário   │         │     │
│  │  └──────────────┘        └──────────────┘         │     │
│  │         │                        │                 │     │
│  │         │                        │                 │     │
│  │         ▼                        ▼                 │     │
│  │  ┌──────────────┐        ┌──────────────┐         │     │
│  │  │  Database    │        │  Fresh API   │         │     │
│  │  │  (SQLite)    │        │              │         │     │
│  │  └──────────────┘        └──────────────┘         │     │
│  │         │                        │                 │     │
│  └─────────┼────────────────────────┼─────────────────┘     │
│            │                        │                       │
│            ▼                        ▼                       │
│     inventario.db           Internet (HTTPS)               │
│                                     │                       │
└─────────────────────────────────────┼───────────────────────┘
                                      │
                                      ▼
                    ┌──────────────────────────────┐
                    │   Fresh Service API          │
                    │   kovitec.freshservice.com   │
                    └──────────────────────────────┘
```

## 🔄 Fluxo de Dados

### 1️⃣ Login

```
Usuario seleciona nome
    │
    ▼
App consulta SQLite
    │
    ├─▶ Primeiro acesso? ──▶ Define senha ──▶ Salva no SQLite
    │
    └─▶ Já tem senha? ──▶ Valida senha ──▶ Carrega API Key
                                              │
                                              ▼
                                    Entra na tela de inventário
```

### 2️⃣ Buscar Ativo

```
Usuario digita patrimônio
    │
    ▼
App consulta Fresh API
(usando API Key do usuário)
    │
    ├─▶ GET /assets?search="asset_tag:'{patrimonio}'"
    │
    ▼
Fresh retorna JSON
    │
    ▼
App extrai dados:
 - Nome
 - Tipo (Notebook/HeadSet/Celular/etc)
 - Serial
 - Status atual
 - Display ID
    │
    ▼
Mostra na tela
```

### 3️⃣ Inventariar

```
Usuario digita email
    │
    ▼
App busca User ID no Fresh
    │
    ├─▶ GET /requesters?email={email}
    ├─▶ GET /agents?email={email}
    │
    ▼
Fresh retorna user_id
    │
    ▼
App atualiza ativo
    │
    ├─▶ PUT /assets/{display_id}
    │   {
    │     "user_id": user_id,
    │     "asset_state": "In Use"
    │   }
    │
    ▼
Fresh confirma atualização
    │
    ▼
App mostra "Sucesso!"
```

### 4️⃣ Enviar Termo (Opcional)

```
Usuario clica "INVENTARIAR + TERMO"
    │
    ▼
App verifica tipo do ativo
    │
    ├─▶ Notebook/HeadSet/Celular? ──▶ SIM ──▶ Envia termo DocuSign
    │                                          (não implementado ainda)
    └─▶ Outro tipo? ──▶ NÃO ──▶ Pula esta etapa
```

## 🗄️ Banco de Dados (SQLite)

### Tabela: `users`

| Campo         | Tipo    | Descrição                    |
|---------------|---------|------------------------------|
| id            | INTEGER | ID auto-incremento           |
| username      | TEXT    | Nome do usuário (único)      |
| password_hash | TEXT    | Hash SHA256 da senha         |
| api_key       | TEXT    | Chave de API do Fresh        |
| first_access  | INTEGER | 1 = primeiro acesso, 0 = não |
| created_at    | TIMESTAMP | Data de criação            |

**Exemplo:**
```sql
INSERT INTO users (username, first_access)
VALUES ('Mikael', 1);

UPDATE users 
SET password_hash = 'abc123...', first_access = 0, api_key = '9hc8kzd...'
WHERE username = 'Mikael';
```

## 🔌 API do Fresh Service

### Endpoints Utilizados

#### 1. Buscar Ativo
```http
GET /api/v2/assets?search="asset_tag:'{patrimonio}'"&include=type_fields
Authorization: Basic {base64(api_key:X)}
```

**Resposta:**
```json
{
  "assets": [{
    "display_id": 123,
    "name": "PE-1234",
    "asset_tag": "001234",
    "user_id": 456,
    "type_fields": {
      "product_22001045183": 789,
      "serial_number_22001045183": "ABC123",
      "asset_state_22001045183": "In Stock"
    }
  }]
}
```

#### 2. Buscar Usuário por Email
```http
GET /api/v2/requesters?email={email}
Authorization: Basic {base64(api_key:X)}
```

**Resposta:**
```json
{
  "requesters": [{
    "id": 456,
    "primary_email": "usuario@exemplo.com",
    "first_name": "João"
  }]
}
```

#### 3. Atualizar Ativo
```http
PUT /api/v2/assets/{display_id}
Authorization: Basic {base64(api_key:X)}
Content-Type: application/json

{
  "asset": {
    "user_id": 456,
    "asset_state": "In Use"
  }
}
```

## 🔐 Segurança

### Armazenamento de Senhas
- **NÃO** armazena senha em texto plano
- Usa **SHA256** para hash
- Hash é salvo no SQLite local

### API Keys
- Cada usuário tem sua própria chave
- Armazenada localmente no tablet (SQLite)
- Enviada em todas as requisições ao Fresh
- Formato: `Authorization: Basic base64(api_key:X)`

### Comunicação
- Todas as chamadas ao Fresh usam **HTTPS**
- Certificados SSL são validados
- Timeout de 30 segundos por requisição

## 📦 Tecnologias

### Frontend (UI)
- **Kivy 2.3.0**: Framework Python para apps mobile
- **KivyMD 1.1.1**: Componentes Material Design
- **KV Language**: Linguagem declarativa para layouts

### Backend (Lógica)
- **Python 3.8+**: Linguagem principal
- **SQLite3**: Banco de dados local
- **Requests**: Cliente HTTP para APIs
- **hashlib**: Criptografia de senhas

### Build
- **Buildozer**: Compila Python → APK
- **Cython**: Otimização de código
- **Android SDK/NDK**: Ferramentas do Android

## 🔄 Ciclo de Vida do App

```
┌─────────────┐
│  App inicia │
└──────┬──────┘
       │
       ▼
┌────────────────┐
│ Inicializa DB  │ ──▶ Cria tabela users se não existir
└──────┬─────────┘     Insere 8 usuários se necessário
       │
       ▼
┌────────────────┐
│ Tela de Login  │
└──────┬─────────┘
       │
       ├─▶ Usuário já tem senha? ──▶ Valida ──▶ Entra
       │
       └─▶ Primeiro acesso? ──▶ Define senha ──▶ Define API Key ──▶ Entra
                                                           │
       ┌───────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────┐
│ Tela Inventário │
└──────┬──────────┘
       │
       ├─▶ Buscar ativo
       ├─▶ Inventariar
       ├─▶ Enviar termo
       └─▶ Logout ──▶ Volta para Login
```

## 🚀 Performance

### Otimizações
- ✅ Requisições HTTP em **threads separadas** (não trava UI)
- ✅ Banco SQLite local (consultas rápidas)
- ✅ Cache de informações do usuário em memória
- ✅ Timeout de 30s em requisições (evita travamentos)

### Tamanho do APK
- **Estimado:** 15-25 MB
- Inclui: Python runtime + Kivy + bibliotecas

## 🔮 Possíveis Melhorias Futuras

1. **Scanner de código de barras**
   - Usar câmera do tablet
   - Ler código de barras do patrimônio

2. **Modo offline**
   - Salvar operações em fila
   - Sincronizar quando tiver internet

3. **Notificações push**
   - Alertas de novos ativos
   - Confirmação de termos assinados

4. **Relatórios**
   - Quantos ativos cada analista inventariou
   - Exportar para Excel

5. **Biometria**
   - Login com digital ou face

6. **Busca avançada**
   - Por nome, serial, usuário, etc.

7. **Histórico local**
   - Ver últimos ativos inventariados
   - Estatísticas do dia

---

**Arquitetura simples, eficiente e escalável!** 🚀
