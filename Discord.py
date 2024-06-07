from League import League
from Teamfight import Teamfight
from Riot import Riot
import discord
import json
from discord.ext import commands

# RESTRUCTURE THIS ENTIRELY

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
async def reference(ctx):
    embed = discord.Embed(title=" ", description="Command prefix: !", color=0xf7f8fa)
    embed.set_author(name="SuCo Command Reference | League of Legends & Teamfight Tactics",
                     icon_url="https://preview.redd.it/xxeelg0amua51.png?width=256&format=png&auto=webp&s"
                              "=1025c1abe85a536dbe72e99c90685031649999f8")
    embed.add_field(name="!account", value="Establish a Riot account to browse through statistics. \n \n !account ["
                                           "gameName] [tagLine] [platformRouting] [regionalRouting] \n", inline=False)
    embed.add_field(name="!lolRanked", value="Rank/statistics for solo, flex, and arena queue.", inline=True)
    embed.add_field(name="!lolMatches", value="Statistics and match data for recent 10 matches.", inline=True)
    embed.add_field(name="!lolChampMastery", value="Statistics for played champions. \n \n !lolChampMastery ["
                                                   "championName] \n")
    embed.add_field(name="!tftRanked", value="Rank/statistics for [] and [] queue.", inline=True)
    embed.add_field(name="!tftMatches", value="Statistics and match data for recent 10 matches.", inline=True)
    await ctx.send(embed=embed)


@client.command()
async def account(ctx, game_name, tag_line, region_code, region):
    global account
    account = Riot(game_name, tag_line, region_code.lower(), region.lower())
    global league
    league = League(account)
    global teamfight
    teamfight = Teamfight(account)

    embed = discord.Embed(color=0xf7f8fa)
    embed.add_field(name="Account established", value=game_name, inline=True)
    embed.set_thumbnail(url=account.profile_icon)
    embed.set_footer(text="For help with commands, use !reference")
    await ctx.send(embed=embed)


@client.command()
async def lolranked(ctx):
    info = league.ranked()
    print(info)
    page = discord.Embed(title='null',
                         description='null',
                         color=0x3b58eb)
    pages = [page for x in range(len(info))]
    for i in range(len(info)):
        if info == "No ranked data present for this user.":
            embed = discord.Embed(title="No ranked data present for this user.", description="")
            await ctx.send(embed)
            break
        elif info[i]['queueType'] == "CHERRY":
            pager = discord.Embed(
                title="ARENA",
                description="",
                color=0x3b58eb
            )
        else:
            pager = discord.Embed(
                title=info[i]['queueType'],
                description=info[i]['tier'] + " " + info[i]['rank'],
                color=0x3b58eb
            )
        pager.add_field(name="Wins", value=info[i]['wins'], inline=True)
        pager.add_field(name="Losses", value=info[i]['losses'], inline=True)
        pager.add_field(name="W/L Rate", value=round(info[i]['wins']/info[i]['losses'], 2), inline=True)

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
async def lolmatches(ctx):
    info = league.matches(20)
    page = discord.Embed(title='null',
                         description='null',
                         colour=0x3b58eb)
    pages = [page for x in range(len(info))]
    for i in range(len(info)):
        pager = discord.Embed(
            title='(' + str((i + 1)) + ') ' + 'Match of ' + str(info[i]['gameCreation']),
            description=info[i]['gameMode'],
            colour=0x3b58eb
        )
        pager.add_field(name="KDA: " + str(info[i]['kills']) + "/" + str(info[i]['deaths']) + "/" + str(info[i]['assists']), value="", inline=False)
        pager.add_field(name=info[i]['championName'], value='Level ' + str(info[i]['champLevel']), inline=True)
        pager.set_thumbnail(url=info[i]['championImg'])
        pager.add_field(name="Kills", value="Double: " + str(info[i]['doubleKills']) + "\nTriple: " + str(info[i]['tripleKills']) + "\nQuadra: " + str(info[i]['quadraKills']) + "\nPenta: " + str(info[i]['pentaKills']), inline=True)
        pager.add_field(name="Total Damage Dealt: " + str(info[i]['totalDamageDealtToChampions']), value="Physical: " + str(info[i]['physicalDamageDealtToChampions']) + "\nMagic: " + str(info[i]['magicDamageDealtToChampions']) + "\nTrue: " + str(info[i]['trueDamageDealtToChampions']))

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
async def lolchampmastery(ctx, champion):
    info = league.champion_mastery(champion)

    champion.lower()
    champion_name_first_letter = champion[0].upper()
    champion = champion_name_first_letter + champion[1:]

    embed = discord.Embed(title=champion, color=0x3b58eb)
    embed.set_thumbnail(url="https://ddragon.leagueoflegends.com/cdn/14.11.1/img/champion/{0}.png".format(champion))
    embed.add_field(name="Champion Level", value='Level ' + str(info['championLevel']), inline=True)
    embed.add_field(name="Champion Points", value=str(abs(info['championPoints'])) + " (" + str(abs(info["championPointsUntilNextLevel"])) + " points until next level.)", inline=False)
    embed.add_field(name="Last time played: ", value=str(info['lastPlayTime']), inline=True)

    await ctx.send(embed=embed)


@client.command()
async def tftranked(ctx):
    info = teamfight.ranked()
    if info == "No ranked data present for this user.":
        ctx.send(embed=discord.Embed(title="Unavailable.", description="No ranked data present for this user.", color=0xebaa3b))
    else:
        page = discord.Embed(title='null',
                             description='null',
                             color=0xebaa3b)
        pages = [page for x in range(len(info))]
        for i in range(len(info)):
            pager = discord.Embed(
                title=info[i]['queueType'],
                description=info[i]['tier'] + " " + info[i]['rank'],
                color=0xebaa3b
            )
            pager.add_field(name="Wins", value=info[i]['wins'], inline=True)
            pager.add_field(name="Losses", value=info[i]['losses'], inline=True)
            pager.add_field(name="W/L Rate", value=round(info[i]['wins'] / info[i]['losses'], 2), inline=True)
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
async def tftmatches(ctx):
    info = teamfight.matches(20)
    page = discord.Embed(title='null',
                         description='null',
                         color=0xebaa3b)
    pages = [page for x in range(len(info))]
    for i in range(len(info)):
        pager = discord.Embed(
            title='(' + str((i + 1)) + ') ' + 'Match of ' + str(info[i]['gameCreation']),
            description='Game Length: ' + str(info[i]['game_length']),
            color=0xebaa3b
        )
        pager.add_field(name="Placement", value=str(info[i]['placement']), inline=True)
        pager.add_field(name="Last Round", value=str(info[i]['last_round']), inline=True)
        pager.add_field(name="Time Eliminated", value=str(info[i]['time_eliminated']), inline=True)
        pager.add_field(name="Players Eliminiated", value=str(info[i]['players_eliminated']), inline=True)

        units = ""
        for j in range(len(info[i]["units"])):
            units += info[i]["units"][j]["character_id"] + "\n"
        pager.add_field(name="Units", value=units, inline=True)
        augments = ""
        for k in range(len(info[i]["augments"])):
            augments += info[i]["augments"][k] + "\n"
        pager.add_field(name="Augments", value=augments, inline=True)
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


file = open("config.json")
config = json.load(file)
client.run(config["TOKEN"])
