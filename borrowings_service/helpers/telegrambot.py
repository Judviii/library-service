import os
import requests
from dotenv import load_dotenv

load_dotenv()


TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
TG_CHAT_ID = os.environ["TG_CHAT_ID"]


def send_message(message):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        error_data = response.json()
        error_message = error_data.get(
            "description",
            "No description available"
        )
        raise Exception(
            f"Error: HTTP {response.status_code} - {error_message}"
        )


def get_borrow_time(obj):
    duration = obj.expected_return_date - obj.borrow_date
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    if hours > 0:
        return f"{hours} hours, {minutes} minutes"
    return f"{minutes} minutes"


def get_message(instance):
    user_name = instance.user.email
    book_title = instance.book.title
    book_author = instance.book.author
    borrowing_time = get_borrow_time(instance)
    message = (f"New borrowing:\n"
               f"User - {user_name} Book - {book_title}, {book_author}\n"
               f"Borrow for: {borrowing_time}\n"
               f"Borrowing end: {instance.expected_return_date}")
    return message
