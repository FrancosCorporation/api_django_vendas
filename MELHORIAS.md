# Melhorias — api_django_vendas

## Diagnóstico

API Django para contas com ativação por e-mail. Os modelos `Products` existem, mas não há endpoints de
catálogo ou pedidos. A aplicação usa um modelo próprio de contas e não autentica por cookie/sessão.

## Estado da execução — 2026-10-11

| Item | Estado | Resultado |
|---|---|---|
| SEC-01 — segredo Django no código | Concluído no código; rotação externa pendente | `DJANGO_SECRET_KEY` obrigatório, mínimo de 50 caracteres e sem fallback de exemplo. A chave antiga permanece no histórico e precisa ser rotacionada nos ambientes que a usaram. |
| SEC-02 — `DEBUG` inseguro | Concluído | `DJANGO_DEBUG` default `False`. |
| SEC-03 — hosts abertos | Concluído | `DJANGO_ALLOWED_HOSTS` exige nomes explícitos e rejeita `*`. |
| SEC-04 — CORS aberto | Concluído | Allowlist explícita, vazia por padrão; credenciais CORS desativadas. |
| SEC-05/07 — autenticação e CSRF | Concluído | Credenciais no corpo de POST; sessão via `Authorization: Bearer`; rotas protegidas usam apenas token e escopo da própria conta. `csrf_exempt` fica somente nas rotas token-only; ativação usa token único de e-mail. |
| SEC-06 / BUG-01/02 — token malformado e exceções | Concluído | Removidos `except:` genéricos da autenticação; token de sessão lido apenas do Bearer; falha de banco não vira “não autenticado”. |
| BUG-03 — token sem validade/logout | Concluído | Token aleatório expira em uma hora, é rotacionado no login e invalidado no logout; ativação é de uso único e expira em 24 horas. |
| TEST-01 — testes | Pendente | Nenhum teste foi adicionado ou executado nesta execução. |
| DEVOPS-04 — cookies/HTTPS | Concluído | Cookies seguros em produção, redirect HTTPS, HSTS por um ano e headers de segurança. HSTS preload fica desativado até revisar domínio/subdomínios. |
| DEVOPS-01/02 — CI e dependências | Concluído | CI roda check de deploy, verificação de migrações, compilação e `pip-audit`; dependências runtime fixadas. |
| DEVOPS-03/05 — configuração | Concluído | `.env.example` criado, `.env` ignorado, arquivo de exemplo antigo removido e segredos explicitados no Compose. |
| DOC-01 — documentação | Concluído | README lista rotas reais, contrato Bearer e configuração de produção. `SECURITY.md` criado. |
| Infra — implantação local | Concluído | Docker multi-stage, Gunicorn, usuário sem privilégios, banco privado, publicação local em loopback e migração inicial do app. |
| Configuração Vercel antiga | Removida | `vercel.json` continha configuração inválida; Docker Compose é o caminho local documentado. |

## Validação realizada

- `python -m compileall -q app firstapi others manage.py` — passou.
- `git diff --check` — passou.
- Build da imagem Docker — passou.
- `python manage.py check --deploy` — passou com o aviso não bloqueante `security.W021` porque preload está desativado deliberadamente.
- `python manage.py makemigrations --check --dry-run` — sem diferenças após ajustar a migração inicial; o comando avisa que não pôde consultar o histórico porque nenhum MySQL foi iniciado.
- `pip-audit` no ambiente do container — nenhuma vulnerabilidade conhecida.
- Nenhum serviço foi iniciado e nenhuma suíte de testes foi executada.

## Mudança de contrato da API

- Cadastro e login agora recebem JSON em `POST`; credenciais por query string não são aceitas.
- Rotas autenticadas usam `Authorization: Bearer <token>`; token em query/body não autentica.
- Atualização requer `current_password`; alteração de senha requer `new_password` e encerra a sessão atual.
- Novos logins invalidam a sessão anterior da mesma conta.
- Clientes antigos precisam migrar para esse contrato antes de publicar a atualização.

## Ações externas pendentes

1. Gerar e configurar uma nova `DJANGO_SECRET_KEY`; invalidar sessões antigas e rotacionar qualquer chave de banco que tenha sido usada fora de ambiente local.
2. Limpar o histórico Git antigo somente em coordenação com quem já clonou o repositório; não foi feito force push.
3. Preencher `.env` com senhas distintas, SMTP, hosts reais, `PUBLIC_BASE_URL` HTTPS e origens CORS necessárias antes de publicar.
4. Avaliar HSTS preload apenas depois de confirmar controle de todos os subdomínios.
5. Atualizar os clientes que ainda enviam credenciais/token na query string.
