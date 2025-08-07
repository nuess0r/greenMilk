#!/usr/bin/env python3
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import os
import re
import signal
import pyliblo3 as liblo
import time

from mididings import *
from mididings import event
from mididings.extra.osc import OSCInterface

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstBase", "1.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Gst, GstBase, GLib, GObject, Gtk  # noqa: E402


class guitest:
    def __init__(self):
        DEBUG = True

        # -----------------------------------------------------------------------------
        # Set up Glade GUI
        glade_file = "greenMilk.glade"

        #------------------------------------------------------------------------------
        # Create GUI
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.builder.connect_signals(self)

        # Create GStreamer bits and bobs

        # Initiate Gstreamer
        Gst.init(None)

        # Some capabilities we want to share between different elements
        commoncaps = Gst.Caps.from_string("video/x-raw,width=1280,height=720,framerate=30/1")

        gstreamer_pipeline = """
                        jackaudiosrc client-name="greenMilk" ! queue ! audioconvert ! tee name=audioin ! \
                        queue ! projectm name=pm1 ! video/x-raw, width=1280, height=720, framerate=30/1 ! videoconvert ! tee name=pm1downscale ! 
                        queue ! m.
                        pm1downscale. ! queue ! videoconvertscale ! video/x-raw, width=480, height=320 ! gtksink name=preview1
                        audioin. ! queue ! projectm name=pm2 ! video/x-raw, width=1280, height=720, framerate=30/1 ! tee name=pm2downscale ! 
                        queue ! glvideomixer name=m ! videoconvert ! gtksink name=screen
                        pm2downscale. ! queue ! videoconvertscale ! video/x-raw, width=480, height=320 ! gtksink name=preview2
        """
        #                        audioin. ! queue ! projectm name=pm2 ! video/x-raw, width=480, height=320, framerate=30/1  !
#                        videoconvert ! gtksink name=preview2
        # GStreamer pipeline
        self.pipeline = Gst.parse_launch(gstreamer_pipeline)

        # Set up a bus to our pipeline to get notified when the video is ready
        self.bus = self.pipeline.get_bus()

        if DEBUG:
            # make DOT file from pipeline
            self.gst_generate_dot(self.pipeline, "greenMilk-pipeline", 1)
    


        # Summon the window and connect the window's close button to quit
        self.mainwindow = self.builder.get_object("main")
        self.mainwindow.connect("delete-event", Gtk.main_quit)


        # Connect the gtksink pipeline elements to the GUI
        # Get the GTK widget from the gtkvideosink and attach it to our placeholder box
        self.builder.get_object("preview1").pack_start(self.pipeline.get_by_name("preview1").props.widget, True, True, 0)
        self.builder.get_object("preview2").pack_start(self.pipeline.get_by_name("preview2").props.widget, True, True, 0)
        self.builder.get_object("screenbox").add(self.pipeline.get_by_name("screen").props.widget)

        # Layout is finished, lets show the windows
        self.mainwindow.show_all()

        # Play!
        self.pipeline.set_state(Gst.State.PLAYING)

    def gst_generate_dot(self, pipeline, name, gst_debug_details):
        try:
            directory = os.environ['GST_DEBUG_DUMP_DOT_DIR']
        except:
            directory = os.path.realpath(os.curdir)

        dotfile = os.path.join(directory, "%s.dot" % name)
        print("Generating DOT image of pipeline '{name}' into '{file}'".format(name=name, file=dotfile))
        Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails(int(gst_debug_details)), name)

    def printText(self, widget):
        print("Hello World!")

    def load_preset1(self, widget):
        
        pm1 = self.pipeline.get_by_name("pm1")
        pm1.set_property("beat-sensitivity", 0.5)
        print("beat-sensitivity!")

    def load_preset2(self, widget):
        
        pm1 = self.pipeline.get_by_name("pm1")
        pm1.set_property("beat-sensitivity", 0.8)
        print("beat-sensitivity!")

    # Workaround to get Ctrl+C to terminate from command line
    # ref: https://bugzilla.gnome.org/show_bug.cgi?id=622084#c12
    signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    try:
        guitest = guitest()
        Gtk.main()
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(1)
