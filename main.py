from bot import MyBot
from dotenv import load_dotenv
import os
load_dotenv()

bot = MyBot()

bot.run(os.environ["BOT_TOKEN"])
