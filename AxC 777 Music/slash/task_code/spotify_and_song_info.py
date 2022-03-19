import discord
from discord import ApplicationContext
import spotipy
from spotipy.oauth2 import *
from lyrics_extractor import SongLyrics
import os
from dotenv import load_dotenv

load_dotenv('code_secrets.env')

class song_info:
    def __init__(self):
        self.json_api_key = os.getenv('json_api_key')
        self.gcs_genius_engineid = os.getenv('gcs_genius_engineid')
        self.sp_clientid = os.getenv('sp_clientid')
        self.sp_clientsecret = os.getenv('sp_clientsecret')

        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.sp_clientid, client_secret=self.sp_clientsecret))


    async def lyrics(self, ctx: ApplicationContext, song: str):
        await ctx.defer()

        extract_lyrics = SongLyrics(self.json_api_key, self.gcs_genius_engineid)

        try:
            lyrics = extract_lyrics.get_lyrics(song)

            my_embed = discord.Embed(title=lyrics['title'],
                                     description=lyrics['lyrics'], color = discord.Color.blurple())

            await ctx.respond("Here are the lyrics!")

        except Exception:
            error = "Lyrics not found. Try reframing the song title and/or check if the song even exists or you or I have ascended into a parallel universe (or multiple for that matter). If that's the case, we're trying our best to contact Emu Lords to give their nails to scrape this configuration off.\n\n**Thanks!**\nTeam AxC"

            my_embed = discord.Embed(title=":octagonal_sign: Error",
                                     description=error, color = discord.Color.red())


        await ctx.respond(embed=my_embed)

    async def top_tracks(self, ctx: ApplicationContext, artist: str):
        await ctx.defer()

        results = self.sp.search(q=artist, limit=10, type="track")

        self.my_embed = discord.Embed(title=f"Top tracks of {artist.title()}", color=0x00ff00)

        for idx, track in enumerate(results['tracks']['items']):
            min_sec = divmod(track['duration_ms'] / 1000, 60)

            self.my_embed.add_field(
                name=f"{idx + 1}. {track['name']}", value=f"**Duration:** {int(min_sec[0])} min {round(min_sec[1],2)} s", inline=False)

        # print(results)

        await ctx.respond(embed=self.my_embed)



