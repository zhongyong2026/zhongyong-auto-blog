import os
from google import genai  # 최신 라이브러리로 변경
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 환경 변수 로드
GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY') # GitHub Secrets 이름과 일치해야 함
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASSWORD')
RECIPIENT = os.environ.get('EMAIL_RECIPIENT')

# 1. AI 원고 생성 (2026년형 최신 방식)
client = genai.Client(api_key=GOOGLE_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash", # 최신 모델 사용
    contents="중용행정사사무소 블로그를 위한 상위 노출용 [식약처/환경부 인허가] 전문 원고를 HTML 형태로 아주 상세하게 작성해줘."
)

# 2. 이메일 구성 및 발송 (하이웍스)
msg = MIMEMultipart()
msg['Subject'] = "[자동발행] 중용행정사 실무 리포트"
msg['From'] = EMAIL_USER
msg['To'] = RECIPIENT
msg.attach(MIMEText(response.text, 'html'))

try:
    with smtplib.SMTP_SSL('smtp.hiworks.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, RECIPIENT, msg.as_string())
    print("✅ 성공적으로 메일을 보냈습니다!")
except Exception as e:
    print(f"❌ 발송 실패: {e}")
