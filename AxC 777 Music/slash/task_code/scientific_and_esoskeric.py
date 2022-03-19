import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft as scipy_fft
import numpy as np
import string
from pydub import AudioSegment
import os
import random
import discord
from discord import ApplicationContext




class scientific_and_esoskeric:
    def __init__(self):
        self.allowed_fft_extensions = ('wav', 'mp3', 'ogg')


    def wav_fft(self, filename: str) -> str:
        rate, data = wav.read(filename)
        fft_out = scipy_fft(data)
        # %matplotlib inline
        plt.plot(data, np.abs(fft_out))

        random_name = f"{''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(128))}.png"

        plt.savefig(random_name)

        return random_name


    def convert(self, input_fp: str, target_extension: str) -> None:
        inp_array = input_fp.split(".")
        output_file = f"{inp_array[0]}.{target_extension}"

        if target_extension == "wav":
            if inp_array[-1] == "mp3":
                sound = AudioSegment.from_mp3(input_fp)
                sound.export(output_file, format=target_extension)

            elif inp_array[-1] == "ogg":
                sound = AudioSegment.from_ogg(input_fp)
                sound.export(output_file, format=target_extension)


    def fft_worker(self, filename: str) -> str:
        filename_array = filename.split('.')
        print(filename_array)

        if filename_array[-1] == "wav":
            return self.wav_fft(filename)

        elif filename_array[-1] == "mp3":
            self.convert(filename, "wav")
            os.remove(filename)
            return self.wav_fft(f"{filename_array[0]}.wav")

        elif filename_array[-1] == "ogg":
            self.convert(filename, "wav")
            os.remove(filename)
            return self.wav_fft(f"{filename_array[0]}.wav")

    async def fft(self, ctx: ApplicationContext, file: discord.Attachment):
        filename = file.filename
        file_components = filename.split('.')

        if file_components[-1] in self.allowed_fft_extensions:
            await file.save(fp=f'{filename}'.format(filename))

            print(filename)

            image_title = self.fft_worker(filename)
            print(image_title)

            fft_image = discord.File(image_title, filename="fft.png")

            await ctx.respond(file=fft_image)

            fft_embed = discord.Embed(title=f"Fourier Transform of {filename}", color=discord.Color.blurple())
            fft_embed.set_image(url="attachment://fft.png")

            await ctx.respond(embed=fft_embed)

            os.remove(image_title)
            os.remove(f"{file_components[0]}.wav")

        else:
            error_embed = discord.Embed(title=":octagonal_sign: Error", description="File type not supported",
                                        color=discord.Color.red())
            await ctx.respond(embed=error_embed)
