# Testing online multiplayer on a single machine

Since (due to the conception specific) python cannot distinguish between active windows launch process should be exactly like this:

1. Start host window and open host. After this, guest waiting page will appear, it does not react on __[0-9]__ key events.
2. Start guest window and connect to host. Note that you should enter address correctly at the first try, because pressing __[Backspace]__ will close host and break the sequence. After this, maze creation waiting page will appear, it does not react on __[0-9]__ key events.
3. Create or load maze. After this, both windows will show it.

Unfortunately, both windows (and hence both players) will react on __[arrows]__ and __[wasd]__. You should trust that trust that only one player is moving from key input and one another is synchronized over network (this may possibly be seen by a small delay in movement, mp player will move approximately one main cycle iteration after local one).