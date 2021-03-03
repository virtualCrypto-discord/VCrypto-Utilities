from discord.ext import commands
import discord
from virtualcrypto import AsyncVirtualCryptoClient


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vcrypto: AsyncVirtualCryptoClient = self.bot.vcrypto

    @commands.command(aliases=['bal', 'money'])
    @commands.has_permissions(manage_guild=True)
    async def balance(self, ctx: commands.Context):
        currency = await self.vcrypto.get_currency_by_guild(ctx.guild.id)
        if currency is None:
            await ctx.send("このサーバーでは通貨は作成されていません。")
            return
        balances = [i for i in await self.vcrypto.get_balances() if i.currency.guild == ctx.guild.id]
        if not balances:
            value = 0
        else:
            value = balances[0].amount

        await ctx.send(f"{value}{currency.unit}を持っています。")


def setup(bot):
    return bot.add_cog(Wallet(bot))
