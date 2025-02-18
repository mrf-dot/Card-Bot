import discord
from discord.ext import commands
from secrets import randbelow
from asyncio import sleep
import json

def check(author):
    def inner_check(message):
        return message.author == author

    return inner_check


class Dice(commands.Cog):
    '''Dice functions'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return True

    @commands.command()
    async def balance(self, ctx, show=True):
        '''
        Displays user balance
        '''
        user_id = ctx.author.id
        path = f"bot_data/users/{user_id}.json"
        try:
            with open(path, "x") as f:
                user_start = {'balance': 1000, 'bankrupt': 0}
                json.dump(user_start, f)
        except:
            pass
        if show:
            f = open(path)
            data = json.load(f)
            embed = discord.Embed(title=f'{ctx.author.name}\'s Balance',
                                  color=self.bot.color)
            embed.add_field(name='Account funds',
                            value=f'${data["balance"]}.00')
            embed.add_field(name='Bankruptcies', value=data["bankrupt"])
            await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx, custom=False, name=''):
        '''
        Rolls two dice
        '''
        if not (custom is True):
            name = ctx.author.name
        one = 1 + randbelow(6)
        two = 1 + randbelow(6)
        emoji = self.bot.get_emoji(800191945816408104)
        await ctx.send(f'{name} is rolling {2*f"{emoji}"}')
        embed = discord.Embed(title=f'{name}\'s roll', color=self.bot.color)
        embed.add_field(name='Dice 1:', value=one)
        embed.add_field(name='Dice 2:', value=two)

        await sleep(0.5)
        await ctx.send(embed=embed)

        return one + two

    @commands.command()
    async def dice(self, ctx, bet='invalid'):
        """Play a round of dice with the bot 

        """
        player_id = ctx.author.id
        await self.balance(ctx, False)
        profile = open(f"bot_data/users/{player_id}.json", "r")
        contents = json.load(profile)
        profile.close()

        if bet.lower() == 'all': bet = contents["balance"]
        try:
            if not contents["balance"] >= (bet := int(bet)) > 0: raise ValueError
        except:
            await ctx.send('```Enter a valid bet```')
            return

        player = await self.roll(ctx)
        player_name = ctx.author.name
        bot = await self.roll(ctx, True, name='Card Tzar')
        if player > bot:
            contents["balance"] += bet
            await ctx.send(f'{player_name} won ${bet}')
        elif player < bot:
            contents["balance"] -= bet
            await ctx.send(f'Card Tzar won ${bet}')
        else: await ctx.send('There was a tie')
        if contents["balance"] == 0:
            await ctx.send('You\'ve gone bankrupt 😬')
            contents["balance"] = 1000
            contents["bankrupt"] += 1
        
        profile = open(f"bot_data/users/{player_id}.json", "w")
        json.dump(contents, profile)
        profile.close()


def setup(bot):
    bot.add_cog(Dice(bot))
