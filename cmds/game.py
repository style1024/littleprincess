import discord
from discord.ext import commands
import numpy as np
import random
import json
import requests
from typing import List

with open('setting.json', "r", encoding="utf8") as file:
  data = json.load(file)

class Game(commands.Cog):
    
    def __init__(self, bot): 
      self.bot = bot

    @commands.slash_command()
    async def 圈叉(self, ctx: discord.ApplicationContext):
      """Starts a tic-tac-toe game with yourself."""
      await ctx.respond("Tic Tac Toe: X goes first", view=TicTacToe())

    @commands.slash_command()
    async def 抽卡(self, ctx, args):
        if (int(args) > 10000):
            await ctx.respond("抽卡數不要超過1萬啦 :(")
            return
        if (int(args) < 0):
            await ctx.respond("小於0要怎麼抽卡 :(")
            return
        ur, sr, ssr, r = 0, 0, 0, 0

        for n in range(0, int(args)):
            card = random.choice(range(1, 101))
            if 1 <= card <= 54:
                r += 1
            if 55 <= card <= 94:
                sr += 1
            if 95 <= card <= 99:
                ssr += 1
            if card == 100:
                ur += 1

        result = '''抽了{a}張
        本次抽卡狀況:
                {r}張        UR
                {q}張        SSR
                {w}張        SR
                {e}張        R
            '''
        result = result.format(a=args, r=ur, q=ssr, w=sr, e=r)
        await ctx.respond(result)
        if ssr + ur <= 0:
            await ctx.respond("https://img.ccyp.com/topic/201610/20161014134444236.png")

    @commands.slash_command()
    async def 抽獎(self, ctx, args):
        memberList = []
        for user in ctx.guild.members:
            # 檢查用戶是否不是機器人且有權限查看當前頻道
            if not user.bot and ctx.channel.permissions_for(user).read_messages:
                memberList.append(user.id)  ## 取得現有伺服器全部人的名字
        for i in range(0, int(args)):
            winner = np.random.choice(memberList)  ## 交給numpy抽獎
            memberList.remove(winner)  ## 移除中獎人
            await ctx.respond(f'恭喜 <@{winner}> 中獎')

    @commands.slash_command()
    async def 老婆(self, ctx):
        await ctx.respond("選擇你的選項:", view=DropdownView())

    @commands.slash_command()
    async def 猜拳(self, ctx, user1: discord.Member, user2: discord.Member):
      Embed = discord.Embed(title="猜拳遊戲", description="請選擇你要出什麼", color=0xf7ff8a)
      Embed.set_thumbnail(url="https://i.imgur.com/lyjRujt.gif")
      Embed.add_field(name="挑戰者", value=f"{user1.mention} VS {user2.mention}", inline=False)
      view = RPSView(user1.id, user2.id, ctx.channel.id)
      await ctx.respond(embed=Embed, view=view)

class Dropdown(discord.ui.Select):

  def __init__(self):
    options = [
      discord.SelectOption(label="waifu", description="Pick waifu!"),
      discord.SelectOption(label="neko", description="Pick neko!"),
      discord.SelectOption(label="shinobu", description="Pick shinobu!"),
      discord.SelectOption(label="megumin", description="Pick megumin!"),
      discord.SelectOption(label="cry", description="Pick cry!"),
      discord.SelectOption(label="hug", description="Pick hug!"),
      discord.SelectOption(label="awoo", description="Pick awoo!"),
      discord.SelectOption(label="kiss", description="Pick kiss!"),
      discord.SelectOption(label="lick", description="Pick lick!"),
      discord.SelectOption(label="pat", description="Pick pat!"),
      discord.SelectOption(label="bonk", description="Pick bonk!"),
      discord.SelectOption(label="yeet", description="Pick yeet!"),
      discord.SelectOption(label="blush", description="Pick blush!"),
      discord.SelectOption(label="smile", description="Pick smile!"),
      discord.SelectOption(label="wave", description="Pick wave!"),
      discord.SelectOption(label="bite", description="Pick bite!"),
      discord.SelectOption(label="slap", description="Pick slap!"),
      discord.SelectOption(label="kill", description="Pick kill!"),
      discord.SelectOption(label="kick", description="Pick kick!"),
      discord.SelectOption(label="happy", description="Pick happy!"),
      discord.SelectOption(label="wink", description="Pick wink!"),
      discord.SelectOption(label="dance", description="Pick dance!"),
      discord.SelectOption(label="cringe", description="Pick cringe!")
    ]
    super().__init__(placeholder='選擇你的選項',
                     min_values=1,
                     max_values=1,
                     options=options)

  async def callback(self, interaction: discord.Interaction):
    selected_option = interaction.data["values"][0]
    url = f'https://api.waifu.pics/sfw/{selected_option}'
    api = requests.get(url)
    pic_dict = json.loads(api.text)
    embed = discord.Embed(
      description=f"<@{interaction.user.id}> 選擇了 {selected_option}!")
    embed.set_image(url=pic_dict['url'])
    await interaction.response.send_message(embed=embed)
    #await interaction.response.send_message(pic_dict['url'])
    await interaction.message.edit(view=None)  # 這行代碼將下拉選單從消息中移除

