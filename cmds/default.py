import discord
from discord.ext import commands
import json

with open('setting.json', "r", encoding="utf8") as file:
  data = json.load(file)

class Default(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #For Every Server
    @commands.slash_command(description="Sends the bot's latency.")
    async def ping(self, ctx):
        await ctx.respond(f'機器人延遲{round(self.bot.latency * 1000)} 豪秒')

    @commands.slash_command(name="userinfo", description="Gets info about a user.")
    async def info(ctx: discord.ApplicationContext, user: discord.Member = None):
        user = (
            user or ctx.author
        )  # If no user is provided it'll use the author of the message
        embed = discord.Embed(
            fields=[
                discord.EmbedField(name="ID", value=str(user.id), inline=False),  # User ID
                discord.EmbedField(
                    name="Created",
                    value=discord.utils.format_dt(user.created_at, "F"),
                    inline=False,
                ),  # When the user's account was created
            ],
        )
        embed.set_author(name=user.name)
        embed.set_thumbnail(url=user.display_avatar.url)

        if user.colour.value:  # If user has a role with a color
            embed.colour = user.colour

        if isinstance(user, discord.User):  # Checks if the user in the server
            embed.set_footer(text="This user is not in this server.")
        else:  # We end up here if the user is a discord.Member object
            embed.add_field(
                name="Joined",
                value=discord.utils.format_dt(user.joined_at, "F"),
                inline=False,
            )  # When the user joined the server

        await ctx.respond(embeds=[embed])  # Sends the embed

    @commands.slash_command(name="num", description="刪除數量")
    @commands.is_owner()
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num)

def setup(bot: commands.Bot):
    bot.add_cog(Default(bot))