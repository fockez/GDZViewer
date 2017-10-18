import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": [], "includes": ["numpy.core._methods","six","mpl_toolkits.axes_grid"], "excludes": ["Tkinter","_tkinter","tkinter","tcl","tk"]}
#,"tornado","sqlite3","osgeo","cvxopt","IPython","scipy","skimage","sphinx","sphinx_rtd_theme","Cython","h5py","test"

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    #base = "Win32GUI"
    base = "Console"

setup(  name = "GDZViewer",
        version = "0.1",
        description = "GDZ Fits Viewer",
        options = {"build_exe": build_exe_options},
        executables = [Executable("GDZViewer.py", base=base)])
