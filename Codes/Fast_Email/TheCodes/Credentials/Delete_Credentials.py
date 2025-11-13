import keyring

servico = "gmail_login"
usuario = "xxxxxxx@gmail.com"
keyring.delete_password(servico, usuario)
print("Credencial deletada com sucesso!")
