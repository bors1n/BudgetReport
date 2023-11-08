import smtplib  # Импортируем библиотеку по работе с SMTP
from mails_file import sources

# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.base import MIMEBase

from email import encoders
import datetime
import calendar

today = datetime.date.today()
currentMonth = today.month


addr_to = sources['addr_to']
addr_from = sources['addr_from']
password = sources['app_password']  # пароль от почты addr_from

msg = MIMEMultipart()  # Создаем сообщение
msg['From'] = addr_from  # Адресат
msg['To'] = addr_to  # Получатель
msg['Subject'] = 'Budget Report'  # Тема сообщения

body = f'Budget Report for {calendar.month_name[currentMonth - 1]}'
msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст
pdfname = '/home/admin/projects/budgeting_report/BudgetReport/report.pdf'
#pdfname = '/Users/bors1n/DataspellProjects/dsProject/budget_report/report.pdf'
# open the file in bynary
binary_pdf = open(pdfname, 'rb')

payload = MIMEBase('application', 'octate-stream', Name=pdfname)
payload.set_payload((binary_pdf).read())

# enconding the binary into base64
encoders.encode_base64(payload)

# add header with pdf name
payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
msg.attach(payload)

server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
#server.starttls()             # Начинаем шифрованный обмен по TLS
server.login(addr_from, password)  # Получаем доступ
server.send_message(msg)  # Отправляем сообщение
server.quit()

#%%
