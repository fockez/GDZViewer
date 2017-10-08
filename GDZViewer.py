#!/usr/bin/env python3

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

from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow

class PlayThread( threading.Thread ):
    def __init__( self, canvas ):
        threading.Thread.__init__( self )
        self.canvas = canvas

    def run( self ):
        fitslist = glob.glob( "/Users/fockez/Desktop/118/*.fits" )

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

class GDZViewer( QtWidgets.QMainWindow, Ui_MainWindow ):
    def __init__( self ):
        super( GDZViewer, self ).__init__()
        self.setupUi( self )
        self.mc = MplCanvas( self.verticalFrame )
        self.mpl_toolbar = NavigationToolbar( self.mc, self.verticalFrame )
        self.verticalLayout_3.addWidget( self.mc )
        self.verticalLayout_3.addWidget( self.mpl_toolbar )

    def Play( self ):
        self.t = PlayThread( self.mc )
        self.t.start()
        #img = self.mc.axes.imshow( fits.getdata( "/Users/fockez/Desktop/T150_20161111210140_20001.c.fits" ) )
        #print( type( img ) )
        #self.mc.fig.canvas.draw()

    def Stop( self ):
        print( self.t.is_alive() )

app = QtWidgets.QApplication( sys.argv )
window = GDZViewer()
window.show()
sys.exit( app.exec_() )

