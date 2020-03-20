# Growtopia-Chemsynth-Router
This program helps you find the best way to compile a puzzle, but this program does not solve it up to 100%

How to Use
1. Type your current color, ex (RYPGYGGBRY) 10 Colors
2. Type your target color, ex (PPGBYYGRBP) 10 Colors
3. Enter and Follow step by step

How this work

this program uses the tool to make Chemsynth available in the chemsynth_tool file to perform tasks.

chemsynth_point is the key for the program to work as expected. This file does a calculation that we can call good_change 
and bad_change. good_change is blocks that have changed and have the same color as the target. bad_change is old blocks 
before they are changed compared to their color similarity to the target block.

and the big job is in Chemsynth_Router file. this file decides with the bruteforce technique to choose the best tool and 
choose the best block to use by the tool.
