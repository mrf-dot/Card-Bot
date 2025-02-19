import discord
from discord.ext import commands
from glob import glob
import os
import json


class DevCommands(commands.Cog):
    '''These are the developer commands'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
                The default check for this cog whenever a command is used. Returns True if the command is allowed.
                '''
        return ctx.author.id == self.bot.author_id

    @commands.command(  # Decorator to declare where a command is.
        name='reload',  # Name of the command, defaults to function name.
        aliases=['rl']  # Aliases for the command.
    )
    async def reload(self, ctx, cog):
        '''
                Reloads a cog.
                '''
        extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
        if cog == 'all':  # Lets you reload all cogs at once
            for extension in extensions:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            await ctx.send('Done')
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.send('Done')  # Sends a message where content='Done'
        else:
            await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.

    @commands.command(name="unload", aliases=['ul'])
    async def unload(self, ctx, cog):
        '''
                Unload a cog.
                '''
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send(f"`{cog}` has successfully been unloaded.")

    @commands.command(name="load")
    async def load(self, ctx, cog):
        '''
                Loads a cog.
                '''
        try:

            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @commands.command(name="listcogs", aliases=['lc'])
    async def listcogs(self, ctx):
        '''
                Returns a list of all enabled commands.
                '''
        base_string = "```css\n"  # Gives some styling to the list (on pc side)
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.send(base_string)

    @commands.command()
    async def delete(self, ctx):
        """Delete your account

        """
        user_id = ctx.author.id
        path = f"bot_data/users/{user_id}.json"

        def check(author):
            def inner_check(message):
                return message.author == author

            return inner_check

        dice = self.bot.get_cog('Dice')
        await dice.balance(ctx, False)
        await ctx.send('Are you sure you want to delete your account? (y/n)')
        while True:
            playerChoice = await self.bot.wait_for('message',
                                                   check=check(ctx.author),
                                                   timeout=30)
            if playerChoice.content.lower() == 'y':
                os.remove(path)
                await ctx.send('Your account has been deleted.')
                break
            elif playerChoice.content.lower() == 'n':
                await ctx.send('Thank you for not deleting your account.')
                break

    @commands.command()
    async def rotundify(self, ctx, *message):
        '''
        formats Rs as rotund Rs when appropriate
        '''
        results = ''
        previous = ''
        message = ' '.join(message)
        for x in message:
            if previous in [
                    'B', 'D', 'O', 'P', 'V', 'W', 'b', 'h', 'o', 'p', 'v', 'w',
                    'y', 'r'
            ] and x == 'r':
                x = 'ꝛ'
            results += x
            if x != '\'':
                previous = x
        await ctx.send(results)

    @commands.command()
    async def phrases(self, ctx):
        '''
        Displays phrase statistics
        '''
        word_list = open('bot_data/words.json', 'r')
        content = json.load(word_list)
        format_content = ''
        for x in content:
            if x not in ["Total Card Tzar Mentions"]:
                format_content += f'{x}: {content[x]:,}\n'
        format_content += f'Total Card Tzar Mentions: {content["Total Card Tzar Mentions"]:,}'
        await ctx.send(f'''```yaml
{format_content}```''')


def setup(bot):
    bot.add_cog(DevCommands(bot))
