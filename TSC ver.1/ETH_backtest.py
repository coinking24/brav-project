import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, render_template
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

# --- 용기를 주는 문구 30개 ---
encouraging_messages = [
    "당신의 용기가 누군가에게는 빛이 될 거예요.", "가장 어두운 밤도 결국 아침을 맞이해요.", "당신은 생각보다 훨씬 강한 사람이에요.",
    "오늘의 눈물은 내일의 무지개를 위한 비예요.", "당신의 이야기는 세상에 단 하나뿐인 소중한 보석입니다.", "괜찮아, 지금까지 정말 잘해왔어요.",
    "마음의 짐을 잠시 내려놓아도 괜찮아요.", "당신의 속도대로 걸어가면 돼요. 조급해하지 말아요.", "모든 위대한 것들은 작은 시작에서 비롯됩니다.",
    "당신 안에는 세상을 놀라게 할 힘이 숨어있어요.", "스스로를 믿어주세요. 당신은 이미 충분해요.", "넘어져도 괜찮아요. 흙을 털고 다시 일어서면 돼요.",
    "당신의 존재만으로도 이미 충분히 가치 있어요.", "상처는 당신이 싸워왔다는 증거이지, 약하다는 증거가 아니에요.", "걱정 말아요. 모든 것은 결국 제자리를 찾을 거예요.",
    "당신의 진심은 반드시 누군가에게 닿을 거예요.", "따뜻한 차 한 잔의 위로가 당신과 함께하기를.", "결과가 어떻든, 당신의 노력은 결코 헛되지 않아요.",
    "당신은 사랑받기 위해 태어난 사람입니다.", "때로는 잠시 멈춰서 하늘을 보는 여유를 가져요.", "당신의 아픔을 이해하려는 마음이 여기에 있어요.",
    "한 걸음, 또 한 걸음. 그렇게 걷다 보면 길이 보일 거예요.", "마음껏 울어도 괜찮아요. 눈물은 마음을 정화시켜 주니까요.", "당신의 이야기는 언젠가 아름다운 꽃을 피울 씨앗이에요.",
    "혼자라고 생각하지 말아요. 보이지 않아도 응원하는 이들이 있어요.", "세상의 모든 좋은 말이 당신에게 향하기를.", "오늘 하루도 정말 고생 많았어요. 편안한 밤 되세요.",
    "당신은 잘 해낼 수 있을 거예요. 언제나 그랬듯이.", "작은 성공들을 축하해주세요. 그것들이 모여 큰 기쁨이 될 거예요.", "당신의 내일은 오늘보다 분명 더 빛날 거예요."
]

def send_email_notification(title, story_content):
    try:
        sender_email = os.getenv("GMAIL_USER")
        sender_password = os.getenv("GMAIL_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL")
        if not all([sender_email, sender_password, recipient_email]):
            print("ERROR: .env 파일에 이메일 정보가 올바르게 설정되지 않았습니다.")
            return
        subject = f"💌 [{title}] 새로운 익명 사연이 도착했습니다!"
        msg = MIMEText(story_content, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, sender_password)
            smtp_server.send_message(msg)
        print("성공: 새로운 사연을 이메일로 발송했습니다.")
    except Exception as e:
        print(f"이메일 발송 실패: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    story = request.form['story']
    if not title.strip() or not story.strip():
        return "<script>alert('제목과 사연 내용을 모두 작성해주세요.'); window.location.href = '/';</script>"
    
    send_email_notification(title, story)

    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>당신을 위한 행운의 쪽지</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Malgun Gothic', sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f2f5; }}
            .container {{ text-align: center; }}
            .fortune-cookie-container {{ position: relative; width: 200px; height: 100px; cursor: pointer; margin: 0 auto; }}
            .cookie-half {{ position: absolute; width: 200px; height: 100px; background-color: #f2d7a5; border-radius: 100px 100px 0 0; transition: transform 0.6s ease-in-out; }}
            .cookie-half.bottom {{ top: 0; transform: rotateX(180deg); }}
            .fortune-paper {{ position: absolute; top: 40px; left: 50%; transform: translateX(-50%); background: white; padding: 10px 20px; white-space: nowrap; box-shadow: 0 2px 5px rgba(0,0,0,0.1); opacity: 0; transition: opacity 0.5s 0.3s; z-index: -1; }}
            .instruction {{ margin-top: 30px; font-size: 18px; color: #555; transition: opacity 0.3s; }}
            .opened .cookie-half.top {{ transform: translateY(-30px) rotateZ(-20deg); }}
            .opened .cookie-half.bottom {{ transform: translateY(30px) rotateX(180deg) rotateZ(20deg); }}
            .opened .fortune-paper {{ opacity: 1; z-index: 1; }}
            .opened .instruction {{ opacity: 0; }}
            .button-wrapper {{ margin-top: 40px; }}
            .blue-button {{ background-color: #007bff; color: white; border: none; padding: 12px 25px; font-size: 15px; border-radius: 25px; cursor: pointer; text-decoration: none; transition: background-color 0.3s; }}
            .blue-button:hover {{ background-color: #0056b3; }}
            .instagram-logo {{ width: 40px; margin-top: 25px; transition: opacity 0.3s; }}
            .instagram-logo:hover {{ opacity: 0.7; }}
            .footer-text {{ margin-top: 20px; font-family: 'Nanum Pen Script', cursive; font-size: 32px; color: #777; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div id="fortune-cookie" class="fortune-cookie-container">
                <div class="cookie-half top"></div>
                <div class.half bottom"></div>
                <div id="fortune-message" class="fortune-paper">행운의 쪽지를 확인하세요!</div>
            </div>
            <p class="instruction">쿠키를 클릭해서 열어보세요</p>
        </div>
        
        <div class="button-wrapper">
            <a href="/" class="blue-button">사연 더 쓰러가기</a>
        </div>

        <a href="https://www.instagram.com/neulz.ip/" target="_blank">
            <img src="{{ url_for('static', filename='insta.png') }}" alt="인스타그램으로 이동" class="instagram-logo">
        </a>
        
        <div class="footer-text">always here for u</div>
        
        <script>
            const fortunes = {json.dumps(encouraging_messages)};
            const cookieContainer = document.getElementById('fortune-cookie');
            const fortuneMessage = document.getElementById('fortune-message');
            let isOpened = false;

            cookieContainer.addEventListener('click', () => {{
                if (isOpened) return;
                isOpened = true;
                const randomIndex = Math.floor(Math.random() * fortunes.length);
                fortuneMessage.textContent = fortunes[randomIndex];
                cookieContainer.parentElement.classList.add('opened');
            }});
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)