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

        # Set up the pipeline
        #self.pipeline = Gst.Pipeline()

        gstreamer_pipeline = """
                        audiotestsrc ! queue ! audioconvert ! projectm ! video/x-raw, width=640, height=480, framerate=30/1  !
                        videoconvert ! gtksink name=videosink
        """
        # GStreamer pipeline
        self.pipeline = Gst.parse_launch(gstreamer_pipeline)

        # Set up a bus to our pipeline to get notified when the video is ready
        self.bus = self.pipeline.get_bus()
        self.bus.enable_sync_message_emission()
        self.bus.connect("sync-message::element", self.OnSyncElement)

        if DEBUG:
            # make DOT file from pipeline
            self.gst_generate_dot(self.pipeline, "greenMilk-pipeline", 1)
    


        # Summon the window and connect the window's close button to quit
        self.mainwindow = self.builder.get_object("main")
        self.mainwindow.connect("delete-event", Gtk.main_quit)
        self.mainwindow.show_all()


        print(self.pipeline.get_by_name("videosink"))
        print(self.pipeline.get_by_name("videosink").props.widget)
        print(self.builder.get_object("preview1"))
        # Get the GTK widget from the gtkvideosink and attach it to our placeholder box
        self.builder.get_object("preview1").pack_start(self.pipeline.get_by_name("videosink").props.widget, True, True, 0)
        #self.builder.get_object("screen").add(self.pipeline.get_by_name("videosink").props.widget)

        # Play!
        self.pipeline.set_state(Gst.State.PLAYING)

    # When we get a message that video is ready to display, set the
    # correct window id to hook it to our viewport
    def OnSyncElement(self, bus, message):
        if message.get_structure().get_name() == "prepare-window-handle":
            print("prepare-window-handle")
            #message.src.set_window_handle(self.win_id)

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


    # Workaround to get Ctrl+C to terminate from command line
    # ref: https://bugzilla.gnome.org/show_bug.cgi?id=622084#c12
    signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    try:
        #main = main()
        guitest = guitest()
        Gtk.main()
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(1)
