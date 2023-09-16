import random
import math
import requests
import disnake
from disnake.ext import commands
import Utils.Utils as Utils
from Paginator import CreatePaginator


class TownCommand(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def town(self, inter):
    pass

  @town.sub_command(description="Provides general info about a town")
  async def search(
      self,
      inter: disnake.ApplicationCommandInteraction,
      town: str = commands.Param(
          description="Town's name, type 'random' for a random choice"),
      server: str = commands.Param(
          description="Server name, defaults to Aurora",
          default="aurora",
          choices=["aurora"])):
    commandString = f"/town search town: {town} server: {server}"
    await inter.response.defer()
    try:
      if town == "random":
        allTownsLookup = Utils.Lookup.lookup(server, endpoint="towns")
        town = random.choice(allTownsLookup["allTowns"])
      townsLookup = Utils.Lookup.lookup(server, endpoint="towns", name=town)

    except:
      embed = Utils.Embeds.error_embed(
          value=
          "Check if you wrote a parameter incorrectly or if the server is currently offline",
          type="userError",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)
      return

    try:
      try:
        locationUrl = f"https://earthmc.net/map/{server}/?zoom=4&x={townsLookup['spawn']['x']}&z={townsLookup['spawn']['z']}"
        location = f"[{int(round(townsLookup['spawn']['x'], 0))}, {int(round(townsLookup['spawn']['z'], 0))}]({locationUrl})"
      except:
        locationUrl = f"https://earthmc.net/map/{server}/?zoom=4&x={townsLookup['home']['x'] * 16}&z={townsLookup['home']['z'] * 16}"
        location = f"[{townsLookup['home']['x'] * 16}, {townsLookup['home']['z'] * 16}]({locationUrl})"

      try:
        nation = townsLookup["affiliation"]["nation"]
        joinedNationAt = f"<t:{round(townsLookup['timestamps']['joinedNationAt'] / 1000)}:R>"
      except:
        nation = None
        joinedNationAt = "N/A"

      rnaoPermsList = Utils.CommandTools.rnao_perms(json=townsLookup)

      embed = Utils.Embeds.embed_builder(
          title=f"`{townsLookup['strings']['town']}`",
          description=townsLookup["strings"]["board"],
          footer=commandString,
          author=inter.author)

      embed.add_field(name="Mayor",
                      value=townsLookup["strings"]["mayor"],
                      inline=True)
      embed.add_field(name="Nation", value=nation, inline=True)
      embed.add_field(name="Location", value=location, inline=True)

      embed.add_field(name="Residents",
                      value=townsLookup["stats"]["numResidents"],
                      inline=True)
      embed.add_field(
          name="Town Blocks",
          value=
          f"{townsLookup['stats']['numTownBlocks']}/{townsLookup['stats']['maxTownBlocks']} ({townsLookup['stats']['numTownBlocks'] * 16 + 48}G)",
          inline=True)
      embed.add_field(name="Balance",
                      value=f"{townsLookup['stats']['balance']}G",
                      inline=True)

      embed.add_field(name="Founder",
                      value=townsLookup["strings"]["founder"],
                      inline=True)
      embed.add_field(
          name="Founded",
          value=
          f"<t:{round(townsLookup['timestamps']['registered'] / 1000)}:R>",
          inline=True)
      embed.add_field(name="Joined Nation", value=joinedNationAt, inline=True)

      embed.add_field(
          name="Perms",
          value=
          f"• `Build` — {rnaoPermsList[0]}\n• `Destroy` — {rnaoPermsList[1]}\n• `Switch` — {rnaoPermsList[2]}\n• `ItemUse` — {rnaoPermsList[3]}",
          inline=True)
      embed.add_field(
          name="Flags",
          value=
          f"• `PvP` — {townsLookup['perms']['flagPerms']['pvp']}\n• `Explosions` — {townsLookup['perms']['flagPerms']['explosion']}\n• `Firespread` — {townsLookup['perms']['flagPerms']['fire']}\n• `Mob Spawns` — {townsLookup['perms']['flagPerms']['mobs']}",
          inline=True)
      embed.add_field(
          name="Status",
          value=
          f"• `Capital` — {townsLookup['status']['isCapital']}\n• `Open` — {townsLookup['status']['isOpen']}\n• `Public` — {townsLookup['status']['isPublic']}\n• `Neutral` — {townsLookup['status']['isNeutral']}\n• `Overclaimed` — {townsLookup['status']['isOverClaimed']}\n• `Ruined` — {townsLookup['status']['isRuined']}",
          inline=True)

      await inter.send(embed=embed, ephemeral=False)

    except:
      embed = Utils.Embeds.error_embed(
          value=
          "If it is not evident that the error was your fault, please report it",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)

  @town.sub_command(description="View all the falling towns")
  async def falling(self,
                    inter: disnake.ApplicationCommandInteraction,
                    server: str = commands.Param(
                        description="Server name, defaults to Aurora",
                        default="aurora",
                        choices=["aurora"])):
    commandString = f"/town falling server: {server}"
    await inter.response.defer()
    try:
      url = "http://PUT_YOUR_OWN_SERVER_IP_HERE/logs/towns.txt"
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
        embed = Utils.Embeds.embed_builder(title="`Falling towns`",
                                           footer=commandString,
                                           author=inter.author)
        embed.add_field(
            name="Town",
            value=
            "No falling towns recently or the searching process is running :(",
            inline=True)
        await inter.send(embed=embed, ephemeral=True)
      else:
        cnt = 1
        resString = ""
        embeds = []
        for town in formatted_lines:
          resString = resString + town + '\n'
          if cnt % 5 == 0:
            embed = Utils.Embeds.embed_builder(title="`Falling towns`",
                                               footer=commandString,
                                               author=inter.author)
            embed.add_field(name="Town", value=resString, inline=True)
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

  @town.sub_command(
      description="Provides 5 nearest nations as the route of the specified town"
  )
  async def route(self,
                  inter: disnake.ApplicationCommandInteraction,
                  town: str = commands.Param(description="Town's name"),
                  nation: str = commands.Param(
                      description="Your nation's name",
                      default="None"),
                  server: str = commands.Param(
                      description="Server name, defaults to Aurora",
                      default="aurora",
                      choices=["aurora"])):
    commandString = f"/town route town: {town} nation: {nation} server: {server}"
    await inter.response.defer()
    try:
      townsLookup = Utils.Lookup.lookup(server,
                                        endpoint="towns",
                                        name=town,
                                        version="v2")
      if nation == 'None':
        nationsLookup = Utils.Lookup.lookup(server,
                                            endpoint="nations",
                                            version="v1")
        allies = nationsLookup['allNations']
      else:
        nationsLookup = Utils.Lookup.lookup(server,
                                            endpoint="nations",
                                            name=nation,
                                            version="v2")
        allies = nationsLookup['allies']
      x, z = townsLookup["coordinates"]["spawn"]["x"], townsLookup[
          "coordinates"]["spawn"]["z"]
      sorted_nations = Utils.CommandTools.NearbyNationRequest(x, z, allies)
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
          title=f"`Route to {townsLookup['name']}`",
          description="5 Nearest nations here!",
          footer=commandString,
          author=inter.author)

      ansString = ""
      top_5_sorted = sorted_nations[:5]
      for key, value in top_5_sorted:
        ansString += f"- Nation: `{key}`   Dist: `{int(value)} blocks`\n"

      embed.add_field(name="Route", value=ansString, inline=True)

      await inter.send(embed=embed, ephemeral=False)
    except:
      embed = Utils.Embeds.error_embed(
          value=
          "If it is not evident that the error was your fault, please report it",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)


def setup(bot):
  bot.add_cog(TownCommand(bot))
