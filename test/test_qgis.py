import pytest
import qgis.utils
from pathlib import Path
import sys


@pytest.mark.parametrize('qgis_locale', [{}, {'locale': 'EN'}, {'locale': 'CA'}], indirect=True)
def test_plugin_is_loaded_01(qgis_app, qgis_locale):
    """
    Tests the plugin load procedure programmatically with different locales

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    """
    root_folder = Path(__file__).parent.parent
    path = str(root_folder) + '/src'
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
    qgis.utils.plugin_paths.remove(path)
    qgis.utils.updateAvailablePlugins()


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': [(str(Path(__file__).parent.parent) + '/src')],
    'names': ['gisfire_spread_simulation']
}], indirect=True)
def test_plugin_is_loaded_02(qgis_app, qgis_locale, qgis_plugin):
    """
    Tests the plugin load fixture with a list of paths and names with just one element

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: list of object
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_plugin_is_loaded_03(qgis_app, qgis_locale, qgis_plugin):
    """
    Tests the plugin load fixture with a single path and name

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: list of object
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': [(str(Path(__file__).parent.parent.parent) + '/GisFIRE-Lightnings/src'),
              (str(Path(__file__).parent.parent) + '/src')],
    'names': ['gisfire_lightnings', 'gisfire_spread_simulation']
}], indirect=True)
def test_plugin_is_loaded_04(qgis_app, qgis_locale, qgis_plugin):
    """
    Tests the plugin load fixture with a list of paths and names with two different plugins. I can't find a better way
    to test the creation or deletion of menu entries depending on the existence of other GisFIRE plugins.

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: list of object
    """
    assert type(qgis.utils.plugins['gisfire_lightnings']).__name__ == 'GisFIRELightnings'
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
