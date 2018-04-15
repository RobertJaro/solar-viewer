# Solar Viewer

This is the first draft of a python viewer application for solar physics.
It features data downloading and manipulation, primarily using functionalities from sunpy and matplotlib.

Installation
------------
Start by installing wxpython and sunpy.

Using anconda:
```
conda install -c conda-forge sunpy
conda install -c anaconda wxpython 
```
Using pip:

Linux user might have to install the prerequirements of wxpython, please see [https://github.com/wxWidgets/Phoenix/blob/master/README.rst#prerequisites] for the full list.
For Windows and Mac the pip installation is sufficient.
``` 
pip install sunpy[all]
pip install wxpython
```

Full instructions can be found here: [http://docs.sunpy.org/en/stable/guide/installation/index.html] and [https://wiki.wxpython.org/How%20to%20install%20wxPython]

Next download this code (or clone the repository).
Execute `python setup.py install` in the project root.
Afterwards the executable can be found in the scripts or bin folder of your python installation(e.g.: ...\Anaconda3\Scripts\solarviewer.exe)

**Note:**

This viewer uses wxpython as GUI. It uses the native GUI of your operating system, so normally the pip installation should be sufficient.
If you encounter difficulties during the installation check the requirements [https://github.com/wxWidgets/Phoenix/blob/master/README.rst#prerequisites].
Linux Users should be aware that the current wxpython version uses gtk3 by default.

Usage
------------

Start the application either by using the executable in the scripts folder or execute main.py in the root directory.
Mac OS users need to use pythonw to start the GUI from an anaconda distribution.