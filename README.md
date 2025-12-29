# 🔌 MyLinks - API Backend

API RESTful desenvolvida em Python com Flask para o projeto **MyLinks**, um agregador de links pessoal (estilo Linktree/Instabio).

🔗 **Deploy**: [pygre.onrender.com](https://pygre.onrender.com)  
📚 **Documentação Interativa**: [pygre.onrender.com/docs](https://pygre.onrender.com/docs)

---

## 🚀 Tecnologias

- **Python 3.10+**
- **Flask** - Framework web
- **Flask-CORS** - Permitir requisições cross-origin
- **Flask-Swagger-UI** - Documentação interativa da API
- **Flask-Limiter** - Rate limiting
- **Flask-Talisman** - Segurança HTTPS
- **MySQL** - Banco de dados relacional
- **mysql-connector-python** - Driver MySQL
- **bcrypt** - Criptografia de senhas
- **PyJWT** - Autenticação com tokens JWT
- **Cloudinary** - Upload e hospedagem de imagens
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Gunicorn** - Servidor WSGI para produção

---

## 📚 Documentação da API

A API está documentada seguindo o padrão **OpenAPI 3.0** (Swagger).

### 🌐 Acesse a Documentação Interativa:
- **Produção**: [https://pygre.onrender.com/docs](https://pygre.onrender.com/docs)
- **Local**: [http://localhost:5000/docs](http://localhost:5000/docs)

Na documentação interativa você pode:
- ✅ Visualizar todos os endpoints disponíveis
- ✅ Ver exemplos de requisições e respostas
- ✅ Testar os endpoints diretamente no navegador
- ✅ Gerar código cliente automaticamente
- ✅ Explorar os schemas de dados

### 📄 Arquivo de Especificação:
O arquivo `openapi.yaml` está na raiz do projeto e pode ser usado com:
- [Swagger Editor](https://editor.swagger.io) - Editor online
- [Postman](https://www.postman.com) - Importar collection
- [Insomnia](https://insomnia.rest) - Importar workspace
- Geradores de código cliente (openapi-generator)

---

## 📂 Estrutura do Projeto

```
mylinks-api/
│
├── app.py                       # Ponto de entrada principal da API
├── openapi.yaml                 # Especificação OpenAPI 3.0
├── extensions.py                # Configuração Flask-Limiter
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
│   ├── valid_email.py           # Validação de e-mails
│   ├── valid_username.py        # Validação de usernames
│   ├── valid_password.py        # Validação de senhas
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

- **Access Token**: Válido por **15 minutos**
- **Refresh Token**: Válido por **7 dias**

```python
# Exemplo de geração de token (userWorker.py)
access_token = jwt.encode(
    {
        "id": user["id"],
        "exp": datetime.utcnow() + timedelta(minutes=15),
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

### **Validação de Senhas**
A API valida senhas no cadastro seguindo critérios de segurança:
- Mínimo 10 caracteres
- Pelo menos 1 letra MAIÚSCULA
- Pelo menos 1 letra minúscula
- Pelo menos 1 número
- Pelo menos 1 caractere especial (!@#$%^&*(),.?":{}|<>)

---

## 🌐 Endpoints da API

### **📍 Base URL**
- **Produção**: `https://pygre.onrender.com`
- **Local**: `http://localhost:5000`

### **📚 Documentação Completa**
Para a documentação completa e interativa de todos os endpoints, acesse:
- **[/docs](https://pygre.onrender.com/docs)** - Interface Swagger UI
- **[/openapi.yaml](https://pygre.onrender.com/openapi.yaml)** - Especificação OpenAPI

---

### **Resumo dos Endpoints Principais**

#### **🔐 Autenticação**
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/auth/register` | Criar nova conta | 👤 |
| POST | `/auth/login` | Login e obter tokens | 👤 |
| POST | `/auth/refresh` | Renovar access token | 🔄 Refresh Token |

#### **👤 Usuário**
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/user/{username}` | Perfil público | 👤 |
| GET | `/{username}` | Redirecionar para frontend | 👤 |
| POST | `/auth/upload` | Upload foto de perfil | ✅ |
| PUT | `/auth/update-username` | Atualizar username | ✅ |
| PUT | `/auth/update-email` | Atualizar e-mail | ✅ |
| PUT | `/auth/update-password` | Atualizar senha | ✅ |
| DELETE | `/auth/delete-account` | Excluir conta | ✅ |

#### **🔗 Links**
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/links` | Listar links do usuário | ✅ |
| POST | `/links` | Criar novo link | ✅ |
| PUT | `/links/{id}` | Atualizar link | ✅ |
| DELETE | `/links/{id}` | Excluir link | ✅ |
| PUT | `/links/reorder` | Reordenar links | ✅ |

#### **⚙️ Sistema**
| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/health` | Health check | 👤 |
| GET | `/` | Informações da API | 👤 |
| GET | `/docs` | Documentação Swagger UI | 👤 |
| GET | `/openapi.yaml` | Especificação OpenAPI | 👤 |

**Legenda:**
- ✅ Requer autenticação (Bearer Token)
- 🔄 Requer Refresh Token
- 👤 Acesso público

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
# Health check
curl http://localhost:5000/health

# Documentação interativa
# Abra no navegador: http://localhost:5000/docs
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

### **Usando Swagger UI (Recomendado)**
1. Acesse [http://localhost:5000/docs](http://localhost:5000/docs)
2. Explore os endpoints disponíveis
3. Clique em "Try it out" para testar
4. Para endpoints autenticados:
   - Faça login em `/auth/login`
   - Copie o `access_token`
   - Clique em "Authorize" 🔒 no topo
   - Cole o token e confirme

### **Usando cURL**

```bash
# Registro
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"teste","email":"teste@email.com","senha":"Senha@123456"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@email.com","senha":"Senha@123456"}'

# Listar links (com token)
curl -X GET http://localhost:5000/links \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### **Usando Postman/Insomnia**
1. Importe a especificação OpenAPI:
   - Postman: File → Import → Link → `https://pygre.onrender.com/openapi.yaml`
   - Insomnia: Create → Import from URL → `https://pygre.onrender.com/openapi.yaml`
2. Configure a variável `{{base_url}}` = `http://localhost:5000`
3. Teste os endpoints

---

## 📊 Códigos de Status HTTP

| Código | Significado | Quando Ocorre |
|--------|-------------|---------------|
| `200` | OK | Requisição bem-sucedida |
| `400` | Bad Request | Dados inválidos ou campos faltando |
| `401` | Unauthorized | Token inválido ou expirado |
| `403` | Forbidden | Senha incorreta ou sem permissão |
| `404` | Not Found | Recurso não encontrado |
| `429` | Too Many Requests | Rate limit excedido |
| `500` | Internal Server Error | Erro no servidor |

### **Diferença entre 401 e 403**
- **401 Unauthorized**: Problema de **autenticação** (token inválido/expirado)
- **403 Forbidden**: **Autenticado**, mas sem **permissão** (ex: senha incorreta)

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
// Token expirado (401)
{ "error": "Token expirado" }

// Senha incorreta (403)
{ "error": "Senha incorreta" }

// Campos faltando (400)
{ "error": "Campos obrigatórios" }

// Username já existe (400)
{ "error": "Username já existente" }

// URL inválida (400)
{ "error": "URL inválida" }

// Rate limit (429)
{
  "error": "Muitas requisições. Tente novamente mais tarde.",
  "message": "5 per 1 minute"
}
```

---

## 🔒 Segurança

### **Implementado:**
- ✅ Senhas criptografadas com bcrypt
- ✅ Validação de senhas (10+ caracteres, MAIÚSCULA, minúscula, número, especial)
- ✅ Tokens JWT com expiração (15min + refresh 7 dias)
- ✅ Refresh token para renovação
- ✅ Validação de URLs
- ✅ Validação de e-mails
- ✅ Validação de usernames
- ✅ Proteção contra SQL Injection (prepared statements)
- ✅ CORS configurado
- ✅ Rate limiting (200/dia, 50/hora, 5/min em endpoints sensíveis)
- ✅ Validação de tipos de arquivo (upload)
- ✅ Limite de tamanho de imagem (15MB)
- ✅ HTTPS forçado (Flask-Talisman)
- ✅ Headers de segurança (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)

### **Recomendado para Produção:**
- ⚠️ HTTPS obrigatório (já implementado no Render)
- ⚠️ Logging detalhado
- ⚠️ Monitoramento de erros (Sentry)
- ⚠️ Backup automatizado do banco

---

## 📦 Dependências

### **Principais (requirements.txt)**
```txt
gunicorn                  # Servidor WSGI
flask                     # Framework web
flask-cors                # CORS
flask-swagger-ui          # Documentação Swagger UI
flask_limiter             # Rate limiting
flask-talisman            # Segurança HTTPS
mysql-connector-python    # Driver MySQL
bcrypt                    # Criptografia
pyjwt                     # JWT
python-dotenv             # Variáveis de ambiente
cloudinary==1.41.0        # Upload de imagens
```

### **Instalação**
```bash
pip install -r requirements.txt
```

---

## 📈 Performance

### **Otimizações Implementadas:**
- ✅ Conexões MySQL reutilizadas (connection pooling)
- ✅ Queries otimizadas (SELECT apenas campos necessários)
- ✅ Índices no banco (username, email)
- ✅ Cloudinary CDN para imagens
- ✅ Logging de erros apenas (não de debug em produção)
- ✅ Rate limiting para prevenir abuso

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

### **Documentação não aparece em /docs**
- Verifique se `flask-swagger-ui` está instalado
- Verifique se o arquivo `openapi.yaml` está na raiz
- Reinicie o servidor

---

## 🔗 Links Relacionados

- **Frontend**: [mylinks-frontend](https://github.com/seu-usuario/mylinks-frontend)
- **Banco de Dados**: [mylinks-db](https://github.com/seu-usuario/mylinks-db)
- **Deploy API**: [pygre.onrender.com](https://pygre.onrender.com)
- **Documentação API**: [pygre.onrender.com/docs](https://pygre.onrender.com/docs)
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
