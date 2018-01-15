from setuptools import find_packages, setup

setup(
    name='sunpyviewer',
    version='0.1',
    description='The SunPy Graphical User Interface (GUI)',
    author='Robert Jarolim',
    packages=find_packages(),
    provides=find_packages(),
    install_requires=['sunpy==0.8.2', 'wxpython', 'pywavelets', 'scikit-image'],
    python_requires='>=3',
    package_data={'sunpyviewer.resources': ['*.png', '*.txt', '*.pkl']},
    entry_points={
        'console_scripts': ['sunpyviewer = sunpyviewer.main:startApplication'],
    }
)
