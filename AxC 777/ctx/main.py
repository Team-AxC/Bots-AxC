#imports
import discord 
from discord.ext import commands
import os
import requests
import json
from keep_alive import *
from discord import User
from discord.ext.commands import Bot, guild_only

#defining the command variable
client = commands.Bot(command_prefix = '$')
open_weather_api_key = os.environ['weather_api_key']
cmds = '**REGULAR COMMANDS:**\n$intro\n$help\n$inspire\n$devinfo\n$joke\n$cat_fact\n$weather (Syntax: `$weather [City]`, e.g. `$weather Lucknow`)\n$convert [original temperature unit] [desired temperature unit] [numeral temperature value] e.g. `$convert F C 212` \n**Note:** Distance conversation in beta. Only conversion from `m` to `km` currently available. The format is the same as the temperature conversion syntax, e.g. `$convert m km 50`\n$spam [message], e.g. `$spam Cool Science`\n\n**MODERATION COMMANDS:**\n$kick\n$ban\n$warn'

music_cmds = "`?play [with audio title]` (the bot will automatically join your voice channel in the server, and the audio will be added to the queue)\n`?lyrics [song title]` (will show the lyrics of the song)\n`?queue` \n`?skip` (to play the next song of the queue)\n`?pause`\n`?resume`\n`?stop`\n `?url [with the URL of the YouTube video]` (to play the sound of a YouTube video)\n`?loop [audio title] [looping constant (no. of times for the audio to loop)]` (to loop music n number of times)\n`?loop_10 [audio title]` (to loop music 10 times)\n`?disconnect` or `?dc` (to disconnect the bot from the voice channel)\n`?clear` (to clear the queue)"

#functions
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)  

def get_joke():
  response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=racist&type=single")
  json_data = json.loads(response.text)
  joke = json_data["joke"]
  return (joke)

#commands
@client.command()
async def intro(ctx):
  grogu_hello = "https://tenor.com/view/mandalorian-baby-yoda-hello-gif-19013340"

  intro_embed = discord.Embed(title = "Essential Introduction", description = "Hey there! I am AxC 777. I am very nerdy 🤓, and made by Abhishek, in collaboration with Chinmay. I am meant to be general purpose with **a lot** of features being worked on and should be added down the road!")
  intro_embed.add_field(name = "Version 0.3", value = "Development stage: Beta", inline=False)
  intro_embed.add_field(name = "GitHub Repo :ninja:", value = "https://github.com/chinmoysir/DISCORD-BOT")
  intro_embed.add_field(name = "Release Time", value = "September 2021", inline = False)
  intro_embed.add_field(name = "Use the `$assist` command for the list of available commands ", value = "\u200b", inline=False)
  await ctx.send(grogu_hello)
  await ctx.send(embed = intro_embed)

@client.command()
async def dev_info(ctx):
  my_embed = discord.Embed(title = "The Creator himself:", description = "Abhishek Saxena")
  my_embed.add_field(name = "Creator description:", value="A *Homo abhishekus* (new species) with God powers in programming", inline=False)
  my_embed.add_field (name = "Co-Creator:", value = "Chinmay Krishna", inline=False)
  my_embed.add_field(name = "Creator description:", value="A person that has more knowledge in physics than our physics teacher",inline=False)
  await ctx.send(embed = my_embed)

@client.command()
async def inspire(ctx):
  quote = get_quote()
  await ctx.send(quote)

@client.command()
async def joke(ctx):
  joke = get_joke()
  await ctx.send(joke)

@client.command()
async def cat_fact(ctx):
  data = requests.get('https://catfact.ninja/fact').json()
  embed = discord.Embed(title=f'Random Cat Fact Number: **{data["length"]}**', description=f'Cat Fact: {data["fact"]}', colour=0x400080)
  embed.set_footer(text="")
  await ctx.send(embed=embed)

@client.command()
async def clear(ctx, amount = 2):
  await ctx.channel.purge(limit = amount)

@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*, reason = "*No specific reason provided to by the moderator*"):
  await member.send("You have been kicked from a server , Because:"+reason)
  await member.kick(reason = reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member,*, reason = "*No specific reason provided to by the moderator*"):
  await member.send("You have been banned from a server, because:"+reason)
  await member.ban(reason = reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
  banned_users = await ctx.guild.bans()
  member_name , member_disc = member.split('#')

  for banned_entry in banned_users:
    user = banned_entry.user

    if(user.name, user.discriminator) == (member_name,member_disc):
      await ctx.guild.unban(user)
      await ctx.send(member_name + " has been unbanned!")

  await ctx.send(member+" was not found")

@client.command()
async def warn(ctx, member : discord.Member,*, reason = "*No specific reason provided to by the moderator*"):
  my_embed = discord.Embed(title = f"{ctx.author} has warned {member}",colour=0x400080)
  my_embed.add_field(name = "Reason:", value= reason, inline=False)
  await ctx.send(embed = my_embed)

@client.command()
async def assist(ctx):
    my_embed = discord.Embed(title = "All commands:", description = cmds, color = 0x00ff00)
    my_embed.add_field(name = "\n\nMusic Commands for AxC 777 Music\n(make sure that the music bot is in the server)", value=music_cmds, inline=False)
    my_embed.set_author(name="Abhishek Saxena (https://github.com/chinmoysir)")
    await ctx.send(embed = my_embed)
    
keep_alive()
my_secret = os.environ['BOT']
client.run(my_secret)
