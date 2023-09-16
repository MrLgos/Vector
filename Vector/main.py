import disnake
from disnake.ext import commands, tasks
import os
import requests
import dotenv
import Utils.Utils as Utils
import threading
from EarthMC import Maps, OfficialAPI
from keep_alive import keep_alive

keep_alive()
Aurora = Maps.Aurora()
bot = commands.InteractionBot()

@tasks.loop(seconds=30)
async def bot_activity():
  activity = disnake.Activity(
      name=f"{len(bot.guilds)} Servers",
      type=disnake.ActivityType.watching,
  )
  await bot.change_presence(activity=activity)


@bot.event
async def on_ready():
  print(f"Logged in as {bot.user}")
  print(f"Operating in {len(bot.guilds)} guild/s")
  bot_activity.start()
  
  cemetery.start()
  townless.start()
  server.start()


@tasks.loop(minutes=30)
async def cemetery():
  try:
    print("The cemetery working now...")
    channel_id = 1145350721252884540
    channel = bot.get_channel(channel_id)
    try:
      with open('./logs/cemetery.txt', 'r', encoding="utf-8") as file:
        lines = file.readlines()
      history = set()
      for line in lines:
        history.add(line.strip())

      url = "http://PUT_YOUR_OWN_SERVER_IP_HERE/logs/cemetery.txt"
      res = requests.get(url)
      if res.status_code == 200:
        file_content = res.text
        lines = file_content.split('\n')
        for line in lines:
          if line != "" and line not in history:
            town = line.split(' ')[0]
            town_size = line.split(' ')[1]
            location = line.split(' ')[2] + ' ' + line.split(' ')[3]
            embed = Utils.Embeds.embed_builder(title=f"`{town}`")
            embed.add_field(name="Chunks", value=town_size, inline=True)
            embed.add_field(name="Location", value=location, inline=True)
            with open('./logs/cemetery.txt', 'a+', encoding="utf-8") as f:
              f.write(f'{town} {town_size} {location}\n')
            f.close()
            await channel.send(embed=embed)
    except:
      embed = Utils.Embeds.error_embed(
          value="Request url from cemeteryTimer error", type="userError")
      await channel.send(embed=embed)
      return
  except Exception as e:
    cemetery.restart()


@tasks.loop(seconds=30)
async def townless():
  try:
    channel_id = 1146817491092390048
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(1146824923730419732)
    embed = Utils.Embeds.embed_builder(title="**Live Townless Players**",
                                       footer="Maintained by Lgos#0001")
    ap = Aurora.Players
    townlessList = ap.townless.all()
    townlessStr = "```\n"
    for player in townlessList:
      townlessStr += f"{player['name']}\n"
    townlessStr += "```"
    embed.add_field(name="What is the Matrix?", value=townlessStr, inline=True)
    await message.edit(embed=embed)
  except Exception as e:
    townless.restart()


@tasks.loop(seconds=60)
async def server():
  try:
    channel_id = 1146817491092390048
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(1146831052262879312)
    serverToolkitLookup = Utils.Lookup.lookup("aurora",
                                              endpoint="serverinfo",
                                              opt="toolkit")
    queue = serverToolkitLookup['queue']
    embed = Utils.Embeds.embed_builder(title="**Live Aurora Info**",
                                       footer="Maintained by Lgos#0001")
    serverLookup = Utils.Lookup.lookup("aurora", version="v2")
    weather = Utils.CommandTools.get_weather(serverLookup)
    embed.add_field(
        name="Online Players",
        value=
        f"{serverToolkitLookup['aurora']}/{serverToolkitLookup['max']}    `queue:{queue}`",
        inline=False)
    embed.add_field(name="Weather", value=weather, inline=True)
    embed.add_field(name="Time",
                    value=f"{serverLookup['world']['time']}/24000",
                    inline=True)
    embed.add_field(name="Day",
                    value=int(
                        round(serverLookup["world"]["fullTime"] / 24000, 0)),
                    inline=True)
    embed.add_field(
        name="Stats",
        value=
        f"• `Residents` — {serverLookup['stats']['numResidents']}\n• `Towns` — {serverLookup['stats']['numTowns']}\n• `Nations` — {serverLookup['stats']['numNations']}",
        inline=False)
    await message.edit(embed=embed)
  except Exception as e:
    server.restart()


bot.load_extension("Commands.ServerCommand")
bot.load_extension("Commands.ResCommand")
bot.load_extension("Commands.TownCommand")
bot.load_extension("Commands.NationCommand")

dotenv.load_dotenv("secrets.env")
bot.run(os.environ["TOKEN"])
