# mylinks-api

---

# 🧭 **Guia do Backend — Projeto MyLinks**

---

## 📂 **1. Estrutura de Pastas**

```bash
mylinks-api/
│
├── app.py                       # Ponto de entrada principal da API
│
├── Controllers/                 # Rotas e endpoints HTTP
│   ├── userController.py
│   └── linkController.py
│
├── Workers/                     # Regras de negócio (camada Service)
│   ├── userWorker.py
│   └── linkWorker.py
│
├── Repositories/                # Acesso ao banco de dados (queries)
│   ├── userRepository.py
│   └── linkRepository.py
│
├── Utils/                       # Utilitários e configurações
│   ├── db.py                    # Conexão MySQL
│   ├── auth.py                  # Validação JWT
│   ├── __init__.py
│
├── uploads/                     # Pasta onde as fotos de perfil são salvas
│
├── .env                         # Variáveis de ambiente
└── requirements.txt              # Dependências do projeto
```

---

## ⚙️ **2. Arquitetura e Fluxo**

O backend é baseado em **três camadas principais** (padrão MVC simplificado):

| Camada               | Responsabilidade                   | Exemplo                                |
| -------------------- | ---------------------------------- | -------------------------------------- |
| **Controller**       | Recebe e responde requisições HTTP | `/auth/login`                          |
| **Worker (Service)** | Aplica regras de negócio e lógica  | Verifica senha, gera token             |
| **Repository**       | Executa comandos SQL no banco      | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |

Fluxo típico de uma requisição:

```
Cliente → Controller → Worker → Repository → Banco → Worker → Controller → Resposta JSON
```

---

## 🔐 **3. Autenticação e Segurança**

* **Login e Registro** retornam e validam **tokens JWT**
* Token é enviado no header:

  ```
  Authorization: Bearer <token>
  ```
* Rotas protegidas usam o **decorator `@token_required`**
* Senhas armazenadas com **bcrypt (hash irreversível)**
* O token expira após algumas horas (por segurança)

---

## 🌐 **4. Rotas da API**

---

### 🧍 **Usuário**

#### `POST /auth/register`

Cria um novo usuário.

📥 **Body JSON:**

```json
{
  "username": "luiz",
  "email": "luiz@email.com",
  "senha": "1234"
}
```

📤 **Resposta:**

```json
{
  "message": "Usuário criado com sucesso"
}
```

---

#### `POST /auth/login`

Autentica o usuário e retorna o token JWT.

📥 **Body JSON:**

```json
{
  "email": "luiz@email.com",
  "senha": "1234"
}
```

📤 **Resposta:**

```json
{
  "token": "<jwt_token>",
  "user": {
    "id": 1,
    "username": "luiz"
  }
}
```

---

#### `POST /upload` (protegida por JWT)

Faz upload da **foto de perfil** do usuário logado.

📥 **Form-Data:**

```
file: <imagem.png>
```

📤 **Resposta:**

```json
{
  "message": "Foto de perfil atualizada com sucesso",
  "foto_perfil": "/uploads/user_1.png"
}
```

📌 A imagem é salva localmente na pasta `/uploads`.

---

#### `GET /user/<username>` (rota pública)

Retorna o **perfil público** de um usuário, incluindo foto e links.

📤 **Resposta:**

```json
{
  "id": 1,
  "username": "luiz",
  "foto_perfil": "/uploads/user_1.png",
  "links": [
    { "id": 1, "titulo": "Meu GitHub", "url": "https://github.com/luiz", "ordem": 1 },
    { "id": 2, "titulo": "LinkedIn", "url": "https://linkedin.com/in/luiz", "ordem": 2 }
  ]
}
```

---

### 🔗 **Links**

#### `GET /links` (JWT obrigatório)

Retorna todos os links do usuário logado.

📤 **Resposta:**

```json
[
  { "id": 1, "titulo": "GitHub", "url": "https://github.com/luiz", "ordem": 1 },
  { "id": 2, "titulo": "LinkedIn", "url": "https://linkedin.com/in/luiz", "ordem": 2 }
]
```

---

#### `POST /links` (JWT obrigatório)

Cria um novo link para o usuário autenticado.

📥 **Body JSON:**

```json
{
  "titulo": "Meu Portfólio",
  "url": "https://meuportfolio.com"
}
```

📤 **Resposta:**

```json
{
  "message": "Link adicionado com sucesso"
}
```

---

#### `PUT /links/<id>` (JWT obrigatório)

Edita o título e a URL de um link existente.

📥 **Body JSON:**

```json
{
  "titulo": "LinkedIn Atualizado",
  "url": "https://linkedin.com/in/luizdev"
}
```

📤 **Resposta:**

```json
{
  "message": "Link atualizado com sucesso"
}
```

---

#### `DELETE /links/<id>` (JWT obrigatório)

Exclui um link do usuário.

📤 **Resposta:**

```json
{
  "message": "Link removido com sucesso"
}
```

---

#### `PUT /links/reorder` (JWT obrigatório)

Reorganiza a ordem dos links.

📥 **Body JSON:**

```json
[
  { "id": 2, "ordem": 1 },
  { "id": 1, "ordem": 2 }
]
```

📤 **Resposta:**

```json
{
  "message": "Links reordenados com sucesso"
}
```

---

## 🗄️ **5. Banco de Dados**

### 🧱 Tabela: `usuarios`

| Campo       | Tipo         | Descrição               |
| ----------- | ------------ | ----------------------- |
| id          | INT (PK)     | Identificador único     |
| username    | VARCHAR(50)  | Nome de usuário (único) |
| email       | VARCHAR(100) | Email (único)           |
| senha_hash  | VARCHAR(255) | Senha criptografada     |
| foto_perfil | VARCHAR(255) | Caminho da foto         |

---

### 🔗 Tabela: `links`

| Campo      | Tipo         | Descrição             |
| ---------- | ------------ | --------------------- |
| id         | INT (PK)     | Identificador do link |
| usuario_id | INT (FK)     | Referência ao usuário |
| titulo     | VARCHAR(100) | Nome do link          |
| url        | VARCHAR(255) | Endereço do link      |
| ordem      | INT          | Posição na lista      |

💡 `usuario_id` tem `ON DELETE CASCADE` — se o usuário for apagado, todos os seus links são removidos automaticamente.

---

## 🧾 **6. Variáveis de Ambiente (.env)**

```env
CONN_URL='railway_url'
SECRET='segredo123'
```

Essas variáveis são lidas em `Utils/db.py` e `Utils/auth.py`.

---

## 🚀 **7. Fluxo de Uso da API**

1. **Cadastro/Login** → recebe token JWT
2. **Dashboard (autenticado)** → CRUD dos links
3. **Upload (autenticado)** → atualiza foto de perfil
4. **Página pública** → `/user/:username` mostra tudo pro visitante

---

## ✅ **8. Status Final**

✔ Estrutura modularizada (MVC limpo)
✔ Todas as rotas implementadas
✔ Segurança JWT + senhas hashadas
✔ Banco relacional com integridade
✔ Upload funcional
✔ Deploy pronto

---
