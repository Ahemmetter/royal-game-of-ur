# royal-game-of-ur
Python implementation of the ancient boardgame "Royal Game of Ur" with TKinter

## Introduction

The Royal Game of Ur is one of the oldest board games known to archaeology. Well-conserved remains of boards, along with a description of the game rules have been found in the 1920s in Mesopotamia. Its history can be traced back up to 5000 years ago, and has been played for a large amount of this time. Variations of this game have been known and played in other ancient civilizations, such as the Egyptians and Romans.

![Original game board in the British Museum](https://raw.githubusercontent.com/ahemmetter/royal-game-of-ur/master/rgouoriginal.jpg)

My personal interest in the game was sparked by a video of the curator of the British Museum, Irving Finkel, explaining the concepts and discovery of the game. Since the game has relatively simple rules and setup, I found it a fitting difficulty to try my hands on object-oriented programming and GUI implementation in Python.

![Implementation in Tkinter and Python. Shown is an early game state](https://raw.githubusercontent.com/ahemmetter/royal-game-of-ur/master/rgouscrshot.png)

## Rules

The rules for the Royal Game of Ur are farily straight-forward. Variations exist, but in this program only one ruleset so far is implemented: the British Museum ruleset.

The game board consists of 20 colored squares, arranged three horizontal rows. Each player initially has 7 stones in his color (black or white).

![Starting board](https://raw.githubusercontent.com/ahemmetter/royal-game-of-ur/master/rgouempty.png)

Players take turns throwing marked tetrahedrons (equivalent to throwing dice with changed probability distribution). The possible outcomes are 0, 1, 2, 3 or 4, where 2 is the most probable. Each player moves any stone the designated number of fields along a certain path with the goal of reaching the end and "freeing" the stone. The game ends when one player has managed to get all his 7 stones out of the game before the other player.

A complication is added by two additional rules:
1. The players can kick each other back to the start. For this a stone must hop to a field where a stone of another player is already sitting.
2. The players can throw the dice again, if they land on a red square ("rosette") with their previous move. The red squares are spaced 4 fields apart. This means that the game can be efficiently traversed, if the players only throw 4s.

## Implementation in Python and Tkinter

The game is implemented in Python and Tkinter. Tkinter provides an event loop into which all actions of the game need to be inserted.


## Features

* Stones can be selected by clicking and placed by clicking on an allowed square
* Upon selecting a stone, the available moves are shown on the board
* The game's state is displayed in the status bar ("Black's turn", "Not possible to move there")
* It is possible to select any stone from the pile of unused stones, not only the first one
* The computer's move is delayed by half a second to make the moves more accesible to the user
* Freed stones are displayed in a golden color
* The game's language (interface) can be changed through a preference menu. The available languages so far are English (default), German and Russian. Support for Spanish, French and Esperanto is planned. The strings are stored in a separate file and are imported at the beginning of the program
* The game's language can be changed during the game without affecting the game state
* The winner is displayed as a popup (alert) window
* The game can be restarted and exited with a menu option

## Issues and Future Tasks

* Sometimes there seems to appear an error, where it is not allowed to make any more moves, even though there are possible ones left
* It is not possible to skip a move, if there are no possible moves left (for example all stones are blocked)
* Sometimes it happens that the other player is skipped several times in a row. This might be due to the fact that they throw a 0 each time
* The ruleset should be allowed to be changed (different paths, different meanings of the special fields)
* The colors and general theme could be allowed to be changed
* The game window can be resized, but the canvas itself does not adapt to the window size. This could be made relative to account for resized windows
* The language does not update immediately, but only after the first move
* An icon should be added to be displayed in the taskbar/dock
* The game should be packaged to be used even without a Python installation (exe/dmg)
