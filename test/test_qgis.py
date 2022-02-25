#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import pytest
import qgis.utils
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsApplication
from qgis.gui import QgisInterface

from src.gisfire_spread_simulation.gisfire_spread_simulation import GisFIRESpreadSimulation


@pytest.mark.parametrize('qgis_locale', [{}, {'locale': 'en_GB'}, {'locale': 'ca_ES'}], indirect=True)
def test_plugin_is_loaded_01(qgis_app: QgsApplication, qgis_locale: QSettings):
    """
    Tests the plugin load procedure programmatically with different locales

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    """
    root_folder: Path = Path(__file__).parent.parent
    path: str = str(root_folder) + '/src'
    qgis.utils.plugin_paths.append(path)
    if path not in sys.path:
        sys.path.insert(0, path)
    qgis.utils.updateAvailablePlugins()
    assert qgis.utils.loadPlugin('gisfire_spread_simulation')
    assert qgis.utils.startPlugin('gisfire_spread_simulation')
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    qgis.utils.unloadPlugin('gisfire_spread_simulation')
    del qgis.utils.plugin_times['gisfire_spread_simulation']
    sys.path.remove(path)
    qgis.utils.plugin_paths.pop()
    qgis.utils.updateAvailablePlugins()


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': [(str(Path(__file__).parent.parent) + '/src')],
    'names': ['gisfire_spread_simulation']
}], indirect=True)
def test_plugin_is_loaded_02(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any]):
    """
    Tests the plugin load fixture with a list of paths and names with just one element

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_plugin_is_loaded_03(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any]):
    """
    Tests the plugin load fixture with a single path and name

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': [(str(Path(__file__).parent.parent.parent) + '/GisFIRE-Lightnings/src'),
              (str(Path(__file__).parent.parent) + '/src')],
    'names': ['gisfire_lightnings', 'gisfire_spread_simulation']
}], indirect=True)
def test_plugin_is_loaded_04(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any]):
    """
    Tests the plugin load fixture with a list of paths and names with two different plugins. I can't find a better way
    to test the creation or deletion of menu entries depending on the existence of other GisFIRE plugins.

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    """
    assert type(qgis.utils.plugins['gisfire_lightnings']).__name__ == 'GisFIRELightnings'
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'


@pytest.mark.parametrize('qgis_locale', [{'locale': 'ca_ES'}], indirect=True)
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': [(str(Path(__file__).parent.parent) + '/src')],
    'names': ['gisfire_spread_simulation']
}], indirect=True)
def test_plugin_is_loaded_05(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any]):
    """
    Tests the correct catalan translation

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    assert plugin._menu_actions['setup'].text() == 'Configuració'


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_plugin_is_loaded_06(qgis_app: QgsApplication, qgis_iface_menu: QgisInterface, qgis_plugin: Dict[str, Any]):
    """
    Tests that the menu is located in the penultimate position of an existing menu

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_iface_menu: QGIS interface fixture with an existing menu bar with menus A, B and C
    :type qgis_iface_menu: QgisInterface
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    """
    actions: List[QAction] = qgis_iface_menu.mainWindow().menuBar().actions()
    assert actions[-2].text() == 'Gis&FIRE'
