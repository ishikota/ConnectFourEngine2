# ConnectFourEngine2
Improved ConnectFour engine with fast algorithms.
=============================
This is a free ConnectFour engine written in Python.  
This engine implmented bitboard and move ordering algorithm.

But **this engine is in progress**, completed version is [here](https://github.com/ishikota/ConnectFourEngine "Connect Four Engine").

You can play with two kinds of computer programs,  
1. MiniMax - use MiniMax algorithm with Alpha-Beta Pruning and Move Ordering.  
2. UCT MCTS - use MonteCarloTreeSearch algorithm with UCT algorithm.  

Set up and Run script
--------
First, download ConnectFour project file and change dicectory to ConnectFour/src/ui.
Here, we assume that you cloned ConnectFour project to your HOME directory.
Then run vs.py script.  
**Do not forget to change you directory to `ConnectFour/src/ui` before run script. (It will cause some error.)**  
```
cd $HOME/ConnectFour/src/ui
python vs.py
```

Game settings 
--------
First you will be asked that first player is human(you) or computer.
```$
> FIRST PLAYER IS ...
	1: HUMAN
	2: COMPUTER
```
If you choose 2(COMPUTER) then choose computer algorithm.
```
> WHAT STRATEGY DOES COMPUTER USE ?
	1: MiniMax (IterativeDeepening)
	2: Flat MonteCarloTreeSearch
```
Next, set computer thinking time.
You would be asked like below, set computer thinking time.
```
> INPUT THINKING TIME OF COMPUTER PLAYER (UNIT IS SECOND) ...
```
If you input 3, then computer thinking time is set to 3 seconds

Start ConnectFour !!
--------

Current board state will be displayed in each turn.  
```
   - - - - X - - 
   - - - - O - - 
   - - - - O - - 
   - - - O X - - 
   - X - X O - - 
   - O X O X - - 
   1 2 3 4 5 6 7 
```
  
Each square state is represented by three character.  
  
1. O : First player  
2. X : Second player  
3. - : Empty square  

You make a move by input the number of column you want to make a move (from 1 to 7) !!  

And if you want to finish the game, input 0 as your input like below.
```
--- TURN [ FIRSTPLAYER (O) ] ---
INPUT > 
0
> ARE YOU SURE TO QUIT THE GAME? (y/n)
y
> FINISH THE GAME
```
Enjoy ConnectFour !!

