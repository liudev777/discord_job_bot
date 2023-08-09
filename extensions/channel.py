import hikari
import lightbulb
from database import Database, Position, Location, Channel

channels_plugin = lightbulb.Plugin("channels", "Creates different category and channels in the server")

@channels_plugin.command
@lightbulb.command("channel", "Channel command group")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def _channel():
    pass

@_channel.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("init", "initializes all the necessary category and channels")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def init(ctx):
    guild_id = ctx.guild_id
    if await is_init(ctx, await get_all_position_list()):
        await ctx.respond("Already populated")
        return
    await ctx.respond("Populating...")
    await populate(guild_id)
    await ctx.respond("Done!")


@_channel.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("delete", "Removes initialized channels")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def delete(ctx):
    await ctx.respond("Deleting...")
    await delete_all(ctx)
    await ctx.respond("Done!")


""" 
checks and creates any categories required thats not already in the server.
Then checks and creates any required channels under each category that is not already there.
"""

# checks if server already has category populated
async def is_init(ctx, category_names: list) -> bool:
    for category in ctx.get_guild().get_channels().values():
        if category.type == hikari.ChannelType.GUILD_CATEGORY and category.name in category_names:
            return True
    return False


async def populate(guild_id) -> None:
    postition_list = await get_all_position_list()
    location_list = await get_all_location_list()
    for position in postition_list:
        category = await populate_categories(guild_id, position)
        print("CATEGORY: ", position)

        await Channel(Database()).query_category(str(guild_id), str(category.id), position)
        for location in location_list:
            channel = await populate_channels(guild_id, category, location)

            await Channel(Database()).query_channel(str(guild_id), str(category.id), str(channel.id), location_name=location)
            print("-  CHANNEL: ", location)


#populates and returns the category object
async def populate_categories(guild_id, position):
    return await channels_plugin.bot.rest.create_guild_category(guild=guild_id, name=position)


async def populate_channels(guild_id, category, location):
    return await channels_plugin.bot.rest.create_guild_text_channel(guild=guild_id, name=(f'{category}-{location}'), category=category)


async def delete_all(ctx):
    db = Database()
    guild_id = ctx.guild_id
    await delete_channels(db, guild_id)
    await delete_categories(db, guild_id)
    pass


async def delete_channels(db, guild_id):
    target_data = await Channel(db).fetch_all_guild_channels(str(guild_id))
    data = [(record["guild_id"], record["channel_id"], record["category_id"]) for record in target_data]
    print(data)
    for guild_id, channel_id, category_id in data:
        try:
            await channels_plugin.bot.rest.delete_channel(channel_id)
        except Exception as e:
            print("Channel already removed")
        await Channel(db).delete_channel(guild_id, category_id, channel_id)


async def delete_categories(db, guild_id):
    target_data = await Channel(db).fetch_all_guild_categories(str(guild_id))
    data = [(record["guild_id"], record["category_id"]) for record in target_data]
    print(data)
    for guild_id, category_id in data:
        try:
            await channels_plugin.bot.rest.delete_channel(category_id)
        except Exception as e:
            print("Category already removed")
        await Channel(db).delete_category(guild_id, category_id)


async def get_all_location_list():
    return [city[0] for city in await Location(Database()).get_all_locations()]


async def get_all_position_list():
    return [position[0] for position in await Position(Database()).get_all_positions()]



def load(bot):
    bot.add_plugin(channels_plugin)

def unload(bot):
    bot.remove(channels_plugin)