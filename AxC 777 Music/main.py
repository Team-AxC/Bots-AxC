import os
import discord
from discord.ext import commands
from music_cog import music_cog
from alive import keep_alive
import random
import asyncio

bot = commands.Bot(command_prefix='?')
bot.remove_command("help")
bot.add_cog(music_cog(bot))

status_1 = f"{len(bot.guilds)} servers | ?help"
status_2 = "RICK ROLL"

@bot.event
async def on_ready():
  for please in range(len(bot.guilds)):
    print(bot.guilds[please])

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command!\nTo know all cmds message `?help`')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Bot Permission Missing!')

    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please retry the cmd with the required Argument")

async def ch_pr():
  await bot.wait_until_ready()
  statuses = [f"{len(bot.guilds)} servers | ?help", "Rick Roll | ?help"]

  while not bot.is_closed():
    main_status = random.choice(statuses)
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.listening, name = main_status))

    await asyncio.sleep(10)

bot.loop.create_task(ch_pr())

my_secret = os.environ['BOT']
keep_alive()
bot.run(my_secret)
