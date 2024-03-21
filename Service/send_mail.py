import smtplib
from logSystem import logging as log
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email_destino, mensagem, email_remetente = 'sct.alerta@gmail.com', nome_remetente = 'SCT', assunto = 'SCT - Alerta de acesso ao computador', tentativas = 3):
    for i in range(tentativas):
        try:
            msg = MIMEMultipart()
            msg['From'] = f'{nome_remetente} <{email_remetente}>'
            msg['To'] = email_destino
            msg['Subject'] = assunto
            msg.attach(MIMEText(mensagem, 'plain'))

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(email_remetente, 'ojsp zkmp pxnk vdpj') ## Default SCT Key: wjnx dnjb qkll vrvf or ojsp zkmp pxnk vdpj
            server.sendmail(email_remetente, email_destino, msg.as_string())
            server.quit()
            log.info(f"Email de alerta enviado com sucesso para {email_destino}")
            ##DEBUG\
            ##print('Email enviado com sucesso!')
            break
        except Exception as e:
            log.error(f"Falha ao enviar um email de alerta. Erro: {e}")
            ##DEBUG\
            ##print(e)