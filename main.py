from bot import MyBot
from dotenv import load_dotenv
import os
load_dotenv()

bot = MyBot()

extensions = [
    'cogs.wallet',
    'cogs.give'
]

for extension in extensions:
    bot.load_extension(extension)

bot.run(os.environ["BOT_TOKEN"])
