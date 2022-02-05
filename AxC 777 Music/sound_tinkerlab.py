import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft as scipy_fft
import numpy as np
import string
import random
import os
from pydub import AudioSegment

def wav_fft(filename: str) -> str:
  rate, data = wav.read(filename)
  fft_out = scipy_fft(data)
  # %matplotlib inline
  plt.plot(data, np.abs(fft_out))

  random_name = f"{''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(128))}.png"

  plt.savefig(random_name)
  
  return random_name


def convert(input_fp: str, target_extension: str) -> None:
  if target_extension == "wav":
    inp_array = input_fp.split(".")
    output_file = f"{inp_array[0]}.{target_extension}"

    if inp_array[-1] == "mp3":
      sound = AudioSegment.from_mp3(input_fp)
      sound.export(output_file, format = target_extension)

    elif inp_array[-1] == "ogg":
      sound = AudioSegment.from_ogg(input_fp)
      sound.export(output_file, format = target_extension)
      
      
def fft(filename: str) -> str:
  filename_array = filename.split('.')
  print(filename_array)

  if filename_array[-1] == "wav":
    return wav_fft(filename)

  elif filename_array[-1] in ["mp3", "ogg"]:
    convert(filename, "wav")
    os.remove(filename)
    return wav_fft(f"{filename_array[0]}.wav")
  
