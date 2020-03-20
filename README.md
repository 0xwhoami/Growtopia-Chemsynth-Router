# Growtopia-Chemsynth-Router
This program helps you find the best way to compile a puzzle, but this program DOES NOT solve it up to 100%

How to Use
1. Type your current color, ex (RYPGYGGBRY) 10 Colors
2. Type your target color, ex (PPGBYYGRBP) 10 Colors
3. Enter and Follow step by step

How This Work
This program uses the tool to make Chemsynth available in the chemsynth_tool file to perform tasks.
chemsynth_point is the key for the program to work as expected. This file does a calculation that we can call good_change 
and bad_change. good_change is blocks that have changed and have the same color as the target. bad_change is old blocks 
before they are changed compared to their color similarity to the target block.
And the big job is in Chemsynth_Router file. This file decides with the bruteforce technique to choose the best tool and 
choose the best block to use by the tool.

How to Improve
Well, the improve is hard to implement. Let me explain the problem.
First I was confused deciding to provide enough color then arranging the puzzle, or arranging the puzzle then providing the color.
If i choose the former, provide enough color then arrange the puzzle, the disadvantage is when providing colors that are 
possible when we arrange it first it turns out easier.
if i choose the latter, the disadvantage is the same, namely when providing color because it can randomize the puzzle that has 
been arranged into a mess.
And many more!

So this is the best choice I have, not implement the "Providing color", and stop at Bruteforce technique.
Thank you for reading this text, and of course using my source to improve your program or play the Growtopia.
Have a nice day!
