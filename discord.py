from pprint import pp
import lightbulb
import hikari
import os
import dotenv
from jsearch import Jsearch
import json

dotenv.load_dotenv()
bot = lightbulb.BotApp(token=os.environ['DISCORD_TOKEN'])

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