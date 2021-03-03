import discord
from discord.ext import commands
from virtualcrypto import AsyncVirtualCryptoClient, Scope, Balance
from typing import Optional
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
        self.balance_cache = {}
        self.guild_lock = {}

    async def refresh_cache(self):
        self.balance_cache = {i.currency.guild: i for i in await self.vcrypto.get_balances()}

    async def get_balance(self, guild_id: int) -> Optional[Balance]:
        if guild_id not in self.balance_cache.keys():
            self.balance_cache = {i.currency.guild: i for i in await self.vcrypto.get_balances()}
        if guild_id not in self.balance_cache.keys():
            return None
        return self.balance_cache[guild_id]

    async def start(self, *args, **kwargs):
        await self.vcrypto.start()
        await super(MyBot, self).start(*args, **kwargs)

    async def close(self):
        await self.vcrypto.close()

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="v!help"))

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.MissingPermissions):
            await context.send("実行権限が足りません。")
            return
        elif isinstance(exception, commands.CommandNotFound):
            return
