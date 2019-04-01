#!/usr/bin/python
# $Id$
u"""
A faithful translation of the classic "Hunt The Wumpus" into Python 3.
"""
from __future__ import absolute_import
__version__ = u'1.0'
__author__ = (u'Lance Finn Helsten <helsten@acm.org>',)
__copyright__ = u"Copyright (C) 2014 Lance Finn Helsten, All rights reserved."
__license__ = u"""
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""
__docformat__ = u"restructuredtext en"

import sys
if sys.version_info < (3,):
    #raise Exception(u"Wumpus requires Python 3.0 or higher.")
    pass
import os
import random
from optparse import OptionParser

PURPOSE = u"""
I originally did a simple translation from BASIC into Python for the fun of
it. I remember this game from when I when I wrote my first program at the
University of Utah "Kids, Turtles, and Computers" class when I was 8 in 1974.

My purpose in making a pythonic version of the game is that I had received
an email from Carl Burch in the Mathematics and Computer Science Department
of Hendrix College where he was using my direct translation in teaching a
course. I felt that a direct translation and a full rewrite would be a usefull
in introductory computer science courses.
"""

MODIFICATIONS = u"""
I have tried to stay as truthful to the original game as possible, but I had
to tinker because if it isn't broke then I haven't played with it enough yet.

The biggest change is from BASIC into Python, using data structures instead
of global variables, and using all of the pythonic features I could
(cf. import this).

I also changed the human interface to be a little more friendly than the
original: mainly so you don't need to have Caps Lock on to play.

If you want the original then I have a BASIC version interspaced with Python
that is exactly like the original at:
    http://www.flyingtitans.com/products/wumpus/wumpus_BASIC.py
"""

INSTRUCTIONS = u"""
Welcome to 'Hunt the Wumpus'.

The Wumpus lives in a cave of 20 rooms. Each room has three tunnels leading
to other rooms: look at a dodecahedron to see how this works (if you don't
know what a dodecahedron is see wikipedia).

Hazards:
Bottomless Pits: Two rooms have pits in them, and if you go there you
    will fall, die, and lose.
Super Bats: Two rooms have super bats. If you go there a bat will grab
    you and take you to a random room: which could cause your problems.
Wumpus: The Wumpus is not bothered by hazards as he has sucker feet and is
    too big for a bat to lift. Usually he is asleep, but if you shoot him
    or walk into his room he will wake up. When he wakes up you have a
    75% chance that he will move, but if he doesn't then he eats you, you
    die, and you lose.

Turns: On each turn you may move or shoot a crooked arrow.
Move: You can move to an adjoining room through a tunnel.
Shoot: You have five arrows to shoot (you run out you lose). Each arrow can
    move through one to five rooms, and you aim by telling the computer which
    rooms to go through. If the arrow cannot go that way it will pick a random
    direction. If the arrow hits the Wumpus you win, but if the arrow hits you
    then you lose.

Warnings: If you are one room from the Wumpus or a Hazard then you will see:
    Wumpus: I smell a Wumpus.
    Bat:    Bats nearby.
    Pit:    I feel a draft.
