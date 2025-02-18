import discord
from discord.ext import commands
import secrets
from glob import glob

images = list(map(lambda file: file.replace('\\', '/'), glob('bot_data/deck/*.png')))
card_ranks = list(map(str, ['Ace', *range(2, 11), 'Jack', 'Queen', 'King']))


#Creates full card suite
def suite(symbol):
    """adds styling to all elements in the list'

    """
    new_suite = []
    for x in card_ranks:
        string = f'{x} of {symbol}'
        new_suite.append(string)
    return new_suite


card = suite('Spades') + suite('Hearts') + suite('Diamonds') + suite('Clubs') + ['Black Joker', 'Red Joker']


class Cards(commands.Cog):
    '''A variety of card functions'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return True

    @commands.command()
    async def fetch(self, ctx, number):
        '''
        Returns a card from an ordered deck (1-54)
        '''
        global images
        if (number := int(number) - 1) in range(54): 
            selection = card[number]
            for x in images:
                if selection.lower().replace(' ', '_') in x:
                    await ctx.channel.send(file=discord.File(x))
                    embed = discord.Embed(title=selection,
                                            color=self.bot.color)
                    await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(
                '`Please enter a number within the range of 1-54.`')

    @commands.command()
    async def random(self, ctx):
        '''
        Returns a cryptographically random card
        '''
        global images
        global card
        selection = secrets.choice(card)
        print(images)
        print(card)
        print(selection)
        for x in images:
            if selection.lower().replace(' ', '_') in x:
                await ctx.channel.send(file=discord.File(x))
                embed = discord.Embed(title=selection, color=self.bot.color)
                await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Cards(bot))
