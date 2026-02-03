import os
import sys
from google import genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. 환경 변수 로드 및 확인
# GitHub Secrets에 등록한 이름과 대소문자까지 정확히 일치해야 합니다.
GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')

if not GOOGLE_API_KEY:
    print("❌ 에러: GEMINI_API_KEY를 찾을 수 없습니다. GitHub Secrets 설정을 확인해 주세요.")
    sys.exit(1) # 키가 없으면 여기서 중단

EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASSWORD')
RECIPIENT = os.environ.get('EMAIL_RECIPIENT')

try:
    # 2. AI 원고 생성
    client = genai.Client(api_key=GOOGLE_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="중용행정사사무소 블로그를 위한 상위 노출용 [2026년 최신 식약처/환경부 인허가] 전문 원고를 HTML 형태로 상세하게 작성해줘."
    )
    content_html = response.text

    # 3. 이메일 구성 및 발송
    msg = MIMEMultipart()
    msg['Subject'] = "[자동발행] 중용행정사 실무 리포트"
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT
    msg.attach(MIMEText(content_html, 'html'))

    with smtplib.SMTP_SSL('smtp.hiworks.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, RECIPIENT, msg.as_string())
    print("✅ 성공적으로 메일을 보냈습니다!")

except Exception as e:
    print(f"❌ 오류 발생: {e}")
    sys.exit(1)
