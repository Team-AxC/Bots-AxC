#imports
import discord 
from discord.ext import commands
import os
import requests
import json
from keep_alive import *
from discord.ext.commands import *
from pprint import *
from weather import *

#defining the command variable
client = commands.Bot(command_prefix = '$')
client.remove_command("help") # now assist is help WOW
open_weather_api_key = os.environ['weather_api_key']
cmds = '**MODERATION COMMANDS:**\n'

regular_cmds = "$intro\n$help\n$inspire\n$devinfo\n$joke\n$cat_fact\n$weather (Syntax: `$weather [City]`, e.g. `$weather Lucknow`)\n$convert [original temperature unit] [desired temperature unit] [numeral temperature value] e.g. `$convert F C 212` \n**Note:** Distance conversation in beta. Only conversion from `m` to `km` currently available. The format is the same as the temperature conversion syntax, e.g. `$convert m km 50`\n$spam [message], e.g. `$spam Cool Science`\n$random_spam"

mod_cmds = "$kick [member name] [reason]\n$ban [member name] [reason]\n$unban [member name]\n$clear [number of messages to clear]\n$warn [member name] [reason]\n\n NOTE: the member you are warning,banning or kicking from the server should be on a lower role than the BOT"

#functions
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  return f'{json_data[0]["q"]} -{json_data[0]["a"]}'  

def get_joke():
  response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=racist&type=single")
  json_data = json.loads(response.text)
  return json_data["joke"]

#commands
@client.command()
async def intro(ctx):
  grogu_hello = "https://tenor.com/view/mandalorian-baby-yoda-hello-gif-19013340"

  intro_embed = discord.Embed(title = "Essential Introduction", description = "Hey there! I am AxC 777. I am very nerdy 🤓, and made by Abhishek, in collaboration with Chinmay. I am meant to be general purpose with **a lot** of features being worked on and should be added down the road!")
  intro_embed.add_field(name = "Version 0.3a", value = "Development stage: Beta", inline=False)
  intro_embed.add_field(name = "GitHub Repo :ninja:", value = "https://github.com/chinmoysir/DISCORD-BOT")
  intro_embed.add_field(name = "Release Month :calendar_spiral:", value = "September 2021", inline = False)
  intro_embed.add_field(name = "Use the `$assist` command for the list of available commands ", value = "\u200b", inline=False)
  await ctx.send(grogu_hello)
  await ctx.send(embed = intro_embed)

@client.command()
async def namaste(ctx, member : discord.Member):
  await ctx.send(f"AxC777 says namaste to {member} on behalf of {ctx.author}")

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
  try:
    try:
      await member.send(f'You have been kicked from a server , Because:{reason}')

    except:
      pass

    await member.kick(reason = reason)

  except:
    my_embed = discord.Embed(title = "", description = "", color = 0x552E12)

    my_embed.add_field(name = "ERROR :red_circle:", value = "either the bot is on a lower role than the member or the both the member and the bot are at the same role")
    await ctx.send(embed = my_embed)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member,*, reason = "*No specific reason provided to by the moderator*"):
  await member.send(f"You have been banned from a server by {ctx.author}, because:"+reason)
  await member.ban(reason = reason)

  ctx.send(f"{ctx.member} has banned and kicked by {ctx.author}")

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
  banned_users = await ctx.guild.bans()
  member_name , member_disc = member.split('#')

  for banned_entry in banned_users:
    user = banned_entry.user

    if (user.name, user.discriminator) == (member_name,member_disc):
      await ctx.guild.unban(user)
      await ctx.send(f'{member_name} has been unbanned!')

    else:
      await ctx.send(f'{member} was not found')

@client.command()
@commands.has_permissions(ban_members = True)
async def warn(ctx, member : discord.Member,*, reason = "*No specific reason provided to by the moderator*"):
  my_embed = discord.Embed(title = f"{ctx.author} has warned {member}",colour=0x400080)
  my_embed.add_field(name = "Reason:", value= reason, inline=False)
  await ctx.send(embed = my_embed)

@client.command()
async def help(ctx):
  my_embed = discord.Embed(title = "", description = "", color = 0x00ff00)

  my_embed.add_field(name = "REGULAR COMMANDS", value = regular_cmds)
  my_embed.add_field(name = "MODERATION COMMANDS" , value = mod_cmds)

  my_embed.set_author(name="Abhishek Saxena (https://github.com/chinmoysir)")
  await ctx.send(embed = my_embed)

@client.command()
async def weather(ctx, *args):
  location = " ".join(args)
  url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={open_weather_api_key}&units=metric'
  try:
      data = parse_data(json.loads(requests.get(url).content)['main'])
      await ctx.send(embed=weather_message(data, location))
        
  except KeyError:
      await ctx.send(embed=error_message(location))

@client.command()
async def attachment_link(ctx):
  attachments = ctx.message.attachments

  for file_no in range(len(attachments)):
    await ctx.send(f"`{attachments[file_no].url}`")
    
    
keep_alive()
my_secret = os.environ['BOT']
client.run(my_secret)
