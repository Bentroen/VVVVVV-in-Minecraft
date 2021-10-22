# VVVVVV in Minecraft

A 1:1 recreation of VVVVVV, the acclaimed platform-puzzle game, in vanilla Minecraft.

## Overview

This project aims to be an accurate recreation of [VVVVVV](https://thelettervsixtim.es/) in vanilla Minecraft using data packs and resource packs. It uses the [beet](https://github.com/mcbeet/beet/) Python library to generate Minecraft functions/assets based on code that's ported from [the game's source](https://github.com/TerryCavanagh/VVVVVV/).

I originally started this project back in 2019, and actually went pretty far into the game's logic ([GIF](https://gfycat.com/fearlessblondhatchetfish)). However, I made a poor design decision at the start, which was to place all rooms in a flat "plane" that was thousands of blocks wide. This meant that all sorts of chunk loading issues would occur when moving across rooms, which were pretty disruptive to the immersive experience I wanted to achieve.

![World map](https://i.imgur.com/KPi0MLi.png)

Not only this, but I was relying solely on observation of recorded game footage, along with a decompilation of the Flash version of the game, which meant not everything could be recreated accurately. Ultimately, I decided the project would have to be started from scratch, and left it on hold for a while.

Two things happened since then:

1. VVVVV's [source code](https://github.com/TerryCavanagh/VVVVVV/) was published, which enabled me to recreate mechanics much more accurately by looking at the source;
2. [beet](https://github.com/mcbeet/beet/) was released, which allowed for a much higher level of control over the integration of code-driven parts into Minecraft data packs and resource packs.

With those two things, I figured it was the perfect time to start over the project!

## Approach

This time, I'm using an approach of hardcoding as much stuff as possible. The idea is to write generators to convert as much of the game's data into a format that's suitable for Minecraft, keeping as much of the game's logic to the generator and _not_ the data pack itself.

For instance, instead of dynamically loading each individual tile for every room like the game does, the code generates static textures containing all the tiles in each room. While this allows for less flexibility (for instance, you can't modify levels on-the-fly with only the data that's exposed to Minecraft), the use of beet allows any change in the source data to be reflected in-game by simply rebuilding the data pack.

Removing this sort of logic from the data pack, making it as simple as possible, can make performance in Minecraft much better, at the cost of having a slightly larger data pack to hold all the precalculated information (it's the old [space-time tradeoff](https://en.wikipedia.org/wiki/Space%E2%80%93time_tradeoff)).

This project is also an attempt at getting familiarized with as many Minecraft file formats as possible. beet, structure files and even GLSL shaders are planned. Some good practices are also being adopted, like type-hinting and [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) (even though I'm not very likely to add CI to this project!)

## Building

1. Make sure you have at least Python 3.9 installed.

2. Clone the project:

   ```shell
   $ git clone https://github.com/Bentroen/VVVVVV-in-Minecraft.git
   ```

3. This project uses [poetry](https://python-poetry.org/) to manage dependencies. Make sure to install it, and run:

   ```shell
   $ poetry install
   ```

4. Clone VVVVVV's repository and place it alongside this repository's folder (not inside it!):

   ```shell
   $ git clone https://github.com/TerryCavanagh/VVVVVV.git
   ```

5. Download the [`data.zip`](https://thelettervsixtim.es/makeandplay/data.zip) file and place that file alongside both folders.

6. Create a 1.17 superflat Minecraft world with 'The Void' preset.

7. Link the project to your newly created world:

   ```shell
   $ beet link VVVVVV-in-Minecraft
   ```

8. Build the project:
   ```shell
   $ beet build
   ```

You're done!

## Contributing

I must admit, this is a crazy project, as much so that I can't even say for sure if I'll ever be able to finish it. However, be assured I still envision being able to play VVVVVV seamlessly in vanilla Minecraft, even if at times it's not a priority project of mine.

That being said, if you are as passionate about both games as I am and want to help this project come closer to a playable state, please open a pull request!
