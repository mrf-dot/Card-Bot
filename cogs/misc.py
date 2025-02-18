import discord
from discord.ext import commands
import contextlib
import io

class Misc(commands.Cog):
    '''Miscellaneous functions'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return True

    @commands.command()
    async def ping(self, ctx):
        '''
        Play ping pong
        '''
        await ctx.send(f'🏓 Pong! `{self.bot.latency:.2f}ms`')

    @commands.command()
    async def echo(self, ctx, *args):
        '''
        Repeat a line
        '''
        await ctx.channel.send(' '.join(args))

    @commands.command()
    async def suggest(self, ctx, *suggestion):
        '''
        Record a suggestion for the bot
        '''
        name = ctx.author.name
        destination = self.bot.get_channel(793019105229406259)
        if suggestion:
            await ctx.channel.send('`Suggestion Recorded`')
            message = await destination.send(
                f'{name} suggests: `{" ".join(suggestion)}`')
            await message.add_reaction('✅')
            await message.add_reaction('❎')

    @commands.command()
    async def svg(self, ctx):
        '''
        download a zip file of a deck of cards in SVG format
        '''
        await ctx.channel.send(
            file=discord.File('bot_data/deck/SVG-cards-1.3.zip'))

    @commands.command()
    async def png(self, ctx):
        '''
        download a zip file of a deck of cards in PNG format
        '''
        await ctx.send(file=discord.File('bot_data/deck/PNG-cards-1.3.zip'))


def setup(bot):
    bot.add_cog(Misc(bot))
