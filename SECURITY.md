# Política de segurança

Envie relatos privados pelo recurso [Security Advisories do GitHub](https://github.com/FrancosCorporation/api_django_vendas/security/advisories/new).
Inclua passos para reproduzir sem publicar credenciais, dados pessoais ou tokens ativos.

## Configuração

- `DJANGO_SECRET_KEY` e credenciais de banco/SMTP devem vir do ambiente ou de um gerenciador de segredos.
- Não habilite `DJANGO_DEBUG` em produção. Liste hosts específicos em `DJANGO_ALLOWED_HOSTS`.
- Use HTTPS; configure `DJANGO_TRUST_X_FORWARDED_PROTO=1` somente atrás de um proxy confiável que seja o único caminho até a aplicação.
- HSTS cobre subdomínios por padrão em produção; confirme que eles também atendem HTTPS antes de publicar.
- Tokens de sessão usam `Authorization: Bearer`, expiram em uma hora e são invalidados no logout/novo login. Não os registre em logs ou URLs.
- O token de ativação é de uso único, expira em 24 horas e aparece apenas no link enviado ao e-mail da conta.
- CORS fica fechado por padrão e não permite cookies. Defina origens completas apenas quando necessário.

A chave e credenciais de banco que constavam no histórico antigo devem ser rotacionadas em qualquer ambiente que as tenha usado.
Limpar esse valor do histórico remoto exige coordenar com quem clonou o repositório; nenhuma reescrita
forçada de histórico é feita nesta atualização.
