#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
from typing import Dict
from typing import Union
from typing import Tuple

import qgis.utils
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QLocale
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QMenu
from qgis.PyQt.QtWidgets import QToolBar
from qgis.core import QgsMapLayer
from qgis.core import QgsProject
from qgis.gui import QgisInterface

# noinspection PyUnresolvedReferences
from .resources import *
from .ui.dialogs.settings import SettingsDialog

PLUGIN_NAME = 'gisfire_spread_simulation'


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

        if QSettings().value('locale/overrideFlag', type=bool):
            locale = QSettings().value('locale/userLocale')
        else:
            locale = QLocale.system().name()

        locale_path = os.path.join(
            os.path.dirname(__file__),
            'i18n',
            '{}_{}.qm'.format(PLUGIN_NAME, locale[0:2]))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Initialization of UI references
        self._toolbar_actions: Dict[str, QAction] = dict()
        self._menu_actions: Dict[str, QAction] = dict()
        self._menu: Union[QMenu, None] = None
        self._menu_gisfire: Union[QMenu, None] = None
        self._toolbar: Union[QToolBar, None] = None
        self._dlg: Union[SettingsDialog, None] = None
        # Initialization of GisFIRE data layers
        self._layers: Dict[str, QgsMapLayer] = dict()
        self._core_application = QCoreApplication.instance()

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
        action: QAction = QAction(
            QIcon(':/{}/setup.png'.format(PLUGIN_NAME)),
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
        action: QAction = self._menu.addAction(self.tr('Setup'))
        action.setIcon(QIcon(':/{}/setup.png'.format(PLUGIN_NAME)))
        action.setIconVisibleInMenu(True)
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
        self._menu.setIcon(QIcon(':/{}/spread-simulation.png'.format(PLUGIN_NAME)))
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
        # Initialization
        project: QgsProject = QgsProject()
        project_instance: QgsProject = project.instance()
        self._dlg: SettingsDialog = SettingsDialog(parent=self.iface.mainWindow(), layers=QgsProject.instance().mapLayers())
        # Retrieve project properties
        ignition_layer: Union[QgsMapLayer, None] = None
        ignition_layer_id: str
        ignition_type_ok: bool
        ignition_layer_id, ignition_type_ok = project_instance.readEntry(PLUGIN_NAME, 'ignition_layer_id', '')
        perimeter_layer: Union[QgsMapLayer, None] = None
        perimeter_layer_id: str
        perimeter_type_ok: bool
        perimeter_layer_id, perimeter_type_ok = project_instance.readEntry(PLUGIN_NAME, 'perimeter_layer_id', '')
        land_cover_layer: Union[QgsMapLayer, None] = None
        land_cover_layer_id: str
        land_cover_type_ok: bool
        land_cover_layer_id, land_cover_type_ok = project_instance.readEntry(PLUGIN_NAME, 'land_cover_layer_id', '')
        if ignition_type_ok:
            ignition_layer = project_instance.mapLayer(ignition_layer_id)
        self._dlg.ignition_layer = ignition_layer
        if perimeter_type_ok:
            perimeter_layer = project_instance.mapLayer(perimeter_layer_id)
        self._dlg.perimeter_layer = perimeter_layer
        if land_cover_type_ok:
            land_cover_layer = project_instance.mapLayer(land_cover_layer_id)
        self._dlg.land_cover_layer = land_cover_layer
        result = self._dlg.exec_()
        if result == QDialog.Accepted:
            ignition_layer = self._dlg.ignition_layer
            perimeter_layer = self._dlg.perimeter_layer
            land_cover_layer = self._dlg.land_cover_layer
            project_instance.writeEntry(PLUGIN_NAME, 'ignition_layer_id', ignition_layer.id())
            project_instance.writeEntry(PLUGIN_NAME, 'perimeter_layer_id', perimeter_layer.id())
            project_instance.writeEntry(PLUGIN_NAME, 'land_cover_layer_id', land_cover_layer.id())

    # TODO - IMPROVEMENT: Write properties for the ignition, perimeter, and land_cover layers to deal automatically with
    # TODO - IMPROVEMENT: the layer and the project settings store

