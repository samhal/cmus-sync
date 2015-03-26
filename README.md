# cmus-sync
Synchronize your device with a existing cmus playlist.

## Installation
1. Clone the repo.
2. Move cmus-sync to /usr/bin
3. Create a config file called .cmus-syncrc in ~/ which follows the same
template as the one given.
4. Create a empty file called "playlist" in your phone's music folder.
5. The source playlist must follow the same format as the one cmus creates
which is located in ~/.config/cmus.

## Limitations
You can't sync your device with music from more than one library. For
instance, you can't sync music from both ~/Music and ~/mnt/External/Music.


