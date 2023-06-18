from pprint import pp
import lightbulb
import hikari
from hikari import Embed
import os
import dotenv
from jsearch import Jsearch
import json
import miru

dotenv.load_dotenv()
bot = lightbulb.BotApp(token=os.environ['DISCORD_TOKEN'])

# Define a new custom View that contains 3 items
class FieldView(miru.View):
    # Define a new Button 
    @miru.button(label="🖥️ Software Engineer", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button1(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await handle_role(ctx, 1117591569495752754, "Software Engineer")
    
    @miru.button(label="🔧 Mechanical Engineer", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button2(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await handle_role(ctx, 1117591640601800726, "Mechanical Engineer")
    
    @miru.button(label="🖌️ Concept Artist", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button4(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await handle_role(ctx, 1117591718817189928, "Concept Artist")


class LocationView(miru.View):
    @miru.button(label="Chicago", style=hikari.ButtonStyle.PRIMARY)
    async def button1(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await handle_role(ctx, 1119033975680270346, "Chicago")


async def handle_role(ctx, role_id, job_title):
    user = ctx.author
    user_id = ctx.author.id
    guild_id = ctx.guild_id
    member = await bot.rest.fetch_member(guild_id, user_id)
    roles = await member.fetch_roles()
    if role_id in [role.id for role in roles]: # checks if user already has role, and remove if they do
        await member.remove_role(role_id)
        print(f"{user} removed role")
        return
    
    await member.add_role(role_id)
    print(f"{user} chose {job_title}!")


miru.install(bot) # Start miru


@bot.listen()
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    me = bot.get_me()

    # If the bot is not mentioned
    if not me.id in event.message.user_mentions_ids:
        return
    
    fieldView = FieldView(timeout=None)  # Create a new view
    locationView = LocationView(timeout=None)
    fieldEmbed = Embed(title="Field", description="Pick a Job!\nSelect Job Again To Remove Role", color=0x00ff00)  # Green
    locationEmbed = Embed(title="Location", description="Pick a location!")
    fieldMessage = await event.message.respond(embed=fieldEmbed, components=fieldView)
    locationMessage = await event.message.respond(embed=locationEmbed, components=locationView)
    await fieldView.start(fieldMessage)  # Start listening for interactions
    await locationView.start(locationMessage)


@bot.listen(hikari.StartingEvent)
async def on_started(event: hikari.StartingEvent) -> None:
    print("Bot is now ready.")


@bot.command
@lightbulb.command("ping", "checks if the bots alive")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("here we go!")


@bot.command
@lightbulb.option("query", "thing you wanna search for idk")
@lightbulb.command("response", "grabs the response url")
@lightbulb.implements(lightbulb.SlashCommand)
async def response(ctx):
    # pp(Jsearch(ctx.options.query).response.json())
    data = Jsearch(ctx.options.query).response.json()
    with open('data1.json', 'w') as outfile:
        json.dump(data, outfile)
    await ctx.respond("responded")


# Runs the bot
bot.run()
