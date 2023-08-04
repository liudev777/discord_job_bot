import hikari
import lightbulb
from hikari import Embed
import miru


"""
Role related bot commands
"""

role_plugin = lightbulb.Plugin("roles", "configure user roles")

# Define a new custom View that contains 3 items
class FieldView(miru.View):
    # Define a new Button 
    @miru.button(label="Internship", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button1(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await handle_role(ctx, 1117591569495752754, "Internship")
    
    @miru.button(label="Junior Developer", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button2(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await handle_role(ctx, 1117591640601800726, "Junior Developer")
    
    @miru.button(label="Senior Developer", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button4(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await handle_role(ctx, 1117591718817189928, "Senior Developer")

class LocationView(miru.View):
    @miru.button(label="Chicago", style=hikari.ButtonStyle.PRIMARY)
    async def button1(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await handle_role(ctx, 1119033975680270346, "Chicago")


# if user already has discord role, delete role, else add role
async def handle_role(ctx, role_id, job_title):
    user = ctx.author
    user_id = ctx.author.id
    guild_id = ctx.guild_id
    member = await role_plugin.bot.rest.fetch_member(guild_id, user_id)
    roles = await member.fetch_roles()
    if role_id in [role.id for role in roles]: # checks if user already has role, and remove if they do
        await member.remove_role(role_id)
        print(f"{user} removed role")
        return
    
    await member.add_role(role_id)
    print(f"{user} chose {job_title}!")

# displays buttons that allow user to select roles
@role_plugin.listener(hikari.GuildMessageCreateEvent)
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    me = await event.app.rest.fetch_my_user()

    # If the bot is not mentioned
    if not me.id in event.message.user_mentions_ids:
        return
    
    fieldView = FieldView(timeout=None)  # Create a new view
    locationView = LocationView(timeout=None)
    fieldEmbed = Embed(title="Field", description="Pick a Job!\nSelect Job Again To Remove Role", color=0x00ff00)  # Green
    locationEmbed = Embed(title="Location", description="Pick a location!")

    fieldMessage = await event.message.respond(embed=fieldEmbed, components=fieldView)
    await fieldView.start(fieldMessage)  # Start listening for interactions
    
    locationMessage = await event.message.respond(embed=locationEmbed, components=locationView)
    await locationView.start(locationMessage)



def load(bot):
    bot.add_plugin(role_plugin)

def unload(bot):
    bot.remove_plugin(role_plugin)