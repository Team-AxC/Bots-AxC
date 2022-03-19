import discord
from discord import ApplicationContext
from discord.commands import slash_command, Option
from discord.ext import commands
from task_code import play, spotify_and_song_info, scientific_and_esoskeric, miscellaneous
from alive import *
from dotenv import load_dotenv
import os
import random
import asyncio

bot = discord.Bot()

load_dotenv('secret.env')
my_secret = os.getenv('TOKEN')


class main_slash_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.play_thingy = play.play_stuff()
        self.spotify_and_song_info = spotify_and_song_info.song_info()
        self.scientific_and_esoskeric = scientific_and_esoskeric.scientific_and_esoskeric()
        self.miscellaneous = miscellaneous.miscellaneous(self.play_thingy)

    # Play.py file, play_stuff class
    @slash_command(name="play", description="Plays audio from YouTube")
    async def play(self, ctx: ApplicationContext, audio: Option(str, "The title to search for", required = True)):
        await self.play_thingy.play_from_query(ctx, audio)

    @slash_command(name="loop", description="Loops audio n number of times (n is user-defined, defaults to 10)")
    async def loop(self, ctx: ApplicationContext, audio: Option(str, "The audio you want to loop", required = True), looping_constant: Option(int, "No. of times you want to loop the audio (defaults to 10)", required = False, default = 10)):
        await self.play_thingy.loop_query(ctx, audio, looping_constant)

    @slash_command(name="url", description="Plays the audio of the provided YouTube URL")
    async def url(self, ctx: ApplicationContext, url: Option(str, "The YouTube URL you want to play", required = True)):
        await self.play_thingy.play_from_url(ctx, url)

    # miscellaneous.py file, miscellaneous class
    @slash_command(name="queue", description="Displays the audio in queue")
    async def queue(self, ctx: ApplicationContext):
        await self.miscellaneous.queue(ctx)

    @slash_command(name="skip", description="Skips the audio being played and plays the next audio in the queue")
    async def skip(self, ctx: ApplicationContext):
        await self.miscellaneous.skip(ctx)

    @slash_command(name="disconnect", description="Disconnects the bot from the voice channel")
    async def disconnect(self, ctx: ApplicationContext):
        await self.miscellaneous.disconnect(ctx)

    @slash_command(name="pause", description="Pauses the audio")
    async def pause(self, ctx: ApplicationContext):
        await self.miscellaneous.pause(ctx)

    @slash_command(name="resume", description="Resumes the audio")
    async def resume(self, ctx: ApplicationContext):
        await self.miscellaneous.resume(ctx)

    @slash_command(name="stop", description="Stops the audio")
    async def stop(self, ctx: ApplicationContext):
        await self.miscellaneous.stop(ctx)

    @slash_command(name="latency", description="Shows the latency of the bot")
    async def latency(self, ctx: ApplicationContext):
        await self.miscellaneous.latency(ctx, self.bot)

    # spotify_and_song_info.py file, song_info class
    @slash_command(name="lyrics", description="Shows the lyrics of a song")
    async def lyrics(self, ctx: ApplicationContext, song: Option(str, "The song you want to find the lyrics of", required = True)):
        await self.spotify_and_song_info.lyrics(ctx, song)

    @slash_command(name="top_tracks", description="Shows the top tracks of an artist")
    async def top_tracks(self, ctx: ApplicationContext, artist: Option(str, "The artist you want to find the top tracks of", required = True)):
        await self.spotify_and_song_info.top_tracks(ctx, artist)

    # scientific_and_esoskeric.py file, scientific_and_esoskeric class
    @slash_command(name="ft", description="Fourier transforms the attachment using the Fast Fourier Transform algorithm")
    async def fft(self, ctx: ApplicationContext, file: Option(discord.Attachment, "The file you want to Fourier Transform", required = True)):
        await self.scientific_and_esoskeric.fft(ctx, file)

################################################################################################
# Running the bot and stuff #
################################################################################################

def setup(bot: discord.Bot):
    @bot.event
    async def on_ready():
        for please in range(len(bot.guilds)):
            print(bot.guilds[please])

        print(f"\n{len(bot.guilds)} servers")


    async def ch_pr():
        await bot.wait_until_ready()
        statuses = [f"{len(bot.guilds)} servers | / cmds", f"{len(bot.guilds)} servers | ?switch", "Rick Roll | / cmds"]

        while not bot.is_closed():
            main_status = random.choice(statuses)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=main_status))

            await asyncio.sleep(10)

    bot.loop.create_task(ch_pr())

    bot.add_cog(main_slash_cog(bot))
    keep_alive()
    bot.run(my_secret)

