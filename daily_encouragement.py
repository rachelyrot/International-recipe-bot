import os
import smtplib
from email.mime.text import MIMEText
import openai

# הגדרת משתני סביבה
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

if not all([OPENAI_API_KEY, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
    raise Exception("אחד או יותר ממשתני הסביבה אינם מוגדרים: OPENAI_API_KEY, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")

# הגדרת מפתח ה-API של OpenAI
openai.api_key = OPENAI_API_KEY

# הגדרת prompt לבקשת תוכן עידוד מה-AI
prompt = (
    "כתוב שיר עידוד קצר ונוגע ללב עם נימה הומוריסטית, "
    "על נושא זה שאין לי עבודה, אך בכל יום מופיעות הזדמנויות חדשות."
)

try:
    response = openai.Completion.create(
        engine="text-davinci-003",  # ניתן לעדכן למנוע אחר אם תרצה
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None
    )
    ai_content = response.choices[0].text.strip()
    print("תוכן מה-AI:")
    print(ai_content)
except Exception as e:
    ai_content = f"לא הצלחנו לקבל תוכן מה-AI: {str(e)}"
    print(ai_content)

subject = "שיר עידוד יומי בנושא שאין עבודה"

# בניית הודעת המייל
msg = MIMEText(ai_content, "plain", "utf-8")
msg["Subject"] = subject
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL

try:
    # התחברות לשרת Gmail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    server.quit()
    print("מייל נשלח בהצלחה!")
except Exception as e:
    print("שגיאה בשליחת המייל:", e)
