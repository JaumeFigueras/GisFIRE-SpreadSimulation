# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GisFIRESpreadSimulator
                                 A QGIS plugin
 GisFire modude to simulate wildfire spread. It is mainly a FARSITE implementation.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-05-21
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Jaume Figueras
        email                : jaume.figueras@upc.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu
from qgis.utils import active_plugins

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .gis_fire_spread_simulator_dockwidget import GisFIRESpreadSimulatorDockWidget
import os.path

class GisFIRESpreadSimulator:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GisFIRESpreadSimulator_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Initialization of UI references
        self._toolbarActions = dict()
        self._menuActions = dict()
        self._menu = None
        self._menu_gisfire = None
        self._toolbar = None
        self._dockwidget = None
        # Initialization of GisFIRE data layers
        self._layers = {}

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GisFIRESpreadSimulator', message)

    def _addToolbarActions(self):
        """Create the toolbar buttons that GisFIRE uses as shortcuts."""
        # Setup parameters
        action = QAction(QIcon(':/plugins/gis_fire_spread_simulator/convert.png'), self.tr('Convert GisFIRE Projet'), None)
        action.triggered.connect(self.onSetup)
        action.setEnabled(True)
        action.setCheckable(False)
        action.setStatusTip(self.tr('Convert GisFIRE Projet'))
        action.setWhatsThis(self.tr('Convert GisFIRE Projet'))
        self._toolbar.addAction(action)
        self._toolbarActions['convert'] = action
        # Separator
        self._toolbar.addSeparator()

    def _addMenuActions(self):
        """Create the menu entries that allow GisFIRE procedures."""
        # Setup parameters
        action = self._menu.addAction(self.tr('Convert GisFIRE Projet'))
        action.setIcon(QIcon(':/plugins/gis_fire_spread_simulator/convert.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onSetup)
        self._menuActions['setup'] = action

    def _addRelations(self):
        """Create mutually exclusive relations between toolbar buttons."""
        pass

    def initGui(self):
        """Initializes the QGIS GUI for the GisFIRE Lightning plugin."""
        # Setup the menu
        menu_name = self.tr(u'Gis&FIRE')
        parent_menu = self.iface.mainWindow().menuBar()
        # Search if the menu exists (there are other GisFIRE modules installed)
        for action in parent_menu.actions():
            if action.text() == menu_name:
                self._menu_gisfire = action.menu()
        # Create the menu if does not exists and add it to the current menubar
        if self._menu_gisfire is None:
            self._menu_gisfire = QMenu(menu_name, self.iface.mainWindow().menuBar())
            actions = self.iface.mainWindow().menuBar().actions()
            self.iface.mainWindow().menuBar().insertMenu(actions[-1], self._menu_gisfire)
        # Create Lightnings menu
        self._menu = QMenu(self.tr(u'Wildfire Spread Simulator'), self._menu_gisfire)
        self._menu_gisfire.addMenu(self._menu)
        # Setup the toolbar for lightnings plugin
        self._toolbar = self.iface.addToolBar(u'GisFIRE Wildfire Spread Simulator')
        self._toolbar.setObjectName(u'GisFIRE Wildfire Spread Simulator')
        #setup the GisFire pane
        self._dockwidget = None

        # Add toolbar buttons
        self._addToolbarActions()
        # Add menu entries
        self._addMenuActions()
        # Create relations with existing menus and buttons
        self._addRelations()

    #--------------------------------------------------------------------------

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Remove toolbar items
        for action in self._toolbarActions.values():
            action.triggered.disconnect()
            self.iface.removeToolBarIcon(action)
            action.deleteLater()
        # Remove toolbar
        if not(self._toolbar is None):
            self._toolbar.deleteLater()
        # Remove menu items
        for action in self._menuActions.values():
            action.triggered.disconnect()
            self._menu.removeAction(action)
            action.deleteLater()
        # Remove menu
        if not(self._menu is None):
            self._menu.deleteLater()
        # Remove dockwidget
        if self._dockwidget != None:
            self._dockwidget.hide()
            self._dockwidget.deleteLater()
        # Remove the menu_gisfire only if I'm the only GisFIRE module installed
        count = 0
        for name in active_plugins:
            if name.startswith('GisFIRE-'):
                count += 1
        if count == 1:
            if not(self._menu_gisfire is None):
                self.iface.mainWindow().menuBar().removeAction(self._menu_gisfire.menuAction())
                self._menu_gisfire.menuAction().deleteLater()
                self._menu_gisfire.deleteLater()

    #--------------------------------------------------------------------------
