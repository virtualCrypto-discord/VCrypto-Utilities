import discord
from discord.ext import commands
from virtualcrypto import AsyncVirtualCryptoClient, Scope
from os import environ


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__("v!", intents=intents)
        self.vcrypto = AsyncVirtualCryptoClient(
            client_id=environ["CLIENT_ID"],
            client_secret=environ["CLIENT_SECRET"],
            scopes=[Scope.Pay, Scope.Claim]
        )

    async def start(self, *args, **kwargs):
        await self.vcrypto.start()
        await super(MyBot, self).start(*args, **kwargs)

    async def close(self):
        await self.vcrypto.close()

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="v!help"))
