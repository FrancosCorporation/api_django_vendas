# API Django Vendas

API REST de vendas em **Django**: autenticação própria de usuários com
ativação por e-mail e token, bloqueio por IP, catálogo de produtos com
categorias e pedidos.

![Python](https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![reCAPTCHA](https://img.shields.io/badge/reCAPTCHA-4285F4?style=flat-square&logo=google&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-projeto%20de%20estudo-lightgrey?style=flat-square)

## Sobre

Back-end de uma loja com dois perfis de acesso:

- **Consumidor** — navega e visualiza os produtos; para comprar/pedir,
  precisa estar logado.
- **Dono de empresa** — cadastra, edita e remove produtos.

Os produtos são organizados por categoria e possuem preço/desconto. O
cadastro de usuário passa por confirmação de e-mail com token e há proteção
contra tentativas repetidas por IP.

## Funcionalidades

Comprovadas pelo código (`app/views.py`, `app/models.py`, `app/urls.py`):

- **Usuários**: `create`, `login`, `logout`, `update`, `delete` e
  `activation` (ativação de conta por token enviado por e-mail).
- **Sessão por token/unidade de login** (`verify_loged`, `connecting_user`,
  `disconect_user`) com `csrf_exempt` nas rotas da API.
- **Bloqueio por IP**: model `Ip` com contador e data da última tentativa
  (`others/block.py`).
- **E-mail transacional**: SMTP configurável, com reCAPTCHA no fluxo de
  cadastro (`others/email.py`).
- **Produtos**: model `Products` (nome, descrição) e endpoints de catálogo.

### Modelo de dados (resumo)

| Entidade | Campos principais |
|---|---|
| `User` | `email` (PK), `username`, `password`, `last_login`, `date_auth`, `token`, `is_active`, `activate` |
| `Products` | `id`, `nameproduct`, `descripction` |
| `Ip` | `ip_address` (PK), `count`, `date_last_try` |

> Observação: o projeto é um estudo de 2022 e não usa o `User` nativo do
> Django — a autenticação foi implementada manualmente. Em uma evolução
> recomendada, migrar para `AbstractUser` + `rest_framework.authtoken`.

## Como rodar

1. Crie e ative um virtualenv, instale o Django:

```bash
python -m venv .venv && source .venv/bin/activate
pip install django djangorestframework mysqlclient psycopg2
```

2. Configure o banco em `firstapi/settings.py` (`DATABASES`) — MySQL,
   PostgreSQL, Oracle ou SQLite.
3. Configure as variáveis de e-mail/reCAPTCHA (veja `.env_sample_file`).
4. Migre e rode:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/users` | Dados do usuário logado |
| POST | `/create` | Cadastro (com reCAPTCHA + e-mail de ativação) |
| POST | `/login` | Login (retorna token) |
| POST | `/logout` | Encerra sessão |
| POST | `/update` | Atualiza usuário |
| POST | `/delete` | Remove usuário |
| GET | `/activation` | Ativa a conta pelo token |

## Estrutura do projeto

```
app/            # models, views, urls, serializers e helpers (others/)
firstapi/       # settings, urls raiz, wsgi/asgi
others/         # app auxiliar
manage.py
vercel.json     # deploy
```

## Licença

MIT — veja [LICENSE](LICENSE).
