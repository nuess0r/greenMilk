#!/usr/bin/env python3
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

#==============================================================================
# User edit section
#==============================================================================

# Mididings MIDI backend: 'alsa' or 'jack'
backend='alsa'

# Client to autoconnect the input MIDI port to
autoconnect='default'

#==============================================================================
# End of user edit section
#==============================================================================

import time
from mididings import *
from mididings import event

# -----------------------------------------------------------------------------
# Mididngs process function

def mididingsProcess(n):
    if (n.type == CTRL):
        print('CTRL received. channel = %d, ndata1 = %d, ndata2 = %d '%(n.channel, n.data1, n.data2) )
    elif (n.type == NOTEON):
        print('NOTEON received. channel = %d, note = %d, velocity = %d'%(n.channel, n.note, n.velocity) )
    elif (n.type == NOTEOFF):
        print('NOTEOFF received. channel = %d, note = %d, velocity = %d'%(n.channel, n.note, n.velocity) )
    elif (n.type == PROGRAM):
        print('PROGRAM received. channel = %d, program-1 = %d'%(n.channel, n.program) )
    #end if n.type
    return n

# -----------------------------------------------------------------------------
# Set up the rest of Mididings

scenes = {
        1:  Scene("Receiver only",
                  Pass()
            )
}

control = Process(mididingsProcess) >> Filter(PROGRAM) >> SceneSwitch()

config(backend=backend,
       client_name='midiReceiver',
       in_ports=[('in',autoconnect)])

# -----------------------------------------------------------------------------
# Print some info for the user
print('\nMIDI receiver\n')
print('Shows incomming MIDI messages in the console')
print('')
print('\n')

# Run mididings
run( scenes=scenes, control=control )
