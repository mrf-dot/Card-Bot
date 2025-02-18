from routines.neverSleep import awake
from routines.call_news import call_news
import os
import discord
from discord.ext import commands
from glob import glob
from pretty_help import PrettyHelp

bot = commands.Bot(command_prefix="&", case_insensitive=True)

# Sets environmental variables
bot.secret = os.getenv('BOT_SECRET')
bot.newsapi_key = os.getenv('NEWSAPI_KEY')
bot.author_id = int(os.getenv('AUTHOR_ID'))
bot.guild_id = int(os.getenv('GUILD_ID'))
bot.color = discord.Color.dark_red()
bot.help_command = PrettyHelp(color=bot.color)


@bot.event
async def on_ready():  # When the bot is ready
    """Category documentations

    """
    await bot.change_presence(activity=discord.Game('&help | bit.ly/card-bot'))
    print(200)
    print(bot.user)  # Prints the bot's username and identifier


extensions = map(lambda filename: filename.replace("/", ".")[:-3], glob("cogs/*py"))

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

awake("https://card-bot.mrfdot.repl.co", True)  # Pings the repl
call_news(bot)  # Starts API news collection
bot.run(bot.secret)  # Starts the bot
