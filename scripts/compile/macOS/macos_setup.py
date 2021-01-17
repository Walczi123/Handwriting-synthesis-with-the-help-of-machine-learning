"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['src/graphical_interface/graphical_interface.py']
DATA_FILES = ['resources/Bachelor_Thesis.ico']
OPTIONS = {
    'iconfile': 'resources/Bachelor_Thesis.ico',
    'packages': ['pywt', 'skimage', 'tensorflow', 'h5py'],
}

setup(
    app=APP,
    name='Scripturam',
    version='1.0.0',
    description='The handwriting synthesis application.',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)