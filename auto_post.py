import os
import sys
from google import genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. 환경 변수 로드
GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASSWORD')
RECIPIENT = os.environ.get('EMAIL_RECIPIENT')

if not GOOGLE_API_KEY:
    print("❌ 에러: GEMINI_API_KEY를 찾을 수 없습니다.")
    sys.exit(1)

try:
    # 2. AI 원고 생성 (2026년 표준 모델명 사용)
    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    # 모델명을 'gemini-2.0-flash'로 정확히 지정합니다.
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents="""중용행정사사무소 블로그용 전문 원고를 작성해줘. 
        주제: 2026년 최신 식약처 인허가 및 KC 인증 절차 가이드.
        형식: HTML 태그(h2, p, li)를 사용해서 아주 상세하게 작성할 것."""
    )
    
    # AI 응답에서 텍스트 추출
    content_html = response.text

    # 3. 이메일 구성 및 발송 (하이웍스)
    msg = MIMEMultipart()
    msg['Subject'] = "[자동발행] 중용행정사 실무 리포트 (2026)"
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT
    msg.attach(MIMEText(content_html, 'html'))

    with smtplib.SMTP_SSL('smtp.hiworks.com', 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, RECIPIENT, msg.as_string())
        
    print("✅ 성공: 하이웍스로 원고를 보냈습니다!")

except Exception as e:
    # 404나 429 등 에러 발생 시 상세 원인 출력
    print(f"❌ 오류 발생: {e}")
    sys.exit(1)
