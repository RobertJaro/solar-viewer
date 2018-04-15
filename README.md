# Solar Viewer

This is the first draft of a python viewer application for solar physics.
It features data downloading and manipulation, primarily using functionalities from sunpy and matplotlib.

Installation
------------
Start by installing PyQt5 and SunPy.

Using anconda:
```
conda install -c conda-forge sunpy
```
PyQt5 should be already installed in the anaconda distribution, if not use: `conda install pyqt`

Using pip:
``` 
pip install sunpy[all]
pip install pyqt5
```

Full instructions can be found here: [http://docs.sunpy.org/en/stable/guide/installation/index.html].

Next download this code (or clone the repository).
Execute `python setup.py install` in the project root.
Afterwards the executable can be found in the scripts or bin folder of your python installation(e.g.: ...\Anaconda3\Scripts\solarviewer.exe)

Usage
------------

Start the application either by using the executable in the scripts folder or execute main.py in the root directory.
Mac OS users need to use pythonw to start the GUI from an anaconda distribution.