from discord.ext import commands
import numpy as np
import cmath
import math


class Math(commands.Cog):
    '''Perform math operations'''

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return True

    @commands.command()
    async def add(self, ctx, *numbers):
        '''
        Add numbers
        '''
        try:
            solution = sum([float(x) for x in numbers])
        except:
            await ctx.send('All numbers must be valid')
        else:
            await ctx.send(f'{solution:.1f}')

    @commands.command()
    async def subtract(self, ctx, *numbers):
        '''
        Subtract numbers
        '''
        try:
            numlist = [float(x) for x in numbers]
            solution = numlist.pop(0)

        except:
            await ctx.send('All number must be valid')
        else:
            for x in numlist:
                solution -= x
            await ctx.send(f'{solution:.1f}')

    @commands.command()
    async def multiply(self, ctx, *numbers):
        '''
        Multiply numbers
        '''
        solution = np.prod([float(x) for x in numbers])
        await ctx.channel.send(f'{solution:.1f}')

    @commands.command()
    async def divide(self, ctx, *numbers):
        '''
        Divide numbers
        '''
        try:
            numlist = [float(x) for x in numbers]
            solution = numlist.pop(0)

        except:
            await ctx.send('All number must be valid')
        else:
            for x in numlist:
                solution /= x
            await ctx.channel.send(f'{solution:.1f}')

    @commands.command()
    async def square(self, ctx, number):
        '''
        Square a number
        '''
        await ctx.channel.send(float(number)**2)

    @commands.command()
    async def sqrt(self, ctx, number):
        '''
        Get the square root of a number
        '''
        number = int(number)
        if number < 0:
            solution = cmath.sqrt(number)
        if number > 0:
            solution = math.sqrt(number)
        await ctx.channel.send(solution)


def setup(bot):
    bot.add_cog(Math(bot))
