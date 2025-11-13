import keyring
from Save_Credentials import servico, usuario

try:
    keyring.delete_password(servico, usuario)
    print(f"Credenciais de '{usuario}' em '{servico}' deletadas com sucesso!")
except keyring.errors.PasswordDeleteError:
    print("Erro: Não foi possível deletar. Credencial inexistente ou erro no cofre do sistema.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
