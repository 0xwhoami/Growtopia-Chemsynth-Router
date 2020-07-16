# Growtopia Chemsynth Router
This program helps you find the best way to finish the Chemsynth puzzle in Growtopia game

## How to Use
Type -r [your current color here] [your target color here] (with -a optional for advance).
the list of allowed colors is 
- R = RED
- Y = YELLOW
- G = GREEN
- B = BLUE
- P = PINK
Type -h or --help for more information

## Example
1. -r pygbpgrbgy bbypgrbrpb [enter]
2. -r pygbpgrbgy bbypgrbrpb -a [enter]

## How This Work
This program works by counting points from each tool available for each color box available, then providing a route based on the
largest points gained. Then this program provides a route based on intelligence in using a catalyst whose work is assisted by a
stirrer and a centrifuge. the characteristics of this second step if you see there are parts that are like **reverse** the steps
the goal is to help the performance of the catalyst because in addition to changing the color to the next color in the color list,
but the catalyst has the side effect of changing the same color as color on the current catalyst, therefore we use a stirrer and
centrifuge to help it.

### 1. Step 1
Routing based on the **highest point** of each tool and each item in the tank

### 2. Step 2
**Smart Catalyst** concept. suppose you have color [RYYBP] as domain and [RGYBP] as target. as we can see the color at index 1 or item
2 is not finished. Y should be G. we can catalyst on it, but wait. the right color is Y too, if we doing catalyst both of them will
be changed to G, DAMN!! Stuck?? maybe. So what we have to do? you can change the color if you smart choosing helper tool like stirrer
or centrifuge to help you. Ok let's start step 2 concept.
- CURRENT = [RYYBP], TARGET = [RGYBP]

  - [RYYBP] -> [RYPBY] #stirrer block 4 or index 3
  - [RYPBY] -> [RGPBY] #catalyst block 2 or index 1
  - [RGPBY] -> [RGYBP] #stirrer block 4 or index 3

## How to Improve
To improve the work of this chemsynth router we can develop algorithms from chempoint and functions in main that are used to determine
the best route, optimize the code that is not optimal, fix bugs, improve the quality of the interface, or even by documenting the source
code.

## Last but NOT Least
I opened the source code so that if anyone wants to learn about how the program is, they can see the source code. if you imagine how that
big software can be made, imagine when you eat a super duper big burger, we don't eat it all at once but instead eat it little by little
until we finish eating the big burger. that's how to build software little by little end to become big software. at first I was not sure
but with my efforts I could make this Chemsynth Router program. last but not least realize the software of your dreams, and share with
others.
Thank you for reading this text, and of course using my source to improve your program or play the Growtopia.
Have a nice day!
