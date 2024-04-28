from LeagueRiot import League
import discord
import json
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print("ready!")


@client.command()  # testing
async def ping(ctx):
    await ctx.send("pong")


@client.command()
async def ref(ctx, game):
    if game.upper() == "LEAGUE" or game.upper() == "LOL":
        embed = discord.Embed(title=" ", description="SuCo prefix: !")
        embed.set_author(name="SuCo Command Reference | League of Legends",
                         icon_url="https://preview.redd.it/xxeelg0amua51.png?width=256&format=png&auto=webp&s"
                                  "=1025c1abe85a536dbe72e99c90685031649999f8")
        embed.add_field(name="!summoner", value="Establish summoner for later search on data.", inline=True)
        embed.add_field(name="!ranked", value="Attributes: solo/duo, flex", inline=True)
        await ctx.send(embed=embed)
    elif game.upper() == "VALORANT" or game.upper() == "VAL":
        embed = discord.Embed(title=" ", description="SuCO prefix: !")
        embed.set_author(name="SuCo Command Reference | VALORANT", icon_url="https://i.bleacherreport.net/images"
                                                                            "/team_logos/328x328/valorant.png?canvas=492,328")
        embed.add_field(name="Under Construction", value="", inline=True)
        await ctx.send(embed=embed)


@client.command()
async def summoner(ctx, game_name, tag_line, region_code, region):
    global player
    player = League(game_name, tag_line, region_code.lower(), region.lower())
    embed = discord.Embed(color=0x3748de)
    embed.add_field(name="Summoner established", value=game_name, inline=True)
    embed.set_thumbnail(url=player.profile_icon)
    embed.set_footer(text="For help with commands, use !reference")
    await ctx.send(embed=embed)


@client.command()
async def ranked(ctx, choice):
    info = player.ranked(choice.lower())
    embed = discord.Embed(color=0xde3753)
    embed.set_thumbnail(url=player.profile_icon)
    embed.add_field(name=player.game_name, value="", inline=False)
    if len(info) == 0:  # something is up with this...
        print("reached else")
        embed.add_field(name="Ranked " + choice.upper(), value="Unranked", inline=True)
    # the else portion doesn't exactly work but i need to handle unranked players
    else:
        embed.add_field(name="Ranked " + choice.upper(), value=info['tier'] + " " + info['rank'], inline=True)
    await ctx.send(embed=embed)


@client.command()
async def embedpages(ctx):  # use this for match data
    page = discord.Embed(title='null',
                         description='null',
                         colour=discord.Colour.orange())
    pages = [page for x in range(10)]
    for i in range(10):
        pager = discord.Embed(
            title='Page' + str(i + 1),
            description='Description',
            colour=discord.Colour.orange()
        )
        pages[i] = pager

    message = await ctx.send(embed=pages[0])
    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '⏮':
            i = 0
            await message.edit(embed=pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed=pages[i])
        elif str(reaction) == '▶':
            if i < (len(pages) - 1):
                i += 1
                await message.edit(embed=pages[i])
        elif str(reaction) == '⏭':
            i = (len(pages) - 1)
            await message.edit(embed=pages[i])

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()


@client.command()
async def puuid(ctx):
    await ctx.send(player.puuid)


@client.command()
async def id(ctx):
    await ctx.send(player.summoner_id)

    # await ctx.send(player.summoner_info(choice.lower()))
    # next thing: make this into an embed using the information from summoner_info and the player icon instance
    # variable.


file = open("config.json")
config = json.load(file)
client.run(config["TOKEN"])
