from setuptools import find_packages, setup

setup(
    name='sunpyviewer',
    version='0.1',
    description='',
    author='Robert Jarolim',
    packages=find_packages(),
    provides=find_packages(),
    install_requires=['sunpy[all]==0.8.2', 'wxpython==4.0.0b2', 'pywavelets', 'scikit-image'],
    python_requires='>=3',
    package_data={'sunpyviewer.resources': ['*.png', '*.txt', '*.pkl']},
    entry_points={
        'console_scripts': ['sunpyviewer = sunpyviewer.main:startApplication'],
    }
)
