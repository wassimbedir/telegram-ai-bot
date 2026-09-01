import requests
import telebot
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(8743000994:AAFoEiIoUx31I1Hw2Dz-hu2sFJyvCApa5Tw)

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {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}",
    "Content-Type": "application/json"
}

user_conversations = {}

def get_conversation(user_id):
    if user_id not in user_conversations:
        user_conversations[user_id] = [
            {"role": "system", "content": "أنت مساعد ذكي ودود، ترد باللهجة العربية العامية البسيطة، إجاباتك مختصرة ومفيدة، وعندك شوية روح مرح."}
        ]
    return user_conversations[user_id]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بيك! أنا مساعدك الذكي، اسألني أي شي 🤖")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    conversation = get_conversation(user_id)

    conversation.append({"role": "user", "content": message.text})

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": conversation
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" not in result:
        bot.reply_to(message, f"صار خطأ: {result}")
        return

    reply = result["choices"][0]["message"]["content"]
    conversation.append({"role": "assistant", "content": reply})

    bot.reply_to(message, reply)

print("البوت شغال...")
bot.polling()
