import keyring
from playwright.sync_api import sync_playwright
import os
import shutil
import tempfile
import time
import psutil
import logging
import pygetwindow as gw
import tkinter as tk
from tkinter import scrolledtext, messagebox



# -------------------------
# Configuração de logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# -------------------------
# Configurações de ambiente
# -------------------------
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Users\pedro.lopes\AppData\Local\Google\Chrome\Application\chrome.exe",
]

ORIG_USER_DATA = r"C:\Users\pedro.lopes\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Default"
SERVICO = "gmail_login"

# -------------------------
# Utilitários
# -------------------------
def get_chrome_path():
    for path in CHROME_PATHS:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Chrome não encontrado! Verifique o caminho.")

def kill_chrome_processes():
    logger.info("Encerrando processos do Chrome...")
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                proc.kill()
        except Exception:
            pass
    time.sleep(1)

def get_credentials(service_name: str):
    usuarios = []
    for backend in keyring.backend.get_all_keyring():
        try:
            cred = backend.get_credential(service_name, None)
            if cred:
                usuarios.append(cred.username)
        except Exception:
            pass

    if not usuarios:
        raise ValueError("Nenhuma credencial encontrada! Execute 'salvar_credenciais.py' primeiro.")

    usuario = usuarios[0]
    senha = keyring.get_password(service_name, usuario)
    logger.info(f"Credenciais recuperadas para: {usuario}")
    return usuario, senha

def make_profile_copy(orig_user_data, profile_name):
    orig_profile_path = os.path.join(orig_user_data, profile_name)
    if not os.path.exists(orig_profile_path):
        raise FileNotFoundError(f"Perfil original não encontrado: {orig_profile_path}")

    tmpdir = tempfile.mkdtemp(prefix="pw_profile_")
    user_data_copy = os.path.join(tmpdir, "User Data")
    os.makedirs(user_data_copy, exist_ok=True)
    target_profile_path = os.path.join(user_data_copy, profile_name)

    logger.info(f"Copiando perfil {profile_name} (isso pode demorar)...")
    ignore = shutil.ignore_patterns("Cache*", "Code Cache*", "GPUCache*", "*.tmp")
    shutil.copytree(orig_profile_path, target_profile_path, dirs_exist_ok=True, ignore=ignore)
    return tmpdir, user_data_copy

def maximizar_janela_titulo(parte_titulo):
    """Procura uma janela do Chrome pelo título e a maximiza."""
    time.sleep(3)  # espera o Chrome abrir totalmente
    for w in gw.getWindowsWithTitle(parte_titulo):
        if "Chrome" in w.title or "Gmail" in w.title:
            try:
                w.maximize()
                print(f"Janela '{w.title}' maximizada com sucesso!")
                return
            except Exception as e:
                print(f" Falha ao maximizar janela: {e}")
    print(" Nenhuma janela correspondente encontrada.")


# -------------------------
# Fluxos principais
# -------------------------
def login_gmail(page, usuario, senha):
    logger.info("Iniciando fluxo de login no Gmail...")
    try:
        criar_conta = page.locator(".VfPpkd-vQzf8d")
        if criar_conta.count() == 0:
            logger.info("Já está logado (ou layout diferente).")
            return

        page.wait_for_selector("input[type='email']", timeout=8000)
        page.fill("input[type='email']", usuario)
        if page.locator("text=Seguinte").count() > 0:
            page.click("text=Seguinte")
        else:
            page.click("text=Avançar")

        page.wait_for_timeout(2000)
        if page.locator("input[type='password']").count() > 0:
            page.wait_for_selector("input[type='password']", timeout=8000)
            page.fill("input[type='password']", senha)
            page.click("text=Seguinte")
        else:
            logger.info("Campo de senha não encontrado — pode já estar logado.")
    except Exception as e:
        logger.error(f"Erro durante o fluxo de login: {e}")