"""

class WumpusKilled(Exception):
    u"""This will be thrown when a player kills the wumpus."""

class PlayerDeath(Exception):
    u"""This will be thrown when a player dies for any reason."""

class Room(object):
    u"""This is a single room in the dodecahedron cave complex. It knows its
    neighboring caves and if it is a pit, has a wumpus, or bats.

    Properties
    --------
    name
        The name of this cave.
    neighbors
        A 3-tuple of caves the hunter can move into.
    wumpus
        A settable property of where the wumpus is located.
    bats
        This cave has super bats.
    pit
        This cave has a pit.
    """
    def __init__(self, name):
        self.name = name
        self.neighbors = (self, self, self)
        self.wumpus = False
        self.hazard = self.EMPTY

    EMPTY = u'empty'
    WUMPUS = u'wumpus'
    BATS = u'bats'
    PIT = u'pit'
    WARNINGS = {EMPTY:u'',
                WUMPUS:u"I smell a Wumpus.",
                BATS:u"Bats nearby.",
                PIT:u"I feel a draft."}

    @property
    def wumpus(self):
        return self.__wumpus

    @wumpus.setter
    def wumpus(self, value):
        self.__wumpus = value

    @property
    def bats(self):
        return self.hazard == self.BATS

    @bats.setter
    def bats(self, value):
        if value:
            assert self.hazard == self.EMPTY, u"Only an empty room can be given bats."
            self.hazard = self.BATS
        else:
            self.hazard = self.EMPTY

    @property
    def pit(self):
        return self.hazard == self.PIT

    @pit.setter
    def pit(self, value):
        if value:
            assert self.hazard == self.EMPTY, u"Only an empty room can be changed to a pit."
            self.hazard = self.PIT
        else:
            self.hazard = self.EMPTY

    def __len__(self):
        return len(self.neighbors)

    def __getitem__(self, key):
        return self.neighbors[key]

    def __iter__(self):
        return iter(self.neighbors)

    def __str__(self):
        ret = [self.WARNINGS[r.hazard] for r in self.neighbors]
        if [r for r in self.neighbors if r.wumpus]:
            ret.insert(0, self.WARNINGS[self.WUMPUS])
        ret = [u'    ' + r for r in ret if r]
        ret.insert(0, u"You are in room {0}.".format(self.name))
        ret.append(u"Tunnels lead to {0}, {1}, {2}.".format(*[n.name for n in self.neighbors]))
        return os.linesep.join(ret)

    def __repr__(self):
        return u"<Room {0} tunnels:[{1}, {2}, {3}] wumpus:{4} hazard:{5}>".format(
            self.name,
            self.neighbors[0].name, self.neighbors[1].name, self.neighbors[2].name,
            self.wumpus, self.hazard)


class Cave(object):
    u"""This is the cave of twenty rooms in the form of a dodecahedron.

    I would have used a graph system to do the work for me, but I wanted this
    to be a completly stand alone system. I will leave it as an exercise for
    the reader to figure out how to change it.

    Properties
    --------
    rooms
        The list of all the rooms in the cave, with room 1 being at offset 0.
    player
        The room the player currently occupies.
    """
    def __init__(self):
        # Layout the cave complex
        self.__rooms = [Room(i + 1) for i in xrange(0, 20)]
        layout = ((1,4,7),    (0,2,9),   (1,3,11),   (2,4,13),   (0,3,5),
                  (4,6,14),   (5,7,16),  (0,6,8),    (7,9,17),   (1,8,10),
                  (9,11,18),  (2,10,12), (11,13,19), (3,12,14),  (5,13,15),
                  (14,16,19), (6,15,17), (8,16,18),  (10,17,19), (12,15,18))
        for i, l in enumerate(layout):
            self.__rooms[i].neighbors = tuple([self.rooms[i] for i in l])

        # Install the hazards
        self.__init_hazard(u"pit")
        self.__init_hazard(u"pit")
        self.__init_hazard(u"bats")
        self.__init_hazard(u"bats")

        # Place the wumpus
        random.choice(self.rooms).wumpus = True

    def __init_hazard(self, field):
        u"""Initialize a single hazard in a random room."""
        room = random.choice(self.rooms)
        while room.bats or room.pit:
            room = random.choice(self.rooms)
        setattr(room, field, True)

    def placeplayer(self):
        u"""Randomly place a player in the cave where there is no hazard."""
        self.__player = random.choice(self.rooms)
        while self.player.wumpus or self.player.bats or self.player.pit:
            self.__player = random.choice(self.rooms)

    def shoot(self):
        u"""Let the player shoot an arrow.

        Exception
        --------
        WumpusKilled
            The player was able to kill the wumpus.
        PlayerDeath
            The player died a horrible a terrible death by shooting himself.
        """
        arrow = self.player
        last = arrow
        dist = self.__readint(u"No. of Rooms (1-5)?", 1, 5)
        for cnt in xrange(dist):
            to = self.__readcave(u"Room #")
            while to == last:
                print u"Arrows aren't that crooked-try another room."
                to = self.__readcave(u"Room #")

            if to in arrow:
                arrow = to
            else:
                arrow = random.choice(arrow)

            if arrow == self.player:
                raise PlayerDeath(u"Ouch! Arrow got you!")
            elif arrow.wumpus:
                raise WumpusKilled(u"AHA! You got the wumpus!")
        print u"Missed."
        self.__movewumpus()

    def move(self):
        u"""Move the player to another room. Deal with any hazards in the new room.

        Exception
        --------
        PlayerDeath
            The player died a horrible a terrible death which needs to be
            reported.
        """
        room = self.__readcave(u"Where to?")
        if room not in self.player:
            print u"Not Possible."
        else:
            self.__player = room
            self.__move0()

    def __move0(self):
        u"""Check to see if the player is in a room with a hazard, handle the
        hazard, and if the player is moved then recursively check for a new
        hazard.

        **CAUTION:** There is a very small chance that bats drop the player
        in a room with bats, which drop the player in a room with bats, and
        so forth until a stack overflow occurs. I decided not to worry about
        it, but a bat carry counter could be put in so after a number of carries
        a bat room will not allowed to be chosen.

        Exception
        --------
        PlayerDeath
            The player died a horrible a terrible death which needs to be
            reported.
        """
        if self.player.wumpus:
            print u"... OOPS! Bumped a Wumpus!"
            if random.random() < 0.75:
                self.__movewumpus()
            else:
                raise PlayerDeath(u"TSK TSK TSK-Wumpus got you!")
        elif self.player.pit:
            raise PlayerDeath(u"YYYYIIIIEEEE . . . Fell in a pit.")
        elif self.player.bats:
            print u"ZAP-Super Bat Snatch! Elsewhereville for you!"
            self.__player = random.choice(self.rooms)
            self.__move0()

    def __movewumpus(self):
        #Move the mumpus to a neighboring room
        wroom = [r for r in self.rooms if r.wumpus][0]
        wroom.wumpus = False
        mover = random.choice(wroom.neighbors)
        mover.wumpus = True
        if mover == self.player:
            raise PlayerDeath(u"TSK TSK TSK-Wumpus got you!")


    def __readint(self, query, min, max):
        u"""Read an integer in the given range.

        Return
            The intenger in the given range.
        """
        ret = -1
        while ret not in xrange(min, max + 1):
            try:
                ret = raw_input(query + u" ")
                ret = int(ret)
            except ValueError:
                pass
        return ret

    def __readcave(self, query):
        u"""Ask the use which cave.

        Return
            The name of the cave.
        """
        ret = None
        while ret is None:
            try:
                num = self.__readint(query, 1, 20)
                ret = self[num - 1]
            except IndexError:
                pass
        return ret

    @property
    def rooms(self):
        return self.__rooms

    @property
    def player(self):
        return self.__player

    def __getitem__(self, key):
        return self.__rooms[key]

    def __str__(self):
        return os.linesep.join([unicode(r) for r in self.rooms])

    def __repr__(self):
        return u"<Cave {0}>".format([repr(r) for r in self.rooms])


def run(cave):
    try:
        win = False
        arrows = 5
        while arrows > 0:
            print
            print cave.player
            act = raw_input(u"Shoot or Move (S-M)? ")[0].lower()
            if act == u'm':
                cave.move()
            elif act == u's':
                arrows = arrows - 1
                cave.shoot()
        print u"Out of ammo."
        print u"You Lose!"
    except WumpusKilled, win:
        print win
        print u"HEE HEE HEE - The Wumpus'll get you next time!!"
    except PlayerDeath, lose:
        print lose
        print u"HA HA HA-You Lose!"


if __name__ == u"__main__":
    parser = OptionParser(
        description=__doc__,
        version=u'%%prog %s' % (__version__,),
        usage=u'usage: %prog [options]')
    parser.add_option(u'', u'--instructions',
            action=u'store_true', dest=u'instructions', default=False,
            help=u'instructions on how to play.')
    parser.add_option(u'', u'--purpose',
            action=u'store_true', dest=u'purpose', default=False,
            help=u'why I did this.')
    parser.add_option(u'', u'--mods',
            action=u'store_true', dest=u'mods', default=False,
            help=u'modifications from original Hunt the Wumpus.')
    options, args = parser.parse_args()

    if options.instructions:
        print INSTRUCTIONS

    elif options.purpose:
        print PURPOSE
        sys.exit(0)

    elif options.mods:
        print MODIFICATIONS
        sys.exit(0)

    else:
        if raw_input(u"Instructions (Y-N)? ")[0].lower() == u'y':
            print INSTRUCTIONS
        cave = Cave()
        try:
            while True:
                cave.placeplayer()
                run(cave)
                if raw_input(u"Same setup (Y-N)? ")[0].lower() == u'n':
                    cave = Cave()
        except KeyboardInterrupt:
            pass

