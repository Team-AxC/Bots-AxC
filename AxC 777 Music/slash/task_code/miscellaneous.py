# Importing some stuff
import discord
from discord import ApplicationContext
from random import randrange


################################################################################################
# Class #
################################################################################################


class miscellaneous:
    # The extremely standard __init__ function with some variables declared
    def __init__(self, music_class):
        self.music_class = music_class



    async def queue(self, ctx: ApplicationContext):
        await ctx.defer()
        if len(self.music_class.music_queue) <= 10 and len(self.music_class.music_queue) > 0:
            retval = []

            for i in range(len(self.music_class.music_queue)):
                retval.append(self.music_class.music_queue[i][0]['title'])

            enumerated_retval = enumerate(retval)

            queue_string = ""

            for x in enumerated_retval:
                queue_string = queue_string + str(x[0] + 1) + ". " + x[1] + "\n"
                
            music_queue_embed = discord.Embed(title = "Audio Queue", description = queue_string, color = discord.Color.blurple())
            
            await ctx.respond(embed = music_queue_embed)
            await ctx.respond('https://tenor.com/view/squid-game-netflix-egybest-film-squid-gif-23324577')
            

            
        elif len(self.music_class.music_queue) <= 21:
            retval = ""
            for i in range(len(self.music_class.music_queue)):
                retval += self.music_class.music_queue[i][0]['title'] + "\n"

#             print(retval)
            
            await ctx.respond(retval)
            await ctx.respond('https://tenor.com/view/squid-game-netflix-egybest-film-squid-gif-23324577')

        elif len(self.music_class.music_queue) > 21:
            retval = ""
            for i in range(len(self.music_class.music_queue)):
                for _ in range(21):
                    retval += self.music_class.music_queue[i][0]['title'] + "\n"
                    await ctx.respond(retval)
                retval = ""
            await ctx.respond("https://tenor.com/view/squid-game-netflix-egybest-film-squid-gif-23324577")

#             print(retval)
            
        else:
            await ctx.respond("No audio in queue")

    async def skip(self, ctx: ApplicationContext):
        await ctx.defer()
        self.vc = self.music_class.vc
        
        if self.vc != "" and self.vc:
            self.vc.stop()
            # try to play next in the queue if it exists
            await self.music_class.play_music()

            self.personal_embed = discord.Embed(
                title="Skipped the Audio", color=discord.Color.gold())
            self.personal_embed.set_author(
                name="AxC 777 Music", icon_url="https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

            await ctx.respond(embed=self.personal_embed)

    async def disconnect(self, ctx: ApplicationContext):
        await ctx.defer()
        # await ctx.voice_client.disconnect()
        self.vc = self.music_class.vc

        if self.vc != "":
            await self.vc.disconnect(force=True)

            self.dc_embed = discord.Embed(
                title="Disconnected 🔇", color=discord.Color.red())
            self.dc_embed.set_author(
                name="AxC 777 Music", icon_url="https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

            await ctx.respond(embed=self.dc_embed)

        else:
            self.error_embed = discord.Embed(title = ":octagonal_sign: Error", description = "Bot not in any voice channel", color = discord.Color.red())
            await ctx.respond(embed = self.error_embed)

    async def pause(self, ctx: ApplicationContext):
        await ctx.defer()
        # voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
        self.vc = self.music_class.vc

        if self.vc != "":
            self.vc.pause()

            self.pause_embed = discord.Embed(
                title="Paused ⏸", color=discord.Color.blue())
            self.pause_embed.set_author(
                name="AxC 777 Music", icon_url="https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

            await ctx.respond(embed=self.pause_embed)

        else:
            self.caution_embed = discord.Embed(title = ":warning: Blunder!", description = "No audio being played", color = discord.Color.yellow())
            await ctx.respond(embed = self.caution_embed)

        # ctx.voice_client.pause()

    async def resume(self, ctx: ApplicationContext):
        await ctx.defer()

        self.vc = self.music_class.vc

        if self.vc != "":
            self.vc.resume()

            self.resume_embed = discord.Embed(
                title="Resumed ⏯", color=discord.Color.green())
            self.resume_embed.set_author(
                name="AxC 777 Music", icon_url="https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

            await ctx.respond(embed=self.resume_embed)

        else:
            await ctx.respond("No audio being played")

    async def stop(self, ctx: ApplicationContext):
        await ctx.defer()
        # ctx.voice_client.stop()

        self.vc = self.music_class.vc

        if self.vc != "":
            self.vc.stop()

            self.stop_embed = discord.Embed(
                title="Stopped 🛑", color=discord.Color.red())
            self.stop_embed.set_author(
                name="AxC 777 Music", icon_url="https://images.unsplash.com/photo-1614680376573-df3480f0c6ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=80&q=80")

            await ctx.respond(embed=self.stop_embed)

        else:
            await ctx.respond("No audio being played")



    async def clear(self, ctx: ApplicationContext):
        await ctx.defer()

        self.vc = self.music_class.vc

        if self.vc != "" and self.vc:
            self.vc.stop()

            for _ in range(len(self.music_class.music_queue)):
                self.music_class.music_queue.pop()

            x = randrange(1, 3)

            await ctx.respond("Queue Cleared!")
            await ctx.respond(
                "https://tenor.com/view/were-all-clear-yellowstone-were-good-to-go-ready-lets-do-this-gif-17723207" if x == 1 else "https://tenor.com/view/squid-game-netflix-gif-23230821"
            )

        else:
            await ctx.respond("No audio in the queue")

    # Scientific commands and functions start
        

    async def latency(self, ctx: ApplicationContext, bot: discord.Bot):
        await ctx.defer()
        await ctx.respond(f"The latency of the bot is **{bot.latency * 1000} ms**")
    
