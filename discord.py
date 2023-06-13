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
class BasicView(miru.View):

    # Define a new Button 
    @miru.button(label="🖥️ Software Engineer", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button1(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        user = ctx.author
        userId = ctx.author.id
        guildId = ctx.guild_id
        roleId = 1117591569495752754
        member = await bot.rest.fetch_member(guildId, userId)
        await member.add_role(roleId)
        print(f"{user} chose software engineer!")
    # Define a new Button 
    
    @miru.button(label="🔧 Mechanical Engineer", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button2(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        user = ctx.author
        userId = ctx.author.id
        guildId = ctx.guild_id
        roleId = 1117591640601800726
        member = await bot.rest.fetch_member(guildId, userId)
        await member.add_role(roleId)
        print(f"{user} chose mechanical engineer!")
    
    @miru.button(label="🖌️ Concept Artist", style=hikari.ButtonStyle.PRIMARY)
    async def basic_button4(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        user = ctx.author
        userId = ctx.author.id
        guildId = ctx.guild_id
        roleId = 1117591718817189928
        member = await bot.rest.fetch_member(guildId, userId)
        await member.add_role(roleId)
        print(f"{user} chose Concept Artist!")
    



# Create an instance of our bot. This doesn't need to be a GatewayBot,
# but needs to implement RESTAware, CacheAware, and EventManagerAware.
miru.install(bot) # Start miru
# This function must be called on startup, otherwise you cannot instantiate views

@bot.listen()
async def buttons(event: hikari.GuildMessageCreateEvent) -> None:

    me = bot.get_me()

    # If the bot is not mentioned
    if not me.id in event.message.user_mentions_ids:
        return
    
    view = BasicView(timeout=None)  # Create a new view
    embed = Embed(title="Greeting", description="Hello miru!", color=0x00ff00)  # Green
    message = await event.message.respond(embed=embed, components=view)
    await view.start(message)  # Start listening for interactions
    await view.wait() # Optionally, wait until the view times out or gets stopped
    await event.message.respond("Goodbye!")

@bot.listen(hikari.StartingEvent)
async def on_started(event: hikari.StartingEvent) -> None:
    print("Bot is now ready.")

@bot.command
@lightbulb.command("ping", "checks if the bots alive")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("here we go!")

# response = requests.get(url, headers=headers, params=querystring)
# gets this and prints out something

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

# helps to run the bot
bot.run()
#anything after this would not be ran until 