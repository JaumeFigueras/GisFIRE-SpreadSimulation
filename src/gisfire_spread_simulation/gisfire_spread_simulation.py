#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
from typing import Dict
from typing import Union

import qgis.utils
from PyQt5.QtCore import Qt
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QLocale
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtCore import QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QMenu
from qgis.PyQt.QtWidgets import QToolBar
from qgis.core import QgsExpressionContextUtils
from qgis.core import QgsMapLayer
from qgis.core import QgsPoint
from qgis.core import QgsPointXY
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.gui import QgisInterface
from qgis.gui import QgsMapCanvas
from qgis.gui import QgsMapTool
from qgis.gui import QgsMapToolEmitPoint

from .qgis_helper_functions.layer import add_ignition_point
# noinspection PyUnresolvedReferences
from .resources import *
from .ui.dialogs.ignition_datetime import IgnitionDateTimeDialog
from .ui.dialogs.settings import SettingsDialog


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
    """

    VERSION = '0.1'
    PLUGIN_NAME = 'gisfire_spread_simulation'

    def __init__(self, iface: QgisInterface) -> None:
        """
        Constructor.

        :param iface: An interface instance that will be passed to this class which provides the hook by which you can
        manipulate the QGIS application at run time.
        :type iface: qgis.gui.QgisInterface
        """
        # Save reference to the QGIS interface and associated GUI objects
        self._iface: QgisInterface = iface
        self._canvas: Union[QgsMapCanvas, None] = None
        self._pointTool: Union[QgsMapToolEmitPoint, None] = None
        self._previousTool: Union[QgsMapTool, None] = None
        self._translator: Union[QTranslator, None] = None

        if QSettings().value('locale/overrideFlag', type=bool):
            locale = QSettings().value('locale/userLocale')
        else:
            locale_instance = QLocale()
            locale = locale_instance.system().name()

        locale_path = os.path.join(
            os.path.dirname(__file__),
            'i18n',
            '{}_{}.qm'.format(self.PLUGIN_NAME, locale[0:2]))

        if os.path.exists(locale_path):
            self._translator = QTranslator()
            self._translator.load(locale_path)
            QCoreApplication.installTranslator(self._translator)

        # Initialization of plugin UI objects
        self._toolbar_actions: Dict[str, QAction] = dict()
        self._menu_actions: Dict[str, QAction] = dict()
        self._menu: Union[QMenu, None] = None
        self._menu_gisfire: Union[QMenu, None] = None
        self._toolbar: Union[QToolBar, None] = None
        self._dlg: Union[SettingsDialog, IgnitionDateTimeDialog, None] = None
        # Plugin data
        self._ignition_layer: Union[QgsVectorLayer, None] = None
        self._perimeter_layer: Union[QgsVectorLayer, None] = None
        self._land_cover_layer: Union[QgsVectorLayer, None] = None
        # noinspection PyUnresolvedReferences
        self._iface.newProjectCreated.connect(self.__on_new_project)
        project = QgsProject()
        project_instance = project.instance()
        if project_instance is not None:
            # noinspection PyUnresolvedReferences
            project_instance.readProject.connect(self.__on_read_project)

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

    def __add_toolbar_actions(self) -> None:
        """
        Creates the toolbar buttons that GisFIRE Spread Simulation uses as shortcuts.

        :return: Nothing
        :rtype: None
        """
        # Setup parameters
        action: QAction = QAction(
            QIcon(':/{}/setup.png'.format(self.PLUGIN_NAME)),
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
        # Create ignition point
        action: QAction = QAction(
            QIcon(':/{}/new_ignition.png'.format(self.PLUGIN_NAME)),
            self.tr('Create ignition point'),
            None
        )
        # noinspection PyUnresolvedReferences
        action.triggered.connect(self._on_create_ignition_point)
        action.setEnabled(True)
        action.setCheckable(False)
        action.setStatusTip(self.tr('Create ignition point'))
        action.setWhatsThis(self.tr('Create ignition point'))
        self._toolbar.addAction(action)
        self._toolbar_actions['new_ignition'] = action

    def __add_menu_actions(self) -> None:
        """
        Creates the menu entries that allow GisFIRE procedures.

        :return: Nothing
        :rtype: None
        """
        # Setup parameters
        action: QAction = self._menu.addAction(self.tr('Setup'))
        action.setIcon(QIcon(':/{}/setup.png'.format(self.PLUGIN_NAME)))
        action.setIconVisibleInMenu(True)
        # noinspection PyUnresolvedReferences
        action.triggered.connect(self.__on_setup)
        self._menu_actions['setup'] = action
        # Create ignition point
        action: QAction = self._menu.addAction(self.tr('Create ignition point'))
        action.setIcon(QIcon(':/{}/new_ignition.png'.format(self.PLUGIN_NAME)))
        action.setIconVisibleInMenu(True)
        action.setEnabled(True)
        # noinspection PyUnresolvedReferences
        action.triggered.connect(self._on_create_ignition_point)
        self._menu_actions['new_ignition'] = action

    def __enable_menu_entries(self, enable: bool = True) -> None:
        """
        Enable or disable all the GisFIRE Spread Simulation menu entries

        :param enable: True to enable or False to disable menu entries, defaults to True
        :type enable: bool
        :return: Nothing
        :rtype: None
        """
        key: str
        action: QAction
        for key, action in self._menu_actions.items():
            action.setEnabled(enable)

    def __enable_toolbar_buttons(self, enable: bool = True) -> None:
        """
        Enable or disable all the GisFIRE Spread Simulation toolbar buttons

        :param enable: True to enable or False to disable toolbar buttons, defaults to True
        :type enable: bool
        :return: Nothing
        :rtype: None
        """
        key: str
        action: QAction
        for key, action in self._toolbar_actions.items():
            action.setEnabled(enable)

    def __enable_menu_setup(self, enable: bool = True) -> None:
        """
        Enable or disable the GisFIRE Spread Simulation 'Setup' menu entry. This entry is available by default

        :param enable: True to enable or False to disable 'Setup' menu entry, defaults to True
        :type enable: bool
        :return: Nothing
        :rtype: None
        """
        self._menu_actions['setup'].setEnabled(enable)

    def __enable_toolbar_button_setup(self, enable: bool = True) -> None:
        """
        Enable or disable the GisFIRE Spread Simulation 'Setup' toolbar button. This button is available by default

        :param enable: True to enable or False to disable 'Setup' toolbar button, defaults to True
        :type enable: bool
        :return: Nothing
        :rtype: None
        """
        self._toolbar_actions['setup'].setEnabled(enable)

    def __add_relations(self) -> None:
        """
        Creates mutually exclusive relations between toolbar buttons.

        :return: Nothing
        :rtype: None
        """
        pass

    # noinspection PyPep8Naming
    # noinspection DuplicatedCode
    def initGui(self) -> None:
        """
        Initializes the QGIS GUI for the GisFIRE Spread Simulation plugin.

        :return: Nothing
        :rtype: None
        """
        # Set up the menu
        menu_name = self.tr(u'Gis&FIRE')
        parent_menu = self._iface.mainWindow().menuBar()
        # Search if the menu exists (there are other GisFIRE modules installed)
        for action in parent_menu.actions():
            if action.text() == menu_name:
                self._menu_gisfire = action.menu()
        # Create the menu if it does not exist and add it to the current menubar
        if self._menu_gisfire is None:
            self._menu_gisfire = QMenu(menu_name, parent_menu)
            actions = parent_menu.actions()
            if len(actions) > 0:
                self._iface.mainWindow().menuBar().insertMenu(actions[-1], self._menu_gisfire)
            else:
                self._iface.mainWindow().menuBar().addMenu(self._menu_gisfire)
        # Create Spread Simulation menu
        self._menu = QMenu(self.tr(u'Spread Simulation'), self._menu_gisfire)
        self._menu.setIcon(QIcon(':/{}/spread-simulation.png'.format(self.PLUGIN_NAME)))
        self._menu_gisfire.addMenu(self._menu)
        # Set up the toolbar for spread simulation plugin
        self._toolbar = self._iface.addToolBar(u'GisFIRE Spread Simulation')
        self._toolbar.setObjectName(u'GisFIRE Spread Simulation')

        # Add toolbar buttons
        self.__add_toolbar_actions()
        # Add menu entries
        self.__add_menu_actions()
        # Create relations with existing menus and buttons
        self.__add_relations()
        # If there is an open project (that has been already saved) check if it is a GisFIRE project and enable toolbar
        # buttons and menus
        if self.__is_gisfire_spread_simulation_project():
            self.__enable_menu_entries()
            self.__enable_toolbar_buttons()
        else:
            self.__enable_menu_entries(False)
            self.__enable_toolbar_buttons(False)
            self.__enable_menu_setup()
            self.__enable_toolbar_button_setup()

    # noinspection DuplicatedCode
    def unload(self) -> None:
        """
        Removes the plugin menu item and icon from QGIS GUI.

        :return: Nothing
        :rtype: None
        """
        # Remove toolbar items
        for key, action in self._toolbar_actions.items():
            # noinspection PyUnresolvedReferences
            action.triggered.disconnect()
            self._iface.removeToolBarIcon(action)
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
                self._iface.mainWindow().menuBar().removeAction(self._menu_gisfire.menuAction())
                self._menu_gisfire.menuAction().deleteLater()
                self._menu_gisfire.deleteLater()
        # noinspection PyUnresolvedReferences
        self._iface.newProjectCreated.disconnect(self.__on_new_project)
        project = QgsProject()
        project_instance = project.instance()
        if project_instance is not None:
            # noinspection PyUnresolvedReferences
            project_instance.readProject.disconnect(self.__on_read_project)

    @staticmethod
    def __is_gisfire_spread_simulation_project() -> bool:
        """
        Determines if the current project has the properties necessary to run a wildfire spread simulation

        :return: True if the project properties are defined, False otherwise
        :rtype: bool
        """
        project: QgsProject = QgsProject()
        project_instance: QgsProject = project.instance()
        plugin_version: Union[str, None]
        plugin_version_ok: bool
        plugin_version, plugin_version_ok = project_instance.readEntry(GisFIRESpreadSimulation.PLUGIN_NAME, 'version',
                                                                       '')
        return plugin_version_ok and plugin_version is not None and plugin_version != ''

    def __on_setup(self) -> None:
        """
        Slot to lint the menu and toolbar button 'Setup'. Loads a Dialog to ask for the basic properties a wildfire
        simulation needs: Layer for ignition points, land-cover, simulation perimeters. Land-cover and fire models
        equivalencies, etc. It also adds the Plugin version that has been used to create the QGIS project.

        :return: Nothing
        :rtype: None
        """
        # Initialization
        project: QgsProject = QgsProject()
        project_instance: QgsProject = project.instance()
        self._dlg: SettingsDialog = SettingsDialog(parent=self._iface.mainWindow(), layers=QgsProject.instance().
                                                   mapLayers())
        # Retrieve project properties
        plugin_version: Union[str, None]
        plugin_version_ok: bool
        plugin_version, plugin_version_ok = project_instance.readEntry(self.PLUGIN_NAME, 'version', '')
        ignition_layer: Union[QgsMapLayer, None] = None
        ignition_layer_id: str
        ignition_type_ok: bool
        ignition_layer_id, ignition_type_ok = project_instance.readEntry(self.PLUGIN_NAME, 'ignition_layer_id', '')
        perimeter_layer: Union[QgsMapLayer, None] = None
        perimeter_layer_id: str
        perimeter_type_ok: bool
        perimeter_layer_id, perimeter_type_ok = project_instance.readEntry(self.PLUGIN_NAME, 'perimeter_layer_id', '')
        land_cover_layer: Union[QgsMapLayer, None] = None
        land_cover_layer_id: str
        land_cover_type_ok: bool
        land_cover_layer_id, land_cover_type_ok = project_instance.readEntry(self.PLUGIN_NAME, 'land_cover_layer_id',
                                                                             '')
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
            self._ignition_layer = self._dlg.ignition_layer
            self._perimeter_layer = self._dlg.perimeter_layer
            self._land_cover_layer = self._dlg.land_cover_layer
            project_instance.writeEntry(self.PLUGIN_NAME, 'ignition_layer_id', self._ignition_layer.id())
            project_instance.writeEntry(self.PLUGIN_NAME, 'perimeter_layer_id', self._perimeter_layer.id())
            project_instance.writeEntry(self.PLUGIN_NAME, 'land_cover_layer_id', self._land_cover_layer.id())
            if plugin_version is None or plugin_version != self.VERSION:
                project_instance.writeEntry(self.PLUGIN_NAME, 'version', self.VERSION)
            # Updates UI
            self.__enable_menu_entries()
            self.__enable_toolbar_buttons()

    def _on_create_ignition_point_callback(self, point: QgsPointXY, mouse_button: Qt.MouseButton) -> None:
        """
        Displays a dialog box to select the date and time the ignition will start. Updates the project ignition layer
        accordingly

        :param point: Point in map reference where the user has clicked
        :type point: QgsPointXY
        :param mouse_button: Mouse button that the user has clicked with
        :type mouse_button: Qt.MouseButton
        :return: Nothing
        :rtype: None
        """
        # noinspection PyUnresolvedReferences
        self._pointTool.canvasClicked.disconnect(self._on_create_ignition_point_callback)
        if mouse_button == Qt.LeftButton:
            project: QgsProject = QgsProject()
            project_instance: QgsProject = project.instance()
            # Create the dialog in charge of collecting needed data
            self._dlg: IgnitionDateTimeDialog = IgnitionDateTimeDialog(self._iface.mainWindow())
            self._dlg.crs = project_instance.crs().authid()
            self._dlg.point_x = point.x()
            self._dlg.point_y = point.y()
            result: int = self._dlg.exec_()
            if result == QDialog.Accepted:
                add_ignition_point(QgsPoint(point), self._dlg.ignition_datetime, self._ignition_layer)
        canvas = self._iface.mapCanvas()
        canvas.setMapTool(self._previousTool)
        del self._pointTool
        self._previousTool = None
        self._pointTool = None

    def _on_create_ignition_point(self) -> None:
        """
        Displays cross a mouse pointer to click on the map canvas in order to determine an ignition point that will be
        used in the wildfire simulation. After the point is selected a dialog box to set the time when the ignition will
        start is shown. This Dialog is managed by the click callback that is set up in this method

        :return: Nothing
        :rtype: None
        """
        # Store the previous tool in use b the user
        canvas = self._iface.mapCanvas()
        self._previousTool = canvas.mapTool()
        # Set the tool and onClick callback
        self._pointTool = QgsMapToolEmitPoint(canvas)
        # noinspection PyUnresolvedReferences
        self._pointTool.canvasClicked.connect(self._on_create_ignition_point_callback)
        canvas.setMapTool(self._pointTool)

    def __on_read_project(self) -> None:
        """
        Slot connection for the Read Project signal. It checks if the loaded project is a GisFIRE spread simulation
        project and updates the GisFIRE UI accordingly

        :return: Nothing
        :rtype: None
        """

        if self.__is_gisfire_spread_simulation_project():
            # Update UI
            self.__enable_menu_entries()
            self.__enable_toolbar_buttons()
            # Retrieve project properties
            project: QgsProject = QgsProject()
            project_instance: QgsProject = project.instance()
            ignition_layer_id: str
            ignition_type_ok: bool
            ignition_layer_id, ignition_type_ok = project_instance.readEntry(self.PLUGIN_NAME, 'ignition_layer_id', '')
            if ignition_type_ok:
                self._ignition_layer = project_instance.mapLayer(ignition_layer_id)
            perimeter_layer_id: str
            perimeter_type_ok: bool
            perimeter_layer_id, perimeter_type_ok = project_instance.readEntry(self.PLUGIN_NAME, 'perimeter_layer_id',
                                                                               '')
            if perimeter_type_ok:
                self._perimeter_layer = project_instance.mapLayer(perimeter_layer_id)
            land_cover_layer_id: str
            land_cover_type_ok: bool
            land_cover_layer_id, land_cover_type_ok = project_instance.readEntry(self.PLUGIN_NAME,
                                                                                 'land_cover_layer_id',
                                                                                 '')
            if land_cover_type_ok:
                self._land_cover_layer = project_instance.mapLayer(land_cover_layer_id)
        else:
            # Update the UI
            self.__enable_menu_entries(False)
            self.__enable_toolbar_buttons(False)
            self.__enable_menu_setup()
            self.__enable_toolbar_button_setup()
            # Update the project properties
            self._ignition_layer = None
            self._perimeter_layer = None
            self._land_cover_layer = None

    def __on_new_project(self) -> None:
        """
        Updated the available menu and toolbar options when a new project is created. It only allows to click the
        'Setup' option

        :return: Nothing
        :rtype: None
        """
        # Update the UI
        self.__enable_menu_entries(False)
        self.__enable_toolbar_buttons(False)
        self.__enable_menu_setup()
        self.__enable_toolbar_button_setup()
        # Update the project properties
        self._ignition_layer = None
        self._perimeter_layer = None
        self._land_cover_layer = None

    # TODO - IMPROVEMENT: Write properties for the ignition, perimeter, and land_cover layers to deal automatically with
    # TODO - IMPROVEMENT: the layer and the project settings store
