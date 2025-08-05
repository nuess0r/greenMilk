#!/usr/bin/env python3
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

#==============================================================================
# User edit section
#==============================================================================

# List of songs. Each item in the list is in the form:
# ( songName, marker, listOfTracks )
# e.g. ('The House That Jack Built', 1, [4,5])
#      will start at marker 1 and unmute tracks 4 and 5.
songs = [
    ('Song 1', 0, [2,3] ),
    ('Song 2', 1, [4,5] ),
    ('Song 3', 2, [6,7] ),
    ('Song 4', 3, [8,9] )
]

# Button map. Each item in the list is in the form:
# ( Channel, note, method to execute )
notemap = [
    (16, 2, 'load_left'),       # load 1
    (16, 3, 'load_right'),      # load 2
    (16, 6, 'load_right'),      # browse knob (click)
]

# Control knop map. Each item in the list is in the form:
# ( Channel, data1, method to execute )
ctrlmap = [
    (16, 0, 'browse'),          # browse knob
    (16, 8, 'crossfade'),       # crossfade fader
    (1, 22, 'level_left'),      # Left level knob
    (2, 22, 'level_right'),     # Right level knob
    (1, 9, 'sensitivity_left'), # tempo fader
    (2, 9, 'sensitivity_left'), # tempo fader)
    (16, 1, 'color_left'),      # master level
    (16, 12, 'color_right'),    # cue level
]

# MIDI CC numbers to control songs and playback
cc_next = 34
cc_prev = 33
cc_play = 35
cc_playPause = 36
cc_stop = 37
cc_toCurrentSongStart = 38

# Mididings MIDI backend: 'alsa' or 'jack'
backend='jack'

# Client to autoconnect the input MIDI port to
autoconnect='default'

#==============================================================================
# End of user edit section
#==============================================================================

import pyliblo3 as liblo
import time
from mididings import *
from mididings import event
from mididings.extra.osc import OSCInterface

import gi
import time

gi.require_version("Gst", "1.0")
gi.require_version("GstBase", "1.0")

from gi.repository import Gst, GstBase, GLib, GObject  # noqa: E402

gstreamer_pipeline = """
                audiotestsrc ! queue ! audioconvert ! projectm ! video/x-raw, width=640, height=480, framerate=30/1  !
                videoconvert ! xvimagesink sync=false
"""

# -----------------------------------------------------------------------------
# Set up liblo
t = liblo.Address(3819)
s = liblo.send
# use s(t,'/my/osc/message',arg1,arg2...) to send

# -----------------------------------------------------------------------------
# Build tracks list from range, excluding ignore list
tracks = range(1,3+1)
#for i in ignore:
#    tracks.remove(i)

currentSong = 0

# -----------------------------------------------------------------------------
# Mute specified track. 1=mute, 0=unmute
def ardour_muteTrack(track, mute):
    print('   muteTrack: %d, %d'%(track,mute))

# -----------------------------------------------------------------------------
# Move Ardour playhead to specified marker, where zero is the start and nonzero
# markers must be after the start.
def ardour_gotoMarker(m):
    time.sleep(0.1)

# -----------------------------------------------------------------------------
def ardour_switchSong(s):
    # Mute all tracks in tracks list
    for i in tracks:
        ardour_muteTrack(i,1)
    # For each song:
    song = songs[s]
    marker = song[1]
    trks = song[2]
    # Unmute all song tracks
    for i in trks:
        ardour_muteTrack(i,0)
    # Switch to song marker
    ardour_gotoMarker(marker)

# -----------------------------------------------------------------------------
def ardour_play():
    if ardourversion==4:
        s(t,'/ardour/transport_play')
    elif ardourversion==5:
        s(t,'/transport_play')

def ardour_stop():
    if ardourversion==4:
        s(t,'/ardour/transport_stop')
    elif ardourversion==5:
        s(t,'/transport_stop')
    
def ardour_playPause():
    if ardourversion==4:
        s(t,'/ardour/toggle_roll')
    elif ardourversion==5:
        s(t,'/toggle_roll')

# -----------------------------------------------------------------------------
# Mididngs process function

