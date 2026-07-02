import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()

server_smtp= os.getenv("SMTP_HOST")
port= int(os.getenv("SMTP_PORT"))
sender_mail= os.getenv("SMTP_USER")
password= os.getenv("SMTP_PASSWORD")
ALERT_RECIPIENTS= os.getenv("ALERT_RECIPIENTS").split(",")

destinatarios = ALERT_RECIPIENTS

aglomerado_erro = {}

def enviar_warning(logging):
    try:
        # Limpa eventuais espaços nos e-mails do .env
        destinatarios_limpos = [email.strip() for email in ALERT_RECIPIENTS]

        if not aglomerado_erro:
            linhas_erro = "<li><b>Teste:</b> Nenhum erro registrado.</li>"
        else:
            linhas_erro = "".join([f"<li><b>{fazenda}:</b> {erro}</li>" for fazenda, erro in aglomerado_erro.items()])
        
        subject = "ERROS RPA INDEA"
        body = f"""
            <html>
                <body>
                    <p><b>FORAM ENCONTRADOS ERROS NO PROCESSAMENTO DE UMA OU MAIS FAZENDAS:</b></p>
                    <ul>
                        {linhas_erro}
                    </ul>
                </body>
            </html>
            """

        # Criando o e-mail em formato texto/html puro
        message = MIMEText(body, "html", "utf-8")
        message["From"] = sender_mail
        message["To"] = ", ".join(destinatarios_limpos)
        message["Subject"] = subject

        # FLUXO DE CONEXÃO IDÊNTICO AO SEGUNDO SCRIPT
        # Sem ehlo() manuais, usando as variáveis globais diretas
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_mail, password)
        
        # O comando de envio que faltava no seu primeiro código original
        server.sendmail(sender_mail, ALERT_RECIPIENTS, message.as_string())
        server.quit()
        

        logging.info("E-mail de alerta enviado com sucesso.")
    except Exception as e:
        logging.error(f"Falha ao enviar e-mail de alerta: {e}")

def armazenar_valor(chave, valor):
    aglomerado_erro[chave] = valor
    print(f"Sucesso! '{chave}' foi armazenado com o valor '{valor}'.")

if __name__ == "__main__":
    enviar_warning()
    armazenar_valor("", "")