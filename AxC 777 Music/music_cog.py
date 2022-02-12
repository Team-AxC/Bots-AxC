import discord
from discord.ext import commands
from discord.ext.commands import *
from discord_components import *
from discord_slash import *
import spotipy
from spotipy.oauth2 import *
from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch
from pytube import YouTube as pyt
import youtube_dl
from lyrics_extractor import SongLyrics
import json
import os
from random import *
from sound_tinkerlab import *
# from discord_slash import *



# music_cmds = "`?play [audio title]` (the bot will automatically join your voice channel in the server, and the audio will be added to the queue)\n`?lyrics [song title]` (will show the lyrics of the song)\n`?queue` \n`?skip` (to play the next song of the queue)\n`?pause`\n`?resume`\n`?stop`\n`?url [URL of the YouTube video]` (to play the sound of a YouTube video)\n`?loop [audio title] [looping constant (no. of times for the audio to loop)]` (to loop music n number of times)\n`?loop_10 [audio title]` (to loop music 10 times)\n`?disconnect` or `?dc` (to disconnect the bot from the voice channel)\n`?clear` (to clear the queue)\n"

music_cmds_dict = {
  'normal_cmds': {
    0: 
    [
    '**Command: **`?play [audio title]`', 
    '**Aliases: **`?p`,`?pl`',
    '**Command Description: **Plays audio from YouTube in the voice channel of the message author'
    ],

    1:
    [
      '**Command: **`?lyrics [song title]`',
      '**Alias: **`?ly`',
      '**Command Description: **Shows the lyrics of a song'
    ],

    2:
    [
      '**Command: **`?queue`',
      '**Alias: **`?q`',
      "**Command Description: **Shows the audio queue (the stuff to be played after the current audio is over)"
    ],
    

    3:
    [
      '**Command: **`?skip`',
      '**Alias: **`?sk`',
      '**Command Description: **Skips the audio currently playing in the voice channel and play the next in the queue, if any'
    ],

    4:
    [
      '**Command: **`?pause`',
      '**Alias: **`?pa`',
      "**Command Description: **Pauses the audio which is playing"
    ],

    5:
    [
      '**Command: **`?resume`',
      '**Alias: **`?r`',
      "**Command Description: **Resumes the paused audio"
    ],

    6:
    [
      '**Command: **`?stop`',
      '**Alias: **`?s`',
      "**Command Description: **Skips playing the audio and does not plays the next item in the queue"
    ],

    7:
    [
      '**Command: **`?url [YouTube video URL]`',
      '**Alias: **None',
      "**Command Description: **Plays the audio of a YouTube link (URL)"
    ],

    8:
    [
      '**Command: **`?loop [title] [looping constant (no. of times to loop the audio, completely optional)]`',
      '**Alias: **`?l`',
      "**Command Description: **Loops some audio n number of times, where n is the looping constant (defaults to 10 times, i.e. without any looping constant)"
    ],

    9:
    [
      '**Command: **`?disconnect`',
      '**Alias: **`?dc`',
      "**Command Description: **Disconnects the bot from a connected voice channel"
    ],

    10:
    [
      '**Command: **`?clear`',
      '**Alias: **`?c`',
      "**Command Description: **Clears the queue"
    ]
    
  }
}

regular_cmds = ""

for i in range(len(music_cmds_dict['normal_cmds'])):
    for y in range(3):
        regular_cmds = regular_cmds + music_cmds_dict['normal_cmds'][i][y] + "\n"
        
    regular_cmds = regular_cmds + "\n"

      # print(regular_cmds)

        
      # print(regular_cmds)

scientific_cmds = "`?fft [wav, mp3 or ogg attachment]` (Fast Fourier Transforms and sends the plot)"

sp_clientid = os.environ['SPOTIFY_CLIENTID']
sp_clientsecret = os.environ['SPOTIFY_CLIENTSECRET']


