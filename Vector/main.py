import disnake
from disnake.ext import commands, tasks
import os
import requests
import dotenv
import Utils.Utils as Utils
import threading
from EarthMC import Maps
from googletrans import Translator

Aurora = Maps.Aurora()
dotenv.load_dotenv("Vector.env")
intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)
flag = 0
service_urls = ['translate.google.cn', 'translate.google.com']
proxies = {'http': "localhost:80"}
translator = Translator(service_urls=['translate.google.com'], proxies=proxies)


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

      url = os.environ["SELF_API_CEMETERY"]
      self_api_town_url = os.environ["SELF_API_TOWN"]
      self_api_nation_url = os.environ["SELF_API_NATION"]
      res = requests.get(url)
      town_res = requests.get(self_api_town_url)
      nation_res = requests.get(self_api_nation_url)
      if town_res.status_code == 200:
        file_content = town_res.text
        with open('./logs/towns.txt', 'w+', encoding="utf-8") as f:
          f.write(file_content)
        f.close()
      if nation_res.status_code == 200:
        file_content = nation_res.text
        with open('./logs/nations.txt', 'w+', encoding="utf-8") as f:
          f.write(file_content)
        f.close()
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


@tasks.loop(seconds=20)
async def server():
  try:
    global flag
    channel_id = 1146817491092390048
    ping_channel_id = 1154791633099968602
    thor_role_id = 1154799932834861197
    guild_id = 1137781194432462888
    channel = bot.get_channel(channel_id)
    ping_channel = bot.get_channel(ping_channel_id)
    guild = bot.get_guild(guild_id)

    thor_role = guild.get_role(thor_role_id)
    message = await channel.fetch_message(1146831052262879312)
    serverToolkitLookup = Utils.Lookup.lookup("aurora",
                                              endpoint="serverinfo",
                                              opt="toolkit")
    queue = serverToolkitLookup['queue']
    embed = Utils.Embeds.embed_builder(title="**Live Aurora Info**",
                                       footer="Maintained by Lgos#0001")
    serverLookup = Utils.Lookup.lookup("aurora", version="v2")
    weather = Utils.CommandTools.get_weather(serverLookup)
    if flag == 0 and weather == "Thundering":
      flag = 1
      await ping_channel.send(
          f"Weather forecast: thunderstorms! {thor_role.mention}")
    elif flag == 1 and weather != "Thundering":
      flag = 0
      await ping_channel.send("The thunderstorm is over.")
    embed.add_field(
        name="Online Players",
        value=
        f"{serverToolkitLookup['aurora']}/{serverToolkitLookup['max']}    `queue:{queue}`",
        inline=False)
    embed.add_field(name="Weather", value=weather, inline=True)
    embed.add_field(
        name="Stats",
        value=
        f"• `Residents` — {serverLookup['stats']['numResidents']}\n• `Towns` — {serverLookup['stats']['numTowns']}\n• `Nations` — {serverLookup['stats']['numNations']}\n• `TownChunks` — {serverLookup['stats']['numTownBlocks']} `worth: {16 * serverLookup['stats']['numTownBlocks']} G`",
        inline=False)
    await message.edit(embed=embed)
  except Exception as e:
    server.restart()


@bot.event
async def on_raw_reaction_add(payload):
  message_id = payload.message_id
  user_id = payload.user_id
  guild_id = payload.guild_id
  emoji = payload.emoji.name
  print(f"{emoji} from {bot.get_guild(guild_id)}")

  if message_id == 1154830519381524521 and emoji == '⚡':
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)
    role = disnake.utils.get(guild.roles, name='Thor')

    if role and member:
      await member.add_roles(role)
      print(f'{member.display_name} is granted Role {role.name}')

  if message_id == 1154830519381524521 and emoji == '✨':
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)
    role = disnake.utils.get(guild.roles, name='Vote-Party')

    if role and member:
      await member.add_roles(role)
      print(f'{member.display_name} is granted Role {role.name}')


@bot.event
async def on_raw_reaction_remove(payload):
  message_id = payload.message_id
  user_id = payload.user_id
  guild_id = payload.guild_id
  emoji = payload.emoji.name

  if message_id == 1154830519381524521 and emoji == '⚡':
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)
    role = disnake.utils.get(guild.roles, name='Thor')

    if role and member:
      await member.remove_roles(role)
      print(f"{member.display_name} 's Role {role.name} has been removed")

  if message_id == 1154830519381524521 and emoji == '✨':
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)
    role = disnake.utils.get(guild.roles, name='Vote-Party')

    if role and member:
      await member.remove_roles(role)
      print(f"{member.display_name} 's Role {role.name} has been removed")

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.channel.id == 1176917443256529038:
    detected_language = translator.detect(message.content).lang
    trans_prefix = translator.translate("Translation",
                                        dest=detected_language).text
    if detected_language == 'en':
      return  
    trans_result = translator.translate(message.content, dest='en').text
    await message.channel.send(f"[{trans_prefix}] {trans_result}")

bot.load_extension("Commands.ServerCommand")
bot.load_extension("Commands.ResCommand")
bot.load_extension("Commands.TownCommand")
bot.load_extension("Commands.NationCommand")

bot.run(os.environ["TOKEN"])
