import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Загружаем или создаём файл с XP
if os.path.exists('xp.json'):
    with open('xp.json', 'r') as f:
        xp_data = json.load(f)
else:
    xp_data = {}

def save_xp():
    with open('xp.json', 'w') as f:
        json.dump(xp_data, f)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')

@bot.command()
async def addxp(ctx, member: discord.Member, amount: int):
    user_id = str(member.id)
    xp_data[user_id] = xp_data.get(user_id, 0) + amount
    save_xp()
    await ctx.send(f'Добавлено {amount} XP для {member.display_name}.')

@bot.command()
async def removexp(ctx, member: discord.Member, amount: int):
    user_id = str(member.id)
    xp_data[user_id] = max(0, xp_data.get(user_id, 0) - amount)
    save_xp()
    await ctx.send(f'Удалено {amount} XP у {member.display_name}.')

@bot.command()
async def xp(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    user_id = str(member.id)
    xp = xp_data.get(user_id, 0)
    await ctx.send(f'{member.display_name} имеет {xp} XP.')

bot.run(os.getenv('TOKEN'))
