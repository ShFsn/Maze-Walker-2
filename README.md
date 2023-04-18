```
              ___  ___     ____   ____   ____
             /   |/   |   /    | |_   | |____|
            / /|   /| |  / /_| |  /  /_ |___|
           /_/ |__/ |_| /_/  |_| |____| |____|
 _   __   __  ____   _      _  __  ____   ____     _   _
| | /  | / / /    | | |    | |/ / |____| | |\ \   | | | |
| |/   |/ / / /_| | | |__  |   |  |___|  | |/ /   | | | |
|___/|___/ /_/  |_| |____| |_|\_\ |____| |_|\_\   |_| |_|
```

This is a simple Python-based game with __ascii__ graphics where you can try your skills at solving mazes.

You can play by your own or compete with your friend as well!

## Installation

1. Download and install the newest version of Python from the [official website](https://www.python.org/);
2. Download and unzip the game;
3. Open terminal (or command line) from the game folder and run this command: `pip install -r requirements.txt`;
4. You are ready to go!;

## Using

Just run the `Maze Walker II.py` file.

After that you can choose offered options by clicking corresponding `[buttons]`.

Players position is controlled by `w,a,s,d` and `arrows`.

## Features

1. You can play the game by yourself or solve mazes with your friend, competing on solving speed. When someone will reach finish, the timer will stop.
2. Mazes can be generated using two different algorithms: "___Depth-first search___" (__DFS__) and "___Minimal spanning tree___" (__MST__). There's no practical difference between them from the users side though.
3. You can choose height and width of your future maze. The game will suggest you maximum possible parameters according to your window size. If you want larger mazes to be displayed -- just stretch the window.
4. There are 3 options for start and finish points available:
   1. First one places them in the corners;
   2. Second one chooses their place randomly;
   3. Third one sticks them to sides randomly.
5. If you want to continue later (or just have accidentally generated a beautiful maze) you can use save it (with current timer value). There's 5 save slots for singleplayer mode and 5 for multiplayer mode. You can find them in ```saves/``` folder.
6. If you (or your friend) got lost -- press `[1]` or `[2]` respectively to show the way to finish.