import discord
from discord.ext import commands
import wikipediaapi
import json
from datetime import date
import requests
wk = wikipediaapi.Wikipedia('en')


class Information(commands.Cog):
    'Get information about various topics'

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return True

    @commands.command()
    async def info(self, ctx, *message):
        """Get information on a topic

        """
        message = ' '.join(message)
        page = wk.page(message)

        try:
            spam = page.canonicalurl
        except:
            if 'card tzar' in message.lower():
                readme = open('README.md', 'r')
                await ctx.send(f'''```markdown
{readme.read()}```''')
                readme.close()
            else:
                await ctx.send('`Enter a valid query`')
        else:
            elipsis = '...' if len(page.summary) > 347 else ''
            embed = discord.Embed(
                title=page.title,
                url=page.canonicalurl,
                description=f'{page.summary[0:347]}{elipsis}',
                colour=self.bot.color)
            try:
                response = requests.get(
                    f'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles={page.title}'
                )
                json_data = json.loads(response.text)
                img_link = list(json_data['query']
                                ['pages'].values())[0]['original']['source']
                embed.set_image(url=img_link)
            except:
                pass
            await ctx.send(embed=embed)

    @commands.command()
    async def news(self, ctx):
        """Get a brief on current events"""
        f = open('bot_data/news.json', 'r')
        news = json.load(f)
        embed = discord.Embed(title=f'Headlines for {date.today()}',
                              color=self.bot.color)
        for x in news["articles"]:
            embed.add_field(name=x["title"],
                            value=f'{x["description"]} {x["url"]}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
