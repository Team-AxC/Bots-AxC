#imports
import discord 
from discord.ext import commands
from discord_components import *
import os
import requests
import json
from keep_alive import keep_alive
from discord.ext.commands import *
from discord_slash import *
from pprint import *
from weather import *
import random
import datetime
# from slash import main_cog

#defining the command variable
client = commands.Bot(command_prefix = '$')
slash = SlashCommand(client, sync_commands = True)
client.remove_command("help")
# client.add_cog(main_cog(client))
open_weather_api_key = os.environ['weather_api_key']
cmds = '**MODERATION COMMANDS:**\n'


regular_cmds = "$intro\n$help\n$inspire\n$devinfo\n$joke\n$cat_fact\n$weather (Syntax: `$weather [City]`, e.g. `$weather Lucknow`)\n$convert [original temperature unit] [desired temperature unit] [numeral temperature value] e.g. `$convert F C 212` \n**Note:** Distance conversation in beta. Only conversion from `m` to `km` currently available. The format is the same as the temperature conversion syntax, e.g. `$convert m km 50`\n$spam [message], e.g. `$spam Cool Science`\n$random_spam"

mod_cmds = "$kick [member name] [reason]\n$ban [member name] [reason]\n$unban [member name]\n$clear [number of messages to clear]\n$warn [member name] [reason]\n\n NOTE: the member you are warning,banning or kicking from the server should be on a lower role than the BOT"

game_tic = "**Tic Tac Toe Game:** \n$tictactoe [ping the player 1] [ping the player 2] (starts a tic tac toe game for you and your friend)\n$place [number of the tile]\n$end_tictactoe\nNOTE: don't ping a role or yourself twice"

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command!\nTo know all cmds write `$help`')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Bot Permission Missing!')

    elif isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please retry the cmd with the required Argument")

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
@client.command(aliases = ['Bombyx mori', '*Bombyx mori*'])
async def Bombyx_mori(ctx):
  await ctx.send("Bombyx mori, maine silkworm nahi ugaayo")

@client.command()
async def intro(ctx):
  grogu_hello = "https://tenor.com/view/mandalorian-baby-yoda-hello-gif-19013340"

  intro_embed = discord.Embed(title = "Essential Introduction", description = "Hey there! I am AxC 777. I am very nerdy 🤓, and made by Abhishek, in collaboration with Chinmay. I am meant to be general purpose with **a lot** of features being worked on and should be added down the road!")
  intro_embed.add_field(name = "Version 0.4a", value = "Development stage: Beta", inline=False)
  intro_embed.add_field(name = "GitHub Repo :ninja:", value = "https://github.com/abhisheksaxena11jul/DISCORD-BOT")
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
      await member.send("You have been kicked from a server , Because:"+reason)

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

    if(user.name, user.discriminator) == (member_name,member_disc):
      await ctx.guild.unban(user)
      await ctx.send(member_name + " has been unbanned!")

    else:
      await ctx.send(member+" was not found")

@client.command()
@commands.has_permissions(ban_members = True)
async def warn(ctx, member : discord.Member,*, reason = "*No specific reason provided to by the moderator*"):
  my_embed = discord.Embed(title = f"{ctx.author} has warned {member}",colour=0x400080)
  my_embed.add_field(name = "Reason:", value= reason, inline=False)
  await ctx.send(embed = my_embed)

@client.command()
async def help(ctx):
  my_embed = discord.Embed(title = "", description = "", color = 0x00ff00)

  my_embed.add_field(name = "REGULAR COMMANDS", value = regular_cmds, inline = True)
  my_embed.add_field(name = "MODERATION COMMANDS" , value = mod_cmds, inline = True)
  my_embed.add_field(name = "Games and Fun Things" , value = game_tic)

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

# HARRY POTTER COMMANDS
# @client.command()
# async def btn(ctx):
    # await ctx.send("hello", components = # [
    #     [Button(label="Hi", style="3", emoji = "🥴", custom_id="button1"), Button(label="Bye", style="4", emoji = "😔", custom_id="button2")# ]
    #     ]# )
    # interaction = await client.wait_for("button_click", check = lambda i: i.custom_id == "button1"# )
    # await interaction.send(content = "Button clicked!", ephemeral=True)

#tic tac toe cmd
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command(aliases = ['ttt'])
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the $tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
      await ctx.send("Please make sure to enter an integer.")

def end_game():
  global gameOver
  if not gameOver:
    result = "GAME ENDED"
    gameOver = True

  else:
    result = "NO TICTACTOE GAME IS IN PROCESS"

  return result

@client.command()
async def end_tictactoe(ctx):
  send = end_game()
  await ctx.send(send)

@slash.slash(name = "Intro", description = "A little intro!")
async def introduction(ctx: SlashContext):
  grogu_hello = "https://tenor.com/view/mandalorian-baby-yoda-hello-gif-19013340"

  intro_embed = discord.Embed(title = "Essential Introduction", description = "Hey there! I am AxC 777. I am very nerdy 🤓, and made by Abhishek, in collaboration with Chinmay. I am meant to be general purpose with **a lot** of features being worked on and should be added down the road!")
  intro_embed.add_field(name = "Version 0.4a", value = "Development stage: Beta", inline=False)
  intro_embed.add_field(name = "GitHub Repo :ninja:", value = "https://github.com/abhisheksaxena11jul/DISCORD-BOT")
  intro_embed.add_field(name = "Release Month :calendar_spiral:", value = "September 2021", inline = False)
  intro_embed.add_field(name = "Use the `$assist` command for the list of available commands ", value = "\u200b", inline=False)
  await ctx.send(grogu_hello)
  await ctx.send(embed = intro_embed)

@slash.slash(name = "TicTacToe", description = "Starts a TicTacToe game")
async def tictactoe_slash(ctx: SlashContext, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@slash.slash(name = "Place", description = "Make your move in TicTacToe", guild_ids = [89071189820055564])
async def place_ctx(ctx: SlashContext, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the $tictactoe command.")


@tictactoe_slash.error
async def tictactoe_error_slash(ctx: SlashContext, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players")

@place_ctx.error
async def place_error_slash(ctx: SlashContext, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
      await ctx.send("Please make sure to enter an integer.")

@slash.slash(name = "End Tictactoe", description = "Ends the running TicTacToe game")
async def end_tictactoe_slash(ctx: SlashContext):
  send = end_game()
  await ctx.send(send)

  
keep_alive()
my_secret = os.environ['BOT']
client.run(my_secret)
