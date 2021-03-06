from setuptools import find_packages, setup

setup(
    name='solarviewer',
    version='0.1',
    description='Viewer application for solar physics',
    author='Robert Jarolim',
    packages=find_packages(),
    provides=find_packages(),
    install_requires=['sunpy>=1.0.3', 'PyQt5>=5.10', 'pywavelets', 'scikit-image', 'radiospectra>=0.1.2',
                      'ndcube>=1.0'],
    python_requires='>=3',
    package_data={'solarviewer.resource': ['*.png', '*.txt'], 'solarviewer.resource.vso': ['*.pkl']},
    entry_points={
        'gui_scripts': ['solarviewer=solarviewer.main:main'],
    }
)
