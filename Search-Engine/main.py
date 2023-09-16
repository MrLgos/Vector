import asyncio
import os
import shutil
import time
import threading
import requests
from datetime import datetime
from time import strftime
from time import gmtime
from dateutil.parser import parse
from concurrent.futures import ThreadPoolExecutor

MAX_REQUESTS_PER_SECOND = 5
REQUEST_INTERVAL = 1 / MAX_REQUESTS_PER_SECOND


def timeTransfer(TimeStamp):
  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  last = datetime.fromtimestamp(TimeStamp).strftime('%Y-%m-%d %H:%M:%S')
  date_now = parse(now)
  date_last = parse(last)
  result = (date_now - date_last).total_seconds()
  m, s = divmod(result, 60)
  h, m = divmod(m, 60)
  d, h = divmod(h, 24)
  return d, h, m, s


def townRequest(town):
  url = f"https://api.earthmc.net/v2/aurora/towns/{town}"
  resNum = 0
  try:
    townsLookup = requests.get(url).json()
    mayor = townsLookup['mayor']
    is_ruined = townsLookup['status']['isRuined']
    is_open = townsLookup['status']['isOpen']
    town_size = townsLookup['stats']['numTownBlocks']
    if is_ruined == True:
      with open('./data/cemetery.txt', 'r') as file:
        lines = file.readlines()
      cemetery = set()
      for line in lines:
        cemetery.add(line.strip())
      if town not in cemetery:
        x = townsLookup['coordinates']['home'][0] * 16
        z = townsLookup['coordinates']['home'][1] * 16
        locationUrl = f"https://earthmc.net/map/aurora/?zoom=4&x={x}&z={z}"
        location = f"[{x}, {z}]({locationUrl})"
        with open('./data/cemetery.txt', 'a+', encoding="utf-8") as f:
            f.write(f'{town} {town_size} {location}\n')
        f.close()
      return
    x = int(townsLookup['coordinates']['spawn']['x'])
    z = int(townsLookup['coordinates']['spawn']['z'])
    town_size = townsLookup['stats']['numTownBlocks']
    resNum = townsLookup['stats']['numResidents']
    bank = townsLookup['stats']['balance']
    nation = townsLookup['nation']
  except Exception as e:
    print(e)
  if resNum <= 2:
    try:
      mayorLookup = requests.get(
          f"https://api.earthmc.net/v2/aurora/residents/{mayor}").json()
    except Exception as e:
      print(e)
    lastOnline_TimeStamp = mayorLookup['timestamps']['lastOnline'] / 1000
    d, h, m, s = timeTransfer(lastOnline_TimeStamp)
    if d >= 37 and d <= 45 and is_ruined == False:
      with open('data/towns.txt', 'a+', encoding="utf-8") as f:
        f.write(
                "Town: %s [Nation: %s][Open: %s]\nBank: %dG [Chunks: %d]\nMayor: %s [Residents: %d]\nOffline since %d days %d hours %d minutes %d seconds.\ndynmap URL: [%d, %d](https://earthmc.net/map/aurora/?worldname=earth&mapname=flat&zoom=5&x=%d&z=%d)\n\n"
            % (town, nation, is_open, bank, town_size, mayor, resNum, d, h, m, s, x, z, x, z))
      f.close()


def nationRequest(nation):
  nurl = f"https://api.earthmc.net/v2/aurora/nations/{nation}"
  try:
    nationsLookup = requests.get(nurl).json()
    capital = nationsLookup['capital']
    is_open = nationsLookup['status']['isOpen']
    bank = nationsLookup['stats']['balance']
    townCount = len(nationsLookup['towns'])
    king = nationsLookup['king']
    turl = f"https://api.earthmc.net/v2/aurora/towns/{capital}"
    capitalLookup = requests.get(turl).json()
    x = capitalLookup['coordinates']['spawn']['x']
    z = capitalLookup['coordinates']['spawn']['z']
    is_capital_open = capitalLookup['status']['isOpen']
    resNum = capitalLookup['stats']['numResidents']
    kurl = f"https://api.earthmc.net/v2/aurora/residents/{king}"
    if resNum <= 3:
      kingLookup = requests.get(kurl).json()
      lastOnline_TimeStamp = kingLookup['timestamps']['lastOnline'] / 1000
      d, h, m, s = timeTransfer(lastOnline_TimeStamp)
      if d >= 30 and d <= 45:
        with open('data/nations.txt', 'a+', encoding="utf-8") as f:
          f.write(
                  "Nation: %s [Nation Open: %s][Capital Open: %s]\nBank: %dG [Towns: %d]\nKing: %s [Capital Residents: %d]\nOffline since %d days %d hours %d minutes %d seconds.\ndynmap URL: [%d, %d](https://earthmc.net/map/aurora/?worldname=earth&mapname=flat&zoom=5&x=%d&z=%d)\n\n"
              % (nation, is_open, is_capital_open,  bank, townCount, king, resNum, d, h, m, s, x, z, x, z))
        f.close()
  except Exception as e:
    print(e)


def Query_Falling_Towns():
  allTownsLookup = requests.get(
      "https://api.earthmc.net/v1/aurora/towns/").json()
  allTowns = allTownsLookup["allTowns"]
  total_requests = len(allTowns)
  if os.path.exists("./data/towns.txt"):
    os.remove("./data/towns.txt")
  os.mknod("./data/towns.txt")
  if os.path.exists("./data/cemetery.txt"):
    os.remove("./data/cemetery.txt")
  os.mknod("./data/cemetery.txt")
  print("Running now, pls wait...")
  with ThreadPoolExecutor(max_workers=total_requests) as executor:
    for town in allTowns:
      try:
        executor.submit(townRequest, town)
        time.sleep(REQUEST_INTERVAL)
      except:
        continue
  if os.path.exists("./logs/towns.txt"):
    os.remove("./logs/towns.txt")
  shutil.copy("./data/towns.txt", "./logs/towns.txt")
  if os.path.exists("./logs/cemetery.txt"):
    os.remove("./logs/cemetery.txt")
  shutil.copy("./data/cemetery.txt", "./logs/cemetery.txt")
  print("Check done. Use /seen in game to check more details!")


def Query_Falling_Nations():
  allNationsLookup = requests.get(
      "https://api.earthmc.net/v1/aurora/nations/").json()
  allNations = allNationsLookup["allNations"]
  total_requests = len(allNations)
  if os.path.exists("./data/nations.txt"):
    os.remove("./data/nations.txt")
  os.mknod("./data/nations.txt")
  print("Running now, pls wait...")
  with ThreadPoolExecutor(max_workers=total_requests) as executor:
    for nation in allNations:
      try:
        executor.submit(nationRequest, nation)
        time.sleep(REQUEST_INTERVAL)
      except:
        continue
  if os.path.exists("./logs/nations.txt"):
    os.remove("./logs/nations.txt")
  shutil.copy("./data/nations.txt", "./logs/nations.txt")
  print("Check done. Use /seen in game to check more details!")

def timer_event():
  Query_Falling_Towns()
  Query_Falling_Nations()

if __name__ == "__main__":
  while True:
    timer_event()
    time.sleep(1800)
