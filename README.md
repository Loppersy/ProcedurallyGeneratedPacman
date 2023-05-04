# Machine Learning Pacman
This project is a Python implementation of the classic arcade game Pacman, but with a twist: it is a 0 player game.
Watch an AI agent learn to play by itseld by using deep Q-learning.

(For the playable implementation with procedurally generated mazes, see the [main branch](https://github.com/Loppersy/ProcedurallyGeneratedPacman))

![](https://i.imgur.com/2ihWcnB.png)

## Features
- Deep-Q learning Pac-Man
- Save and load models
- Ability to create your own maze
- Four ghosts with different personalities and behaviors
- A* Star algorithm for ghost pathfinding
- Classic arcade graphics and sound effects
- GUI for changing a few display options

## Requirements
- numpy==1.23.5
- Pillow==9.5.0
- pygame==2.1.2
- tensorflow==2.12.0
- tensorflow_intel==2.12.0

## Usage
- Run the file `pacman.py`, here are the different parameters that we used:
- -n: number of games to play in total (both training and testing)
- -x: number of games to use for training (the rest will be used for testing)
- -l: the map to use
- -g: the ghost to use (AStarGhost, RandomGhost)

Here are some examples of how to run the program:

If you want to train the neural net for 100 games, and test it for 50 games, in the classic maze
you can run:
- `python pacman.py -n 150 -x 100 -l maze1.png -g AStarGhost`

If you want to train the model for 1 game, and test it for 50 games, in the small maze you can run:
- `python pacman.py -n 51 -x 1 -l maze2.png -g AStarGhost`

If you want to train the model for 5000 games, and test it for 1000 games, in the medium maze you can run:
- `python pacman.py -n 6000 -x 5000 -l maze3.png -g AStarGhost`

There is also the possibility to load saved models. To do so, you have to edit the "param"
portion of the code in the `pacmanDQN_Agents.py` file. There are some commented examples that you can
use. You can find the saved models in the "saves" folder.

Once the program is running, you will be presented with a black screen and your machine may tell you
it is not responding. This is normal, the program is training in the background and you can see the progress
in the terminal (every 100 games, the program will print the score for that specifc game).

Once the training is done, you will be presented with a similar screen to the one in the 1-player version
and you will see Pac-Man playing the game by himself!
(Keep in mind some GUI debugging features are not available in this version)

## Maze Creation
To create your own maze, just edit an image with any image editor of your choice. It must be a 32x32 pixel image where each pixel represents a tile in the maze. Once you are done editing, load the maze by placing its name in the command paramaters (see above for examples). Here are the possible tiles with its RGB values.

- Empty Space: (0,0,0)
- Pac-Man: (0,0,255)
- Pellet: (255,255,0)
- Power Pellet: (0,255,0)
- Ghost House*: (255,0,0)
- Ghost**: (255,0,255)
- Wall: Any other color

\* Ghost houses ocupy 8x5 tiles with the red tile being its top left corner. When spawned, ghost houses will replace any tiles that would ocupy their space. Ghost houses spawn all 4 classic ghosts like the original game, whom will return to the same ghost house when eaten. 

\** "Homeless" ghosts will return to their spawning position when eaten (keep in mind ghost houses already spawn their own ghosts).

## Credits
- The original Pac-Man game.
- J. Pittman. "The Pacman Dossier" [Online]. https://pacman.holenet.info/
- A. Zhang (alzh9000). ”Pacman DQN” [source code].
https://github.com/alzh9000/PacmanDQN
- Tycho van der Ouderaa (tychovdo). ”Pacman DQN” [source code].
https://github.com/tychovdo/PacmanDQN
- Tejas Kulkarni (mrkulk). ”deepQN Tensorflow” [source code]
https://github.com/mrkulk/deepQN tensorflow
- UC Berkeley. ”AI Materials” [Online] http://ai.berkeley.edu
