Urls:

    Os usuarios vão ser criados por esses metodos

url /account
Com Metodo Get : Pega os dados do usuario   (Necessario : token)
Com Metodo Post : Criação de usuario        (Necessario : username , email, password)
Com Metodo Put :  Alteracao de usuario      (Necessario : token) & (informações a serem alteradas, (username ou password))
Com Metodo Delete : Deleta o usuario        (Necessario : token, front end (confirmacao de certeza do usuario) ) nao tem volta


url /account/login
Com metodo Post : Faz o login para usar as funcionar que sao necessario o token  (Necessario : email e senha)
                                                                                 (recebe : Token)

url /account/logout
Com metodo Post : Faz o logout, usuario nao pode mais usar as funcoes  (Necessario : token)

url /account/all
Com metodo Get :  Voce pode ver todos os usuarios, desde que seja um usuario que tenha permissao

url /account/activation
Com metodo Get: Voce podera fazer a ativacao da conta, com a url enviada para o email 