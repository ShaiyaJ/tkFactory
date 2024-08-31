# Tinker factory
Tinker factory is a game that I made in response to a challenge that I came up with to use Python and Tkinter to make a tile-based game. Originally the restriction was to not use the canvas widget, but it became apparent that I would have to make use of this widget in order to achieve acceptable framerates.

I completed the programming for the project in a total of 14 days and the levels in 2. These 16 days were spread over the course of a month and a half. Overall, I'm impressed that I managed to finish a game in this amount of time, however I do feel that the code is lacking in many areas for many reasons. 

For one, tkinter and Python aren't the best tools for making games with. I am also not familiar with the best practices in this library, which only exacerbates the problem.

Secondly, I was rushing quite heavily to get this project done by a self-imposed deadline which was very unrealistic for game development. Especially as this is my first original game.

Finally, I planned very little beforehand, and seldom stuck to that little plan. 

Overall, I learned some pretty valuable lessons from this project. I have more in-depth thoughts written down which I may post somewhere one day. For now, enjoy the messy source code and the somewhat difficult to understand game. It is hard to explain the game, but it's quite a neat puzzle game after you've wrapped your head around it.

The tutorials do an okay job at explaining the game, but I feel it's necessary to include a manual. Treat it like a reference:

## Manual
### Controls
The game is controlled with the mouse for the most part. Buttons navigate through menus, select action modes and determine where actions take place. 

You can also control this game somewhat via the keyboard. You can control the menus using the number keys, and the main gameplay window can be controlled via the keyboard. "d" for destroy mode, "r" to reset and "6789yuiohjklnm,." for build mode (for each building).

You can't place buildings using the keyboard, you still have to click the tile you wish to place on.

### Aim of the game
#### Destroy
Destroy mode sees you attempting to remove every source material block on the map. You can leave harvested materials laying around, but source material blocks must be harvested! 

#### Destroy (timed)
This is the same as regular destroy mode, but you are under a time limit.

#### Collect for HQ
In this mode, you must destroy all source materials and make sure a HQ tile gets them. The only requirement is that there is a HQ on the map and no source or harvested materials. This means that you can build useless buildings to use up resources as a technique to cheese this mode.

### Materials
#### Wood
<img src="./assets/tree.png" style="width: 256; height: 256; image-rendering: pixelated;">
<img src="./assets/h_tree.png" style="width: 256; height: 256; image-rendering: pixelated;">

Mined by a chopping site. 

#### Stone
<img src="./assets/stone.png" style="width: 256; height: 256; image-rendering: pixelated;">
<img src="./assets/h_stone.png" style="width: 256; height: 256; image-rendering: pixelated;">

Mined by a mining site.

#### Metal
<img src="./assets/metal.png" style="width: 256; height: 256; image-rendering: pixelated;">
<img src="./assets/h_metal.png" style="width: 256; height: 256; image-rendering: pixelated;"> 

Mined by a drill.

#### Oil
<img src="./assets/oil.png" style="width: 256; height: 256; image-rendering: pixelated;">
<img src="./assets/h_oil.png" style="width: 256; height: 256; image-rendering: pixelated;"> 

Mined by an oil drill.

#### Water
<img src="./assets/water.png" style="width: 256; height: 256; image-rendering: pixelated;">
<img src="./assets/h_water.png" style="width: 256; height: 256; image-rendering: pixelated;"> 

Not mined. However, it is a requirement in making power.

#### Gold
<img src="./assets/gold.png" style="width: 256; height: 256; image-rendering: pixelated;">

Gold is not a material that you can mine. It was originally intended as that, but it was repurposed as a currency which acts as a penalty for buying materials and destroying buildings. 

Materials and building destruction costs 2 gold each. Destroying the HQ costs 4 gold.

It's possible to generate infinite gold in the game, just place a HQ in such a way that it's range covers the top 3 tiles of any output tile. You'll spend 2 gold on the material and generate 3 gold by the time it's broken!

I was going to fix this, but I thought it would be more fun for players to have a way to get out of tricky situations by abusing this exploit if they deemed it necessary. It isn't even that game-breaking to be honest... 

But it's worth mentioning :).


### Buildings
You may wonder why the building names are in FULL CAPS. In short, this is because I used Python's enum library to distinguish between buildings and I gave the enums full cap variable names. That's right, every building responsible for harvesting materials is secretly the same class. I've changed the order some to be more natural.

The game's tutorials didn't really have the room to get into super "in-depth" specifics about buildings. I just mention that they require materials to build and you can see what materials those are in the info bubble. Here you can see the building stats. Including the unused health, the range and the building requirements. 

Any requirements do appear in a bubble next to a red warning triangle. If you're ever confused on what you need, then the next requirement for the building can be seen in the bubble.

#### CHOPPING SITE
<img src="./assets/chopping_site.png/" style="width: 256; height: 256; image-rendering: pixelated;" />

| | | 
| --- | --- | 
| **Health** | 2 |
| **Range** | 1 |
| **Requirements** | 1 <img src="./assets/h_tree.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_stone.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_metal.png" style="width: 38; height: 38; image-rendering: pixelated;"> | 

