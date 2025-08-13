# greenMilk
#####

This is a VJ tool to mix Milkdrop visuals.

It's using projectM, its gstreamer plugin, gstreamer, mididings and GTK3.

Everything is glued together with Python3.

## Warning

This is considered an example, research and/or experimental code.

Some of the underlying projects might be not in the shape yet for such a use.
The UX is a first guess of what might be useful.

## Future plans

At some unknown time in the future it will be necessary to design a software from scratch
with a proper architeture, evaluation what technologies, libaries etc. shall be used etc.

## Contribution

Until then, let's find out, what is actually needed by users, VJs, package maintainers etc.

Pull requests welcome :-)

Feel free to open a Github issue for any idea, wish, feature you have.

Feel free to play around with the GUI, tailor it for your needs, make themes and show it to others.
Hopefully we can at some point discuss then more about workflows, feedback from real world useage. 


## Installation

###  Requirements

* Python 3 (Tested with 3.13.3)
* python3-pi (Tested with 3.50.0-4)
* python3-gst-1.0 (Tested with 1.26.1-1)
* pyliblo3 (Tested with  0.16.3)
* mididings (Tested with 20230114)
* BOOST (Tested with 1.88)

### Debian Trixie

1. Install the prequisites

  sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-opencv gstreamer1.0-python3-plugin-loader gstreamer1.0-tools gstreamer1.0-gtk3 libasound2-dev libpython3-dev python3-gi python>

2. Download greenMilk and set up the Python environment

  git clone https://github.com/nuess0r/greenmilk.git
  python3 -m venv --system-site-packages .
  source bin/activate
  pip install pyliblo3 mididings

## Usage

1. Launch greenMilk

You should see two windows, one with GUI elements and the other for the full screen
projection output.

  ./greenMilk.py

2. Test MIDI controller


 ./midireceiver.py


3. Show the GUI designed with glade.

No function behind, just to test the layout of the GUI and your installation.
Can be handy when you work on in the glade designer.

  ./guitest.py

4. You can generate and view the implemented gstreamer pipleline as PDF

  export GST_DEBUG_DUMP_DOT_DIR=/tmp && ./greenMilk.py
  dot -Tpdf /tmp/greenMilk-pipeline.dot > output.pdf

## Notes



## References

Uses mididings for MIDI receiving: https://das.nasophon.de/mididings/

This script started based three other Python scripts that showed me the basics of
how to process MIDI and create a gStreamer pipeline:
- https://github.com/noedigcode/ArdourSongSwitcher/tree/master
- https://fluendo.com/blog/opencv-to-gstreamer-cs-service/
- https://git.slaskete.net/python-gstreamer-examples/tree

Thanks for the hint to get it working on Wayland:
- https://github.com/otsaloma/gaupol/commit/dee6b6544e6ba2d26f287d46a13a731c48fa1c9f#diff-8eeb9510b240fb19cb27c8d8ff87ae3b367c2570a48e71c4977eed73dc01212d

Also thanks for the Python GUI: [Gtk 3 + Glade] tutorial:
- https://www.youtube.com/watch?v=MLgZ6ngBZF4

GStreamer Python discussion channel (Matrix): #python:gstreamer.org

projectM discussion channel (Discord): https://discord.com/channels/737206408482914387/737206408948220057
