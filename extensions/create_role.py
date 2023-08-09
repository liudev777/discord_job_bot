import hikari 
import lightbulb
from database import Position, Location, Database, Role

"""
Role creation related commands
"""

create_role_plugin = lightbulb.Plugin("create_role", "Role creation related commands")


@create_role_plugin.command
@lightbulb.command("role", "Role command group")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def _role():
    pass


@_role.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("init", "Initializes required roles")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def init(ctx):
    await ctx.respond("Creating roles...")
    await create_all_role(ctx)
    await ctx.respond("Finished!")


@_role.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("delete", "deletes auto created roles")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def delete(ctx):
    await ctx.respond("Deleting roles...")
    await remove_all_role(ctx)
    await ctx.respond("Finished!")


async def create_all_role(ctx):
    guild_id = ctx.guild_id
    locations_list = await get_all_location_list()
    positions_list = await get_all_position_list()
    reason = "Job bot standard roles"
    for location in locations_list:
        role = await create_role_plugin.bot.rest.create_role(guild_id, name=location, mentionable=True, reason=reason)
        await Role(Database()).insert_role(str(guild_id), str(role.id))
    
    for position in positions_list:
        role = await create_role_plugin.bot.rest.create_role(guild_id, name=position,reason=reason)
        await Role(Database()).insert_role(str(guild_id), str(role.id))


async def remove_all_role(ctx):
    guild_id = ctx.guild_id
    target_data = await Role(Database()).fetch_all_roles(str(guild_id))
    data = [(record["guild_id"], record["role_id"]) for record in target_data]
    for guild_id, role_id in data:
        await create_role_plugin.bot.rest.delete_role(guild_id, role_id)
        try:
            await Role(Database()).delete_role(str(guild_id), str(role_id))
        except:
            print("Already Deleted")

async def get_all_location_list():
    return [city[0] for city in await Location(Database()).get_all_locations()]


async def get_all_position_list():
    return [position[0] for position in await Position(Database()).get_all_positions()]


def load(bot):
    bot.add_plugin(create_role_plugin)

def unload(bot):
    bot.remove_plugin(create_role_plugin)