[![CodeQL](https://github.com/chinmoysir/DISCORD-BOT/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/chinmoysir/DISCORD-BOT/actions/workflows/codeql-analysis.yml)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-success.svg?labelColor=2d3339)](https://github.com/chinmoysir/DISCORD-BOT/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20in-Python-1f425f.svg?labelColor=2d3339)](https://www.python.org/)
![works-with](https://img.shields.io/badge/Works_with-Python_3.5+-21415b?labelColor=2d3339)
[![Repl.it](https://img.shields.io/badge/Hosted_on-Replit-0d101e.svg?logo=replit&logoColor=white&labelColor=2d3339)](https://replit.com/@Abhisheksaxena4)
# The AxC Bot Family
## Add our Bots (Currently in Public Beta, but mostly stable)!
**AxC 777** (general-purpose, features not locked): https://discord.com/api/oauth2/authorize?client_id=889098056606298172&permissions=1644972474359&scope=bot%20applications.commands 

**AxC 777 Music** (The Music Bot): https://discord.com/api/oauth2/authorize?client_id=885787951483731998&permissions=1644972474359&scope=applications.commands%20bot 

---
Made with code aid from https://github.com/sohan-py/DiscordWeatherBot (@sohan-py)

**Note:** Both the ctx and non-ctx versions of AxC 777 run simultaneously, for some features are in one or the other.

Many times the code on Replit and GitHub is different. Although the difference is usually subtle, the reason is that our bots run on Replit and the code of the bots is updated more frequently there. These changes are usually incorporated (if accepted by our team) into this GitHub Repository within a matter of a day or two. Yes, we know that Replit supports GitHub integration (or Git, but still), and we are surely looking forward to use that, but for the time being, we are sticking to this route (for the time being here refers to about a week or two).

## Requirements (all bots inclusive)
1. `py-cord >= 2.0.0b4`
1. `matplotlib`
1. `numpy`
1. `scipy`
1. `PyNaCl`
1. `lyrics-extractor`
1. `pydub`
1. `wheel`
1. `youtube_dl`
2. `youtube-search`
3. `Flask`
4. `weather-api`
5. `spotipy`

All these required libraries can be installed using `pip` or `poetry`.

## MYOB (Make Your Own Bots)
**Note:** Replace `python` with `python3` and `pip` with `pip3` if Python 2 is already installed on your system

For making your own copy of our bots, you can either:-
1. Fork the Repository and do your stuff there
2. Clone the repository (using `git clone https://github.com/abhisheksaxena11jul/DISCORD-BOT.git`, `gh repo clone abhisheksaxena11jul/DISCORD-BOT` or something similar)

Please fill out `secrets.env` with the required values in the case of `AxC 777 Music`, and in other cases, please fill out the "secret values" in the bot code itself, where ever written. We are planning to move everything to `secrets.env`, but please wait a while for that.

If you cloned this GitHub Repository, please install the requirements using the following command in the directory in which `requirements.txt` is located (and make sure that Python 3.5 or greater is installed on your system):-
```
pip install -U -r requirements.txt
```

For hosting your own copy of `AxC 777 Music` **with slash commands**, navigate to the `AxC 777 Music` directory and run the following command:-
```
python slash.py
```

For hosting your own copy of `AxC 777 Music` **without slash commands**, navigate to the `AxC 777 Music` directory and run the following command:-
```
python main.py
```

For hosting your own copy of `AxC 777`, navigate to the `AxC 777` directory and run the following command:-
```
python main.py
```

**AND IT'S DONE 🥳🎉** (if you didn't encounter any bugs! 🥲😵‍💫)

**Additional:**
If you don't want to host the bot on a Flask application, you can remove the following lines from `slash.py`, `main.py` (basically the file you will run on Python):
```python
from alive import *

keep_alive()
```

