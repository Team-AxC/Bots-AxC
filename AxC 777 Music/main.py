import os
import discord
from discord.ext import commands
from music_cog import music_cog
from alive import alive

bot = commands.Bot(command_prefix='?')
bot.add_cog(music_cog(bot))

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="?cmd"))
  # await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name="Rick Astley"))

my_secret = os.environ['BOT']
alive()
bot.run(my_secret)
