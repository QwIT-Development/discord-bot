# Firkx

The bot source code used for the Firka Discord server.

---

## Define .env variables

```env
TOKEN=<your main bot token>
DEBUGTOKEN=<your debug bot's token, can be same if the bot is private [optional]>
PAT=<your github personal access token [optional if the repo is public]>
OWNER=<the owner of the github repo ex. QwIT-Development>
REPO=<the name of the github repo ex. discord-bot>
```

## Run the project

### Pull latest files from the repo specified in your .env file

```bash
python3 -m pip install pygithub
python3 -m pip install discord
git clone https://github.com/QwIT-Development/discord-bot.git
cd discord-bot
python3 starter.py
```

### Run the bot without pulling from GitHub

```bash
python3 -m pip install discord
cd bot
python3 main.py
```

## Info

- If there isn't a DEBUGTOKEN key in the .env file, the bot will use the main token.
- The bot won't automatically pull every change from the repo, you have to restart it manually by running `starter.py`.
- If you don't plan on using a GitHub repo, you don't have to use the `starter.py` file, and you also don't have to define a PAT, OWNER or REPO key in the .env file.
- Every word `DirtyWords.xml` file in `bot/` has either **`f`** or **`m`** set as the type. **`f`** means it is a noun (főnév), **`m`** means it's an adjective (melléknév). If you plan on adding more words manually, you MUST set the type of the word, or else they won't be in the calculation for the `/insult` command.

_Have fun! :D_

<sup>Made with ❤️ by Pearoo - please mention Firka if you use this bot</sup>
