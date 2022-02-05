import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import youtube_dl
from lyrics_extractor import SongLyrics
import json
import os
from random import *
from sound_tinkerlab import *


music_cmds = "`?play [audio title]` (the bot will automatically join your voice channel in the server, and the audio will be added to the queue)\n`?lyrics [song title]` (will show the lyrics of the song)\n`?queue` \n`?skip` (to play the next song of the queue)\n`?pause`\n`?resume`\n`?stop`\n`?url [URL of the YouTube video]` (to play the sound of a YouTube video)\n`?loop [audio title] [looping constant (no. of times for the audio to loop)]` (to loop music n number of times)\n`?loop_10 [audio title]` (to loop music 10 times)\n`?disconnect` or `?dc` (to disconnect the bot from the voice channel)\n`?clear` (to clear the queue)\n`?fft [wav, mp3 or ogg attachment]` (Fast Fourier Transforms and sends the plot)"


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        self.vc = ""

    #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item,
                                        download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                         after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc is None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                         after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", help="Plays a selected song from YouTube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        else:
            # if (ctx.author == "Abhishek Saxena (https://github.com/chinmoysir)"):
            #         await ctx.send("RICKLOCKED 🔐\nNo more rickrolls allowed")

            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send(
                    "Could not play the song. Incorrect format, try another keyword. This could be due to a playlist or livestream format."
                )
            else:
                self.music_queue.append([song, voice_channel])

                # await ctx.send(
                #     f"Song added to the queue, just for you {ctx.author.mention}")

                self.personal_embed = discord.Embed(title = "Song added to Queue", color = 0x00ff00)

                self.personal_embed.add_field(name = "Song playing for: " , value = ctx.author.mention)
                self.personal_embed.set_author(name = "AxC777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80")
                
                await ctx.send(embed = self.personal_embed)

                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        if len(self.music_queue) <= 50:
            for i in range(len(self.music_queue)):
                retval += self.music_queue[i][0]['title'] + "\n"

            print(retval)

            if not retval:
                await ctx.send("No music in queue")

            else:
                await ctx.send(retval)
        else:
            for i in range(51):
                retval += self.music_queue[i][0]['title'] + "\n"

            print(retval)

            ctx.send(
                "First 50 songs shown. The queue is too long to be sent at once."
            )

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music()

            self.personal_embed = discord.Embed(title = "Skipped the Playing Audio", color = discord.Color.gold())
            self.personal_embed.set_author(name = "AxC777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")
                
            await ctx.send(embed = self.personal_embed)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected 🔇")

    @commands.command()
    async def dc(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected 🔇")

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused ⏸")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send('Resumed ⏯')

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("Stopped 🛑")

    @commands.command()
    async def url(self, ctx, url):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()

        else:
            await ctx.voice_client.move_to(voice_channel)

        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(
                url2, **FFMPEG_OPTIONS)
            await ctx.send("Playing the URL in the voice channel")
            vc.play(source)

    @commands.command()
    async def help(self, ctx):
        self.my_embed = discord.Embed(title="All commands:",
                                      description=music_cmds,
                                      color=0x00ff00)
        self.my_embed.set_author(
            name="author - Abhishek Saxena (https://github.com/chinmoysir)")
        await ctx.send(embed=self.my_embed)

    @commands.command()
    async def loop(self, ctx, *args):
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")

        else:
            content = list(args)
            # print(content)

            try:
                looping_constant = int(content[-1])

                content.pop()

                query = " ".join(content)
                # print(query)

                song = self.search_yt(query)

                if type(song) == type(True):
                    await ctx.send(
                        "Could not play the song. Incorrect format try another keyword. This could be due to a playlist or a livestream format."
                    )

                else:
                    await ctx.send("Song added to the queue")

                    for _ in range(looping_constant + 1):
                        self.music_queue.append([song, voice_channel])

                    if self.is_playing == False:
                        await self.play_music()

            except ValueError:
                await ctx.send(
                    "Improper looping constant found. Please keep the looping constant (i.e. the no of times the audio. should be looped) a whole number."
                )

    @commands.command()
    async def loop_10(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)

            if type(song) == type(True):
                await ctx.send(
                    "Could not play the song. Incorrect format try another keyword. This could be due to a playlist or a livestream format."
                )

            else:
                for _ in range(11):
                    self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def clear(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()

        for _ in range(len(self.music_queue)):
            self.music_queue.pop()

        await ctx.send("Queue Cleared!")
        await ctx.send(
            "https://tenor.com/view/were-all-clear-yellowstone-were-good-to-go-ready-lets-do-this-gif-17723207"
        )

    @commands.command()
    async def lyrics(self, ctx, *args):
        query = " ".join(args)

        json_api_key = os.environ['GCS_JSON_API']
        gcs_genius_engineid = os.environ['GCS_GENIUS_ENGINE_ID']

        extract_lyrics = SongLyrics(json_api_key, gcs_genius_engineid)

        try:
            lyrics = extract_lyrics.get_lyrics(query)

            self.my_embed = discord.Embed(title=lyrics['title'],
                                          description=lyrics['lyrics'])

        except Exception:
            error = "Lyrics not found. Try reframing the song title and/or check if the song even exists or you or I have ascended into a parallel universe.\n\n**Thanks!**\nTeam AxC"

            self.my_embed = discord.Embed(title=":octagonal_sign:  Error",
                                          description=error)

        await ctx.send(embed=self.my_embed)

    # Scientific commands and functions start

    @commands.command()
    async def sample_fft(self, ctx):
      my_embed = discord.Embed(title = "Sample Fast Fourier Transform", description = "\u200b")
      # sample_fft()
      file = discord.File("fft.png", filename = "fft.png")
      my_embed.set_image(url="attachment://fft.png")
      await ctx.send(file = file, embed = my_embed)

    @commands.command()
    async def fft(self, ctx):
      if str(ctx.message.attachments) == "[]": 
        await ctx.send("No attachment")

      else: 
        split_v1 = str(ctx.message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]

        allowed_extensions = ('wav', 'mp3', 'ogg')
        file_components = filename.split('.')

        if file_components[-1] in allowed_extensions:
          await ctx.message.attachments[0].save(fp = f'{filename}'.format(filename))

          print(filename)

          image_title = fft(filename)
          
          print(image_title)
  
          fft_image = discord.File(image_title, filename = "fft.png")
  
          await ctx.send(file = fft_image)
  
          os.remove(image_title)
          os.remove(f"{file_components[0]}.wav")

        else:
            await ctx.send("File type not supported")