def open_gmail(destinatario, assunto, corpo):
    usuario, senha = get_credentials(SERVICO)
    chrome_path = get_chrome_path()
    kill_chrome_processes()


    with sync_playwright() as p:
        context = None
        tmpdir = None
        try:
            tmpdir, user_data_copy = make_profile_copy(ORIG_USER_DATA, PROFILE_NAME)
            context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_copy,
                channel="chrome",
                headless=False,
                args=[
                    f"--profile-directory={PROFILE_NAME}",
                    "--start-maximized",
                    "--window-size=1920,1080",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
            )
            logger.info("Chrome aberto com cópia temporária do perfil.")
            page = context.new_page()
            page.goto("https://mail.google.com/", wait_until="load")
            page.wait_for_timeout(3000)
            maximizar_janela_titulo("Gmail")
            login_gmail(page, usuario, senha)

            # Espera carregar e clica em "Escrever"
            page.wait_for_timeout(30000)
            escrever = page.locator(".T-I.T-I-KE.L3")  # botão "Escrever"
            if escrever.count() > 0:
                escrever.first.click()
                logger.info("Botão 'Escrever' clicado.")
                page.wait_for_timeout(2000)
                
                def compose_email(page, destinatario, assunto, corpo):
                    """Preenche os campos do e-mail no Gmail."""
                    try:
                        logger.info("Preenchendo o email...")

                        # ----- DESTINATÁRIO -----
                        to_input = page.locator(
                            "input[aria-label='To recipients'], input[aria-label='Destinatários']"
                        )
                        to_input.first.wait_for(timeout=20000)
                        to_input.first.fill(destinatario)
                        logger.info("Destinatário preenchido.")
                        page.keyboard.press("Tab")
                        page.wait_for_timeout(300)

                        # ----- ASSUNTO -----
                        subject_input = page.locator("input[name='subjectbox']")
                        subject_input.wait_for(timeout=20000)
                        subject_input.fill(assunto)
                        logger.info("Assunto preenchido.")
                        page.keyboard.press("Tab")
                        page.wait_for_timeout(300)

                        # ----- CORPO DA MENSAGEM -----
                        body = page.locator(
                            "div[aria-label='Message Body'], div[aria-label='Corpo da mensagem']"
                        )
                        logger.info(f"Quantidade de possíveis corpos encontrados: {body.count()}")
                        body.first.wait_for(timeout=20000)
                        body.first.click()

                        # Aqui dá pra usar fill OU keyboard.type. 
                        body.first.fill(corpo)
                        # Se quiser simular digitação humana, poderia ser:
                        # page.keyboard.type(corpo, delay=20)

                        logger.info(" Email preenchido com sucesso.")

                        page.wait_for_timeout(4000)
                        page.keyboard.press("Control+Enter")
                    except Exception as e:
                        logger.error(f"Erro ao preencher o email: {e}")
                
                compose_email(page, destinatario, assunto, corpo)
            else:
                logger.warning("Botão 'Escrever email' não encontrado.")


        finally:
            if context:
                context.close()
            if tmpdir:
                logger.info("Removendo cópia temporária...")
                shutil.rmtree(tmpdir, ignore_errors=True)

def run_gui():
    root = tk.Tk()
    root.title("Envio automático de e-mail - Gmail")
    root.resizable(False, False)

    # --- Linha 0: Destinatário ---
    tk.Label(root, text="Destinatário:").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
    entry_dest = tk.Entry(root, width=50)
    entry_dest.grid(row=0, column=1, padx=10, pady=(10, 5))

    # --- Linha 1: Assunto ---
    tk.Label(root, text="Assunto:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_assunto = tk.Entry(root, width=50)
    entry_assunto.grid(row=1, column=1, padx=10, pady=5)

    # --- Linha 2: Corpo ---
    tk.Label(root, text="Corpo da mensagem:").grid(row=2, column=0, sticky="nw", padx=10, pady=5)
    txt_corpo = scrolledtext.ScrolledText(root, width=50, height=10)
    txt_corpo.grid(row=2, column=1, padx=10, pady=5)

    # --- Função chamada ao clicar em "Enviar" ---
    def on_send():
        destinatario = entry_dest.get().strip()
        assunto = entry_assunto.get().strip()
        corpo = txt_corpo.get("1.0", tk.END).strip()

        if not destinatario or not assunto or not corpo:
            messagebox.showwarning("Campos obrigatórios", "Preencha destinatário, assunto e corpo.")
            return

        try:
            # Aqui chamamos a lógica de automação
            open_gmail(destinatario, assunto, corpo)
            messagebox.showinfo(
                "Concluído",
                "Processo de envio finalizado.\nConfira o Gmail no Chrome."
            )
        except Exception as e:
            logger.exception("Erro ao enviar e-mail pelo Gmail")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o envio:\n{e}")

    # --- Linha 3: Botão ---
    btn_enviar = tk.Button(root, text="Enviar e abrir Gmail", command=on_send)
    btn_enviar.grid(row=3, column=1, sticky="e", padx=10, pady=(5, 10))

    root.mainloop()


if __name__ == "__main__":
    run_gui()
