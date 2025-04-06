import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Токеныг .env файлаас унших
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Ботыг command prefix-тэй эхлүүлэх (жишээ: "!")
bot = commands.Bot(
    command_prefix='!', 
    intents=discord.Intents.all(),
    help_command=None  # Default help командыг устгах
)

# Бот серверт холбогдсон үед
@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} бот ажиллаж эхлэлээ!')
    await bot.change_presence(activity=discord.Game(name="!тусламж"))

# Энгийн командууд
@bot.command(name='сайнбайнауу')
async def hello(ctx):
    await ctx.send(f'👋 Сайн байна уу, {ctx.author.mention}!')

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! ({latency}ms)')

# Модерацийн командууд
@bot.command(name='цэвэрлэх')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'🗑️ {amount} мессеж устгагдлаа!', delete_after=3)

# Алдааны боловсруулалт
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Танд энэ командыг ашиглах эрх байхгүй!")

# Custom Help командууд
@bot.command(name='тусламж')
async def help(ctx):
    embed = discord.Embed(
        title="📚 Ботын тухай",
        description="Бот командуудын жагсаалт:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!сайнбайнауу", value="Мэндчилгээ илгээнэ", inline=False)
    embed.add_field(name="!ping", value="Ботын latency шалгана", inline=False)
    embed.add_field(name="!цэвэрлэх [тоо]", value="Мессеж цэвэрлэнэ (Админ)", inline=False)
    await ctx.send(embed=embed)

# Ботыг ажиллуулах
if __name__ == '__main__':
    bot.run(TOKEN)
