import os
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 환경 변수에서 비밀번호 가져오기
GEMINI_KEY = os.environ['GEMINI_API_KEY']
EMAIL_USER = os.environ['EMAIL_USER']
EMAIL_PASS = os.environ['EMAIL_PASSWORD']
RECIPIENT = os.environ['EMAIL_RECIPIENT']

# 1. AI 원고 생성
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')
prompt = "중용행정사사무소 블로그를 위한 상위 노출용 [식약처/환경부 인허가] 전문 원고를 HTML 형태로 아주 상세하게 작성해줘."
response = model.generate_content(prompt)

# 2. 이메일 구성 및 발송
msg = MIMEMultipart()
msg['Subject'] = f"[자동발행] 중용행정사 실무 리포트"
msg['From'] = EMAIL_USER
msg['To'] = RECIPIENT
msg.attach(MIMEText(response.text, 'html'))

with smtplib.SMTP_SSL('smtp.hiworks.com', 465) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.sendmail(EMAIL_USER, RECIPIENT, msg.as_string())
print("성공적으로 메일을 보냈습니다!")
