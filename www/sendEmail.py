#!/usr/bin/python
# -*- coding: UTF-8 -*-

username = '289097294@qq.com'
password = 'rpwymeinexbycbdf'
addr_to = 'sjl902@163.com'
smtp_server = 'smtp.qq.com'
smtp_port = 465

from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

subject = '这是用python和smtp模块发送的邮件'
content = 'hello world Python 你好'
file = '../QQ图片20200107124217.png'


def sendPainEmail(addr_to, subject, content):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = username
    msg['To'] = addr_to
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.login(username, password)
        smtp.sendmail(username, [addr_to], msg.as_string())
        smtp.quit()
        print('发送成功')
    except smtplib.SMTPAuthenticationError as e:
        print(smtplib.SMTPAuthenticationError, e)
        print('发送失败')


def sendFileEmail(addr_to, subject, content, file):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = password
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    with open(file, 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'png', filename=file)
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=file)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')

        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)

    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    smtp.login(username, password)
    smtp.sendmail(username, [addr_to], msg.as_string())
    smtp.quit()
    print('发送成功')
