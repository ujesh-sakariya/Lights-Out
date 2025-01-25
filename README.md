Lights-Out

Lights-Out is a unique game I created for my final coursework project for Intro to Programming 1, for which I received a 1st.

Overview
The aim of the game is for you, the miner, to navigate the maze using the arrow keys to find all the candles on the map. However, you can only see within a certain radius of the miner, and this circle continuously gets smaller until you can no longer see anything. In addition to the time reducing your vision, getting hit by a boulder results in a penalty, causing the radius to become even smaller. Collecting candles increases the vision radius. To advance to the next level, you must collect all the candles before the light closes in on the miner.

Maze Design
The maze is designed using a depth-first search algorithm, which randomly generates a completely new maze design when the game is played.
I used this video to help create the algorithm:
https://youtu.be/Ez7U6jU0q5k?si=8C6YT-ol-sAcR8V1

Features
Leaderboard: Players can see the top 5 scores achieved in the game.
Save and Load: If players want to pause a game session and come back to it later, they can save the game session data and will be provided with a unique key. If this key is entered at the start menu, the player can resume from where they left off.
Boss Key: If, for any reason, you are playing this game when you shouldn't be, you can press the boss key to immediately display a computer screen showing someone working.
Remappable Key Binds: Players can customize the keys to their preferred controls.
Cheat Codes: With the cheat codes 'UJ', 'LEO', 'TV', players can unlock additional features.
Pause: The game can be paused at any time during gameplay by pressing 'p'.
