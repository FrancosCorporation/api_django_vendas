# Plan — api_django_vendas

## 1. Visão geral
API Django 5.2 + DRF de contas com ativação por e-mail e tokens Bearer de 1h com rotação; endurecida em 2026-10-11 (segredo por env, DEBUG/hosts/CORS fechados, cookies seguros, migrations verificadas em CI).

## 2. Arquitetura e tecnologias
Django 5.2.18, DRF 3.18, mysqlclient 2.3, gunicorn 27 não declara, `gunicorn 26.2`; MySQL via env `DB_*`; Docker/Compose. CI: `manage.py check --deploy`, `makemigrations --check`, `compileall`, `pip-audit`, em Python **3.12/3.13** (3.14 requer mysqlclient novo/Django 6).

## 3. Funcionalidades existentes
- [x] SEC-01..07, BUG-01..03, DEVOPS-04 concluídos (2026-10-11).
- [x] CI com verificação estática/auditoria — **modernizada nesta sessão** (Ubuntu 24.04, checkout v7, setup-python v7, matriz 3.12/3.13).

## 4. Objetivos futuros
- OBJ-01 (P2, concluído nesta sessão): CI previsível com matriz de Python suportado.
- OBJ-02 (P3): TEST-01 — suíte pytest/django-test com banco de testes (vedada nesta esteira).
- OBJ-03 (P3, externo): rotação da `DJANGO_SECRET_KEY` antiga exposta no histórico (ação do dono nos ambientes).
- OBJ-04 (P3): avaliar upgrade Django 6 + Python 3.14 quando mysqlclient suportar.

## 5–9. Melhorias / Roadmap / Riscos / Ideias
- Risco externo: credencial Django antiga no histórico — rotação pendente (não reescrever histórico).
- Sem testes na esteira: verificar comportamento de ativação por e-mail apenas quando TEST-01 for liberado.

*(Gerado em 2026-10-14 pelo agente orquestrador)*
