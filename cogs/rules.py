import discord
from discord.ext import commands


class Rules(commands.Cog):
    '''The rules of the server'''

    def __init__(self, bot):
        self.bot = bot
        self.rule_list = {
            'courtesy':
            'No doxxing or harassment (especially threats on someone’s life/property) or encouraging self harm.',
            'spam':
            'No spamming, phishing, or attempting to steal another user’s account (broadly speaking, one could consider this “no spamming or scamming.”)',
        }

    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        try:
            return ctx.guild.id == self.bot.guild_id
        except:
            return False

    @commands.command()
    async def rule(self, ctx, my_rule):
        '''Get information on a specific rule'''
        my_rule = my_rule.lower()
        try:
            selection = self.rule_list.get(my_rule)
        except:
            await ctx.send(f'`There is no rule about {my_rule}`')
        else:
            await ctx.send(embed=discord.Embed(title=f'{my_rule.title()}',
                                               color=self.bot.color,
                                               description=selection))

    @commands.command()
    async def rules(self, ctx):
        '''Display all server rules'''
        embed = discord.Embed(title='Card Tzar Fanclub Rules',
                              color=self.bot.color)
        for x in self.rule_list.keys():
            embed.add_field(name=x.title(),
                            value=self.rule_list[x],
                            inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Rules(bot))
