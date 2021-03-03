from discord.ext import commands
from bot import MyBot
from virtualcrypto import AsyncVirtualCryptoClient
import discord


class Give(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.vcrypto: AsyncVirtualCryptoClient = self.bot.vcrypto

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def give(self, ctx: commands.Context, amount: int, *, users):
        """メンションした相手全てに通貨を配布します。"""
        currency = await self.vcrypto.get_currency_by_guild(ctx.guild.id)
        if currency is None:
            await ctx.send("このサーバーでは通貨は作成されていません。")
            return

        users = ctx.message.mentions
        if len(users) > 15:
            await ctx.send("15人までに配布できます。")
            return

        balance = await self.bot.get_balance(ctx.guild.id)
        if balance.amount < amount * len(users):
            await ctx.send(f"通貨が{amount * len(users) - balance.amount}{currency.unit}足りません。")
            return

        await ctx.send("配布しています...")
        for user in users:
            await self.vcrypto.create_user_transaction(
                unit=currency.unit,
                receiver_discord_id=user.id,
                amount=amount
            )
        await self.bot.refresh_cache()
        await ctx.send("配布完了しました。")


def setup(bot):
    return bot.add_cog(Give(bot))
