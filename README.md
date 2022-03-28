[![CodeQL](https://github.com/chinmoysir/DISCORD-BOT/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/chinmoysir/DISCORD-BOT/actions/workflows/codeql-analysis.yml)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-success.svg?labelColor=2d3339)](https://github.com/chinmoysir/DISCORD-BOT/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20in-Python-1f425f.svg?logo=python&labelColor=2d3339)](https://www.python.org/)
![works-with](https://img.shields.io/badge/Works_with-Python_3.8_to_3.10-21415b?logo=python&labelColor=2d3339)
[![Repl.it](https://img.shields.io/badge/Hosted_on-Replit-0d101e.svg?logo=replit&logoColor=white&labelColor=2d3339)](https://replit.com/@Abhisheksaxena4)
[![Heroku](https://img.shields.io/badge/Hosted%20on-Heroku-3b2f63?logo=heroku&labelColor=2d3339)](https://music-bot-axc-777.herokuapp.com/)
# The AxC Bot Family
## Add our Bots (Currently in Public Semi-Beta {yes, we made up the term "semi-beta"}, but mostly stable)!
**AxC 777** (general-purpose, features not locked): https://discord.com/api/oauth2/authorize?client_id=889098056606298172&permissions=1644971949559&scope=bot%20applications.commands 

**AxC 777 Music** (The Music Bot): https://discord.com/api/oauth2/authorize?client_id=885787951483731998&permissions=389297593664&scope=bot%20applications.commands 

---
🚨**EMERGENCY ALERT:** AxC 777 Music will not function till 31st March 2022 GMT because of some problems with Heroku Hosting. Please be patient. Services will resume on 1st April 2022, give or take some hours.

**Note:** The text-based commands of AxC 777 Music may still function (e.g. `?switch` and `?ft`), because they are hosted using Replit. However, they do basically nothing (except for the `?ft` command, of course!).

---

Made with code aid from https://github.com/sohan-py/DiscordWeatherBot (@sohan-py)

**Note:** Both the ctx and non-ctx versions of AxC 777 run simultaneously, for some features are in one or the other.

Many times the code on Replit/Heroku and GitHub is different. Although the difference is usually subtle, the reason is that our bots run on Replit (now Heroku as well) and the code of the bots is updated more frequently there. These changes are usually incorporated (if accepted by our team) into this GitHub Repository within a matter of a day or two. Yes, we know that Replit supports GitHub integration (or Git, but still), and we are surely looking forward to use that, but for the time being, we are sticking to this route (for the time being here refers to about a week or two).

## Requirements (all bots inclusive)
The required libraries are listed in `requirements.txt`. All these libraries can be installed using `pip`.

## MYOB (Make Your Own Bots)
**Note:** Replace `python` with `python3` and `pip` with `pip3` if Python 2 is already installed on your system

For making your own copy of our bots, you can either:-
1. Fork the Repository and do your stuff there
2. Clone the repository (using `git clone https://github.com/abhisheksaxena11jul/DISCORD-BOT.git`, `gh repo clone abhisheksaxena11jul/DISCORD-BOT` or something similar)

Please fill out `secrets.env` with the required values in the case of `AxC 777 Music`, and in other cases, please fill out the "secret values" in the bot code itself, where ever written. We are planning to move everything to `secrets.env`, but please wait a while for that.

If you cloned this GitHub Repository, please install the requirements using the following command in the directory in which `requirements.txt` is located (and make sure that Python 3.8 or greater is installed on your system):-
```
pip install -U -r requirements.txt
```

For hosting your own copy of `AxC 777 Music` (with slash commands), navigate to the `AxC 777 Music\slash` directory and run the following command:-
```
python setup.py
```
Note that it can take upto about an hour to register slash commands globally, therefore if you are testing your bot(s) on just one server or some collection of servers, please edit the following lines of code of _each and every_ slash command:-
```python
@slash_command(name = "command_name", description = "command_description", guild_ids = [server_id_of_server_1, server_id_of_server_2]
```
This should give an almost instantaneous access to the slash commands of the bot(s) in the mentioned servers.

For hosting your own copy of `AxC 777`, navigate to the `AxC 777` directory and run the following command:-
```
python main.py
```

**AND IT'S DONE 🥳🎉** (if you didn't encounter any bugs! 🥲😵‍💫)

**Additionally,** if you don't want to host the bot on a Flask application, you can remove the following lines of code from `main_slash.py` (for AxC 777 Music) and `main.py` (for AxC 777):
```python
from alive import *

keep_alive()
```

