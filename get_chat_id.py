import requests

BOT_TOKEN = "8570843218:AAFbzOkfiuuOIeBPCpA2QLKALGNtI9SBlPI"

def main():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    print(data)

    # Если были апдейты — выведем chat_id первого апдейта
    if "result" in data and data["result"]:
        chat = data["result"][0]["message"]["chat"]
        chat_id = chat["id"]
        print("\nВаш chat_id:", chat_id)
    else:
        print("Нет апдейтов. Напишите что-нибудь боту в Telegram и попробуйте ещё раз.")

if __name__ == "__main__":
    main()


#.\.venv\Scripts\Activate активировать виртуальное окружение