def mididingsProcess(n):
    global currentSong
    if (n.type == CTRL):
        print('CTRL received. channel = %d, ndata1 = %d, ndata2 = %d '%(n.channel, n.data1, n.data2) )
        
        if (n.data2 == 127):
            if n.data1 == cc_next:
                # Next song
                print('CC received: Next song')
                if currentSong < len(songs)-1:
                    currentSong += 1
                # Switch to next song in Ardour
                print('   Switching to song %d in Ardour'%currentSong)
                ardour_switchSong(currentSong)
                # Return program event to switch Mididings scene
                print('   Switching to scene %d'%(currentSong+1))
                return  event.ProgramEvent(1,1,currentSong+1)
            
            elif n.data1 == cc_prev:
                # Previoius song
                print('CC received: Previous song')
                if currentSong > 0:
                    currentSong -= 1
                # Switch to previous song in Ardour
                print('   Switching to song %d in Ardour'%currentSong)
                ardour_switchSong(currentSong)
                # Return program event to switch Mididings scene
                print('   Switching to scene %d'%(currentSong+1))
                return event.ProgramEvent(1,1,currentSong+1)
            
            elif n.data1 == cc_play:
                # Play
                print('CC received: Play')
                ardour_play()
            
            elif n.data1 == cc_playPause:
                # Play/Pause
                print('CC received: Play/Pause')
                ardour_playPause()
            
            elif n.data1 == cc_stop:
                # Stop
                print('CC received: Stop')
                ardour_stop()
                
            elif n.data1 == cc_toCurrentSongStart:
                # Goto current song start
                print('CC received: to current song start')
                ardour_switchSong(currentSong)
            # end if n.data1
        # end if n.data2

    if (n.type == NOTEON):
        print('NOTEON received. channel = %d, note = %d, velocity = %d'%(n.channel, n.note, n.velocity) )

        if n.note == cc_next:
            # Next song
            print('CC received: Next song')
            if currentSong < len(songs)-1:
                currentSong += 1
            # Switch to next song in Ardour
            print('   Switching to song %d in Ardour'%currentSong)
            ardour_switchSong(currentSong)
            # Return program event to switch Mididings scene
            print('   Switching to scene %d'%(currentSong+1))
            return  event.ProgramEvent(1,1,currentSong+1)
        
        elif n.data1 == cc_prev:
            # Previoius song
            print('CC received: Previous song')
            if currentSong > 0:
                currentSong -= 1
            # Switch to previous song in Ardour
            print('   Switching to song %d in Ardour'%currentSong)
            ardour_switchSong(currentSong)
            # Return program event to switch Mididings scene
            print('   Switching to scene %d'%(currentSong+1))
            return event.ProgramEvent(1,1,currentSong+1)
        
        elif n.data1 == cc_play:
            # Play
            print('CC received: Play')
            ardour_play()
        
        elif n.data1 == cc_playPause:
            # Play/Pause
            print('CC received: Play/Pause')
            ardour_playPause()
        
        elif n.data1 == cc_stop:
            # Stop
            print('CC received: Stop')
            ardour_stop()
            
        elif n.data1 == cc_toCurrentSongStart:
            # Goto current song start
            print('CC received: to current song start')
            ardour_switchSong(currentSong)
            # end if n.data1
        # end if n.data2
            
    elif (n.type == PROGRAM):
        if n.program-1 < len(songs):
            print('PRG received: %d'%n.program)
            currentSong = n.program-1
            # Switch to song in Ardour
            print('   Switching to song %d in Ardour'%currentSong)
            ardour_switchSong(currentSong)
            print('   Switching to scene %d'%(currentSong+1))
    #end if n.type
    return n

# -----------------------------------------------------------------------------
# Set up the rest of Mididings

hook(OSCInterface()) # For Livedings GUI

# Set up scenes
scenes = {}
# Song format: ('Song Name', 0, [2,3] )
i = 1
for song in songs:
    scenes[i] = Scene(song[0], Pass())
    i += 1

control = Process(mididingsProcess) >> Filter(PROGRAM) >> SceneSwitch()

config(backend=backend,
       client_name='greenMilk',
       in_ports=[('in',autoconnect)],
       out_ports=[])

# -----------------------------------------------------------------------------
# Set up gstreamer
Gst.init(None)
Gst.init_python()

# -----------------------------------------------------------------------------
# Print some info for the user
print('\nArdour Song Switcher\n')
print('Use Livedings if you need a visual indicator')
print('(However, clicking on the Livedings interface will not switch songs)')
print('')
print('\n')

ardour_switchSong(currentSong)


# GStreamer pipeline
pipeline = Gst.parse_launch(gstreamer_pipeline)

# Start processing
start_time = time.time()
pipeline.set_state(Gst.State.PLAYING)
bus = pipeline.get_bus()


# Run mididings
run( scenes=scenes, control=control )

# Wait for the pipeline to finish
msg = bus.timed_pop_filtered(
    Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS
)

if msg:
    t = msg.type
    if t == Gst.MessageType.ERROR:
        err, debug = msg.parse_error()
        print(f"Error: {err}, {debug}")
    elif t == Gst.MessageType.EOS:
        print("Pipeline finished successfully.")

pipeline.set_state(Gst.State.NULL)

# Log total video processing time
total_time = time.time() - start_time
print(f"Total wall-clock processing time for the video: {total_time:.2f} seconds")
