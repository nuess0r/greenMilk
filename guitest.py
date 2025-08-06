#!/usr/bin/env python3
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import os

import gi
import time

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk  # noqa: E402

class guitest:
    def __init__(self):
        # -----------------------------------------------------------------------------
        # Set up Glade GUI
        glade_file = "greenMilk.glade"

        #------------------------------------------------------------------------------
        # Create GUI
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.builder.connect_signals(self)

        window = self.builder.get_object("main")
        window.connect("delete-event", Gtk.main_quit)
        window.show()

    def printText(self, widget):
        print("Hello World!")

if __name__ == '__main__':
    guitest = guitest()
    Gtk.main()
