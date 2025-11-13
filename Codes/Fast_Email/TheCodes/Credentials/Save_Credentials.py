import keyring

servico = "gmail_login"
usuario = input("Digite seu e-mail do Gmail: ")
senha = input("Digite sua senha do Gmail: ")

def salvar_senha():
    keyring.set_password(servico, usuario, senha)
    print(f"Credenciais salvas com sucesso para {usuario}!")


if __name__ == "__main__":
    salvar_senha()
