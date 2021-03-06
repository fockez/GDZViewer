#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import inspect
import re, sys
import os
if hasattr( sys, "frozen" ):
    sys.path.insert( -1, os.path.join( os.path.dirname( sys.executable ), "astropy" ) )
    old_getabsfile = inspect.getabsfile
    def inspect_getabsfile_wrapper( *args, **kwargs ):
        path = old_getabsfile( *args, **kwargs )
        last_part = re.sub( "(.*?yportsa).*", r"\1", path[::-1] )[::-1]
        if os.path.splitext( last_part )[1] == '.py':
            last_part = os.path.splitext( last_part )[0] + '.pyc'
        return os.path.join( os.path.dirname( sys.executable ), last_part ).lower()
    inspect.getabsfile = inspect_getabsfile_wrapper

import matplotlib
matplotlib.use( "Qt5Agg" )
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from astropy.io import fits
from astropy.visualization import ( ZScaleInterval, ImageNormalize, LinearStretch )
import numpy as np

import time
import glob
import sys
import threading
import configparser

from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow
from manframe import Ui_Frame

conf = configparser.ConfigParser()
conf.read( 'defaults.conf' )

class PlayThread( threading.Thread ):
    def __init__( self, canvas ):
        threading.Thread.__init__( self )
        self.canvas = canvas

    def run( self ):
        fitslist = glob.glob( r"D:\tmp\20160614\118-nf\*.fits" )

        for f in fitslist:
            t = time.time()
            data = fits.getdata( f )
            norm = ImageNormalize( data, interval = ZScaleInterval(), stretch = LinearStretch() )
            self.canvas.img.set_data( data )
            self.canvas.img.set_norm( norm )
            self.canvas.axes.draw_artist( self.canvas.img )
            self.canvas.fig.canvas.update()
            self.canvas.fig.canvas.flush_events()
            print( time.time() - t )

class MplCanvas( FigureCanvas ):
    def __init__( self, parent = None ):
        self.fig = Figure( figsize = ( 5, 5 ), dpi = 100, tight_layout = True )
        self.fig.gca().set_aspect( 'equal', adjustable = 'box' )
        self.axes = self.fig.add_subplot( 111 )
        self.axes.axis( 'off' )

        FigureCanvas.__init__( self, self.fig )
        self.setParent( parent )

        FigureCanvas.setSizePolicy( self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding )
        FigureCanvas.updateGeometry( self )

        self.img = self.axes.imshow( np.zeros( ( 100, 100 ) ), cmap = 'gray', origin = 'lower' )

class TMFrame( QtWidgets.QFrame, Ui_Frame ):
    def __init__( self ):
        super( TMFrame, self ).__init__()
        elf.setupUi( self )

class GDZViewer( QtWidgets.QMainWindow, Ui_MainWindow ):
    def __init__( self ):
        super( GDZViewer, self ).__init__()
        self.setupUi( self )
        self.mc = MplCanvas( self.verticalFrame )
        self.mpl_toolbar = NavigationToolbar( self.mc, self.verticalFrame )
        self.verticalLayout_3.addWidget( self.mc )
        self.verticalLayout_3.addWidget( self.mpl_toolbar )

        button_names = []
        self.hosts = {}
        self.mainpaths = {}
        for key in conf['BUTTONS']: button_names.append( key )
        button_positions = [( j, i ) for j in range( int( len( button_names ) / 4 + 1 ) ) for i in range( 4 ) ]
        for button_position, button_name in zip( button_positions, button_names ):
            button = QtWidgets.QPushButton()
            button.setObjectName( button_name )
            button.setText( button_name[7:] )
            button.clicked.connect( self.Switch_unit )
            self.gridLayout_3.addWidget( button, *button_position )
            self.mainpaths[button_name], self.hosts[button_name] = conf['BUTTONS'][button_name].split('@')

    def Play( self ):
        self.t = PlayThread( self.mc )
        self.t.start()
        #img = self.mc.axes.imshow( fits.getdata( "/Users/fockez/Desktop/T150_20161111210140_20001.c.fits" ) )
        #print( type( img ) )
        #self.mc.fig.canvas.draw()
        #pass

    def Stop( self ):
        #print( self.t.is_alive() )
        pass

    def Switch_unit( self ):
        print( self.sender().objectName() )

    def Tel_Management( self ):
        self.tmframe = TMFrame()
        self.tmframe.show()

app = QtWidgets.QApplication( sys.argv )
window = GDZViewer()
window.show()
sys.exit( app.exec_() )