json_api_key = os.environ['GCS_JSON_API']
gcs_genius_engineid = os.environ['GCS_GENIUS_ENGINE_ID']

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=sp_clientid, client_secret=sp_clientsecret))



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

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
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

    @commands.command(name="play", help="Plays a selected song from YouTube", aliases = ['p','pl'])
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        else:
            # if (ctx.author == "Abhishek Saxena ()"):
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

                self.personal_embed = discord.Embed(title = "Song added to Queue", color = 0xFF0000)

                if self.is_playing == False:
                    await self.play_music()

                results = YoutubeSearch(query, max_results=1).to_dict()

                yt_link = f"https://www.youtube.com/watch?v={results[0]['id']}"

                yt_video_info = pyt(yt_link)
                
                self.personal_embed.add_field(name = ":adult: Audio playing for:" , value = ctx.author.mention)

                self.personal_embed.add_field(name = ":musical_note: Audio:" , value = f"[{yt_video_info.title}]({yt_link})", inline = False)

                self.personal_embed.add_field(name = ":hourglass_flowing_sand: Duration:" , value = f"{yt_video_info.length // 60} min {yt_video_info.length % 60} s", inline = False)

                self.personal_embed.add_field(name = ":eye: Views (on YouTube):" , value = f"{format(int(yt_video_info.views),',d')}", inline = False)

                self.personal_embed.set_thumbnail(url = yt_video_info.thumbnail_url)

                self.personal_embed.set_author(name = "AxC 777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80")

                await ctx.send(embed = self.personal_embed)
                


    @commands.command(name="queue", help="Displays the current songs in queue", aliases = ['q'])
    async def queue(self, ctx):
        if len(self.music_queue) <= 50:
            retval = ""
            for i in range(0, len(self.music_queue)):
                retval += self.music_queue[i][0]['title'] + "\n"

            print(retval)

            if retval != "":
                await ctx.send(retval)
                await ctx.send('https://tenor.com/view/squid-game-netflix-egybest-film-squid-gif-23324577')
            else:
                await ctx.send("No music in queue")

        else:
            retval = ""
            for i in range(0, 51):
                retval += self.music_queue[i][0]['title'] + "\n"

            print(retval)

            ctx.send(
                "First 50 songs shown. The queue is too long to be sent at once."
            )

    @commands.command(name="skip", help="Skips the current song being played", aliases = ['sk'])
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music()

            self.personal_embed = discord.Embed(title = "Skipped the Audio", color = discord.Color.gold())
            self.personal_embed.set_author(name = "AxC 777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")
                
            await ctx.send(embed = self.personal_embed)

    @commands.command(aliases = ['dc'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

        self.dc_embed = discord.Embed(title = "Disconnected 🔇", color = discord.Color.red())
        self.dc_embed.set_author(name = "AxC 777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

        await ctx.send(embed = self.dc_embed)

    @commands.command(aliases=['pa'])
    async def pause(self, ctx):
        ctx.voice_client.pause()

        self.pause_embed = discord.Embed(title = "Paused ⏸", color = discord.Color.blue())
        self.pause_embed.set_author(name = "AxC 777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

        choice = randrange(3)
        await ctx.send(embed = self.pause_embed)
        await ctx.send('https://tenor.com/view/pause-no-homo-whoa-stop-gif-15052205')

    @commands.command(aliases=['r'])
    async def resume(self, ctx):
        ctx.voice_client.resume()

        self.resume_embed = discord.Embed(title = "Resumed ⏯", color = discord.Color.green())
        self.resume_embed.set_author(name = "AxC 777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

        await ctx.send(embed = self.resume_embed)

    @commands.command(aliases = ['s'])
    async def stop(self, ctx):
        ctx.voice_client.stop()

        self.stop_embed = discord.Embed(title = "Stopped 🛑", color = discord.Color.red())
        self.stop_embed.set_author(name = "AxC 777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

        await ctx.send(embed = self.stop_embed)
        await ctx.send('https://tenor.com/view/stop-sign-when-you-catch-feelings-note-to-self-stop-now-gif-4850841')

    @commands.command(aliases = ['u'])
    async def url(self, ctx, url: str):
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

    @commands.command(aliases = ['h'])
    async def help(self, ctx):
        self.my_embed = discord.Embed(title="", description= "", color=0x00ff00)

        self.my_embed.add_field(name = "Regular Cmds:" , value = regular_cmds, inline = False)

        print(regular_cmds)

        self.my_embed.add_field(name = "Spotify Integrated Cmds" , value = "`?top_tracks [artist name]`", inline = True)

        self.my_embed.add_field(name = "Scientific Cmds" , value = scientific_cmds, inline = True)     

        self.my_embed.set_author(
            name = "AxC 777 Music" , icon_url = "https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")
            
        await ctx.send(embed=self.my_embed)

    @commands.command(aliases = ['l'])
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

                    for num in range(looping_constant + 1):
                        self.music_queue.append([song, voice_channel])

                    if self.is_playing == False:
                        await self.play_music()

            except ValueError:
                query = " ".join(content)
                # print(query)

                song = self.search_yt(query)
                
                if type(song) == type(True):
                  await ctx.send(
                    "Could not play the song. Incorrect format try another keyword. This could be due to a playlist or a livestream format."
                )

                else:
                  for num in range(11):
                    self.music_queue.append([song, voice_channel])

                  if self.is_playing == False:
                    await self.play_music()

    @commands.command(aliases = ['c'])
    async def clear(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()

        for num in range(len(self.music_queue)):
            self.music_queue.pop()
        x = randrange(1,3)
        await ctx.send("Queue Cleared!")
        await ctx.send(
            "https://tenor.com/view/were-all-clear-yellowstone-were-good-to-go-ready-lets-do-this-gif-17723207" if x == 1 else "https://tenor.com/view/squid-game-netflix-gif-23230821"
        )

    @commands.command(aliases = ['ly'])
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

    @commands.command(aliases = ['ft'])
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
          await ctx.send('https://tenor.com/view/fourier-fourier-series-gif-17422885')
  
          os.remove(image_title)
          os.remove(f"{file_components[0]}.wav")

        else:
            await ctx.send("File type not supported")

    @commands.command(name = "top_tracks", aliases = ['tt'])
    async def top_tracks(self, ctx, *args):
        artist = " ".join(args)
  
        results = sp.search(q=artist, limit=10, type="track")

        self.my_embed = discord.Embed(title = f"Top tracks of {artist.title()}", color = 0x00ff00)

        for idx, track in enumerate(results['tracks']['items']):
            min_sec = divmod(track['duration_ms'] / 1000, 60)
            
            self.my_embed.add_field(name = f"{idx + 1}. {track['name']}", value = f"**Duration:** {int(min_sec[0])} min {round(min_sec[1],2)} s", inline = False)
            
        # print(results)

        await ctx.send(embed = self.my_embed)
