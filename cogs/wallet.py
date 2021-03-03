from discord.ext import commands
from bot import MyBot
from virtualcrypto import AsyncVirtualCryptoClient


class Wallet(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.vcrypto: AsyncVirtualCryptoClient = self.bot.vcrypto

    @commands.command(aliases=['bal', 'money'])
    @commands.has_permissions(manage_guild=True)
    async def balance(self, ctx: commands.Context):
        currency = await self.vcrypto.get_currency_by_guild(ctx.guild.id)
        if currency is None:
            await ctx.send("このサーバーでは通貨は作成されていません。")
            return
        balance = await self.bot.get_balance(ctx.guild.id)
        if balance is None:
            value = 0
        else:
            value = balance.amount

        await ctx.send(f"{value}{currency.unit}を持っています。")


def setup(bot):
    return bot.add_cog(Wallet(bot))
