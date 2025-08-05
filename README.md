# Lens Correction plugin for GStreamer
#####

A GStreamer plugin written in Python to correct lens distortion using the Lenfun database. 

Should be usable with any camera in the lensfun db.

List of supported cameras and lenses: https://lensfun.github.io/lenslist/

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

## Notes



## References

Uses mididings for MIDI receiving: https://das.nasophon.de/mididings/

This script started based two other Python scripts that showed me the basics of
how to process MIDI and create a gStreamer pipeline:
- https://github.com/noedigcode/ArdourSongSwitcher/tree/master
-https://fluendo.com/blog/opencv-to-gstreamer-cs-service/

GStreamer Python discussion channel (Matrix): #python:gstreamer.org

projectM discussion channel (Discord): https://discord.com/channels/737206408482914387/737206408948220057
