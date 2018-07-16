# Solar Viewer

This is a Python based viewer application for solar physics.
It features downloading, manipulating and analyzing data. The application is primarily build upon functionalities from SunPy and Matplotlib.

Check out the [wiki](/wiki) page for the full documentation.

Installation
------------
Start by installing PyQt5 and SunPy.

Using anaconda:
```
conda install -c conda-forge sunpy
```
PyQt5 should be already installed in the anaconda distribution, if not use: `conda install pyqt`.
Make sure that the PyQt version is at least 5.10. To ensure that the newest version is installed execute: 'pip install pyqt5 --upgrade'.

Using pip:
``` 
pip install sunpy[all]
pip install pyqt5
```

Next download the project (or clone the repository).
In the project root directory execute:
```
python setup.py install
```

Afterwards the executable can be found in the scripts or bin folder of your Python installation (e.g.: ...\Anaconda3\Scripts\solarviewer.exe).

For additional installation information see:
SunPy: [http://docs.sunpy.org/en/stable/guide/installation/index.html]
PyQt: [http://pyqt.sourceforge.net/Docs/PyQt5/installation.html]

Usage
------------

Start the application either by using the executable in the scripts folder or execute main.py located in the solarviewer directory.
(Note: Mac OS users need to use pythonw to start the GUI from an anaconda distribution.)