There are no operating requirements for this building.

#### MINING SITE
<img src="./assets/mining_site.png/" style="width: 256; height: 256; image-rendering: pixelated;" />

| | | 
| --- | --- | 
| **Health** | 2 |
| **Range** | 1 |
| **Requirements** | 2 <img src="./assets/h_tree.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_stone.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_metal.png" style="width: 38; height: 38; image-rendering: pixelated;"> | 

There are no operating requirements for this building.

#### BOILER
<img src="./assets/boiler.png/" style="width: 256; height: 256; image-rendering: pixelated;" />

| | | 
| --- | --- | 
| **Health** | 4 |
| **Range** | 1 |
| **Requirements** | 2 <img src="./assets/h_tree.png" style="width: 38; height: 38; image-rendering: pixelated;"> 2 <img src="./assets/h_stone.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_metal.png" style="width: 38; height: 38; image-rendering: pixelated;"> | 

This building requires water to run. It produces steam.

#### STEAM GEN
<img src="./assets/generator.png/" style="width: 256; height: 256; image-rendering: pixelated;" />

| | | 
| --- | --- | 
| **Health** | 4 |
| **Range** | 2 |
| **Requirements** | 2 <img src="./assets/h_tree.png" style="width: 38; height: 38; image-rendering: pixelated;"> 2 <img src="./assets/h_stone.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_metal.png" style="width: 38; height: 38; image-rendering: pixelated;"> | 

This building requires steam to run. It produces power.

#### DRILL
<img src="./assets/drill.png/" style="width: 256; height: 256; image-rendering: pixelated;" />

| | | 
| --- | --- | 
| **Health** | 2 |
| **Range** | 1 |
| **Requirements** | 0 <img src="./assets/h_tree.png" style="width: 38; height: 38; image-rendering: pixelated;"> 1 <img src="./assets/h_stone.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_metal.png" style="width: 38; height: 38; image-rendering: pixelated;"> | 

This building requires power to run.

#### OIL DRILL
<img src="./assets/oil_drill.png/" style="width: 256; height: 256; image-rendering: pixelated;" />

| | | 
| --- | --- | 
| **Health** | 4 |
| **Range** | 1 |
| **Requirements** | 0 <img src="./assets/h_tree.png" style="width: 38; height: 38; image-rendering: pixelated;"> 3 <img src="./assets/h_stone.png" style="width: 38; height: 38; image-rendering: pixelated;"> 1 <img src="./assets/h_metal.png" style="width: 38; height: 38; image-rendering: pixelated;"> | 

This building requires power to run.

#### POWER LINE
<img src="./assets/power_line.png/" style="width: 256; height: 256; image-rendering: pixelated;" />

| | | 
| --- | --- | 
| **Health** | 1 |
| **Range** | 2 |
| **Requirements** | 1 <img src="./assets/h_tree.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_stone.png" style="width: 38; height: 38; image-rendering: pixelated;"> 1 <img src="./assets/h_metal.png" style="width: 38; height: 38; image-rendering: pixelated;"> | 

This building requires power to run. It produces (carries) power.

#### CONVEYOR
<img src="./assets/conveyor.png/" style="width: 256; height: 256; image-rendering: pixelated;" />

| | | 
| --- | --- | 
| **Health** | 1 |
| **Range** | Single tile (dependent on rotation) |
| **Requirements** | 0 <img src="./assets/h_tree.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_stone.png" style="width: 38; height: 38; image-rendering: pixelated;"> 0 <img src="./assets/h_metal.png" style="width: 38; height: 38; image-rendering: pixelated;"> | 

This building requires power to run.

### Development information
#### Brief development story (development logs)
I considered adding my actual personal logs in here but I felt they were too incoherent.

I started by writing up a brief plan of the game and boilerplate code (07/18 - 07/21).

I then stopped working on the project as I went away without my laptop. 

I played around with Python's new(-ish) generics, which was super novel to me since I had been using version 3.6.1 up until this point. (07/28)

I was out quite a lot over the next few days, but I still managed to work on both tile logic, saving/loading and basic rendering. If I recall correctly, I got a single tile to render but a lot of logic was being worked on behind the scenes. It was mainly attempting to abstract tile logic in a way that avoided me repeating code multiple times per tile. (08/02). 

By the next day I had rendering pretty much done. Next on the list was UI. I had laid out all the buttons and the state machine that drives the UI, but I still hadn't written any of the functions the buttons were to run. On the same day, I decided to just chill on the development side and make some assets. (08/03).

However, I had to go out again, meaning that I didn't finish making the assets until much later (08/09).

The next day I made rapid progress. Making scaling assets and finishing up rendering completely. However, player input and UI were still not done (08/10).

On (08/25), (08/25), (08/27) and (08/28) I finished all collection-based tiles, conveyors and did all bug fixing related to those tiles. It was also at this time that I decided to remove any offensive enemies or defensive tiles.

On (08/29) I finished all game code. And on (08/30) and (08/31) I designed levels and tweaked parameters in the game. This was also around the time where I gutted the random levels feature.

