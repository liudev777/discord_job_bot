import hikari
import lightbulb
from neetcode import Neetcode
from hikari import Embed

"""
Leetcode related bot commands
"""

leetcode_plugin = lightbulb.Plugin("leetcode", "displays leetcode related items")

leet = Neetcode()

@leetcode_plugin.command
@lightbulb.command("leet", "posts leetcode questions")
@lightbulb.implements(lightbulb.SlashCommand)
async def leet(ctx, leet=leet):
    desc = f'[Video Solution 🔗]({leet.get_youtube_url()}) ||```py\n{leet.get_solution_raw()}```||'
    embed = Embed(
        title = leet.get_name(),
        description = desc,
        url=leet.get_leetcode_url()
    )
    embed.set_thumbnail("https://leetcode.com/static/images/LeetCode_logo_rvs.png")
    await ctx.respond(embed=embed)


def load(bot):
    bot.add_plugin(leetcode_plugin)

def unload(bot):
    bot.remove_plugin(leetcode_plugin)