# CS 11 Project of Calim, Camacho, Vinluan
Welcome to Shroom Raider! :>

## Playing the Game
This is a quick tutorial on how to play and run our game.

### How does the Game Work?
Welcome to Shroom Raider. Here, you are playing as Laro Craft, and your goal is to navigate forests and collect all the mushrooms in them!

The forest is represented as a grid of tiles and items, and the table below shows the tiles and items you may encounter. Note that if Laro ever steps on a tile containing water, the game ends in a loss.
| Tile | Name | Notes |
| :------- | :------: | -------: |
| 🧑 | Laro Craft  | This is the player you are controlling.  |
| ( ) | Empty Tile  | You can move to any empty tile as long as Laro is orthogonally adjacent to it.  |
| 🌲 | Tree | Without an axe or a flamethrower, you cannot move into trees. |
| 🍄 | Mushroom | Collect all the mushrooms in the stage to win!|
| 🪨| Rock | Rocks can be pushed into empty tiles, paved tiles, and water. Note that multiple rocks cannot be moved at the same time. |
| 🟦 | Water | You lose if you step on water! If a rock is pushed into water, the tile becomes a paved tile. |
| ⬜ | Paved Tile | This is created when a rock is pushed to a tile with water. This tile is like an empty tile—Laro can move to it, and rocks can be pushed on paved tiles. |
|🪓 | Axe | When moving to a tree while holding an axe, the tree is chopped down. Then, the tile becomes empty and the axe is used up, meaning Laro no longer holds the axe afterward. |
|🔥| Flamethrower | When moving to a certain tree while holding a flamethrower, all trees connected to this tree are burned up and their tile become empty. Afterward, the flamethrower is used up. |

While the game is still ongoing, you can keep giving move sequences for Laro to execute. Here are the possible moves you can give:
| Move | Description |
| :------- | :------: |
| W  | Move up.  |
| A  | Move left. |
| S  | Move down. |
| D  | Move right. |
| P  | Pick up the item Laro is currently on. If no item is present on the tile Laro is currently on, nothing happens. |
| !  |  Reset the stage to its original state. |
| E  | Exit the game. |

### Running the Game
First, clone the repository using `git clone`.
```bash
git clone https://github.com/UPD-CS11-251/project-1-shroom-raider-u-philippines-mga-sogo-ni-e-t.git
```
Navigate to the game's main directory:
```bash
cd project-1-shroom-raider-u-philippines-mga-sogo-ni-e-t/
```
Now, there are many ways to run the game. The command
```bash
python3 shroom_raider.py
```
loads the default stage, which we have designed to help users familiarize themselves with the game. The following commands allow the user to select a stage file to be played:
```bash
python3 shroom_raider.py -f <path_to_stage_file>
python3 -m shroom_raider -f <path_to_stage_file>
```
Optionally, the user may also specify a sequence of moves and a file on which the final output will be written. The following commands allow the user to do just that:
```bash
python3 shroom_raider.py -f <path_to_stage_file> -m <string_of_moves_enclosed_in_quotes> -o <path_to_output_file>
python3 -m shroom_raider -f <path_to_stage_file> -m <string_of_moves_enclosed_in_quotes> -o <path_to_output_file>
```
## On Coding

These are our thoughts on how we implemented the project.

We separated the game and testing into components so that understanding and debugging the code would be easier. Separate files were used for displaying the game on the terminal, outputting results to files, and reading and handling unit tests.

When we created the game, we decided to separate it into the following classes:
1. Player
    - This class represents the Player and contains information about the Player's position in the grid and currently held item.
1. Stage
    - This class represents the Stage that the Player is playing. The code for how the Stage is altered depending on the moves of the Player are contained here.
    - Given a sequence of moves, individual moves are performed until an invalid move is found. At this point and beyond, no further moves are performed.
    - Furthermore, given a sequence of moves where the Player either wins or loses at some point in the middle of this sequence, moves after this point are no longer performed.
    - Updates to the grid after a single sequence of moves are done only after the last valid non-reset move.
    - The functionality of the flamethrower item was implemented using iterative depth-first search. This algorithm can find connected components; thus, it is apt for finding and destroying all trees connected to a specific tree.
1. Status
    - This class is an enum with three possible values that represent the current state of the game: `Status.ONGOING`, `Status.WIN`, and `Status.LOSE`.

While the game is ongoing, important information, such as the current state of the grid, any items the Player is standing on, the count of mushrooms the Player has collected, and others, are displayed, and the Player is asked for move sequences as input. When a win or loss state is reached, the final state of the grid is displayed, along with the total number of mushrooms the Player managed to collect.

Unit Testing is implemented with Pytest. Stages and correct outputs are read from a text file, and given various move sequences, the outputs of the program are tested against the correct outputs.


// Details on how you organized the code, how your algorithm works, and how you implemented it.

## On Unit Testing
// A description of your unit tests, how they can be run, why you think they’re reasonably thorough, and how to add new tests.


## Bonus Features
// A description of all the bonus features you’d like to be credited for bonus points.