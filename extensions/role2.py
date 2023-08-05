import hikari
import lightbulb
from hikari import Embed
from database import Database, User, Location, Position

"""
Role related bot commands
"""

role2_plugin = lightbulb.Plugin("roles", "configure user roles")


def get_all_location_list():
    return [city[0] for city in Location(Database()).get_all_locations()]


def get_all_position_list():
    return [position[0] for position in Position(Database()).get_all_positions()]


@role2_plugin.command
@lightbulb.command("p", "displays user job parameters")
@lightbulb.implements(lightbulb.SlashCommand)
async def parameter(ctx):
    discord_id = ctx.author.id
    db = Database()
    user = User(db, discord_id)
    roles = user.get_all_role()

    # returns if user didn't setup any parameters
    if not roles: 
        await ctx.respond("No roles set up")
        return
    
    print(user.get_all_role())
    await ctx.respond("test")


@role2_plugin.command
@lightbulb.command("set", "set command groups")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def set_():
    pass


@set_.child
@lightbulb.command("help", "display a list of set help functions")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_help(ctx):
    description = f'- /set help\n- /set location\n- /set position\n'
    embed = Embed(
        title="/set commands",
        description=description,
    )
    await ctx.respond(embed=embed)


@set_.child
@lightbulb.option("location", "requested location that is listed", required=True, choices=get_all_location_list())
@lightbulb.command("location", "sets desired job location")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_location(ctx):
    print(ctx.options.location)
    await ctx.respond("test")


@set_.child
@lightbulb.option("position",  "requested position that is listed", required=True, choices=get_all_position_list())
@lightbulb.command("position", "sets desired job location")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def set_position(ctx):
    print(ctx.options.position)
    await ctx.respond("test")


def load(bot):
    bot.add_plugin(role2_plugin)

def unload(bot):
    bot.remove_plugin(role2_plugin)