class DropdownView(discord.ui.View):

  def __init__(self):
    super().__init__()
    self.add_item(Dropdown())

class RPSView(discord.ui.View):
  def __init__(self, user1_id: int, user2_id: int, channel_id, timeout=30, interaction=''):
    super().__init__(timeout=timeout)
    self.user1_id = user1_id
    self.user2_id = user2_id
    self.choices = {}  # 用于存储用户的选择
    self.channel_id = channel_id
    
  
  async def disable_all_buttons(self):
    for item in self.children:
      if isinstance(item, discord.ui.Button):
        item.disabled = True  # 禁用按钮
    self.stop()  # 停止视图，防止进一步交互
  
  async def interaction_check(self, interaction: discord.Interaction) -> bool:
    if interaction.user.id in [self.user1_id, self.user2_id]:
      self.interaction = interaction
      return True
    else:
      await interaction.response.send_message("這個按钮不是给你的！", ephemeral=True)
      return False
  
  async def handle_choice(self, interaction: discord.Interaction, choice: str):
    self.choices[self.interaction.user.id] = choice
    await self.interaction.response.send_message(f"<@{self.interaction.user.id}> 選擇了 {choice}", ephemeral=True)
  
    # 检查是否是第一位做出选择的玩家
    if len(self.choices) == 1:
      other_user_id = self.user1_id if self.interaction.user.id == self.user2_id else self.user2_id
      channel = self.interaction.client.get_channel(self.channel_id)
      await channel.send(f"<@{other_user_id}>，現在輪到你了！")
  
    if len(self.choices) == 2:  # 如果兩位都做出決定
      await self.disable_all_buttons()
      await self.compare_choices(interaction)

  async def compare_choices(self, interaction: discord.Interaction):
    # 比較結果並決定勝負
    result = ""
    choice1 = self.choices[self.user1_id]
    choice2 = self.choices[self.user2_id]
    if choice1 == choice2:
      result = f"平局！雙方都選擇 {choice1}"
    elif (choice1 == "石頭" and choice2 == "剪刀") or \
         (choice1 == "剪刀" and choice2 == "布") or \
         (choice1 == "布" and choice2 == "石頭"):
      result = f"<@{self.user1_id}> 選擇了 {choice1}。 <@{self.user2_id}> 選擇了 {choice2}。 <@{self.user1_id}> 贏了"
    else:
      result = f"<@{self.user1_id}> 選擇了 {choice1}。 <@{self.user2_id}> 選擇了 {choice2}。 <@{self.user2_id}> 贏了"
  
    await self.interaction.followup.send(result)
  
  async def on_timeout(self):
    channel = self.interaction.client.get_channel(self.channel_id)
    await channel.send("時間已超過，遊戲已結束。")
    await self.disable_all_buttons()  # 视图超时时禁用所有按钮
  
  @discord.ui.button(label="石頭", row=0, style=discord.ButtonStyle.primary)
  async def rock(self, interaction, button):
    await self.handle_choice(interaction, "石頭")
  
  @discord.ui.button(label="剪刀", row=0, style=discord.ButtonStyle.primary)
  async def scissors(self, interaction, button):
    await self.handle_choice(interaction, "剪刀")
  
  @discord.ui.button(label="布", row=0, style=discord.ButtonStyle.primary)
  async def papper(self, interaction, button):
    await self.handle_choice(interaction, "布")

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used.
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed.
    # This is part of the "meat" of the game logic.
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons.
    # This is not required.
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons.
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner and is used by the TicTacToeButton.
    def check_board_winner(self):
        # Check horizontal
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        # If we're here, we need to check if a tie has been reached.
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

def setup(bot):
  bot.add_cog(Game(bot))