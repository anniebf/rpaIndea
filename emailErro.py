from email.mime.image import MIMEImage
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

IMG_PATH = r"C:\rpaIndea\img\bf_workflow.png"

aglomerado_erro = {}

def enviar_warning(logging):
    try:
        # Limpa eventuais espaços nos e-mails do .env
        destinatarios_limpos = [email.strip() for email in ALERT_RECIPIENTS]
        tag_imagem = '<img src="cid:logo_alerta" alt="Header" style="display:block; margin-bottom:15px;"><br>'
        if not aglomerado_erro:
            subject = "FINALIZAÇÃO DO RPA INDEA"
            body = f"""
                <html>
                    <body>
                        {tag_imagem}
                        <p><b>NÃO FOI ENCONTRADA ERROS NO PROCESSO</b></p>
                        <p>Todos os CNPJs foram processados com sucesso.</p>
                        <p style="text-align: right; font-size: 11px; color: #555555;">E-mail gerado por Python — host: 10.194.0.57. caminho: /python_bf/rpaIndea/main.py</p>
                    </body>
                </html>
                """
        else:
            linhas_erro = "".join([f"<li><b>{fazenda}:</b> {erro}</li>" for fazenda, erro in aglomerado_erro.items()])
            
            subject = "ERROS RPA INDEA"
            body = f"""
                <html>
                    <body>
                        {tag_imagem}
                        <p><b>FORAM ENCONTRADOS ERROS NO PROCESSAMENTO DE UMA OU MAIS FAZENDAS:</b></p>
                        <ul>
                            {linhas_erro}
                        </ul>
                        <p style="text-align: right; font-size: 11px; color: #555555;">E-mail gerado por Python — host: 10.194.0.57. caminho: /python_bf/rpaIndea/main.py</p>
                    </body>
                </html>
                """

        # 1. Cria o container que permite anexar a imagem ao HTML
        message = MIMEMultipart("related")
        message["From"] = sender_mail
        message["To"] = ", ".join(destinatarios_limpos)
        message["Subject"] = subject

        # 2. Anexa o corpo HTML ao container
        msg_html = MIMEText(body, "html", "utf-8")
        message.attach(msg_html)

        # 3. LÃª a imagem do servidor e a anexa vinculando-a ao 'logo_alerta'
        if os.path.exists(IMG_PATH):
            with open(IMG_PATH, "rb") as f:
                img_data = f.read()
            
            msg_image = MIMEImage(img_data)
            msg_image.add_header("Content-ID", "<logo_alerta>")
            msg_image.add_header("Content-Disposition", "inline", filename=os.path.basename(IMG_PATH))
            message.attach(msg_image)
        else:
            logging.warning(f"Imagem nÃ£o encontrada no caminho: {IMG_PATH}")

        # 4. ConexÃ£o e envio (usando o objeto 'message' atualizado)
        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_mail, password)
        server.sendmail(sender_mail, destinatarios_limpos, message.as_string())
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