And that's it. I would take the logs with a grain of salt... As I'm writing it out the pacing seemed all off, but that's also because there was heavy amounts of experimenting in the early stages, especially as the idea of the game was just taking shape. The project was done in about 2 weeks worth of days. But, of course, this was spread over a month and a half.

#### Notes
The code is MIT. I reiterate this fact because I know ways to optimise the code for the game to run on lower end hardware, but I probably will not return to this project to optimise it. So, if anyone does end up reading the manual, I encourage you to play around with the confusing codebase and perhaps even optimise this to run better on your machine. Perhaps you can change TARGET_TICKRATE in order to make the game run faster! (If you have a machine powerful enough). 

Acknowledgements of sub-optimal code can be found in the comments of the project and in this very manual. I'm quite ashamed of the way I've handled some of the things in the code for the sake of "just releasing" the game. But, to be honest, I'm happy that this project hasn't fell prey to my endless tendency to decide to start fresh. Many of my software projects are just sitting on my hard drive half-finished, or deleted. Do you know where they aren't sitting? On my Github page! Completed! 

So at least this is completed and on my Github page.... Despite the fact I really dislike the code.

#### Removed features
I kept a lot of old assets and old features in the code. This was on purpose, just incase anyone is interested in how removed features might have worked.

- Random mode

It was on the last day of development that I removed random mode. In this mode, a randomly generated map was created for you to play on. My intentions with random mode was for players to have something to do after the main levels had been beaten. But, as it turns out, it's actually quite difficult to make a random world beatable. In the end I decided it wasn't worth it - the feature was difficult to write, especially into a codebase which was already quite messy. 

- Jammers

Jammers were going to be towers that blocked your ability to perform certain actions. If a build jammer tower was in range of a building, then it would be destroyed. If a destroy jammer tower was in range of a building, then you couldn't destroy that building. I still feel this would've added another layer of depth to the levels, and it is relatively simple to add. But, sadly, by the time I had this idea it was very late into development and I really wanted to be finished with the project. In retrospect, I feel like I wouldn't have been able to design levels using this feature simply because of the complexity of it. A single level already took me ages to make... I can't imagine trying to factor this into potential solutions.

- Defense buildings and enemies

Defensive buildings and enemies were planned for the game. This added an element of real-time strategy to the game. I removed this feature early on in development though, leaving the semi-pseudo Python source code in the files. I wanted to get the core functionality of the game out of the way (harvesting materials). Once I largely finished that, I didn't really see the point in the game anymore. I somewhat regretted gutting the feature up until I started playtesting the game. The slow tickrate of the game means that reacting in real-time feels like a slog. I don't feel it would've added good gameplay. As a result of this feature though, you'll see a lot of different towers have "health" that is checked every tick. I was intending to use this health mechanic in some way (like having towers decay) up until the end of development. But I never really ended up doing anything with it. *If your computer struggles to run the game you could probably take out some of these useless calls.*. 

#### Creating your own levels
Levels follow a very simple format. In "./levels/levels.json" you can find the JSON format for the game's main levels.

```json
{
    "win": "no_source",
    "starting_gold": 0,
    "tiles": [
        "========",
        "========",
        "====w===",
        "=====W==",
        "=~===M=O",
        "====~===",
        "w=WS~===",
        "~~W===S=",
        "=====ww="
    ],
    "message": "Example level (taken from one of the tutorials)"
}
```

`win` can be one of three possible strings. `"no_source"` is the destroy mode, `"all_hq"` is the collect for HQ mode, and finally a valid positive integer is timed destroy mode. Win conditions are surprisingly extendable, requiring you to edit the `World`'s win condition check every tick.

`starting_gold` is self-explanatory. This is the amount of gold you start with in the level.

`tiles` is an array of strings. Lowercase dictates harvested materials, uppercase dictates source materials. `W`ood, `S`tone, `M`etal and `O`il can be seen in this example. Water is `~`. The equals signs are not necessary, but I add them to make it easier to count tiles by sight rather than manually doing it with the cursor.

`message` is a string that is displayed at the bottom of the screen. This is usually where I put tutorial text or the game-mode being played. But you could also name your levels or credit yourself here.

A good tip for making levels is to not restart the game. You can edit the file and just hit "r" to reload it.

Another tip is to not waste time going through your pack just to hit a level you want to test. Go to "./save.txt" and edit the number in there. 

Make sure to test your intended solution(s) multiple times.  

### Thank you
Thank you for reading the manual and expressing interest in the game. While it may sound like I'm quite annoyed at this project at times, it was still super fun to work on, and it makes me hopeful for future projects.

I also wanted to take the time to thank a good friend of mine, Batheo. Seeing him work on his own games in Godot inspired me to take a break from working on software and utilities to focus on one "big" project. For the past month, I've not scrapped or reworked anything, I've not just made a bunch of small weekend projects. I've actually stuck it out. And seeing his progress on his games was a big part of my ability to do that. A link to his Itch.io page can be found here: https://batheo.itch.io/. 

I intend to make more games. I have more ideas. Although I feel I'll probably choose a more fitting toolchain next time... 