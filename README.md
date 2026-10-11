# API Django Vendas

API de estudo em Django para contas de usuário com ativação por e-mail. O repositório contém modelos
iniciais de produtos, mas ainda não oferece endpoints de catálogo ou pedidos.

## Requisitos

- Docker e Docker Compose (recomendado para execução local)
- Python 3.12 para execução fora do Docker
- MySQL 8.4

## Executar localmente

1. Copie `.env.example` para `.env`.
2. Gere um segredo para `DJANGO_SECRET_KEY` com `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
3. Substitua os valores de exemplo de `DB_PASSWORD` e `MYSQL_ROOT_PASSWORD` por senhas diferentes.
4. Inicie a API e o banco:

```bash
docker compose up --build
```

A API fica em `http://localhost:3213`; a porta está vinculada apenas a `127.0.0.1`. No perfil local,
o Django imprime o e-mail de ativação no log do container:

```bash
docker compose logs -f api
```

O volume `api_django_vendas_mysql_data` preserva o banco entre reinicializações. As migrações são
aplicadas ao iniciar a API.

Para executar Django fora do Docker, instale `requirements.txt`, configure as mesmas variáveis no
ambiente e inicie um servidor WSGI para produção. `runserver` serve somente para desenvolvimento.

## API de contas

Credenciais de cadastro/login vão em JSON no corpo, nunca na query string. Tokens de sessão são
retornados no login e enviados nas próximas requisições no cabeçalho `Authorization: Bearer <token>`.
Eles expiram após uma hora e são invalidados no logout ou em um novo login para a mesma conta.

| Método | Rota | Uso |
|---|---|---|
| POST | `/account/create` | JSON `{ "username": "...", "email": "...", "password": "..." }`; envia ativação por e-mail |
| GET | `/account/activation?token=...` | Ativa o link de uso único, válido por 24 horas |
| POST | `/account/login` | JSON `{ "email": "...", "password": "..." }`; retorna `access_token` |
| GET | `/account/users` | Retorna os dados da conta autenticada, sem repetir o token |
| PUT | `/account/update` | Bearer + JSON com `current_password` e `username` ou `new_password` |
| POST | `/account/logout` | Invalida a sessão Bearer atual |
| DELETE | `/account/delete` | Exclui a conta autenticada |

A autenticação usa um token aleatório de alta entropia armazenado no banco e vinculado a uma validade
máxima de uma hora. O controle de tentativas de login é persistido por endereço IP no MySQL.

## Variáveis de ambiente

Consulte `.env.example`. Em produção, configure no gerenciador de segredos:

- `DJANGO_SECRET_KEY`: valor aleatório de pelo menos 50 caracteres.
- `DJANGO_DEBUG=0` e `DJANGO_ALLOWED_HOSTS` com os hosts exatos.
- `DJANGO_SECURE_SSL_REDIRECT=1` e HTTPS no proxy de entrada.
- `DJANGO_TRUST_X_FORWARDED_PROTO=1` somente quando o app só puder ser acessado pelo proxy confiável.
- `CORS_ALLOWED_ORIGINS`: lista de origens completas, se um frontend separado precisar chamar a API.
- `DB_PASSWORD` e `MYSQL_ROOT_PASSWORD`: senhas distintas; nunca use os exemplos.
- SMTP (`EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `DEFAULT_FROM_EMAIL`) e
  `PUBLIC_BASE_URL` HTTPS para envio de ativação.

Não há autenticação por cookie/sessão nas rotas da API. CORS não permite credenciais por padrão. Se
um endpoint passar a usar sessão, implemente CSRF para esse endpoint antes de remover sua proteção.

## Licença

MIT — veja [LICENSE](LICENSE).
