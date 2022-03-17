#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import pytest
import pytz
import qgis.utils
import qgis.utils
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QVariant
from pytest_qgis.qgis_bot import QgisBot
from pytestqt.qtbot import QtBot
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QPushButton
from qgis.core import QgsApplication
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsField
from qgis.core import QgsProject
from qgis.core import QgsVectorDataProvider
from qgis.core import QgsVectorLayer
from qgis.gui import QgsMapCanvas

from src.gisfire_spread_simulation.gisfire_spread_simulation import GisFIRESpreadSimulation
from src.gisfire_spread_simulation.ui.dialogs.ignition_datetime import IgnitionDateTimeDialog


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_dialog_01(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                  qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the UI is correctly set up when a new project is created

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    :param qgis_bot: QGIS Bot to automate GUI tests
    :type qgis_bot: QgisBot
    :param qtbot: QT fixture to automate GUI tests
    :type qtbot: QtBot
    :param qgis_new_project: Ensures the project instance is clean
    :type qgis_new_project: None
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    assert plugin._menu_actions['setup'].isEnabled()
    assert not plugin._menu_actions['new_ignition'].isEnabled()
    assert plugin._toolbar_actions['setup'].isEnabled()
    assert not plugin._toolbar_actions['new_ignition'].isEnabled()
    assert plugin._ignition_layer is None
    assert plugin._perimeter_layer is None
    assert plugin._land_cover_layer is None


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_dialog_02(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                  qgis_bot: QgisBot, qtbot: QtBot, non_gisfire_project: None):
    """
    Tests the UI is correctly set up when a project is loaded and is not GisFIRE

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    :param qgis_bot: QGIS Bot to automate GUI tests
    :type qgis_bot: QgisBot
    :param qtbot: QT fixture to automate GUI tests
    :type qtbot: QtBot
    :param non_gisfire_project: Ensures the project instance a custom project without GisFIRE data
    :type non_gisfire_project: None
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    assert plugin._menu_actions['setup'].isEnabled()
    assert not plugin._menu_actions['new_ignition'].isEnabled()
    assert plugin._toolbar_actions['setup'].isEnabled()
    assert not plugin._toolbar_actions['new_ignition'].isEnabled()
    assert plugin._ignition_layer is None
    assert plugin._perimeter_layer is None
    assert plugin._land_cover_layer is None


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_dialog_03(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                  qgis_bot: QgisBot, qtbot: QtBot, gisfire_blank_project: None):
    """
    Tests the UI is correctly set up when a project is loaded and is a GisFIRE project

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    :param qgis_bot: QGIS Bot to automate GUI tests
    :type qgis_bot: QgisBot
    :param qtbot: QT fixture to automate GUI tests
    :type qtbot: QtBot
    :param gisfire_blank_project: Ensures the project instance a custom project with GisFIRE blank data
    :type gisfire_blank_project: None
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    assert plugin._menu_actions['setup'].isEnabled()
    assert plugin._menu_actions['new_ignition'].isEnabled()
    assert plugin._toolbar_actions['setup'].isEnabled()
    assert plugin._toolbar_actions['new_ignition'].isEnabled()
    assert plugin._ignition_layer is not None
    assert plugin._perimeter_layer is not None
    assert plugin._land_cover_layer is not None

