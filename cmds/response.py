import discord
from discord.ext import commands
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import random

class Response(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        
        if msg.author == self.bot.user:
            return

        if '跳樓' in msg.content:
            await msg.channel.send('''
                        ━━━━━┒咪醬等我
                        ┓┏┓┏┓┃我馬上陪妳
                        ┛┗┛┗┛┃＼😭／
                        ┓┏┓┏┓┃  /
                        ┛┗┛┗┛┃ノ)
                        ┓┏┓┏┓┃
                        ┛┗┛┗┛┃
                        ┓┏┓┏┓┃
                        ┛┗┛┗┛┃
                        ┻┻┻┻┻┻''')

        if '三分鐘' in msg.content:
            await msg.channel.send("https://media.discordapp.net/attachments/1101391546101801012/1224599319152296006/606e8e4a2b29c58e6f44ed7bbfa43702.gif?ex=661e13fd&is=660b9efd&hm=d13a481ae228455c467d4cef2f985e6cb1c3c549d5e7c9d9432f4b4ae590feaa&=&width=450&height=340")

        if msg.content.startswith('占卜'):
            tmp = msg.content.split(" ", 2)
            luck = np.random.choice(['大吉', '吉', '小吉', '凶', '大凶'],
                                    size=1,
                                    p=[0.15, 0.3, 0.2, 0.25, 0.1])
            luck = str(luck).replace("['", "").replace("']", "")

            if len(tmp) == 1:
                await msg.channel.send(f"{msg.author.mention} 要占卜什麼？")
            else:
                await msg.channel.send(f'{msg.author.mention} {tmp[1]}的運勢是 {luck}!!')

        if '柴犬' in msg.content:
            res = requests.get('https://dog.ceo/api/breed/shiba/images/random')
            pic = json.loads(res.text)
            await msg.channel.send(pic['message'])

        if '吉娃娃' in msg.content:
            res = requests.get('https://dog.ceo/api/breed/chihuahua/images/random')
            pic = json.loads(res.text)
            await msg.channel.send(pic['message'])

        if '哈士奇' in msg.content:
            res = requests.get('https://dog.ceo/api/breed/husky/images/random')
            pic = json.loads(res.text)
            await msg.channel.send(pic['message'])

        if '柯基' in msg.content:
            res = requests.get('https://dog.ceo/api/breed/corgi/images/random')
            pic = json.loads(res.text)
            await msg.channel.send(pic['message'])

        if '羅威那' in msg.content:
            res = requests.get('https://dog.ceo/api/breed/rottweiler/images/random')
            pic = json.loads(res.text)
            await msg.channel.send(pic['message'])

        if '貓'in msg.content:
            res = requests.get('https://api.thecatapi.com/v1/images/search')
            pic = json.loads(res.text)
            await msg.channel.send(pic[0]['url'])

        if 'huh' in msg.content:
            await msg.channel.send("https://media.tenor.com/7t63GFnoIPUAAAAd/huh-cat-huh-m4rtin.gif")

        if '急了' in msg.content:
            await msg.channel.send("https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1693521527021.jpg")

        if '三小' in msg.content:
            await msg.channel.send("https://memeprod.ap-south-1.linodeobjects.com/user-maker-thumbnail/2ee6a32602be36dc7655bc9bbcdda2fd.gif")

        
def setup(bot: commands.Bot):
  bot.add_cog(Response(bot))