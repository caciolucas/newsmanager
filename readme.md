# Gerenciador de Notícias 🚀

Este projeto é uma aplicação de gerenciamento de notícias baseada em Django, que facilita a criação, edição, publicação e controle de acesso às notícias. Além disso, as notícias podem ser salvas em richtext utilizando o **django-prose-editor** para uma edição mais rica e flexível.

---

## 🗺️ Roadmap

- [ ] **Adicionar configuração para S3**
- [ ] **Implementar CI/CD** (para rodar testes, linters, buildar a imagem, enviar para o registry e realizar o deploy no EKS)
- [ ] **Criar endpoints para gerenciamento de Planos**
- [ ] **Adicionar configuração de CORS**


## 🚀 Começando

### 🔧 Pré-requisitos

- Docker & Docker Compose  
- [Extensão VS Code Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (para desenvolvimento local)

---

## 💡 Funcionalidades

### 📰 Gerenciamento de Notícias

A gestão de notícias é implementada através do `NewsViewSet`, permitindo operações de criação, leitura, atualização e exclusão.  
**Destaque:** As notícias podem ser salvas em richtext com o **django-prose-editor**.

#### Endpoints

1. **Listar Notícias** (`GET /api/v1/news/post/`)  
   Recupera uma lista de notícias publicadas.
   - 👑 **Administradores:** Têm acesso total a todas as operações.
   - ✍️ **Editores:** Podem criar, atualizar e excluir apenas suas próprias notícias.
   - 👥 **Usuários Autenticados:** Podem visualizar notícias publicadas de acordo com sua inscrição ativa nos planos de assinatura da vertical da notícia.

2. **Criar Notícia** (`POST /api/v1/news/post/`)  
   Permite a criação de uma nova notícia. Apenas administradores e editores podem executar essa ação.

3. **Recuperar Notícia** (`GET /api/v1/news/{id}/`)  
   Retorna os detalhes de uma notícia específica, seguindo as mesmas regras de permissões da listagem.

4. **Atualizar Notícia** (`PUT /api/v1/news/posts/{id}/`)  
   Atualiza uma notícia existente. Administradores podem atualizar qualquer notícia, enquanto editores só podem atualizar suas próprias publicações.

5. **Excluir Notícia** (`DELETE /api/v1/news/posts/{id}/`)  
   Remove uma notícia. Essa operação é exclusiva para administradores.

---

### ⏰ Agendamento de Notícias

Após o cadastro, uma notícia inicia no status de rascunho (`DRAFT`).  
Para publicá-la, envie uma requisição para o endpoint:  
`POST /api/v1/news/posts/{id}/publish/`  
A publicação ocorrerá na data e hora definida no campo `publish_at` ou imediatamente, se o campo estiver vazio.

---

### 📋 Planos

Os planos são utilizados para controlar o acesso dos usuários às notícias.  
- Cada plano possui uma lista de verticais de notícias associadas.
- Usuários podem se inscrever em planos para ter acesso às notícias das verticais correspondentes.

---

## ⚙️ Setup

1. **Copiar o arquivo de ambiente**  
   Crie sua configuração local copiando o arquivo de exemplo:
   ```sh
   cp .env.example .env
   ```

2. **Iniciar o servidor de desenvolvimento**  
   Utilize o Docker Compose para iniciar o servidor:
   ```sh
   docker-compose -f .docker/docker-compose.yaml up
   ```
   A aplicação estará disponível em [http://localhost:8000](http://localhost:8000). Consulte a [documentação da API](http://localhost:8000/api/v1/docs) para mais detalhes.

3. **Executar Testes**  
   Rode os testes via Docker Compose:
   ```sh
   docker-compose -f .docker/docker-compose.yaml run --rm news-manager-api make test
   ```

---

## 💻 Desenvolvimento Local

1. **Iniciar o Servidor de Desenvolvimento**  
   Abra o projeto no VS Code e inicie o servidor usando a extensão Remote Containers.

2. **Executar Testes**  
   Utilize o terminal integrado do VS Code:
   ```sh
   make test
   ```

3. **Formatação de Código**  
   Formate o código com o Black:
   ```sh
   make lint
   ```

4. **Adicionando Dependências**  
   Para adicionar novas dependências, insira-as nos arquivos `requirements.in` (ou `requirements-dev.in`) e atualize o `requirements.txt` com:
   ```sh
   make dev-requirements  # para dependências de desenvolvimento
   make requirements      # para dependências de produção
   ```

---
