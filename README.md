# terminal-tv

## Abstract

This software converts video files into frames of ascii text that it is then capable of playing in the terminal.

## Requirements

- Python3

Everything else will be taken care of during setup

## Installation

### Basic

1. Clone the repo
2. Enter the folder and run setup.sh
3. Run with example_batch.csv to get an idea of what's happening
4. Convert and play files

### Advanced

1. Clone Repo
2. Modify setup.sh to set the desired media location and other variables
3. Run setup.sh
4. Make a Delimited File (see below)
5. Convert and play files

## Usage

Both the converter and player are capable of being added to your path and run from anywhere

If desired, add bin to your path

### Converter

1. Set up a delimited file (example_batch.csv is provided for you)(More on this below)
2. Double check values
3. Run bin/tv_converter \[delimited_filename\] \[delimiter\]

**NOTES:** Make sure that the video filepath is relative to the batch file. This should also be the same location you run the program from. ALSO, the program is currently only capable of converting .mp4 and .mkv files.

### Player

1. Run bin/tv_player

#### Player Controls

Within the player, there are essentially 2 sections. Whenever a file tree is on the screen, we'll call that the **selector**, and whenever a frame is there, we'll refer to that as the **video screen**.

At all times, **Q** quits the program.

In the **Selector:**

- W --> UP
- S --> DOWN
- Spacebar --> Select

In the **Video Screen:**

- Spacebar --> Play/Pause
- E --> Eject/End video (return to selector)
- D --> Skip forward 30 seconds
- A --> Skip backwards 10 seconds
- W --> (If available) Change to Higher Resolution (Bigger Terminal)
- S --> (If available) Change to Lower Resolution (Smaller Terminal)

The last two will require you having converted a second copy of the video at a different Term_Width to the same episode folder.

## The Delimited File

The file is going to expect 6 pieces of data. The last three can be skipped, and the defaults in .env will be used, but there still need to be 5 delimiters on each line. Please see example_batch.csv for an idea of what I'm talking about. You can add as many lines as desired, which makes it ideal for converting entire seasons of a show.

**Data:**

| Video file | Destination | Episode | Term_Width | FPS | Color_Offset |
| --- | --- | --- | --- | --- | --- |

- Video file: Speaks for itself
- Destination: Folder(s) in Media Drive to store episodes in
- Episode: The name to call the file, no exts
- Term_Width: The number of characters wide the video should end up being
- FPS: The target frames per second to shoot for
- Color_Offset: The program tends to classify a lot of colors as being on the gray spectrum. I that's your thing, cool. If not, raising the color_offset asks the program to give a higher weight to character conversions that add any degree of color rather than just being a shade of gray. I personally like 15 as a starting point.

## Images/Videos/Proof

![test1](https://jormungandr1105.github.io/assets/images/terminal_test1.png)
![test1](https://jormungandr1105.github.io/assets/images/terminal_test2.png)

[Videos](https://youtube.com/playlist?list=PLLkrk54i7avHiKDN3ENUukqMjOVQNE-ZC)

## Additional Notes

This project was designed to run on Linux machines that utilize ANSI sequences. Theoretically, it could also be run on Windows, but the Windows terminal simply doesnt print quickly enough for it to actually be usable.

If you have any problems with the software, add an issue to the repo. Any questions can be sent to my email: maxtmarshall99@gmail.com and I'll do my best to get back to you when I get a free second.
