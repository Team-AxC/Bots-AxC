import os
import discord
from discord import *
import requests
import json
from random import randrange
from pprint import *
from weather import *
from keep_alive import *

client = discord.Client()
my_secret = os.environ['TOKEN']
open_weather_api_key = os.environ['weather_api_key']


#on ready function
@client.event
async def on_ready():
    #The bot is watching commands and nerdy stuff
    # await client.change_presence(activity=discord.Activity(
    #     type=discord.ActivityType.listening, name="$assist"))

    await client.change_presence(activity = discord.Game(name = f"in {len(client.guilds)} servers | $help"))

    # await client.change_presence(activity = discord.Game(name = f"🛑Temporary outage"))
    
    

    for please in range(len(client.guilds)):
      print(client.guilds[please])

    print(
        'ICBM launched by {0.user}, expect destruction soon (of your brain). Dimag Tikka Order being made...'
        .format(client))


#executables
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$convert F C '):
        temp_value = message.content.replace("$convert F C ", "")
        try:
            value = float(temp_value)
            conversion = (value - 32) * 5 / 9
            title = discord.Embed(title="🌡️ Temperature Conversion")
            convert_case = "Fahrenheit to Celsius"

            title.add_field(
                name=convert_case,
                value=f"The converted temperature is **{conversion}°C**",
                inline=False)
            title.set_footer(text="Formula used: C = (F-32) ⨉ 5/9")

            await message.channel.send(embed=title)

        except ValueError:
            await message.channel.send(
                "The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors."
            )

    if message.content.startswith('$convert F K '):
        temp_value = message.content.replace("$convert F K ", "")
        try:
            value = float(temp_value)
            conversion = ((value - 32) * 5 / 9) + 273.15
            title = discord.Embed(title="🌡️ Temperature Conversion")
            convert_case = "Fahrenheit to kelvin"

            title.add_field(
                name=convert_case,
                value=f"The converted temperature is **{conversion} K**",
                inline=False)
            title.set_footer(text="Formula used: K = (F-32) ⨉ 5/9 + 273.15")

            await message.channel.send(embed=title)

        except ValueError:
            await message.channel.send(
                "The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors."
            )

    if message.content.startswith('$convert C F '):
        temp_value = message.content.replace("$convert C F ", "")
        try:
            value = float(temp_value)
            conversion = (9 / 5 * value) + 32
            title = discord.Embed(title="🌡️ Temperature Conversion")
            convert_case = "Celsius to Fahrenheit"

            title.add_field(
                name=convert_case,
                value=f"The converted temperature is **{conversion}°F**",
                inline=False)
            title.set_footer(text="Formula used: F = (9/5 ⨉ C) + 32")

            await message.channel.send(embed=title)

        except ValueError:
            await message.channel.send(
                "The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors."
            )

    if message.content.startswith('$convert C K '):
        temp_value = message.content.replace("$convert C K ", "")
        try:
            value = float(temp_value)
            conversion = value + 273.15
            title = discord.Embed(title="🌡️ Temperature Conversion")
            convert_case = "Celsius to kelvin"

            title.add_field(
                name=convert_case,
                value=f"The converted temperature is **{conversion} K**",
                inline=False)
            title.set_footer(text="Formula used: K = C + 273.15")

            await message.channel.send(embed=title)

        except ValueError:
            await message.channel.send(
                "The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors."
            )

    if message.content.startswith('$convert K C '):
        temp_value = message.content.replace("$convert K C ", "")
        try:
            value = float(temp_value)
            conversion = value - 273.15
            title = discord.Embed(title="🌡️ Temperature Conversion")
            convert_case = "kelvin to Celsius"

            title.add_field(
                name=convert_case,
                value=f"The converted temperature is **{conversion}°C**",
                inline=False)
            title.set_footer(text="Formula used: C = K - 273.15")

            await message.channel.send(embed=title)

        except ValueError:
            await message.channel.send(
                "The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors."
            )

    if message.content.startswith('$convert K F '):
        temp_value = message.content.replace("$convert K F ", "")
        try:
            value = float(temp_value)
            conversion = (9 / 5 * (value - 273.15)) + 32
            title = discord.Embed(title="🌡️ Temperature Conversion")
            convert_case = "Celsius to Fahrenheit"

            title.add_field(
                name=convert_case,
                value=f"The converted temperature is **{conversion}°F**",
                inline=False)
            title.set_footer(
                text="Formula used: F = {9/5 ⨉ (K - 273.15)} + 32")

            await message.channel.send(embed=title)

        except ValueError:
            await message.channel.send(
                "The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper temperature values without any symbols of sorts to avoid errors."
            )

    if message.content.startswith("$convert m km "):
        temp_value = message.content.replace("$convert m km ", "")
        try:
            value = float(temp_value)
            conversion = value / 1000
            title = discord.Embed(
                title=":straight_ruler: ️ Distance Conversion")
            convert_case = "meters to kilometers"

            title.add_field(
                name=convert_case,
                value=f"The converted distance is **{conversion} km**",
                inline=False)
            title.set_footer(text="Formula used: km = m / 1000")

            await message.channel.send(embed=title)

        except ValueError:
            await message.channel.send(
                "The input was in an incorrect format. It looks like that you might have not used numbers and/or have additional text in your message. Please try to keep the message to the command itself with proper distance values without any symbols of sorts to avoid errors."
            )

    if message.content.startswith("$spam "):
        spammer = message.content.replace("$spam ", "")

        for _ in range(11):
            await message.channel.send(spammer)

    if message.content.startswith("$random_spam"):
        spam2 = "Science is Everything"
        spam3 = "Computer Forever"
        spam4 = "e"
        spam5 = "Rick Roll"

        x = randrange(6)

        if x == 1:
            spam1 = "CRISPR-Cas9 Bring me a gene (A Capella Science)"
            for _ in range(10):
                await message.channel.send(spam1)

        elif x == 2:
            for _ in range(10):
                await message.channel.send(spam2)

        elif x == 3:
            for _ in range(10):
                await message.channel.send(spam3)

        elif x == 4:
            for _ in range(10):
                await message.channel.send(spam4)

        elif x == 5:
            for _ in range(10):
                await message.channel.send(spam5)


keep_alive()
client.run(my_secret)
