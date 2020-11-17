# api-django-vendas

Objetivo:

Temos dois tipos de usuarios:

Os consumidores: Podem entrar para ver os produtos, ele podem ver, mas para fazer pedidos eles precisam logar.

Os donos de empresa: Podem entrar cadastrar , editar e deletar os produtos.


Os produtos:

Devem ter categorias para os diferenciar alem de preço





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
- fotos (img) podem ser mais de uma



Category:


- Id 	(AutoIncrement)
- CategoryName (Char - 40)



Pedidos: M

- Id 	(AutoIncrement)
- ProdutoName (Char - 40)
- DataPedido	(Date)
- Status  (Text - 10)
- usuario () ForenKey - Users





