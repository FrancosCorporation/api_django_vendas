# Resumo — api_django_vendas

## Sessão 2026-10-14 (planejamento padronizado + modernização da CI)

- **Resumo:** SEC/BUG/DEVOPS já concluídos em 2026-10-11. Nesta sessão: CI fixada (Ubuntu 24.04, checkout v7/setup-python v7 por SHA, matriz Python 3.12/3.13). Docs padronizadas.
- **Decisão documentada:** perna 3.14 não incluída — Django 5.2 suporta oficialmente ≤3.13 e o mysqlclient 2.3 falha na construção em interpretadores mais novos; upgrade condicional é OBJ-04.
- **Validações:** CI remota executa `check --deploy`, `makemigrations --check`, `compileall`, `pip-audit` (com libs MySQL do runner); localmente pip-audit não rodou por ausência de headers MySQL no host.
- **Resultado:** [x] CI verde; [x] docs; [x] nada a preservar (`__pycache__` regenerável).
- **Continuidade:** HEAD sincronizado; checkout removível. TEST-01 segue vedado.
