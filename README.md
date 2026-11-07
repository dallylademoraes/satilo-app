# satilo
Projeto para a disciplina de Desenvolvimento Web-Mobile. Este projeto é uma aplicação web e mobile, que permite que o usuário crie sua própria árvore genealógica. O nome Satilo é o sobrenome do meu falecido avô

## Requisitos

- Python 3.11+
- Um projeto no [Supabase](https://supabase.com) com um bucket de Storage (padrão: `media`) para as fotos

## Instalação

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

## Configuração

O projeto lê a configuração de variáveis de ambiente. Use `.env.example` como referência e exporte as variáveis no seu shell:

```bash
export SECRET_KEY="YOUR_SECRET_KEY_HERE"
export SUPABASE_URL="https://YOUR_PROJECT.supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="YOUR_API_KEY_HERE"
```

No PowerShell: `$env:SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"` (e assim por diante).

Sem `DATABASE_URL`, o projeto usa um banco SQLite local (`db.sqlite3`).

## Migrar o banco

```bash
python manage.py migrate
python manage.py createsuperuser   # opcional
```

## Rodar

```bash
python manage.py runserver
```

Acesse http://127.0.0.1:8000/. A API REST fica em `/api/` (autenticação por token em `/api/auth/`).

## Testes

```bash
python manage.py test
```

## Licença

MIT. Veja [LICENSE](LICENSE).
