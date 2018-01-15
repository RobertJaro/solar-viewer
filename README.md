# Solar Viewer

This is the first draft of a python viewer application for solar physics.
It features data downloading and manipulation, primarily using functionalities from sunpy and matplotlib.

Installation
------------

With anaconda installed, simply download this code (or clone the repository).
Execute `python setup.py install` in the project root.
Afterwards the executable can be found in the scripts folder of your python installation(e.g.: ...\Anaconda3\Scripts\sunpyviewer.exe)

If not using anaconda make sure sunpy [http://docs.sunpy.org/en/stable/guide/installation/index.html] is working, then this application should work as well.

This viewer uses wxpython as GUI. Check out this website [https://wiki.wxpython.org/How%20to%20install%20wxPython] for the requirements.
Normally the pip installation during the setup.py install should be sufficient.

Usage
------------

Start the application either by using the executable in the scripts folder or execute main.py in the root directory.