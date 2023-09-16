import datetime
import disnake
import requests
import traceback
import random
import math
import time


class CommandTools():

  def get_weather(serverLookup):
    if serverLookup["world"][
        "hasStorm"] == True & serverLookup["world"]["isThundering"] == True:
      weather = "Thundering"
    elif serverLookup["world"]["hasStorm"] == True:
      weather = "Raining"
    else:
      weather = "Clear"

    return weather

  def list_to_string(list):
    listString = ""
    for i in range(len(list)):
      if i == len(list) - 1:
        listString += list[i]
      else:
        listString += list[i] + ", "

    return listString

  def NearbyNationRequest(x, z, allies, bulkNationLookup):
    nations = {}
    sorted_nations = []
    for nation in bulkNationLookup:
      if nation['name'] not in allies:
        continue
      nx = nation['spawn']['x']
      nz = nation['spawn']['z']
      dist = math.hypot(nx - x, nz - z)
      nations[nation['name']] = dist
    sorted_nations = sorted(nations.items(), key=lambda item: item[1])
    return sorted_nations

  def NotInside(x, z):
    rx, rz = 300, 300
    url = f"https://emctoolkit.vercel.app/api/aurora/nearby/towns/{x}/{z}/{rx}/{rz}"
    nearbyLookup = requests.get(url).json()
    if not nearbyLookup:
      return True
    else:
      return False

  def IsNewPlayer(name):
    url = f"https://api.earthmc.net/v2/aurora/residents/{name}"
    current_millisecond_timestamp = int(time.time() * 1000)
    playerLookup = requests.get(url).json()
    register_timestamp = playerLookup['timestamps']['registered']
    if (current_millisecond_timestamp - register_timestamp) > 86400000:
      return False
    else:
      return True


class Lookup():

  def lookup(server, endpoint=None, name=None, version="v1", opt="emc"):
    if opt == "emc":
      if endpoint == None:
        api_url = f"https://api.earthmc.net/{version}/{server}/"
      elif name == None:
        api_url = f"https://api.earthmc.net/{version}/{server}/{endpoint}"
      else:
        api_url = f"https://api.earthmc.net/{version}/{server}/{endpoint}/{name}"
    elif opt == "toolkit":
      if name == None:
        if endpoint != 'serverinfo':
          api_url = f"https://emctoolkit.vercel.app/api/aurora/{endpoint}"
        else:
          api_url = f"https://emctoolkit.vercel.app/api/{endpoint}"
    lookup = requests.get(api_url).json()
    return lookup


class Embeds():

  def embed_builder(title,
                    description=None,
                    author=None,
                    footer=None,
                    thumbnail=None):
    embed = disnake.Embed(title=title,
                          description=description,
                          color=(random.randint(0, 255) << 16) +
                          (random.randint(0, 255) << 8) +
                          (random.randint(0, 255)),
                          timestamp=datetime.datetime.now())

    if author != None:
      embed.set_author(name=f"Queried by {author.name}",
                       icon_url=author.avatar)

    if footer != None:
      embed.set_footer(
          icon_url=
          "https://cdn.discordapp.com/attachments/1137781195023851542/1142481288377409597/logo.png",
          text=footer)

    else:
      embed.set_footer(
          icon_url=
          "https://cdn.discordapp.com/attachments/1137781195023851542/1142481288377409597/logo.png",
          text="Yue")

    if thumbnail != None:
      embed.set_thumbnail(url=thumbnail)

    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1050945545037951048/1099030835220467872/linebreak.png"
    )

    return embed

  def error_embed(value, type=None, footer=None):
    if type != "userError":
      traceback.print_exc()
    embed = Embeds.embed_builder(title="`Error`", footer=footer)

    embed.add_field(name="Something went wrong", value=value, inline=True)

    return embed
