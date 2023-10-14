import disnake
from disnake.ext import commands, tasks
import os
import requests
import Utils
import threading
from EarthMC import Maps, OfficialAPI
from keep_alive import keep_alive

keep_alive()
Aurora = Maps.Aurora()
bot = commands.InteractionBot()

@bot.event
async def on_ready():
  activity = disnake.Activity(
      name="The Sky",
      type=disnake.ActivityType.watching,
  )
  await bot.change_presence(activity=activity)
  print(f"Logged in as {bot.user}")
  print(f"Operating in {len(bot.guilds)} guild/s")
  if not victims.is_running():
    victims.start()

@tasks.loop(seconds=60)
async def victims():
  sayings = ["May the Force be with you.", "I'm inevitable.", "Good afternoon, good evening and good night."]
  channel_id = 1146817491092390048
  channel = bot.get_channel(channel_id)
  message = await channel.fetch_message(1147227436199718983)
  embed = Utils.Embeds.embed_builder(title="**Live Wilderness Victims**",
                                     footer="Maintained by Lgos#0001")
  ap = Aurora.Players
  onlineLookup = ap.online.all()
  nationsLookup = Utils.Lookup.lookup("aurora",
                                      endpoint="nations",
                                      version="v1")
  bulkNationLookup = Utils.Lookup.lookup(server="aurora", endpoint="nations", version="v2")
  allies = nationsLookup['allNations']
  victimStr = ""
  allStr = []
  cnt = 0
  for player in onlineLookup:
    x, z = player['x'], player['z']
    if player[
        'world'] != '-some-other-bogus-world-' and Utils.CommandTools.NotInside(
            x, z) == True and Utils.CommandTools.IsNewPlayer(
                player['name']) == False:
      nation = Utils.CommandTools.NearbyNationRequest(x, z, allies, bulkNationLookup)[:1]
      victimStr += (
          f"- **{player['name']}** [{int(x)}, {int(z)}](https://earthmc.net/map/aurora/?worldname=earth&mapname=flat&zoom=3&x={x}&z={z})  nation: `{nation[0][0]}` Dist: `{int(nation[0][1])}`\n"
      )
      cnt += 1
      if cnt % 6 == 0:
        allStr.append(victimStr)
        victimStr = ""
  if not cnt:
    victimStr = "- **No Victims in the Wilderness now.**"
    embed.add_field(name=sayings[2],
                    value=victimStr,
                    inline=False)
  elif cnt < 6:
    embed.add_field(name=sayings[0],
                  value=victimStr,
                  inline=False)
  else:
    index = 0
    for x in allStr:
      embed.add_field(name=sayings[index],
                    value=x,
                    inline=False)
      index += 1
    if cnt % 6 != 0:
      embed.add_field(name=sayings[index],
                    value=victimStr,
                    inline=False)
      
  await message.edit(embed=embed)

bot.run(os.getenv("TOKEN"))
