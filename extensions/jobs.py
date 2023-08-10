import json
from random import randint
import time
import hikari
import lightbulb
from hikari import Embed, Color
from jsearch import Jsearch
from linkedin import Linkedin
from database import Location, Position, Database, Channel

"""
Job related bot commands
"""

jobs_plugin = lightbulb.Plugin("jobs", "post job listings")

async def get_all_location_list():
    return [city[0] for city in await Location(Database()).get_all_locations()]


async def get_all_position_list():
    return [position[0] for position in await Position(Database()).get_all_positions()]


# Sends a list of jobs to the discord channel
async def embed_job(job_data) -> Embed:
    print(job_data.get("employer_name"))
    responsibilities = "\n".join("- " + r for r in job_data.get("job_responsibilities")) if job_data.get("job_responsibilities") else "N/A"
    qualifications = "\n".join("- " + r for r in job_data.get("job_qualifications")) if job_data.get("job_qualifications") else "N/A"

    description = (
        f'Job Title: {job_data.get("job_title", "N/A")}\n\n'
        f'Employment type: {job_data.get("job_employment_type", "N/A")}\n\n'
        f'Description: {job_data.get("job_description", "N/A")[:500]}...\n\n'
        f'Qualifications:\n {qualifications}\n\n'
        f'Responsibilities:\n {responsibilities}\n\n'
        f'{job_data.get("job_city")} {job_data.get("job_state")}\n\n'
    )

    embed = Embed(
        title = job_data.get("employer_name", "N/A"),
        description = description,
        url = job_data.get("job_apply_link", "N/A"),
    )
    embed.set_thumbnail(job_data.get("employer_logo"))
    return embed


async def post_jobs(ctx) -> None:
    channel_id = 1129920047444402376
    unique_role_combination = await fetch_unique_roles(ctx)
    for role_combinations in unique_role_combination:
        if not role_combinations:
            continue
        print([role for role in role_combinations])
        job_search_string = "Software Developer " + " ".join([role for role in role_combinations])
        print(job_search_string, "\n")
        for job_data in Jsearch(job_search_string).get_job():
            await jobs_plugin.bot.rest.create_message(channel_id, embed= await embed_job(job_data))


@jobs_plugin.command
@lightbulb.option("query", "thing you wanna search for idk")
@lightbulb.command("response", "grabs the response url")
@lightbulb.implements(lightbulb.SlashCommand)
async def response(ctx):
    # pp(Jsearch(ctx.options.query).response.json())
    data = Jsearch(ctx.options.query).response.json()
    with open('data1.json', 'w') as outfile:
        json.dump(data, outfile)
    await ctx.respond("responded")

    
# returns all the existing unique combinations of discord roles
async def fetch_unique_roles(ctx) -> set:
    print("posting jobs\n")
    guild_id = ctx.guild_id
    members = await jobs_plugin.bot.rest.fetch_members(guild_id)
    unique_role_combination = set()
    unique_role_colors = set()
    excluded_role_colors = [Color(0x00000), Color(0xf1c40f)]

    me = jobs_plugin.bot.get_me()

    for member in members:
        # skip if member is bot
        if member.id == me.id:
            continue
        
        roles = await member.fetch_roles()
        role_ids = tuple([role.name for role in roles if role.color not in excluded_role_colors])
        unique_role_combination.add(role_ids)
        role_colors = tuple([role.color for role in roles if role.color not in excluded_role_colors])
        unique_role_colors.add(role_colors)

    print(len(unique_role_combination))
    print(unique_role_combination)
    print(unique_role_colors)
    return unique_role_combination
    

@jobs_plugin.command
@lightbulb.command("list", "list job postings")
@lightbulb.implements(lightbulb.SlashCommand)
async def list(ctx):
    await post_jobs(ctx)


@jobs_plugin.command
@lightbulb.option("location", "Job location", required=False)
@lightbulb.option("position", "Job position", required=False)
@lightbulb.command("linkedin", "Posts jobs from linkedin")
@lightbulb.implements(lightbulb.SlashCommand)
async def linkedin(ctx):
    await ctx.respond("Fetching jobs...")
    await post_linkedin_jobs(ctx, ctx.options.location, ctx.options.position)


@jobs_plugin.command
@lightbulb.command("daily", "daily job listings")
@lightbulb.implements(lightbulb.SlashCommand)
async def daily(ctx):
    await ctx.respond("Getting daily job listings...")
    await post_in_respective_channel(ctx)
    await ctx.respond("Thats all for today!")



def linkedin_embed(job):
    embed = Embed(
        title=job.get("company_name"),
        description=job.get("job_title"),
        url=job.get("job_link")
    )
    embed.set_image(job.get("job_image_url"))
    return embed

async def post_linkedin_jobs(ctx, location_name=None, position=None, channel_id = None):
    # channel_id = ctx.channel_id
    # unique_role_combination = await fetch_unique_roles(ctx)
    # for role_combinations in unique_role_combination:
    #     if not role_combinations:
    #         continue
    #     print([role for role in role_combinations])
    if not channel_id:
        channel_id = ctx.channel_id
    linkedin_job_list = Linkedin(location_name=location_name, position=position).get_job_list()
    for job in linkedin_job_list:
        embed = linkedin_embed(job)
        await jobs_plugin.bot.rest.create_message(channel_id, embed=embed)
    

async def post_in_respective_channel(ctx):
    for position in await get_all_position_list():
        locations = [(location["channel_id"], location["location_name"], location["position"]) for location in await Channel(Database()).fetch_position_locations(str(ctx.guild_id), position=position)]
        for channel_id, location_name, position in locations:
            await post_linkedin_jobs(ctx, location_name=location_name, position=position, channel_id=channel_id)
        time.sleep(randint(3,5))


def load(bot):
    bot.add_plugin(jobs_plugin)

def unload(bot):
    bot.remove_plugin(jobs_plugin)