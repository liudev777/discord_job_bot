import lightbulb
import hikari
import os
import dotenv
import miru
from hikari import Embed

# load plugins from the extensions folder
dotenv.load_dotenv()
bot = lightbulb.BotApp(token=os.environ['DISCORD_TOKEN'])
bot.load_extensions("extensions.leetcode")
miru.install(bot)
bot.load_extensions("extensions.roles")
# bot.load_extensions("extensions.role2")
bot.load_extensions("extensions.jobs")
bot.load_extensions("extensions.channel")


@bot.listen(hikari.StartingEvent)
async def on_started(event: hikari.StartingEvent) -> None:
    print("Bot is now ready.")


@bot.listen(hikari.StartedEvent)
async def started(event: hikari.StartedEvent) -> None:
    # await post_jobs()
    pass

@bot.command
@lightbulb.command("help", "displays commands")
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    description = (
        f"- /leet: displays leetcode questions\n- /p: displays user job parameters\n\n- /set help: displays a list of setter commands to configure job search parameters"

    )
    embed = Embed(
        title="Commands",
        description=description
    )

    await ctx.respond(embed=embed)


# Runs the bot
def run() -> None:
    bot.run()

__all__ = ["run", "post_jobs"]

if __name__ == "__main__":
    run()