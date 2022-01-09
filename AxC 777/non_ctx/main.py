import os
import discord
from discord import *
import requests
import json
from random import randrange
from pprint import *
from weather import *
from keep_alive import *
import time

client = discord.Client()
my_secret = os.environ['TOKEN']
open_weather_api_key = os.environ['weather_api_key']
# cmds = '**REGULAR COMMANDS:**\n$intro\n$help\n$inspire\n$devinfo\n$joke\n$cat_fact\n$weather (Syntax: `$weather [City]`, e.g. `$weather Lucknow`)\n$convert [original temperature unit] [desired temperature unit] [numeral temperature value] e.g. `$convert F C 212` **Note:** Distance conversation in beta. Only conversion from `m` to `km` currently available. The format is the same as the temperature conversion syntax, e.g. `$convert m km 50`\n$spam [message], e.g. `$spam Cool Science`\n'

# music_cmds = "`?play [with song/music composition name]` (the bot will automatically join your voice channel in the server, and the song/musical composition will be added to the queue)\n`?lyrics [song title]` (will show the lyrics of the song)\n`?queue` \n`?skip` (to play the next song of the queue)\n`?pause`\n`?resume`\n`?stop`\n `?url [with the URL of the YouTube video]` (to play the sound of a YouTube video)\n`?loop [audio name] [looping constant (no. of times for the audio to loop)]` (to loop music n number of times)\n`?loop_10 [audio name]` (to loop music 10 times)\n`?disconnect` (to disconnect the bot from the voice channel)\n`?clear` (to clear the queue)"

#on ready function
@client.event
async def on_ready():
  #The bot is watching commands and nerdy stuff
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="$assist"))
  print('ICBM launched by {0.user}, expect destruction soon (of your brain). Dimag Tikka Order being made...'.format(client))

#executables
@client.event
async def on_message(message):
  if message.author == client.user:
    return


  if message.content.startswith('$weather'):
    location = message.content.replace("$weather ", '')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={open_weather_api_key}&units=metric'
    try:
      data = parse_data(json.loads(requests.get(url).content)['main'])
      await message.channel.send(embed=weather_message(data, location))
    except KeyError:
      await message.channel.send(embed=error_message(location))

  if message.content.startswith('$convert F C '):
    temp_value = message.content.replace("$convert F C ","")
    try:
      value = float(temp_value)
      conversion = (value-32) * 5/9
      title = discord.Embed(title = "🌡️ Temperature Conversion")
      convert_case = "Fahrenheit to Celsius"

      title.add_field(name = convert_case, value = f"The converted temperature is **{conversion}°C**", inline=False)
      title.set_footer(text = "Formula used: C = (F-32) ⨉ 5/9")


      await message.channel.send(embed = title)

    except ValueError:
      await message.channel.send("The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors.")

  if message.content.startswith('$convert F K '):
    temp_value = message.content.replace("$convert F K ","")
    try:
      value = float(temp_value)
      conversion = ((value-32) * 5/9) + 273.15
      title = discord.Embed(title = "🌡️ Temperature Conversion")
      convert_case = "Fahrenheit to kelvin"

      title.add_field(name = convert_case, value = f"The converted temperature is **{conversion} K**", inline=False)
      title.set_footer(text = "Formula used: K = (F-32) ⨉ 5/9 + 273.15")


      await message.channel.send(embed = title)

    except ValueError:
      await message.channel.send("The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors.")

  if message.content.startswith('$convert C F '):
    temp_value = message.content.replace("$convert C F ","")
    try:
      value = float(temp_value)
      conversion = (9/5 * value) + 32
      title = discord.Embed(title = "🌡️ Temperature Conversion")
      convert_case = "Celsius to Fahrenheit"

      title.add_field(name = convert_case, value = f"The converted temperature is **{conversion}°F**", inline=False)
      title.set_footer(text = "Formula used: F = (9/5 ⨉ C) + 32")


      await message.channel.send(embed = title)

    except ValueError:
      await message.channel.send("The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors.")

  if message.content.startswith('$convert C K '):
    temp_value = message.content.replace("$convert C K ","")
    try:
      value = float(temp_value)
      conversion = value + 273.15
      title = discord.Embed(title = "🌡️ Temperature Conversion")
      convert_case = "Celsius to kelvin"

      title.add_field(name = convert_case, value = f"The converted temperature is **{conversion} K**", inline=False)
      title.set_footer(text = "Formula used: K = C + 273.15")


      await message.channel.send(embed = title)

    except ValueError:
      await message.channel.send("The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors.")

  if message.content.startswith('$convert K C '):
    temp_value = message.content.replace("$convert K C ","")
    try:
      value = float(temp_value)
      conversion = value - 273.15
      title = discord.Embed(title = "🌡️ Temperature Conversion")
      convert_case = "kelvin to Celsius"

      title.add_field(name = convert_case, value = f"The converted temperature is **{conversion}°C**", inline=False)
      title.set_footer(text = "Formula used: C = K - 273.15")


      await message.channel.send(embed = title)

    except ValueError:
      await message.channel.send("The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors.")

  if message.content.startswith('$convert K F '):
    temp_value = message.content.replace("$convert K F ","")
    try:
      value = float(temp_value)
      conversion = (9/5 * (value - 273.15)) + 32
      title = discord.Embed(title = "🌡️ Temperature Conversion")
      convert_case = "Celsius to Fahrenheit"

      title.add_field(name = convert_case, value = f"The converted temperature is **{conversion}°F**", inline=False)
      title.set_footer(text = "Formula used: F = {9/5 ⨉ (K - 273.15)} + 32")


      await message.channel.send(embed = title)

    except ValueError:
      await message.channel.send("The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors.")

  if message.content.startswith("$convert m km "):
      temp_value = message.content.replace("$convert m km ", "")
      try:
        value = float(temp_value)
        conversion = value / 1000
        title = discord.Embed(title=":straight_ruler: ️ Distance Conversion")
        convert_case = "meters to kilometers"
        
        title.add_field(name=convert_case, value=f"The converted distance is **{conversion} km**", inline=False)
        title.set_footer(text="Formula used: km = m / 1000")
        
        await message.channel.send(embed=title)
        
      except ValueError:
        await message.channel.send("The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper distance values without any symbols of sorts to avoid errors.")

  if message.content.startswith("$spam "):
    spammer = message.content.replace("$spam ","")

    for num in range(11):
      await message.channel.send(spammer)

  if message.content.startswith("$random_spam"):
    spam1 = "CRISPR-Cas9 Bring me a gene (A Capella Science)"
    spam2 = "Science is Everything"
    spam3 = "Computer Forever"
    spam4 = "e"
    spam5 = "Rick Roll"

    x = randrange(6)

    if x == 1:
      i = 0
      while i < 2:
        await message.channel.send(spam1)
        

    elif x == 2:
      i = 0
      while i < 2:
        await message.channel.send(spam2)
        

    elif x == 3:
      i = 0
      while i < 2:
        await message.channel.send(spam3)
        

    elif x == 4:
      i = 0
      while i < 2:
        await message.channel.send(spam4)
        

    elif x == 5:
      i = 0
      while i < 2:
        await message.channel.send(spam5)
        

    else:
      pass

  


keep_alive()
client.run(my_secret)
