import keyring

servico = "gmail_login"
usuario = "pedrotigershowfoda@gmail.com"
keyring.delete_password(servico, usuario)
print("Credencial deletada com sucesso!")
