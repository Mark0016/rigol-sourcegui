# rigol-sourcegui
A GUI application for controlling built-in function generator in oscilloscopes over the network (tested on RIGOL MSO1000Z series)

It can set the parameters of the output channels on a built-in source in an oscilloscope.

EXECUTE gui.py TO RUN ("python3 gui.py" in CLI or just make it executable)

Dependencies:

Python 3 (>=3.1)

PyQt4    (>=4.9)

vxi11    (included in files)

This is a GUI application I threw together as a school project along with rigol-scopegui.
It uses the network to communicate (IPv4).
It was tested on a RIGOL MSO1074Z-S oscilloscope on Debian, Ubuntu and Fedora (should work on any major OS).

rigol-scopegui (for controling the oscilloscope itself):
https://github.com/Mark0016/rigol-scopegui
