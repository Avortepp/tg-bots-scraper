import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import requests
from bs4 import BeautifulSoup

API_TOKEN = "YourTOKen"

logging.basicConfig(level=logging.INFO)
bot = Bot(token= API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start','help'])
async def send_welkome(message:types.Message):
    await message.reply("Hello! Send me a URL and I'll scrape some data for you.")

@dp.message_handler()
async def scrape_website(message: types.Message):
    url = message.text
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

      
        headlines = [h1.get_text() for h1 in soup.find_all('h1')]
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        
        response_text = "Headlines:\n" + "\n".join(headlines) + "\n\n" \
                        "Paragraphs:\n" + "\n".join(paragraphs) + "\n\n" \
                        "Links:\n" + "\n".join(links)
                        
        if not response_text.strip():
            response_text = "No data found."
            
        await message.reply(response_text[:4000])  
    except requests.RequestException as e:
        await message.reply(f"An error occurred: {e}")


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)