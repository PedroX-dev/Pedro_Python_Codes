import keyring

servico = "gmail_login"
usuario = input("Digite seu e-mail do Gmail: ")
senha = input("Digite sua senha do Gmail: ")

#  Salva no cofre seguro do sistema
keyring.set_password(servico, usuario, senha)

print(f"Credenciais salvas com sucesso para {usuario}!")
