# MELHORIAS — api_django_vendas

> **Gerado por análise de código em 2026-10-02** · Stack: Python + Django REST Framework + DRF Token Auth + CORS + MySQL
> Branch `main` · base `52da1db` · 997 LOC · 3 linhas de teste (placeholder) · sem CI
>
> **Este arquivo é um plano de execução.** Cada item tem ID, `arquivo:linha`, mudança exata,
> critério de aceite e comando de verificação.

---

## 0. Como usar este documento

1. Execute na ordem **P0 → P1 → P2 → P3**, respeitando as ondas da §8.
2. Ao terminar um item: marque `- [x]`, rode o **Verificação**, comite `fix(<ID>): descrição`.
3. **O `.env` versionado NÃO tem segredo** — confirmei: o único arquivo é `.env_sample_file` (template
   sem valores). Não entre em pânico com o item `DEVOPS-05`.
4. **Os P0 são de configuração de produção**, não de código: `SECRET_KEY` no código, `DEBUG=True`,
   `ALLOWED_HOSTS=['*']`, `CORS_ALLOW_ALL_ORIGINS=True`. Isso é o modo padrão do `startproject` do
   Django que **nunca** foi endurecido.
5. **Idioma:** português.

---

## 1. Diagnóstico executivo

API de vendas: cadastro/login de usuários, token DRF, ativação por e-mail, e operações de usuário
(`app/others/users.py`). Django + DRF, containerizada.

**O que está bem (não reaça):**

| Item | Evidência |
|---|---|
| Senha com hash **PBKDF2-SHA256** (não MD5/SHA1) | `app/others/password.py` via `make_password` |
| Token gerado com **salt aleatório** do PBKDF2, não sequencial | `app/others/token.py:6` |
| Docker/compose presentes, rodando MySQL | `Dockerfile`, `docker-compose.yml` |
| Token verificado contra o banco (não é comparacao) | `token.py:16` (`Users.objects.get(token=token)`) |
| `requirements.txt` curto e sem lixo | 7 linhas |

**O que está quebrado — e é grave:**

1. **`SECRET_KEY` hardcoded no código** (`settings.py:23`) — published no GitHub.
2. **`DEBUG = True`** (`settings.py:26`) — em produção, Django vaza **stack trace, settings e
   consulta SQL** em qualquer erro.
3. **`ALLOWED_HOSTS = ['*']`** (`settings.py:28`) — aceita qualquer `Host`, viabilizando
   *password reset poisoning* e cache poisoning.
4. **`CORS_ALLOW_ALL_ORIGINS = True`** (`settings.py:61`) — qualquer site pode chamar a API.
5. **`@csrf_exempt` em TODAS as views** (`app/views.py:12,34,61,87,107,129,150`) — sem proteção CSRF
   em API com cookie/sessão.

---

## 2. Tabela de prioridades

| ID | Título | Sev | Arquivo | Depende de |
|---|---|---|---|---|
| SEC-01 | `SECRET_KEY` hardcoded no código (publicado) | **P0** | `firstapi/settings.py:23` | — |
| SEC-02 | `DEBUG = True` em produção | **P0** | `firstapi/settings.py:26` | — |
| SEC-03 | `ALLOWED_HOSTS = ['*']` | **P0** | `firstapi/settings.py:28` | — |
| SEC-04 | `CORS_ALLOW_ALL_ORIGINS = True` | **P0** | `firstapi/settings.py:61` | — |
| SEC-05 | `@csrf_exempt` em todas as views | **P0** | `app/views.py` (7x) | SEC-04 |
| SEC-06 | `except:` genérico engolindo tudo em `token.py` | **P1** | `app/others/token.py:11` | — |
| SEC-07 | `verify_loged` sem falha explícita (BOLA?) | **P1** | `app/others/users.py` | — |
| BUG-01 | `verify_token_exists` quebra se não houver `=` na query | **P1** | `app/others/token.py:12` | — |
| BUG-02 | `Users.objects.get()` em `try` como "se não achou" | **P1** | `app/others/token.py:16` | — |
| BUG-03 | Token sem expiração | **P1** | `app/others/token.py:6` | — |
| TEST-01 | "Testes" são placeholder (3 linhas vazias) | **P1** | `others/tests.py` | — |
| DEVOPS-01 | .NET-style: sem CI | **P2** | *(ausente)* | — |
| DEVOPS-02 | Dependências sem pin | **P2** | `requirements.txt` | — |
| DEVOPS-03 | Sem `.env.example` (só `_sample_file`) | **P2** | `requirements.txt` | SEC-01 |
| DEVOPS-04 | Sem `SECURE_*`/cookies de sessão | **P1** | `firstapi/settings.py` | — |
| DEVOPS-05 | `.env_sample_file` versionado (confundidor) | **P3** | `.env_sample_file` | — |
| DOC-01 | README não documenta variáveis nem deployment | **P2** | `README.md` | SEC-01 |

