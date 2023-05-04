# Procedurally Generated Pacman
This project is a Python implementation of the classic arcade game Pacman, with a twist: the maze 
is randomly generated every time you play. You can either play as Pacman yourself, or watch an AI agent 
learn to play using deep Q-learning.

(For the deep Q-learning implementation, see the [machine learning branch](https://github.com/Loppersy/ProcedurallyGeneratedPacman/tree/Machine_Learning_Implementation))

![Screenshot Example](https://i.imgur.com/clmO7ob.jpeg)

## Features
- Randomly generated mazes
- Ability to create your own maze
- Four ghosts with different personalities and behaviors
- A* Star algorithm for ghost pathfinding (in addition to the original algorithm)
- Classic arcade graphics and sound effects
- GUI for setting game options and parameters

## Requirements
- `pygame`
- `numpy`

## Usage
To play the game yourself, run the file `main.py`. A GUI will pop up where you can choose the game options, such as maze type,
difficulty, number of ghosts, etc. You can also create your own custom maps by editing the “maze1.png” file in the “assets” folder (more info below). 

Use the arrow keys to move Pacman and collect all the pellets while avoiding the ghosts. You can also eat power pellets to turn the ghosts blue and eat
them for extra points. The game will save your high score in a file called “highscore.txt” in the same folder.

## Maze Creation
To create your own maze, just edit the `maze1.png` image with any image editor of your choice.
It is a 32x32 pixel image where each pixel represents a tile in the maze. 
Once you are done editing, load the maze by cliking on the "Classic" button.
Here are the possible tiles with its RGB values.

- Empty Space: (0,0,0)
- Pac-Man*: (0,0,255)
- Pellet: (255,255,0)
- Power Pellet: (0,255,0)
- Bonus Fruit*: (255,128,0)
- Ghost House**: (255,0,0)
- Wall: Any other color

\* This objects will be shifted to the right by half a tile when spawned, to aling with the original game.

\** Ghost houses ocupy 8x5 tiles with the red tile being its top left corner. When spawned, ghost houses will replace any tiles that would ocupy their space. 
Ghost houses spawn all 4 classic ghosts like the original game, whom will return to the same ghost house when eaten. Code for "homeless" ghosts is written;
however, if you want to spawn them yourself you will have to modify the `populate_maze` function in `main.py` and add its sprite to the respective sprite group.

## Credits
- The original Pac-Man game.
- https://pacman.holenet.info/

## License
See the LICENSE file for details.
