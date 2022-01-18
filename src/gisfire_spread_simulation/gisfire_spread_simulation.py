#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QTranslator
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QToolBar
from qgis.PyQt.QtWidgets import QMenu
from qgis.gui import QgisInterface
from qgis.core import QgsMapLayer
import qgis.utils
from qgis.core import QgsSettings
from typing import Dict
from typing import Union

from .resources import *


class GisFIRESpreadSimulation:
    """
    GisFIRE Spread Simulation QGIS plugin implementation

    :type iface: QgisInterface
    :type _toolbar_actions: Dict[str, QAction]
    :type _menu_actions: Dict[str, QAction]
    :type _menu: QMenu
    :type _menu_gisfire: QMenu
    :type _toolbar: QToolBar
    :type _dlg: QDialog
    :type _layers: Dict[str, QgsMapLayer]
    """

    def __init__(self, iface: QgisInterface) -> None:
        """
        Constructor.

        :param iface: An interface instance that will be passed to this class which provides the hook by which you can
        manipulate the QGIS application at run time.
        :type iface: qgis.gui.QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface: QgisInterface = iface

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        plugin_dir = os.path.dirname(__file__)
        locale_path = os.path.join(
            plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)

        # Initialization of UI references
        self._toolbar_actions: Dict[str, QAction] = dict()
        self._menu_actions: Dict[str, QAction] = dict()
        self._menu: Union[QMenu, None] = None
        self._menu_gisfire: Union[QMenu, None] = None
        self._toolbar: Union[QToolBar, None] = None
        self._dlg: Union[QDialog, None] = None
        # Initialization of GisFIRE data layers
        self._layers: Dict[str, QgsMapLayer] = dict()

    # noinspection PyMethodMayBeStatic
    def tr(self, message: str) -> str:
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
        """
        Creates the toolbar buttons that GisFIRE Spread Simulation uses as shortcuts.
        """
        # Setup parameters
        action = QAction(
            QIcon(':/gisfire_spread_simulation/setup.png'),
            self.tr('Setup GisFIRE Spread Simulation'),
            None
        )
        # noinspection PyUnresolvedReferences
        action.triggered.connect(self.__on_setup)
        action.setEnabled(True)
        action.setCheckable(False)
        action.setStatusTip(self.tr('Setup GisFIRE Spread Simulation'))
        action.setWhatsThis(self.tr('Setup GisFIRE Spread Simulation'))
        self._toolbar.addAction(action)
        self._toolbar_actions['setup'] = action
        # Separator
        self._toolbar.addSeparator()
        """# Meteo.cat Download lightnings
        action = QAction(
            QIcon(':/gisfire_lightnings/meteocat-lightnings.png'),
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
            QIcon(':/gisfire_lightnings/clip-lightnings.png'),
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
            QIcon(':/gisfire_lightnings/filter-lightnings.png'),
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
            QIcon(':/gisfire_lightnings/process-lightnings.png'),
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
        """
        Creates the menu entries that allow GisFIRE procedures.
        """
        # Setup parameters
        action = self._menu.addAction(self.tr('Setup'))
        action.setIcon(QIcon(':/gisfire_spread_simulation/setup.png'))
        action.setIconVisibleInMenu(True)
        # noinspection PyUnresolvedReferences
        action.triggered.connect(self.__on_setup)
        self._menu_actions['setup'] = action
        """"# Meteo.cat Download lightnings
        action = self._menu.addAction(self.tr('Download meteo.cat Lightnings'))
        action.setIcon(QIcon(':/gisfire_lightnings/meteocat-lightnings.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onDownloadMeteoCatLightnings)
        self._menu_actions['download-meteocat-lightnings'] = action
        # Clip lightnings
        action = self._menu.addAction(self.tr('Clip lightnings on layer and features'))
        action.setIcon(QIcon(':/gisfire_lightnings/clip-lightnings.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onClipLightnings)
        self._menu_actions['clip-lightnings'] = action
        # Filter lightnings
        action = self._menu.addAction(self.tr('Filter lightnings'))
        action.setIcon(QIcon(':/gisfire_lightnings/filter-lightnings.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onFilterLightnings)
        self._menu_actions['clip-lightnings'] = action
        # Process lightnings
        action = self._menu.addAction(self.tr('Calculate lightnings route'))
        action.setIcon(QIcon(':/gisfire_lightnings/process-lightnings.png'))
        action.setIconVisibleInMenu(True)
        action.triggered.connect(self.onProcessLightnings)
        self._menu_actions['process-lightnings'] = action"""

    def __add_relations(self):
        """
        Creates mutually exclusive relations between toolbar buttons.
        """
        pass

    # noinspection PyPep8Naming
    # noinspection DuplicatedCode
    def initGui(self):
        """
        Initializes the QGIS GUI for the GisFIRE Spread Simulation plugin.
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
        # Create Spread Simulation menu
        self._menu = QMenu(self.tr(u'Spread Simulation'), self._menu_gisfire)
        self._menu.setIcon(QIcon(':/gisfire_spread_simulation/spread-simulation.png'))
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

    # noinspection DuplicatedCode
    def unload(self):
        """
        Removes the plugin menu item and icon from QGIS GUI.
        """
        # Remove toolbar items
        for action in self._toolbar_actions.values():
            # noinspection PyUnresolvedReferences
            action.triggered.disconnect()
            self.iface.removeToolBarIcon(action)
            action.deleteLater()
        # Remove toolbar
        if not (self._toolbar is None):
            self._toolbar.deleteLater()
        # Remove menu items
        for action in self._menu_actions.values():
            # noinspection PyUnresolvedReferences
            action.triggered.disconnect()
            self._menu.removeAction(action)
            action.deleteLater()
        # Remove menu
        if not (self._menu is None):
            self._menu.deleteLater()
        # Remove the menu_gisfire only if I'm the only GisFIRE module installed
        count = 0
        for name in qgis.utils.active_plugins:
            if name.startswith('gisfire'):
                count += 1
        if count == 1:
            if not (self._menu_gisfire is None):
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
