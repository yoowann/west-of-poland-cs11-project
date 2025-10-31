# CS 11 Project of Calim, Camacho, Vinluan
Welcome to Shroom Raider! :>

## Playing the Game
This is a quick tutorial on how to play and run our game.

### How does the Game Work?
TODO explanation on objectives, controls, what the tiles do, etc.

### Cloning the Repository
First, clone the repository using `git clone`.
```bash
git clone https://github.com/yoowann/west-of-poland-cs11-project.git # TODO replace with real link
```

### Running the Game
Navigate to the game's main directory:
```bash
cd west-of-poland-cs11-project/ # TODO replace with real repo name
```
Now, there are many ways to run the game. The command
```bash
python3 shroom_raider.py
```
loads the default stage, which we have designed to help users familiarize themselves with the game. The following commands allow the user to select a stage file to be played:
```bash
python3 shroom_raider.py -f <stage_file>
python3 -m shroom_raider -f <stage_file>
```
Optionally, the user may also specify a sequence of moves and a file on which the final output will be written. The following commands allow the user to do just that:
```bash
python3 shroom_raider.py -f <stage_file> -m <string_of_moves> -o <output_file>
python3 -m shroom_raider -f <stage_file> -m <string_of_moves> -o <output_file>
```
## On Coding
TODO

## Unit Testing
TODO

## Bonus Features
TODO