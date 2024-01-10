import random
import disnake
from disnake.ext import commands
import Utils.Utils as Utils


class ResCommand(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.slash_command()
  async def res(self, inter):
    pass

  @res.sub_command(description="Provides general info about a resident")
  async def search(
      self,
      inter: disnake.ApplicationCommandInteraction,
      username: str = commands.Param(
          description="Resident's username, type 'random' for a random choice"
      ),
      server: str = commands.Param(
          description="Server name, defaults to Aurora",
          default="aurora",
          choices=["aurora"])):
    commandString = f"/res search username: {username} server: {server}"
    await inter.response.defer()
    try:
      if username == "random":
        allResidentsLookup = Utils.Lookup.lookup(server, endpoint="residents")
        username = random.choice(allResidentsLookup["allResidents"])
      residentsLookup = Utils.Lookup.lookup(server,
                                            endpoint="residents",
                                            name=username)

    except:
      embed = Utils.Embeds.error_embed(
          value=
          "Check if you wrote a parameter incorrectly or if the server is currently offline",
          type="userError",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)
      return

    try:
      fullNameList = [
          residentsLookup["strings"]["title"],
          residentsLookup["strings"]["username"],
          residentsLookup["strings"]["surname"]
      ]
      fullNameList = [x for x in fullNameList if x != ""]

      fullName = ""
      for i in range(len(fullNameList)):
        if i == len(fullNameList) - 1:
          fullName += fullNameList[i]
        else:
          fullName += fullNameList[i] + " "

      if residentsLookup["timestamps"]["lastOnline"] != 0:
        lastOnline = f"<t:{round(residentsLookup['timestamps']['lastOnline'] / 1000)}:R>"
      else:
        lastOnline = "NPC"

      try:
        town = residentsLookup["affiliation"]["town"]
        joinedTownAt = f"<t:{round(residentsLookup['timestamps']['joinedTownAt'] / 1000)}:R>"
        try:
          nation = residentsLookup["affiliation"]["nation"]
        except:
          nation = None

      except:
        town = None
        joinedTownAt = "N/A"
        nation = None

      rnaoPermsList = Utils.CommandTools.rnao_perms(json=residentsLookup)
      TrueFalse_Flag = {True: "🟢", False: "🔴"}

      embed = Utils.Embeds.embed_builder(
          title=f"`{fullName}`",
          author=inter.author,
          footer=commandString,
          thumbnail=
          f"https://mc-heads.net/head/{residentsLookup['strings']['username']}"
      )

      embed.add_field(name="Affiliation",
                      value=f"• `Town` — {town}\n• `Nation` — {nation}",
                      inline=True)
      embed.add_field(
          name="Online",
          value=TrueFalse_Flag[residentsLookup["status"]["isOnline"]],
          inline=True)
      embed.add_field(name="Balance",
                      value=f"{residentsLookup['stats']['balance']}G",
                      inline=True)

      embed.add_field(
          name="Registered",
          value=
          f"<t:{round(residentsLookup['timestamps']['registered'] / 1000)}:R>",
          inline=True)
      embed.add_field(name="Last Online", value=lastOnline, inline=True)
      embed.add_field(name="Joined Town", value=joinedTownAt, inline=True)

      embed.add_field(
          name="Perms",
          value=
          f"• `Build` — {rnaoPermsList[0]}\n• `Destroy` — {rnaoPermsList[1]}\n• `Switch` — {rnaoPermsList[2]}\n• `ItemUse` — {rnaoPermsList[3]}",
          inline=True)
      embed.add_field(
          name="Flags",
          value=
          f"• `PvP` — {TrueFalse_Flag[residentsLookup['perms']['flagPerms']['pvp']]}\n• `Explosions` — {TrueFalse_Flag[residentsLookup['perms']['flagPerms']['explosion']]}\n• `Firespread` — {TrueFalse_Flag[residentsLookup['perms']['flagPerms']['fire']]}\n• `Mob Spawns` — {TrueFalse_Flag[residentsLookup['perms']['flagPerms']['mobs']]}",
          inline=True)

      for rankType in residentsLookup["ranks"]:
        if len(residentsLookup["ranks"][rankType]) != 0:
          rankString = Utils.CommandTools.list_to_string(
              list=residentsLookup["ranks"][rankType])

          if rankType == "townRanks":
            name = "Town Ranks"
          else:
            name = "Nation Ranks"

          embed.add_field(name=name, value=rankString.title(), inline=False)

      await inter.send(embed=embed, ephemeral=False)

    except:
      embed = Utils.Embeds.error_embed(
          value=
          "If it is not evident that the error was your fault, please report it",
          footer=commandString)

      await inter.send(embed=embed, ephemeral=True)


def setup(bot):
  bot.add_cog(ResCommand(bot))