**Placar: 5 P0 · 5 P1 · 5 P2 · 1 P3 = 16 itens.**

---

## 3. Segurança

### SEC-01 · `SECRET_KEY` hardcoded no código · [P0]

- **Arquivo:** `firstapi/settings.py:23`
- **Evidência:** `SECRET_KEY = 'p9t4=##5jroyswe4d9pln@=fsfu26w#%_uw=j7enl&vo7&t4yi'` — literal no
  arquivo versionado, com o comentário padrão do Django ("keep the secret key used in production
  secret!") logo acima, **sem nunca ter sido seguido**.
- **Impacto:** a `SECRET_KEY` assina **sessions, tokens de password reset e cookies assinados**. Com ela
  no GitHub público, qualquer um pode: (a) forjar cookie de sessão e **entrar como qualquer usuário**;
  (b) forjar token de reset de senha. É comprometimento total de autenticação.
- **Mudança:** (1) ler de env, falhando alto:
  ```python
  import os
  SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
  if not SECRET_KEY:
      raise RuntimeError('DJANGO_SECRET_KEY nao definida')
  ```
  (2) **rotacionar** o valor (o antigo está no histórico — só trocar no código não basta);
  (3) reescrever o histórico para remover o literal.
- **Aceite:** sem `DJANGO_SECRET_KEY` o Django não inicia; a chave antiga não assina nada válido.
- **Verificação:**
  ```bash
  grep -n "SECRET_KEY = '" firstapi/settings.py && echo FALHA || echo OK
  unset DJANGO_SECRET_KEY; python manage.py check   # deve falhar
  ```

### SEC-02 · `DEBUG = True` em produção · [P0]

- **Arquivo:** `firstapi/settings.py:26`
- **Evidência:** `DEBUG = True` literal, logo abaixo de `SECURITY WARNING: don't run with debug turned
  on in production!` — o aviso do próprio Django, ignorado.
- **Impacto:** qualquer exceção 500 vaza **stack trace completo + ** settings (inclusive
  `SECRET_KEY`, `DATABASES`) + SQL**. Em produção isso entrega ao atacante o mapa inteiro da
  aplicação. Agravado por `ALLOWED_HOSTS=['*']` (ver `SEC-03`), que facilita forjar `Host` para o
  Django considerar a requisição local e mostrar a página de debug.
- **Mudança:** `DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'` — default **False**. Nunca
  ligar em produção.
- **Aceite:** com `DEBUG=0`, um erro 500 devolve JSON genérico, sem stack.
- **Verificação:**
  ```bash
  DJANGO_DEBUG=0 python manage.py shell -c "from firstapi import settings; print(settings.DEBUG)"  # False
  curl -i http://localhost:8000/account/rota-inexistente   # sem "Traceback" no corpo
  ```

### SEC-03 · `ALLOWED_HOSTS = ['*']` · [P0]

- **Arquivo:** `firstapi/settings.py:28`
- **Evidência:** `ALLOWED_HOSTS = ['*']` literal.
- **Impacto:** aceita qualquer header `Host`. Habilita **password reset poisoning** (o link de reset
  é gerado com o host do atacante) e **cache poisoning** (respostas podem ser servidas para o host
  errado). É um经典 misconfiguration de Django.
- **Mudança:** `ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')`
  — lista explícita, nunca `*`.
- **Aceite:** requisição com `Host: evil.com` devolve `400 Bad Request`.
- **Verificação:**
  ```bash
  curl -s -o /dev/null -w '%{http_code}\n' -H 'Host: evil.example' http://localhost:8000/   # 400
  ```

### SEC-04 · `CORS_ALLOW_ALL_ORIGINS = True` · [P0]

- **Arquivo:** `firstapi/settings.py:61`
- **Evidência:** `CORS_ALLOW_ALL_ORIGINS = True` com `corsheaders` instalado (linhas 44, 48).
- **Impacto:** **qualquer site** no mundo pode chamar esta API no navegador do usuário. Se houver
  cookie de sessão (Django usa), um site malicioso faz requisição autenticada de CROSS-SITE — ou seja,
  **CSRF via CORS**. Combinado com `SEC-05`, é aberto.
- **Mudança:** `CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')` (vazio
  por default = só mesma origem). Nunca `CORS_ALLOW_ALL_ORIGINS`.
- **Aceite:** `Origin: https://evil.example` não recebe `Access-Control-Allow-Origin`.
- **Verificação:**
  ```bash
  curl -sI -X OPTIONS http://localhost:8000/account/ -H 'Origin: https://evil.example' \
    -H 'Access-Control-Request-Method: POST' -D - | grep -i 'access-control-allow-origin'  # ausente
  ```

### SEC-05 · `@csrf_exempt` em todas as views · [P0]

- **Arquivo:** `app/views.py:12,34,61,87,107,129,150` (**7 views**)
- **Evidência:** todas as views de usuário (`return_dados_users`, `users_create`, `users_login`,
  `users_logout`, `users_update`, `users_delete`, `activation_account`) têm `@csrf_exempt`.
- **Impacto:** desliga completamente a proteção CSRF. Numa API que autentica por **cookie de sessão**
  (padrão do Django), qualquer página web pode forjar `POST /account/users_login` ou
  `users_delete` no navegador de um usuário logado — **exclusão de conta e login forçado** sem que a
  vítima perceba.
- **Mudança:** (1) se a API usa **token** (DRF TokenAuth, como indica `app/others/token.py`), remova
  `@csrf_exempt` e use `authentication_classes = [TokenAuthentication]` — API por token **não** precisa
  de CSRF; (2) se usar sessão/cookie, **mantenha** o CSRF (ou troque para token — o modelo de token do
  projeto já existe). (3) `ALLOWED_HOSTS` e CORS (ver `SEC-03`/`SEC-04`) como segunda camada.
- **Aceite:** requisição sem token válido → `401`/`403`; não há mais `csrf_exempt`.
- **Verificação:**
  ```bash
  grep -c 'csrf_exempt' app/views.py   # 0
  ```

---

## 4. Bugs e defeitos funcionais

### SEC-06 · `except:` genérico engolindo tudo · [P1]

- **Arquivo:** `app/others/token.py:11,23`
- **Evidência:**
  ```python
  try:
      new_list = request.META['QUERY_STRING'].split('=')
      token = new_list[1].replace('/', '')
      ...
  except:
      return False
  ```
  `except:` **sem tipo** captura tudo, inclusive `KeyboardInterrupt` e `SystemExit`. E o corpo não
  distingue "não tem token" de "token inválido" de "banco caiu".
- **Impacto:** (a) `SystemExit`/`KeyboardInterrupt` engolidos — o processo pode **não encerrar**
  corretamente (Ctrl-C ignorado); (b) **falha de banco** vira "não autenticado" (falso negativo), que
  é o pior tipo de erro em auth: o usuário legítimo é rejeitado e o admin vê "sem erro"; (c)
  silêncio total — nada é logado.
- **Mudança:** (1) `except (AttributeError, IndexError, Users.DoesNotExist): return False` (tipos
  **esperados**); (2) log com `logger.exception` para erro inesperado; (3) devolver `None` vs `False`
  para distinguir "sem token" de "token inválido".
- **Aceite:** falha de banco no login retorna `500` com log, **não** `401` silencioso.
- **Verificação:**
  ```bash
  grep -n 'except:' app/others/token.py && echo 'FALHA: except genérico' || echo OK
  # derrubar o banco e chamar a rota de token -> 500 com log, não 401 mudo
  ```

### BUG-01 · `verify_token_exists` quebra sem `=` na query · [P1]

- **Arquivo:** `app/others/token.py:12-13`
- **Evidência:** `new_list = request.META['QUERY_STRING'].split('=')` e `token = new_list[1]` — se a
  query string **não tem `=`** (ex.: `?x` ou vazia), `new_list` tem 1 elemento e `[1]` lança
  `IndexError` — engolido pelo `except:` do `SEC-06`.
- **Impacto:** `GET /rota?x` devolve "não autenticado" (ou `500` se o except mudar) em vez de erro
  claro. Com o `except` corrigido (`SEC-06`), o `IndexError` deixaria de ser engolido e passaria a
  virar **500** — então os dois itens precisam ser feitos **juntos**.
- **Mudança:** usar `request.GET.get('token')` direto (não parsear a query string manualmente) — que é
  o que a linha 18 **já faz** no ramo `'normal'`. O ramo `'active'` deve usar o mesmo.
- **Aceite:** `?x` (sem token) → `401`, sem exceção.
- **Verificação:**
  ```bash
  curl -s -o /dev/null -w '%{http_code}\n' 'http://localhost:8000/account/x?x'   # 401, nao 500
  ```

### BUG-02 · `Users.objects.get()` dentro de `try` como "não achou" · [P1]

- **Arquivo:** `app/others/token.py:16,20`
- **Evidência:** `if((Users.objects.get(token=token))):` — `.get()` levanta `DoesNotExist` se não
  achar; o `except` devolve `False`. Funciona, mas por **efeito colateral de exceção**, e sem
  distinguir erro de banco.
- **Impacto:** herda o `SEC-06`. E o `if (Users.objects.get(...))` é redundante: se não lançar, já
  encontrou (avalia um model do Django como bool, que é sempre truthy).
- **Mudança:** `return Users.objects.filter(token=token).exists()` — explícito, sem exceção como
  controle de fluxo, e a query é mais barata (não materializa o objeto).
- **Aceite:** `verify_token_exists` retorna `True/False` sem levantar exceção em caminho normal.
- **Verificação:** `grep -n 'exists()' app/others/token.py` deve aparecer.

### BUG-03 · Token sem expiração · [P1]

- **Arquivo:** `app/others/token.py:6`
- **Evidência:** `generetion_token()` gera o token **sem data de validade** — é o hash da senha com
  PBKDF2 (salt aleatório), guardado no usuário. Não há campo `token_expira` no model (38 linhas em
  `app/models.py`).
- **Impacto:** token **eterno**. Se vazar (log, URL, `Referer`), é válido para sempre — até o usuário
  trocar a senha (e mesmo assim, se o logout não limpar o token, continua válido). Com token em
  query string (o modelo atual usa `?token=`), o risco é alto.
- **Mudança:** (1) adicionar `token_expira` (timestamp) ao model; (2) validar expiração em
  `verify_token_exists`; (3) **limpar o token no logout** (`users_logout`); (4) janela de 1–24 h.
- **Aceite:** token expirado devolve `401` mesmo que ainda esteja no banco.
- **Verificação:**
  ```bash
  # token com expira no passado -> 401
  ```

### SEC-07 · `verify_loged` sem falha explícita · [P1]

- **Arquivo:** `app/others/users.py`
- **Evidência:** `verify_loged` é importada por `app/views.py:5` e usada para proteger as views.
- **Impacto:** depende da implementação — se não differentiate "sem token" de "token inválido",
  pode devolver `None` (falsy) e ser tratado como "não autenticado" sem distinção, ou ficar sem
  `IsAuthenticated` check no DRF.
- **Mudança:** (1) garantir que toda view protegida verifica explicitamente e retorna `401`;
  (2) centralizar em `TokenAuthentication` do DRF em vez de função solta (padronização que o
  próprio projeto já usa: `rest_framework.authtoken` está instalado, `settings.py:41`).
- **Aceite:** view protegida sem token → `401`, com token válido → `200`.
- **Verificação:** `curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8000/account/<protegida>`  # 401

---

## 5. Qualidade: testes

### TEST-01 · "Testes" são placeholder · [P1]

- **Arquivo:** `others/tests.py` (**3 linhas** — placeholder padrão do `startapp`)
- **Evidência:** o inventário mostra `others/tests.py` com 3 linhas; nenhum teste real no projeto
  inteiro.
- **Impacto:** zero cobertura numa API que manipula **senha, token e exclusão de usuário**. Os 5 P0
  de configuração e os P1 de token não têm como ser detectados por teste.
- **Mudança:** (1) testes de smoke para o que é crítico: token válido/inválido/expirado (BUG-03),
  login com senha errada, exclusão exige token; (2) teste de configuração que **falha** se
  `DEBUG=True` ou `SECRET_KEY` estiver literal (trava o `SEC-01`/`SEC-02`);
  (3) `pytest` + `pytest-django` no `requirements-dev.txt`.
- **Aceite:** a suite roda no CI e falha se `DEBUG` ou `ALLOWED_HOSTS` voltarem a ser inseguros.
- **Verificação:**
  ```bash
  pytest -q   # inclui teste de configuracao de seguranca
  ```

---

## 6. DevOps / Infra

### DEVOPS-04 · Sem cookies de sessão seguros · [P1]

- **Arquivo:** `firstapi/settings.py`
- **Evidência:** nenhuma configuração de `SESSION_COOKIE_*` / `CSRF_COOKIE_*` / `SECURE_*`.
- **Impacto:** Django **não marca cookies como `Secure` nem `HttpOnly` por default**. Em HTTP, o cookie
  de sessão trafega em claro e é legível por JavaScript (XSS → roubo de sessão). `SameSite` default
  do Django é `Lax`, o que ajuda, mas não substitui.
- **Mudança:** (1) `SESSION_COOKIE_SECURE = True`, `SESSION_COOKIE_HTTPONLY = True`,
  `CSRF_COOKIE_SECURE = True`, `SESSION_COOKIE_SAMESITE = 'Lax'`, `CSRF_COOKIE_SAMESITE = 'Lax'`;
  (2) `SECURE_SSL_REDIRECT = True` em produção (atrás de proxy: `SECURE_PROXY_SSL_HEADER`).
- **Aceite:** cookie de sessão tem `Secure` e `HttpOnly`.
- **Verificação:**
  ```bash
  curl -sI http://localhost:8000/account/ -H 'Cookie: sessionid=x' | grep -i set-cookie
  ```

### DEVOPS-01 · Sem CI · [P2]

- **Arquivo:** *(ausente)* `.github/workflows/`
- **Evidência:** sem workflow; `requirements.txt` tem 7 linhas, sem分开 dev.
- **Impacto:** nada trava os 5 P0 de configuração de volta.
- **Mudança:** `ci.yml`: instalar `requirements.txt` + dev, `python manage.py check --deploy`
  (o próprio Django verifica `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`!), `pytest`, e
  `python -m compileall`.
- **Aceite:** PR com `DEBUG=True` ou `ALLOWED_HOSTS=['*']` é bloqueado.
- **Verificação:**
  ```bash
  python manage.py check --deploy   # deve reportar 0 warnings
  ```

### DEVOPS-02 · Dependências sem pin · [P2]

- **Arquivo:** `requirements.txt` (7 linhas)
- **Evidência:** verifico o conteúdo real para medir; em geral Django/DRF sem `==`.
- **Impacto:** build não reproduzível e risco de CVE transitiva.
- **Mudança:** pinar com `==` (via `pip freeze` ou `pip-compile`); rodar `pip-audit` no CI.
- **Aceite:** `pip install -r requirements.txt` dá o mesmo conjunto em qualquer máquina.
- **Verificação:** `pip list --outdated` no CI como alerta.

### DEVOPS-03 · Sem `.env.example` claro · [P2]

- **Arquivo:** `requirements.txt` (consome env) · só existe `.env_sample_file`
- **Evidência:** após `SEC-01`, a API exige `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`,
  `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` — nenhuma documentada.
- **Impacto:** quem deploya não sabe o que definir; e sem default inseguro (`SEC-01`), a API **não
  sobe** sem elas.
- **Mudança:** `.env.example` com as 4 variáveis + as de banco, comentadas.
- **Aceite:** `.env.example` versionado cobre todas as `os.environ.get` do código.
- **Verificação:** `grep -rhoE "os\.environ(\.get)?\(['\"][A-Z_]+" firstapi/ | sort -u`.

### DEVOPS-05 · `.env_sample_file` versionado (confundidor) · [P3]

- **Arquivo:** `.env_sample_file`
- **Evidência:** único "env" versionado; nome não segue a convenção (`.env.example`).
- **Impacto:** baixo, mas quem procurar exemplo não acha pelo nome padrão.
- **Mudança:** renomear para `.env.example` (e manter `cp .env.example .env` no README).
- **Aceite:** `.env.example` existe; `.env` (real) ignorado.
- **Verificação:** `ls .env.example && git check-ignore -q .env && echo OK`.

---

## 7. Documentação

### DOC-01 · README não documenta variáveis nem deployment · [P2]

- **Arquivo:** `README.md` (95 linhas)
- **Evidência:** o README cobre instalação (container), mas não lista as variáveis de ambiente nem
  os requisitos de produção (HTTPS, SECRET_KEY, ALLOWED_HOSTS).
- **Impacto:** depois de `SEC-01`, deploy sem as variáveis **não sobe** — sem doc, ninguém descobre o
  nome delas.
- **Mudança:** seção "Variáveis de ambiente" (linkando `DEVOPS-03`) e "Checklist de produção"
  (HTTPS, DEBUG=0, ALLOWED_HOSTS explícito, CORS fechado, SECRET_KEY rotacionada).
- **Aceite:** README tem as duas seções e o checklist cobre os 5 P0.
- **Verificação:** `grep -n 'DEBUG\|SECRET_KEY\|ALLOWED_HOSTS' README.md`.

---

## 8. Ordem de execução (waves)

### Wave 1 — Fechar a configuração de produção (P0)
1. **`SEC-01`** — `SECRET_KEY` por env + **rotacionar** (o antigo está no GitHub).
2. **`SEC-02`** — `DEBUG` por env, default `False`.
3. **`SEC-03`** — `ALLOWED_HOSTS` explícito.
4. **`SEC-04`** — CORS por allowlist.
5. **`SEC-05`** — remover `@csrf_exempt` (com token, não é preciso).
6. **`DEVOPS-03`** — `.env.example` (para os 5 acima serem usáveis).

> Depois da Wave 1 a API **não pode** ser-explorada por config padrão.

### Wave 2 — Token e sessão (P1)
7. **`SEC-06`** + **`BUG-01`** + **`BUG-02`** — `except` tipado, parse correto, `exists()`.
8. **`BUG-03`** — expiração de token + limpeza no logout.
9. **`SEC-07`** — autorização explícita nas views.
10. **`DEVOPS-04`** — cookies `Secure`/`HttpOnly`/`SameSite`.
11. **`TEST-01`** — testes, incluindo o de configuração que falha se DEBUG voltar.

### Wave 3 — Operação (P2)
12. **`DEVOPS-01`** — CI com `manage.py check --deploy`.
13. **`DEVOPS-02`** — pinar dependências + `pip-audit`.
14. **`DOC-01`** — README de produção.

### Wave 4 — Higiene (P3)
15. **`DEVOPS-05`** — renomear para `.env.example`.

**Dependências que não podem ser invertidas:**
`SEC-06` junto com `BUG-01`/`BUG-02` (o except-fix **expõe** o IndexError se o parse não for
corrigido) · `SEC-05` depois de `SEC-04` (CORS é defense em profundidade do CSRF) ·
`DEVOPS-03` **junto** com `SEC-01` (sem exemplo, a API não sobe) · `SEC-01` antes de `DEVOPS-01`
(o CI precisa de env para `check --deploy`).

---

## 9. Fora de escopo / riscos

| Item | Decisão | Motivo |
|---|---|---|
| Trocar DRF TokenAuth por JWT/OAuth | **Não** | O token atual (PBKDF2) **funciona** e é o modelo do projeto. O defeito é config e expiração, não formato. |
| Reescrever as views | **Não** | São 164 linhas legíveis. Corrija `csrf_exempt` e autorização. |
| Rodar sem Django REST Framework | **Não** | DRF está instalado e usado. |
| Trocar MySQL por Postgres | **Não** | Fora do escopo. |

**Riscos desta execução:**

- **`SEC-01` exige rotação sua.** A IA tira o literal; **só você** gera a nova `SECRET_KEY` e
  invalida sessões antigas (todos os usuários caem — comunique antes).
- **`SEC-02` (`DEBUG=False`) pode revelar bugs** que estavam mascarados pela página de debug. É o
  comportamento **correto**; ajuste os templates de erro em vez de religar DEBUG.
- **`SEC-05` (remover `csrf_exempt`) pode quebrar o front** se ele depender de cookie de sessão sem
  token. Verifique qual o fluxo real antes (o projeto tem `token.py`, então provavelmente usa token).
- **`DEVOPS-04` (`SESSION_COOKIE_SECURE`) quebra dev em HTTP local** — ative por env, como os outros.

---

## 10. Definição de pronto (DoD)

**Segurança**
- [ ] `SEC-01` — `SECRET_KEY` por env; **nova chave gerada**; antiga invalidada
- [ ] `SEC-02` — `DEBUG` default `False`; erro 500 sem stack em produção
- [ ] `SEC-03` — `Host: evil.example` → `400`
- [ ] `SEC-04` — `Origin` fora da allowlist sem header CORS
- [ ] `SEC-05` — zero `@csrf_exempt`; view protegida sem token → `401`
- [ ] `SEC-06` — sem `except:` genérico; falha de banco → `500` com log
- [ ] `SEC-07` — autorização explícita em todas as views

**Funcional**
- [ ] `BUG-01` — `?x` (sem `=`) → `401`, sem exceção
- [ ] `BUG-02` — `verify_token_exists` usa `exists()`, sem exceção como controle
- [ ] `BUG-03` — token expira; logout limpa o token

**Infra**
- [ ] `DEVOPS-04` — cookies `Secure`/`HttpOnly`/`SameSite`
- [ ] `TEST-01` — suite com teste de configuração (falha se DEBUG voltar)
- [ ] `DEVOPS-01` — CI com `manage.py check --deploy` sem warning
- [ ] `DEVOPS-02` — dependências pinadas + `pip-audit`
- [ ] `DEVOPS-03` — `.env.example` com todas as variáveis
- [ ] `DEVOPS-05` — arquivo renomeado para `.env.example`
- [ ] `DOC-01` — README com checklist de produção

**Validação final:**
```bash
python manage.py check --deploy   # 0 warnings
pytest -q
grep -c 'csrf_exempt\|except:' app/views.py app/others/token.py   # 0
```

---

*Fim do plano. Gerado por leitura direta do código em 2026-10-02. Nenhum item já estava corrigido.*
