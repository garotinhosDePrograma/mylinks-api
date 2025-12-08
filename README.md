# 🔌 MyLinks - API Backend

API RESTful desenvolvida em Python com Flask para o projeto **MyLinks**, um agregador de links pessoal (estilo Linktree/Instabio).

🔗 **Deploy**: [pygre.onrender.com](https://pygre.onrender.com)

---

## 🚀 Tecnologias

- **Python 3.10+**
- **Flask** - Framework web
- **Flask-CORS** - Permitir requisições cross-origin
- **MySQL** - Banco de dados relacional
- **mysql-connector-python** - Driver MySQL
- **bcrypt** - Criptografia de senhas
- **PyJWT** - Autenticação com tokens JWT
- **Cloudinary** - Upload e hospedagem de imagens
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Gunicorn** - Servidor WSGI para produção

---

## 📂 Estrutura do Projeto

```
mylinks-api/
│
├── app.py                       # Ponto de entrada principal da API
│
├── Controllers/                 # Rotas e endpoints HTTP
│   ├── userController.py        # Endpoints de usuário e autenticação
│   └── linkController.py        # Endpoints de links
│
├── Workers/                     # Regras de negócio (camada Service)
│   ├── userWorker.py            # Lógica de usuários
│   └── linkWorker.py            # Lógica de links
│
├── Repositories/                # Acesso ao banco de dados (queries)
│   ├── userRepository.py        # Queries de usuários
│   └── linkRepository.py        # Queries de links
│
├── Models/                      # Classes de domínio (Entidades)
│   ├── user.py                  # Entidade User
│   └── link.py                  # Entidade Link
│
├── Utils/                       # Utilitários e configurações
│   ├── db.py                    # Conexão MySQL local
│   ├── db_railway.py            # Conexão MySQL Railway (produção)
│   ├── auth.py                  # Decorator @token_required
│   ├── cloudinary.py            # Configuração Cloudinary
│   ├── valid_url.py             # Validação de URLs
│   └── __init__.py
│
├── .env                         # Variáveis de ambiente (não commitado)
├── .gitignore                   # Arquivos ignorados pelo Git
├── requirements.txt             # Dependências Python
├── run.bat                      # Script Windows para rodar localmente
└── README.md                    # Este arquivo
```

---

## ⚙️ Arquitetura (MVC + Repository Pattern)

O backend segue uma **arquitetura em camadas** baseada no padrão MVC com Repository:

```
┌─────────────────────────────────────────────┐
│          Cliente (Frontend)                 │
└─────────────────┬───────────────────────────┘
                  │
                  ↓ HTTP Request
┌─────────────────────────────────────────────┐
│   CONTROLLER (Rotas HTTP)                   │
│   • Recebe requisições                      │
│   • Valida dados de entrada                 │
│   • Retorna respostas JSON                  │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│   WORKER/SERVICE (Regras de Negócio)       │
│   • Aplica lógica de negócio                │
│   • Valida regras de domínio                │
│   • Orquestra chamadas ao Repository        │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│   REPOSITORY (Acesso a Dados)               │
│   • Executa queries SQL                     │
│   • Retorna dados do banco                  │
│   • Abstrai detalhes do MySQL               │
└─────────────────┬───────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────┐
│          Banco de Dados (MySQL)             │
└─────────────────────────────────────────────┘
```

### **Fluxo de uma Requisição**
```
Cliente → Controller → Worker → Repository → MySQL
        ← JSON     ← Dados  ← Resultado  ←
```

---

## 🔐 Autenticação e Segurança

### **JWT (JSON Web Token)**
A API utiliza tokens JWT para autenticação:

- **Access Token**: Válido por **1 hora**
- **Refresh Token**: Válido por **7 dias**

```python
# Exemplo de geração de token (userWorker.py)
access_token = jwt.encode(
    {
        "id": user["id"],
        "exp": datetime.utcnow() + timedelta(hours=1),
        "type": "access"
    },
    SECRET_KEY,
    algorithm="HS256"
)
```

### **Proteção de Rotas**
Rotas sensíveis usam o decorator `@token_required`:

```python
@link_bp.route("/links", methods=["GET"])
@token_required
def get_links(usuario_id):
    # usuario_id é extraído automaticamente do token
    result = worker.getAll(usuario_id)
    return jsonify(result), 200
```

### **Senhas Criptografadas**
- Utiliza **bcrypt** para hash irreversível
- Senhas NUNCA são armazenadas em texto puro

```python
# Registro
hashed = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

# Login
bcrypt.checkpw(senha.encode("utf-8"), user["senha"].encode("utf-8"))
```

---

## 🌐 Endpoints da API

### **📍 Base URL**
- **Produção**: `https://pygre.onrender.com`
- **Local**: `http://localhost:5000`

---

### **🔐 Autenticação**

#### `POST /auth/register`
Cria um novo usuário.

**Body:**
```json
{
  "username": "joao",
  "email": "joao@email.com",
  "senha": "senha123"
}
```

**Resposta:**
```json
{
  "message": "Usuário criado com sucesso!"
}
```

---

#### `POST /auth/login`
Autentica o usuário e retorna tokens JWT.

**Body:**
```json
{
  "email": "joao@email.com",
  "senha": "senha123"
}
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "joao",
    "email": "joao@email.com"
  }
}
```

---

#### `POST /auth/refresh`
Renova o access token usando o refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

#### `POST /auth/upload` 🔒
Faz upload da foto de perfil (requer autenticação).

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Body (Form-Data):**
```
file: <imagem.png>
```

**Resposta:**
```json
{
  "message": "Foto de perfil atualizada com sucesso",
  "foto_perfil": "https://res.cloudinary.com/.../user_1.png"
}
```

---

#### `PUT /auth/update-username` 🔒
Altera o username do usuário (requer autenticação).

**Body:**
```json
{
  "newUsername": "joao_silva",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "message": "Username atualizado com sucesso",
  "username": "joao_silva"
}
```

---

#### `PUT /auth/update-email` 🔒
Altera o e-mail do usuário (requer autenticação).

**Body:**
```json
{
  "newEmail": "joao.silva@email.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "message": "E-mail atualizado com sucesso",
  "email": "joao.silva@email.com"
}
```

---

#### `PUT /auth/update-password` 🔒
Altera a senha do usuário (requer autenticação).

**Body:**
```json
{
  "currentPassword": "senha123",
  "newPassword": "novaSenha456"
}
```

**Resposta:**
```json
{
  "message": "Senha atualizada com sucesso"
}
```

---

#### `DELETE /auth/delete-account` 🔒
Exclui permanentemente a conta do usuário (requer autenticação).

**Body:**
```json
{
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "message": "Conta excluída com sucesso"
}
```

---

### **👤 Usuário**

#### `GET /user/<username>`
Retorna o perfil público de um usuário (incluindo links).

**Exemplo:**
```
GET /user/joao
```

**Resposta:**
```json
{
  "id": 1,
  "username": "joao",
  "foto_perfil": "https://res.cloudinary.com/.../user_1.png",
  "links": [
    {
      "id": 1,
      "titulo": "Meu GitHub",
      "url": "https://github.com/joao",
      "ordem": 1
    },
    {
      "id": 2,
      "titulo": "LinkedIn",
      "url": "https://linkedin.com/in/joao",
      "ordem": 2
    }
  ]
}
```

---

#### `GET /<username>`
Redireciona para a página de perfil no frontend.

**Exemplo:**
```
GET /joao → Redireciona para: https://mylinks-352x.onrender.com/profile.html?user=joao
```

---

### **🔗 Links**

#### `GET /links` 🔒
Retorna todos os links do usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta:**
```json
[
  {
    "id": 1,
    "usuario_id": 1,
    "titulo": "GitHub",
    "url": "https://github.com/joao",
    "ordem": 1
  },
  {
    "id": 2,
    "usuario_id": 1,
    "titulo": "LinkedIn",
    "url": "https://linkedin.com/in/joao",
    "ordem": 2
  }
]
```

---

#### `POST /links` 🔒
Cria um novo link (requer autenticação).

**Body:**
```json
{
  "titulo": "Meu Portfólio",
  "url": "https://meusite.com"
}
```

**Resposta:**
```json
{
  "message": "Link adicionado com sucesso"
}
```

---

#### `PUT /links/<id>` 🔒
Atualiza um link existente (requer autenticação).

**Exemplo:**
```
PUT /links/1
```

**Body:**
```json
{
  "titulo": "GitHub Atualizado",
  "url": "https://github.com/joao-silva"
}
```

**Resposta:**
```json
{
  "message": "Link atualizado com sucesso"
}
```

---

#### `DELETE /links/<id>` 🔒
Exclui um link (requer autenticação).

**Exemplo:**
```
DELETE /links/1
```

**Resposta:**
```json
{
  "message": "Link removido com sucesso"
}
```

---

#### `PUT /links/reorder` 🔒
Reordena os links do usuário (requer autenticação).

**Body:**
```json
[
  { "id": 2, "ordem": 1 },
  { "id": 1, "ordem": 2 },
  { "id": 3, "ordem": 3 }
]
```

**Resposta:**
```json
{
  "message": "Links reordenados com sucesso"
}
```

---

## 🗄️ Banco de Dados

### **Modelo de Dados**

```sql
-- Tabela usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    senha VARCHAR(255) NOT NULL,
    foto_perfil VARCHAR(255)
);

-- Tabela links
CREATE TABLE links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    titulo VARCHAR(100),
    url VARCHAR(150),
    ordem INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
```

### **Relacionamentos**
- **1:N** entre `usuarios` e `links`
- **ON DELETE CASCADE**: Ao deletar um usuário, todos os seus links são removidos automaticamente

---

## 🛠️ Configuração Local

### **1. Pré-requisitos**
- Python 3.10+
- MySQL 8.0+
- Conta no Cloudinary (para upload de imagens)

### **2. Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/mylinks-api.git
cd mylinks-api
```

### **3. Crie um Ambiente Virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **4. Instale as Dependências**
```bash
pip install -r requirements.txt
```

### **5. Configure o Banco de Dados**
```bash
# Entre no MySQL
mysql -u root -p

# Execute o script SQL
source caminho/para/MyLinks.sql
```

### **6. Configure as Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados Local
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_PORT=3306
DB_DATABASE=MyLinks

# OU Banco de Dados Railway (Produção)
CONN_URL=mysql://user:password@host:port/MyLinks

# JWT Secret
SECRET_KEY=sua_chave_secreta_super_forte

# Cloudinary
CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=seu_api_secret
```

### **7. Execute a API**
```bash
# Desenvolvimento (com Flask)
python -m flask run --host=0.0.0.0 --port=5000

# OU Windows
run.bat

# Produção (com Gunicorn)
gunicorn app:app
```

### **8. Teste a API**
```bash
curl http://localhost:5000/user/joao
```

---

## 🚀 Deploy (Render)

### **1. Conecte o GitHub**
1. Acesse [Render.com](https://render.com)
2. Crie um novo "Web Service"
3. Conecte o repositório `mylinks-api`

### **2. Configurações**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Environment**: Python 3

### **3. Variáveis de Ambiente**
Configure no dashboard do Render:
```
CONN_URL=mysql://...
SECRET_KEY=...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

### **4. Deploy Automático**
Cada push no GitHub fará deploy automaticamente.

---

## 🧪 Testando os Endpoints

### **Usando cURL**

```bash
# Registro
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","email":"teste@email.com","senha":"123456"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@email.com","senha":"123456"}'

# Listar links (com token)
curl -X GET http://localhost:5000/links \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### **Usando Postman/Insomnia**
1. Importe a collection (crie uma nova)
2. Configure a variável `{{base_url}}` = `http://localhost:5000`
3. Teste os endpoints conforme documentado acima

---

## 📊 Códigos de Status HTTP

| Código | Significado | Quando Ocorre |
|--------|-------------|---------------|
| `200` | OK | Requisição bem-sucedida |
| `400` | Bad Request | Dados inválidos ou campos faltando |
| `401` | Unauthorized | Token inválido ou expirado |
| `404` | Not Found | Recurso não encontrado |
| `500` | Internal Server Error | Erro no servidor |

---

## 🔍 Tratamento de Erros

Todas as respostas de erro seguem o padrão:

```json
{
  "error": "Descrição do erro"
}
```

**Exemplos:**
```json
// Token expirado
{ "error": "Token expirado" }

// Campos faltando
{ "error": "Campos obrigatórios" }

// Username já existe
{ "error": "Username já existente" }

// URL inválida
{ "error": "URL inválida" }
```

---

## 🔒 Segurança

### **Implementado:**
- ✅ Senhas criptografadas com bcrypt
- ✅ Tokens JWT com expiração
- ✅ Refresh token para renovação
- ✅ Validação de URLs
- ✅ Proteção contra SQL Injection (uso de prepared statements)
- ✅ CORS configurado
- ✅ Validação de tipos de arquivo (upload)
- ✅ Limite de tamanho de imagem (15MB)

### **Recomendado para Produção:**
- ⚠️ Rate limiting (limitar requisições por IP)
- ⚠️ HTTPS obrigatório
- ⚠️ Logging detalhado
- ⚠️ Monitoramento de erros (Sentry)
- ⚠️ Backup automatizado do banco

---

## 📦 Dependências

### **Principais (requirements.txt)**
```txt
gunicorn              # Servidor WSGI
flask                 # Framework web
flask-cors            # CORS
mysql-connector-python  # Driver MySQL
bcrypt                # Criptografia
pyjwt                 # JWT
python-dotenv         # Variáveis de ambiente
cloudinary==1.41.0    # Upload de imagens
```

### **Instalação**
```bash
pip install -r requirements.txt
```

---

## 📈 Performance

### **Otimizações Implementadas:**
- ✅ Conexões MySQL reutilizadas
- ✅ Queries otimizadas (SELECT apenas campos necessários)
- ✅ Índices no banco (username, email)
- ✅ Cloudinary CDN para imagens
- ✅ Logging de erros apenas (não de debug em produção)

### **Métricas Esperadas:**
- Tempo de resposta: < 200ms (média)
- Throughput: 100+ req/s
- Uptime: 99%+

---

## 🐛 Troubleshooting

### **Erro: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

### **Erro: "Access denied for user"**
Verifique as credenciais no `.env`:
```env
DB_USER=root
DB_PASSWORD=sua_senha_correta
```

### **Erro: "Token inválido"**
- Verifique se o token está no formato: `Bearer <token>`
- Verifique se `SECRET_KEY` é a mesma no `.env`

### **Erro: "CORS policy"**
- Verifique se `CORS(app)` está configurado em `app.py`
- Adicione o domínio do frontend na configuração CORS se necessário

---

## 🔗 Links Relacionados

- **Frontend**: [mylinks-frontend](https://github.com/seu-usuario/mylinks-frontend)
- **Banco de Dados**: [mylinks-db](https://github.com/seu-usuario/mylinks-db)
- **Deploy API**: [pygre.onrender.com](https://pygre.onrender.com)
- **Deploy Frontend**: [mylinks-352x.onrender.com](https://mylinks-352x.onrender.com)

---

## 📄 Licença

Este projeto foi desenvolvido como parte do **Curso Técnico em Desenvolvimento de Sistemas - SENAI Cabo**.

**Projeto Final**: O Senhor dos Projetos  
**Docente**: Givanio José de Melo  
**Data de Entrega**: 10/12/2025

---

## 🤝 Contribuindo

Este é um projeto acadêmico, mas contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 👨‍💻 Desenvolvedores

**[Luiz, Thalis, Diego, Renan e João]**

---

**"Um Projeto para a todos integrar, Um Projeto para conectar, Um Projeto para a tudo coroar e com a lógica concretizar."** 🔥
