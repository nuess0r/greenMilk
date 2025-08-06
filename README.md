# greenMilk
#####



## Requirements

* Python 3 (Tested with 3.13.3)
* python3-pi (Tested with 3.50.0-4)
* python3-gst-1.0 (Tested with 1.26.1-1)
* pyliblo3 (Tested with  0.16.3)
* mididings (Tested with 20230114)
* BOOST (Tested with 1.88)

## Usage

1. Install the prequisites
```
#Debian Trixie
```
sudo apt-get install gstreamer1.0-plugins-base gstreamer1.0-opencv gstreamer1.0-python3-plugin-loader gstreamer1.0-tools libpython3-dev python3-gi python3-gst-1.0 libboost-python1.88-dev libboost-thread1.88-dev
git clone https://github.com/nuess0r/greenmilk.git
python3 -m venv --system-site-packages .
source bin/activate
pip install pyliblo3 mididings
```

1. Test MIDI controller

```
midireceiver.py
```

2. Show the GUI designed with glade. No function behind, just to test the layout of it and your installation

```
guitest.py
```

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
