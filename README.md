# api-django-vendas

Objetivo:

Temos dois tipos de usuarios:

Os consumidores: Podem entrar para ver os produtos, ele podem ver, mas para fazer pedidos eles precisam logar.

Os donos de empresa: Podem entrar cadastrar , editar e deletar os produtos.


Os produtos:

Devem ter categorias para os diferenciar alem de preço



# Modo de instalação:

Executar a instalação dos pacotes:

`
1 -- Install Python Pelo Site : https://www.python.org/downloads/

2 -- install BuildTools     :   pip install buildtools

3 -- install Django   :    pip install django     or  "FORCED"  : python -m pip install --upgrade django --force-reinstall    

4 -- install Git Django : git clone https://github.com/django/django.git

5 --  Change the django clone global :  python -m pip install -e django/

6 -- Remove if in file on django, if error is == true; in final line;

7 -- config the file Settings.py in project:  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.(Your BD selected)',  <----- Remove () Options   (mysql, oracle, postgresql, sqlite3)
        'NAME': 'NameBD',
        'USER':'YourUser',
        'PASSWORD':'YourPassaword',
        'HOST':'IP OF MACHINE',
        'PORT':'Port Acess Libert'
    }
}
  
8 -- Check your BD and if Up , in the past of project run for Up your aplication  : python manage.py runserver 
 
 
 
 Projects:
 
 Verify if exist migrate the Models for BD :  python manage.py makemigrations
 Action on migrate the models for the new BD: python manage.py migrate
 
 
 
 Utility:
 
 For Debug :  pip install djangorestframework
 
 python -m pip install --upgrade
 pip install MySQL-python
 pip install psycopg2

 
 Update:
 
 PIP : python -m pip install --upgrade pip 

 Dev Tools: python -m pip install python-dev-tools --user --upgrade
 
 
 DownGrade:
 
  Downgrade django : pip install -U Django==2.0.0

 
 
 I dont know if this:
 
 pip install django-crispy-forms
`

# Relacionamentos 

Usuario: One (a diferença vai ser o level e o grupo)
- Username	(Char - 20)
- Password	(Char - 30)
- Email		(Email - 40)
- Date Last Login	(Date)
- Date Validade Token	(Date)
- Confirm Token		(Boolean)
- Logged		(Boolean)
- Token   (Text - 60)
- Description (Text - 60)
- Level		(int -  2)
- Group 	(Char - 20)
- Session  (Date)


Produtos: M

- Id 	(AutoIncrement)
- ProdutoName (Char - 40)
- Preço		(Float - 10)
- Desconto (Float - 10)
- Category	(ForenKey)



Category:


- Id 	(AutoIncrement)
- CategoryName (Char - 40)



Pedidos: M

- Id 	(AutoIncrement)
- ProdutoName (Char - 40)
- DataPedido	(Date)
- Status  (Text - 10)





