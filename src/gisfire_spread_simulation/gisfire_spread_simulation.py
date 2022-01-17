#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QTranslator
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialog
from PyQt5.QtWidgets import QMenu

import qgis.utils
from qgis.core import QgsSettings


class GisFIRESpreadSimulation:
    """
    GisFIRE Spread Simulation QGIS plugin implementation

    :type iface: QgisInterface
    """
    def __init__(self, iface):
        """
        Constructor.

        :param iface: An interface instance that will be passed to this class which provides the hook by which you can
        manipulate the QGIS application at run time.
        :type iface: qgis.gui.QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        plugin_dir = os.path.dirname(__file__)
        locale_path = os.path.join(
            plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Initialization of UI references
        self._toolbar_actions = dict()
        self._menu_actions = dict()
        self._menu = None
        self._menu_gisfire = None
        self._toolbar = None
        self._dlg = None
        # Initialization of GisFIRE data layers
        self._layers = {}

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """
        Get the translation for a string using Qt translation API.

        :param message: String for translation.
        :type message: str
        :returns: Translated version of message.
        :rtype: str
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GisFIRESpreadSimulation', message)

    def __add_toolbar_actions(self):
        pass
        """
        Creates the toolbar buttons that GisFIRE Spread Simulation uses as shortcuts.
        """
        """# Setup parameters
        action = QAction(
            QIcon(':/plugins/gis_fire_spread_simulation/setup.png'),
            self.tr('Setup GisFIRE Lightnings'),
            None
        )
        action.triggered.connect(self.__on_setup)
        action.setEnabled(True)
        action.setCheckable(False)
        action.setStatusTip(self.tr('Setup GisFIRE Lightnings'))
        action.setWhatsThis(self.tr('Setup GisFIRE Lightnings'))
        self._toolbar.addAction(action)
        self._toolbar_actions['setup'] = action
        # Separator
        self._toolbar.addSeparator()
        # Meteo.cat Download lightnings
        action = QAction(
            QIcon(':/plugins/gisfire_lightnings/meteocat-lightnings.png'),
            self.tr('Download meteo.cat Lightnings'),
            None
        )"""
        """action.triggered.connect(self.onDownloadMeteoCatLightnings)
        action.setEnabled(True)
        action.setCheckable(False)
        action.setStatusTip(self.tr('Download meteo.cat Lightnings'))
        action.setWhatsThis(self.tr('Download meteo.cat Lightnings'))
        self._toolbar.addAction(action)
        self._toolbar_actions['download-meteocat-lightnings'] = action
        # Clip lightnings
        action = QAction(
            QIcon(':/plugins/gisfire_lightnings/clip-lightnings.png'),
            self.tr('Clip lightnings on layer and features'),
            None
        )
        action.triggered.connect(self.onClipLightnings)
        action.setEnabled(True)
        action.setCheckable(False)
        action.setStatusTip(self.tr('Clip lightnings on layer and features'))
        action.setWhatsThis(self.tr('Clip lightnings on layer and features'))
        self._toolbar.addAction(action)
        self._toolbar_actions['clip-lightnings'] = action
        # Clip lightnings
        action = QAction(
            QIcon(':/plugins/gisfire_lightnings/filter-lightnings.png'),
            self.tr('Filter lightnings'),
            None
        )
        action.triggered.connect(self.onFilterLightnings)
        action.setEnabled(True)
        action.setCheckable(False)
        action.setStatusTip(self.tr('Filter lightnings'))
        action.setWhatsThis(self.tr('Filter lightnings'))
        self._toolbar.addAction(action)
        self._toolbar_actions['filter-lightnings'] = action
        # Process lightnings
        action = QAction(
            QIcon(':/plugins/gisfire_lightnings/process-lightnings.png'),
            self.tr('Calculate lightnings route'),
            None
        )
        action.triggered.connect(self.onProcessLightnings)
        action.setEnabled(True)
        action.setCheckable(False)
        action.setStatusTip(self.tr('Calculate lightnings route'))
        action.setWhatsThis(self.tr('Calculate lightnings route'))
        self._toolbar.addAction(action)
        self._toolbar_actions['process-lightnings'] = action"""

    def __add_menu_actions(self):
        pass
        """
        Creates the menu entries that allow GisFIRE procedures.
        """
        """# Setup parameters
        action = self._menu.addAction(self.tr('Setup'))
        action.setIcon(QIcon(':/plugins/gis_fire_spread_simulation/setup.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.__on_setup)
        self._menu_actions['setup'] = action"""
        """"# Meteo.cat Download lightnings
        action = self._menu.addAction(self.tr('Download meteo.cat Lightnings'))
        action.setIcon(QIcon(':/plugins/gisfire_lightnings/meteocat-lightnings.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onDownloadMeteoCatLightnings)
        self._menu_actions['download-meteocat-lightnings'] = action
        # Clip lightnings
        action = self._menu.addAction(self.tr('Clip lightnings on layer and features'))
        action.setIcon(QIcon(':/plugins/gisfire_lightnings/clip-lightnings.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onClipLightnings)
        self._menu_actions['clip-lightnings'] = action
        # Filter lightnings
        action = self._menu.addAction(self.tr('Filter lightnings'))
        action.setIcon(QIcon(':/plugins/gisfire_lightnings/filter-lightnings.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onFilterLightnings)
        self._menu_actions['clip-lightnings'] = action
        # Process lightnings
        action = self._menu.addAction(self.tr('Calculate lightnings route'))
        action.setIcon(QIcon(':/plugins/gisfire_lightnings/process-lightnings.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onProcessLightnings)
        self._menu_actions['process-lightnings'] = action"""

    def __add_relations(self):
        """
        Creates mutually exclusive relations between toolbar buttons.
        """
        pass

    # noinspection PyPep8Naming
    def initGui(self):
        """
        Initializes the QGIS GUI for the GisFIRE Lightning plugin.
        """
        # Set up the menu
        menu_name = self.tr(u'Gis&FIRE')
        parent_menu = self.iface.mainWindow().menuBar()
        # Search if the menu exists (there are other GisFIRE modules installed)
        for action in parent_menu.actions():
            if action.text() == menu_name:
                self._menu_gisfire = action.menu()
        # Create the menu if it does not exist and add it to the current menubar
        if self._menu_gisfire is None:
            self._menu_gisfire = QMenu(menu_name, parent_menu)
            actions = parent_menu.actions()
            if len(actions) > 0:
                self.iface.mainWindow().menuBar().insertMenu(actions[-1], self._menu_gisfire)
            else:
                self.iface.mainWindow().menuBar().addMenu(self._menu_gisfire)
        # Create Lightnings menu
        self._menu = QMenu(self.tr(u'Spread Simulation'), self._menu_gisfire)
        self._menu_gisfire.addMenu(self._menu)
        # Set up the toolbar for spread simulation plugin
        self._toolbar = self.iface.addToolBar(u'GisFIRE Spread Simulation')
        self._toolbar.setObjectName(u'GisFIRE Spread Simulation')

        # Add toolbar buttons
        self.__add_toolbar_actions()
        # Add menu entries
        self.__add_menu_actions()
        # Create relations with existing menus and buttons
        self.__add_relations()

    def unload(self):
        """
        Removes the plugin menu item and icon from QGIS GUI.
        """
        # Remove toolbar items
        for action in self._toolbar_actions.values():
            action.triggered.disconnect()
            self.iface.removeToolBarIcon(action)
            action.deleteLater()
        # Remove toolbar
        if not(self._toolbar is None):
            self._toolbar.deleteLater()
        # Remove menu items
        for action in self._menu_actions.values():
            action.triggered.disconnect()
            self._menu.removeAction(action)
            action.deleteLater()
        # Remove menu
        if not(self._menu is None):
            self._menu.deleteLater()
        # Remove the menu_gisfire only if I'm the only GisFIRE module installed
        count = 0
        for name in qgis.utils.active_plugins:
            if name.startswith('gisfire'):
                count += 1
        if count == 1:
            if not(self._menu_gisfire is None):
                self.iface.mainWindow().menuBar().removeAction(self._menu_gisfire.menuAction())
                self._menu_gisfire.menuAction().deleteLater()
                self._menu_gisfire.deleteLater()

    def __on_setup(self):
        pass
        """self._dlg = DlgSettings(self.iface.mainWindow())
        qgs_settings = QgsSettings()
        # Get values and initialize dialog
        self._dlg.meteocat_api_key = qgs_settings.value("gisfire_lightnings/meteocat_api_key", "")
        self._dlg.gisfire_api_url = qgs_settings.value("gisfire_lightnings/gisfire_api_url", "")
        self._dlg.gisfire_api_username = qgs_settings.value("gisfire_lightnings/gisfire_api_username", "")
        self._dlg.gisfire_api_token = qgs_settings.value("gisfire_lightnings/gisfire_api_token", "")
        result = self._dlg.exec_()
        if result == QDialog.Accepted:
            # Store correct values
            qgs_settings.setValue("gisfire_lightnings/meteocat_api_key", self._dlg.meteocat_api_key)
            qgs_settings.setValue("gisfire_lightnings/gisfire_api_url", self._dlg.gisfire_api_url)
            qgs_settings.setValue("gisfire_lightnings/gisfire_api_username", self._dlg.gisfire_api_username)
            qgs_settings.setValue("gisfire_lightnings/gisfire_api_token", self._dlg.gisfire_api_token)
            print(self._dlg.meteocat_api_key)
            print(self._dlg.gisfire_api_url)
            print(self._dlg.gisfire_api_username)
            print(self._dlg.gisfire_api_token)"""

