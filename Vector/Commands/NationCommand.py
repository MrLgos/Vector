from datetime import timedelta
import random
import requests
import disnake
from disnake.ext import commands
import Utils.Utils as Utils

from Paginator import CreatePaginator
from disnake import Embed


class NationCommand(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def nation(self, inter):
    pass

  @nation.sub_command(description="Provides general info about a nation")
  async def search(
      self,
      inter: disnake.ApplicationCommandInteraction,
      nation: str = commands.Param(
          description="Nation's name, type 'random' for a random choice"),
      server: str = commands.Param(
          description="Server name, defaults to Aurora",
          default="aurora",
          choices=["aurora"])):
    commandString = f"/nation search nation: {nation} server: {server}"
    await inter.response.defer()
    try:
      if nation == "random":
        allNationsLookup = Utils.Lookup.lookup(server, endpoint="nations")
        nation = random.choice(allNationsLookup["allNations"])
      nationsLookup = Utils.Lookup.lookup(server,
                                          endpoint="nations",
                                          name=nation)

    except:
      embed = Utils.Embeds.error_embed(
          value=
          "Check if you wrote a parameter incorrectly or if the server is currently offline",
          type="userError",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)
      return

    try:
      locationUrl = f"https://earthmc.net/map/{server}/?zoom=4&x={nationsLookup['spawn']['x']}&z={nationsLookup['spawn']['z']}"

      embed = Utils.Embeds.embed_builder(
          title=f"`{nationsLookup['strings']['nation']}`",
          description=nationsLookup["strings"]["board"],
          footer=commandString,
          author=inter.author)

      embed.add_field(name="King",
                      value=nationsLookup["strings"]["king"],
                      inline=True)
      embed.add_field(name="Capital",
                      value=nationsLookup["strings"]["capital"],
                      inline=True)
      embed.add_field(
          name="Location",
          value=
          f"[{int(round(nationsLookup['spawn']['x'], 0))}, {int(round(nationsLookup['spawn']['z'], 0))}]({locationUrl})",
          inline=True)

      embed.add_field(name="Residents",
                      value=nationsLookup["stats"]["numResidents"],
                      inline=True)
      embed.add_field(name="Towns",
                      value=nationsLookup["stats"]["numTowns"],
                      inline=True)
      embed.add_field(
          name="Town Blocks",
          value=
          f"{nationsLookup['stats']['numTownBlocks']} ({nationsLookup['stats']['numTownBlocks'] * 16 + (48 * nationsLookup['stats']['numTowns'])}G)",
          inline=True)

      embed.add_field(name="Balance",
                      value=f"{nationsLookup['stats']['balance']}G",
                      inline=True)
      embed.add_field(
          name="Founded",
          value=
          f"<t:{round(nationsLookup['timestamps']['registered'] / 1000)}:R>",
          inline=True)
      embed.add_field(
          name="Status",
          value=
          f"• `Open` — {nationsLookup['status']['isOpen']}\n• `Public` — {nationsLookup['status']['isPublic']}\n• `Neutral` — {nationsLookup['status']['isNeutral']}",
          inline=True)

      await inter.send(embed=embed, ephemeral=False)

    except:
      embed = Utils.Embeds.error_embed(
          value=
          "If it is not evident that the error was your fault, please report it",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)

  @nation.sub_command(
      description=
      "View all the nations that the specified nation can now send ally request"
  )
  async def ally(
      self,
      inter: disnake.ApplicationCommandInteraction,
      nation: str = commands.Param(description="Your nation's name"),
      server: str = commands.Param(
          description="Server name, defaults to Aurora",
          default="aurora",
          choices=["aurora"])):
    commandString = f"/nation ally nation: {nation} server: {server}"
    await inter.response.defer()
    try:
      nationsLookup = Utils.Lookup.lookup(server,
                                          endpoint="nations",
                                          name=nation)
      allNationsLookup = Utils.Lookup.lookup(server, endpoint="nations")
      onlineLookup = Utils.Lookup.lookup(server,
                                         endpoint="onlineplayers",
                                         opt="toolkit")
      nationsOnetimeLookup = Utils.Lookup.lookup(server,
                                                 endpoint="nations",
                                                 version="v2")
    except:
      embed = Utils.Embeds.error_embed(
          value=
          "Check if you wrote a parameter incorrectly or if the server is currently offline",
          type="userError",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)
      return

    try:
      embed = Utils.Embeds.embed_builder(
          title=f"`{nationsLookup['strings']['nation']}'s online target`",
          footer=commandString,
          author=inter.author)
      enemyList = nationsLookup["enemies"]
      allyList = nationsLookup["allies"]
      allNations = allNationsLookup["allNations"]
      allNations.remove(nationsLookup["strings"]["nation"])
      allNations = [x for x in allNations if x not in enemyList]
      unalliedList = list(set(allNations).difference(set(allyList)))

      leader_nation = {}
      leader_rank = {}
      for n in nationsOnetimeLookup:
        nation_name = n["name"]
        leader_nation[n["king"]] = nation_name
        leader_rank[n["king"]] = "King"
        if "ranks" in n:
          if "Chancellor" in n["ranks"]:
            for chancellor in n["ranks"]["Chancellor"]:
              leader_nation[chancellor] = nation_name
              if not chancellor in leader_rank:
                leader_rank[chancellor] = "Chancellor"
          if "Diplomat" in n["ranks"]:
            for diplomat in n["ranks"]["Diplomat"]:
              if diplomat not in leader_nation:
                leader_nation[diplomat] = nation_name
                if not diplomat in leader_rank:
                  leader_rank[diplomat] = "Diplomat"
      cnt = 0
      embeds = []
      for player in onlineLookup:
        if player["name"] in leader_nation:
          if leader_nation[player["name"]] in unalliedList:
            if cnt % 5 == 0:
              embed = Utils.Embeds.embed_builder(
                  title=
                  f"`{nationsLookup['strings']['nation']}'s online target`",
                  footer=commandString,
                  author=inter.author)
              embeds.append(embed)
            ansString = ""
            ansString += f'- {leader_nation[player["name"]]}\n' + f'- `{player["name"]}`\n' + f'- {leader_rank[player["name"]]}'
            embed.add_field(name="Nation", value=ansString, inline=True)
            cnt += 1
      if cnt:
        await inter.send(embed=embeds[0], view=CreatePaginator(embeds))
      else:
        embed.add_field(
            name="Well done!",
            value=
            f"- {nationsLookup['strings']['nation']} has allied every online nations that can be allied :)",
            inline=True)
        await inter.send(embed=embed, ephemeral=True)

    except:
      embed = Utils.Embeds.error_embed(
          value=
          "If it is not evident that the error was your fault, please report it",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)

  @nation.sub_command(
      description="View all the mayors last online time of a specified nation")
  async def activity(self,
                     inter: disnake.ApplicationCommandInteraction,
                     nation: str = commands.Param(description="Nation's name"),
                     server: str = commands.Param(
                         description="Server name, defaults to Aurora",
                         default="aurora",
                         choices=["aurora"])):
    commandString = f"/nation activity nation: {nation} server: {server}"
    await inter.response.defer()
    try:
      time_mayor = {}
      mayor_town = {}
      nationsLookup = Utils.Lookup.lookup(server,
                                          endpoint="nations",
                                          name=nation)
      king = nationsLookup["strings"]["king"]
      townCount = len(nationsLookup["towns"])
      for town in nationsLookup["towns"]:
        townsLookup = Utils.Lookup.lookup(server, endpoint="towns", name=town)
        mayorsLookup = Utils.Lookup.lookup(
            server, endpoint="residents", name=townsLookup["strings"]["mayor"])
        lastOnline = f"<t:{round(mayorsLookup['timestamps']['lastOnline'] / 1000)}:R>"
        time_mayor[lastOnline] = townsLookup["strings"]["mayor"]
        mayor_town[townsLookup["strings"]["mayor"]] = town
    except:
      embed = Utils.Embeds.error_embed(
          value=
          "Check if you wrote a parameter incorrectly or if the server is currently offline",
          type="userError",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)
      return

    try:
      embeds = []
      cnt = 0
      for time in time_mayor:
        if cnt % 6 == 0:
          embed = Utils.Embeds.embed_builder(
              title=
              f"`{nationsLookup['strings']['nation']} has {townCount} towns`",
              footer=commandString,
              author=inter.author,
              thumbnail=f"https://mc-heads.net/head/{king}")
          embeds.append(embed)
        ansString = ""
        ansString += f'- {mayor_town[time_mayor[time]]}\n'+f'- `{time_mayor[time]}`\n'+f'- {time}'
        embed.add_field(name="Town", value=ansString, inline=True)
        cnt += 1
      await inter.send(embed=embeds[0], view=CreatePaginator(embeds))

    except:
      embed = Utils.Embeds.error_embed(
          value=
          "If it is not evident that the error was your fault, please report it",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)

  @nation.sub_command(description="View all the falling nations")
  async def falling(self,
                    inter: disnake.ApplicationCommandInteraction,
                    server: str = commands.Param(
                        description="Server name, defaults to Aurora",
                        default="aurora",
                        choices=["aurora"])):
    commandString = f"/nation falling server: {server}"
    await inter.response.defer()
    try:
      url = "http://PUT_YOUR_OWN_SERVER_IP_HERE/logs/nations.txt"
      res = requests.get(url)
      if res.status_code == 200:
        file_content = res.text
        lines = file_content.split('\n')
        formatted_lines = []
        for line in lines:
          if line != "":
            formatted_lines.append(f"- {line}")
    except:
      embed = Utils.Embeds.error_embed(
          value="Request url from FallingEventTimer error",
          type="userError",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)
      return

    try:
      if len(res.text) < 5:
        embed = Utils.Embeds.embed_builder(title="`Falling nations`",
                                           footer=commandString,
                                           author=inter.author)
        embed.add_field(
            name="Nation",
            value=
            "No falling nations recently or the searching process is running :(",
            inline=True)
        await inter.send(embed=embed, ephemeral=True)
      else:
        cnt = 1
        resString = ""
        embeds = []
        for town in formatted_lines:
          resString = resString + town + '\n'
          if cnt % 5 == 0:
            embed = Utils.Embeds.embed_builder(title="`Falling nations`",
                                               footer=commandString,
                                               author=inter.author)
            embed.add_field(name="Nation", value=resString, inline=True)
            embeds.append(embed)
            resString = ""
          cnt += 1
        await inter.send(embed=embeds[0], view=CreatePaginator(embeds))
    except:
      embed = Utils.Embeds.error_embed(
          value=
          "If it is not evident that the error was your fault, please report it",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)


def setup(bot):
  bot.add_cog(NationCommand(bot))
