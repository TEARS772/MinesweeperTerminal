This code is a sumo robot simulation made for EAL robotics, programming branch as a beginner.
Mostly overwritten over and over again with different mindsets and ideas as the code became a mess that could be seen in test.txt (the previous version before being edited in real.py)
screen is written in 800width  x  800height
This code features a player, for testing purposes, and a bot with 3 censors (ignore the one at back) being capable of actively tracking the player to push them off the screen without a lose-win situation for easier testing.

Bot's capabilities:
-Censors in each direction actively tracks the player and the EDGE. Upon seeing EDGE in 50 pixels or closer bot is coded to retreat and can see the player in range of 200 pixels
-Bot can turn in 90 degrees. Upon seeing the back, it'll turn once since there is no delay between turns letting it see the player from sides to turn again.
-can push the player and is faster than player (is the reason why shift exists)


Features that were unable to be coded due lack of free time:
-Active turning delays to make it more realistic.
-Motor functions instead of turns. For example: Power the right motor to let it turn left.
-Changes in velocity: slower while searching, faster while retreating and even faster while attacking
-Visible censors, was going to be only AI part but couldnt even ask claude to do that yet ç-ç


W, A, S, D for movement and LShift for sprint

!NOTE!: Yaman abi bunları yazamadım diye beni asma please--
