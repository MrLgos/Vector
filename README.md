<h1 align="center">
  <a href="https://discord.gg/yG7GSrGcbS"><img src="https://cdn.discordapp.com/attachments/1078305413503651932/1152506659843887164/IMG_6490.jpg" alt="Moon by Lgos"></a>
  <br>
  <font color="#000000">V</font><font color="#333333">e</font><font color="#666666">c</font><font color="#999999">t</font><font color="#CCCCCC">or</font>
  <br>
</h1>
<h4 align="center">Vibrant, Elegant, Creative, Tenacious, Outstanding and Remarkable.</h4>

<p align="center">
  <a href="https://discord.gg/yG7GSrGcbS">
    <img src="https://discordapp.com/api/guilds/1137781194432462888/widget.png?style=shield" alt="Discord Server">
  </a>
  <br>
  <a href="https://github.com/Fruitloopins/Plunkten/">
     <img src="https://img.shields.io/badge/Fruitloopins-plunkten-blue" alt="plunken">
  </a>
  <a href="https://github.com/Owen3H">
     <img src="https://img.shields.io/badge/Owen3H-emctoolkit-red" alt="emctoolkit">
  </a>
  <a href="https://github.com/DorianAarno/Paginator">
     <img src="https://img.shields.io/badge/DorianAarno-paginator-g" alt="paginator">
  </a>
</p>

Hello EarthMC players & developers,
glad to bring **Vector** to EMC Community.
Today it's running on 30 Discord servers for free and soon there will be more developers join us.
We can not only enjoy the game, we can also enjoy the joy of writing code.
So, I decide to open-source my code for reference and discussion to **avoid reinventing the wheel**. I hope everyone can help me improve the code.
Thanks for your support.

## Structure
**Main Structure**: `Vector/Pinned-Vector <=> Search-Engine` 

**1.1 Vector structure/** Based on [Plunkten](https://github.com/Fruitloopins/Plunkten)
```shell
./
|-- Commands          # Based on Plunkten.
|   |-- NationCommand.py
|   |-- ResCommand.py
|   |-- ServerCommand.py
|   `-- TownCommand.py
|-- LICENSE
|-- README.md
|-- Utils
|   `-- Utils.py      # Tools.
|-- keep_alive.py     # Optional. Free cloud server like replit, will need this.
|-- logs
|   `-- cemetery.txt  # Store fallen towns that have been outputted.
`-- main.py
```

**1.2 Pinned-Vector structure/** Based on Vector
```shell
./
|-- Utils.py          # Tools.
|-- keep_alive.py     # Optional. Free cloud server like replit, will need this.
`-- main.py           # Updating pinned message about wilderness victims.
```

**2.1 Search engine structure/**
```shell
./
|-- data              # Temporarily store the result here in order to prevent Vector get Updating empty *.txt
|   |-- cemetery.txt
|   |-- nations.txt
|   `-- towns.txt
|-- logs              # Vector request the data from here.
|   |-- cemetery.txt
|   |-- nations.txt
|   `-- towns.txt
|-- main.py           # Request data every 30 mins and write analysis result to /data/*.txt and /logs/*.txt.
`-- restart6h.sh      # Restart main.py every 6 hours in case main.py accidently crash.
```

## Contact
Any ideas or issues, feel free to contact me.
<p align="center">
  <a href="https://discord.gg/yG7GSrGcbS">
    <img src="https://discord-cards.kurizu.repl.co/api/card/803182913582792755?about=%E5%BE%85%E5%88%B0%E7%A7%8B%E6%9D%A5%E4%B9%9D%E6%9C%88%E5%85%AB&banner=https://cdn.discordapp.com/attachments/1078305413503651932/1152506659843887164/IMG_6490.jpg&large_image=&small_image=https://cdn.discordapp.com/attachments/1078305413503651932/1152517790922706954/R.png&hex=" alt="Lgos">
  </a>
</p>