# 🐾 DevsPets

Aplicação web em Django para adoção de pets — projeto final da disciplina de Python.

## Como rodar o projeto

```bash
# 1. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Rodar as migrações (cria o banco de dados)
python manage.py migrate

# 4. Popular o banco com dados de exemplo (pets, tutor e adotante de teste)
python manage.py seed_demo

# 5. Criar um super usuário para acessar o /admin (opcional se já rodou o seed)
python manage.py createsuperuser

# 6. Rodar o servidor
python manage.py runserver
```

Acesse http://127.0.0.1:8000/

## Logins de teste (criados pelo `seed_demo`)

| Perfil   | Usuário       | Senha         |
|----------|---------------|---------------|
| Tutor    | tutor_demo    | devspets123   |
| Adotante | adotante_demo | devspets123   |

## O que o sistema faz

- Cadastro de usuários como **Tutor** (quem doa um pet) ou **Adotante** (quem quer adotar), com login/logout.
- CRUD completo de **Pet**: um tutor logado pode cadastrar, editar e excluir seus próprios pets.
- Listagem pública de pets disponíveis para adoção, com busca por nome e filtro por espécie/porte.
- Painel do usuário (`/painel/`) mostrando os pets do tutor ou um atalho para o adotante ver os pets disponíveis.
- Painel administrativo (`/admin/`) customizado com busca e filtros para gerenciar Pets, Tutores, Adotantes e Perfis.
- Mensagens de sucesso/erro após ações importantes (cadastro, login, criar/editar/excluir pet).
- Apenas usuários logados e donos do próprio pet podem editar ou excluir — visitantes só podem visualizar.

## Estrutura

- `config/` — configurações do projeto Django (settings, urls raiz).
- `petx/` — app principal: `models.py` (Pet, Tutor, Adotante, Perfil, Raça, Porte, Cor, Anúncio, etc.), `views.py`, `forms.py`, `urls.py`, `templates/`, `static/`.

## Próximos passos (se sobrar tempo)

- Deploy público (ex: PythonAnywhere) — item do checklist da disciplina.
- Upload de imagens reais dos pets (hoje o sistema usa um ícone ilustrativo quando não há foto).
