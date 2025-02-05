import os
import smtplib
from email.mime.text import MIMEText
import openai

# הגדרת משתני סביבה
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

# בדיקה אם כל המשתנים קיימים
if not all([OPENAI_API_KEY, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
    raise Exception("אחד או יותר ממשתני הסביבה אינם מוגדרים: OPENAI_API_KEY, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")

# התחברות ל-OpenAI
openai.api_key = OPENAI_API_KEY

# הגדרת prompt לבקשת תוכן עידוד מה-AI
prompt = "כתוב שיר עידוד קצר ומצחיק על זה שאין לי עבודה, עם נימה הומוריסטית."

# קבלת תגובה מ-OpenAI
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "את עוזרת חכמה שתפקידה לספק שירי עידוד"},
            {"role": "user", "content": prompt}
        ]
    )
    ai_content = response['choices'][0]['message']['content'].strip()
    print("תוכן מה-AI:")
    print(ai_content)
except Exception as e:
    ai_content = f"שגיאה בהתחברות ל-OpenAI: {str(e)}"
    print(ai_content)

# נושא המייל
subject = "שיר עידוד יומי בנושא שאין עבודה"

# בניית הודעת המייל
msg = MIMEText(ai_content, "plain", "utf-8")
msg["Subject"] = subject
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL

# שליחת המייל
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    server.quit()
    print("המייל נשלח בהצלחה!")
except Exception as e:
    print(f"שגיאה בשליחת המייל: {e}")
