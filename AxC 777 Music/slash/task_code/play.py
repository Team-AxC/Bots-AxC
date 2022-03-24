# Importing some stuff
import discord
from discord import ApplicationContext
from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch
from pytube import YouTube as pyt
import youtube_dl


################################################################################################
# Class #
################################################################################################


class play_stuff:
    # The extremely standard __init__ function with some variables declared
    def __init__(self):

        # all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {
                            'format': 'bestaudio',
                            'noplaylist': 'True'
                            }
        self.FFMPEG_OPTIONS = {
            'before_options':
                '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        self.vc = ""

    # searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{item}",
                                        download=False)['entries'][0]

            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    # What's next?
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]['source']

            # remove the first element as you are currently playing it
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

            # try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            print(self.music_queue)
            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                         after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_from_query(self, ctx: ApplicationContext, audio: str):
        await ctx.defer()

        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.respond("Connect to a voice channel!")

        else:
            # if (ctx.author == "Abhishek Saxena ()"):
            #         await ctx.respond("RICKLOCKED 🔐\nNo more rickrolls allowed")
            voice_channel = ctx.author.voice.channel

            song = self.search_yt(audio)
            if type(song) == type(True):
                await ctx.respond(
                    "Could not play the audio. Incorrect format, try another keyword. This could be due to a playlist or livestream format, or because of some internal error."
                )
            else:
                self.music_queue.append([song, voice_channel])

                # await ctx.respond(
                #     f"Song added to the queue, just for you {ctx.author.mention}")

                self.personal_embed = discord.Embed(
                    title="Audio added to Queue", color=0xFF0000)

                if self.is_playing == False:
                    await self.play_music()

                results = YoutubeSearch(audio, max_results=1).to_dict()

                yt_link = f"https://www.youtube.com/watch?v={results[0]['id']}"

                yt_video_info = pyt(yt_link)

                self.personal_embed.add_field(
                    name=":adult: Audio playing for:", value=ctx.author.mention)

                self.personal_embed.add_field(
                    name=":musical_note: Audio:", value=f"[{yt_video_info.title}]({yt_link})", inline=False)

                self.personal_embed.add_field(name=":hourglass_flowing_sand: Duration:",
                                              value=f"{yt_video_info.length // 60} min {yt_video_info.length % 60} s", inline=False)

                self.personal_embed.add_field(
                    name=":eye: Views (on YouTube):", value=f"{format(int(yt_video_info.views),',d')}", inline=False)

                self.personal_embed.set_thumbnail(
                    url=yt_video_info.thumbnail_url)

                self.personal_embed.set_author(
                    name="AxC 777 Music", icon_url="https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80")

                await ctx.respond(embed=self.personal_embed)


    async def play_from_url(self, ctx: ApplicationContext, url: str):
        await ctx.defer()
        if ctx.author.voice is None:
            await ctx.respond("You're not in a voice channel")

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
            await ctx.respond("Playing the URL in the voice channel")
            vc.play(source)


    async def loop_query(self, ctx: ApplicationContext, audio: str, looping_constant: int):
        await ctx.defer()
        voice_state = ctx.author.voice

        if voice_state is None:
            # you need to be connected so that the bot knows where to go
            await ctx.respond("Connect to a voice channel!")

        else:
            voice_channel = ctx.author.voice.channel

            song = self.search_yt(audio)

            if type(song) == type(True):
                await ctx.respond(
                    "Could not play the song. Incorrect format try another keyword. This could be due to a playlist or a livestream format or because of some internal error."
                )

            else:
                for _ in range(looping_constant + 1):
                    self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()
                
                self.personal_embed = discord.Embed(title=":loop: Loopin' it up! :musical_note:", color=0xFF0000)

                results = YoutubeSearch(audio, max_results=1).to_dict()

                yt_link = f"https://www.youtube.com/watch?v={results[0]['id']}"

                yt_video_info = pyt(yt_link)

                self.personal_embed.add_field(
                    name=":adult: Audio playing for:", value=ctx.author.mention)

                self.personal_embed.add_field(
                    name=":musical_note: Audio:", value=f"[{yt_video_info.title}]({yt_link})", inline=False)

                self.personal_embed.add_field(name=":hourglass_flowing_sand: Duration:",
                                              value=f"{(yt_video_info.length * looping_constant) // 60} min {(yt_video_info.length * looping_constant) % 60} s total\n({yt_video_info.length // 60} min {yt_video_info.length % 60} s each)", inline=False)

                self.personal_embed.add_field(
                    name=":eye: Views (on YouTube):", value=f"{format(int(yt_video_info.views),',d')}", inline=False)

                self.personal_embed.set_thumbnail(
                    url=yt_video_info.thumbnail_url)

                self.personal_embed.set_author(
                    name="AxC 777 Music", icon_url="https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80")

                await ctx.respond(embed=self.personal_embed)
