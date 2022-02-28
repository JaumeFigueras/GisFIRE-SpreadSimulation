#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any
from typing import Dict

import pytest
import qgis.utils
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette
from pytest_qgis.qgis_bot import QgisBot
from pytestqt.qtbot import QtBot
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QPushButton
from qgis.core import QgsApplication
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer

from src.gisfire_spread_simulation.gisfire_spread_simulation import GisFIRESpreadSimulation
from src.gisfire_spread_simulation.ui.dialogs.layer_name import LayerNameDialog
from src.gisfire_spread_simulation.ui.dialogs.settings import SettingsDialog


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_layer_name_dialog_01(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                              qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the layer name dialog is correctly shown with an Ok

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

    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    QgsProject.instance().addMapLayer(vl_a)
    QgsProject.instance().addMapLayer(vl_b)
    QgsProject.instance().addMapLayer(vl_c)

    dialog: LayerNameDialog = LayerNameDialog(layers=QgsProject.instance().mapLayers())
    assert len(dialog._layer_names) == 3
    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    buttons: QDialogButtonBox = dialog._button_box
    button_cancel: QPushButton = buttons.button(QDialogButtonBox.Cancel)
    qtbot.mouseClick(button_cancel, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_layer_name_dialog_02(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                              qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the layer name dialog is correctly shown with an Ok

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

    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    QgsProject.instance().addMapLayer(vl_a)
    QgsProject.instance().addMapLayer(vl_b)
    QgsProject.instance().addMapLayer(vl_c)

    dialog: LayerNameDialog = LayerNameDialog(layers=QgsProject.instance().mapLayers())
    assert len(dialog._layer_names) == 3
    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_layer_name_dialog_03(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                              qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the layer name dialog is correctly shown with an Ok

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

    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    QgsProject.instance().addMapLayer(vl_a)
    QgsProject.instance().addMapLayer(vl_b)
    QgsProject.instance().addMapLayer(vl_c)

    dialog: LayerNameDialog = LayerNameDialog(layers=QgsProject.instance().mapLayers())
    assert len(dialog._layer_names) == 3
    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    assert dialog._lineedit_layer_name.palette().color(QPalette.WindowText) == QColor(dialog._text_color)
    qtbot.keyClicks(dialog._lineedit_layer_name, 'a')
    assert dialog._lineedit_layer_name.palette().color(QPalette.WindowText) == QColor('red')
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(QDialogButtonBox.Ok)
    assert not button_ok.isEnabled()
    qtbot.keyClicks(dialog._lineedit_layer_name, 'f')
    assert dialog._lineedit_layer_name.palette().color(QPalette.WindowText) == QColor(dialog._text_color)
    assert button_ok.isEnabled()
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()
    assert dialog.layer_name == 'af'


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_dialog_01(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                            qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the settings dialog is correctly shown with an Ok

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

    dialog: SettingsDialog = SettingsDialog()
    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    buttons: QDialogButtonBox = dialog._button_box
    button_cancel: QPushButton = buttons.button(qgis.PyQt.QtWidgets.QDialogButtonBox.Cancel)
    qtbot.mouseClick(button_cancel, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_dialog_02(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                            qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the settings dialog is correctly shown with a Cancel

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
    # noinspection DuplicatedCode
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'

    dialog: SettingsDialog = SettingsDialog()
    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(qgis.PyQt.QtWidgets.QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_dialog_03(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                            qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the settings dialog loads correctly the different layers of the project depending on its type and its
    selection

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

    # Create possible vector layers to choose from
    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    QgsProject.instance().addMapLayer(vl_a)
    QgsProject.instance().addMapLayer(vl_b)
    QgsProject.instance().addMapLayer(vl_c)
    vl_d = QgsVectorLayer('Polygon', 'd', 'memory')
    vl_e = QgsVectorLayer('Polygon', 'e', 'memory')
    vl_f = QgsVectorLayer('Polygon', 'f', 'memory')
    vl_g = QgsVectorLayer('Polygon', 'g', 'memory')
    QgsProject.instance().addMapLayer(vl_d)
    QgsProject.instance().addMapLayer(vl_e)
    QgsProject.instance().addMapLayer(vl_f)
    QgsProject.instance().addMapLayer(vl_g)

    dialog: SettingsDialog = SettingsDialog(layers=QgsProject.instance().mapLayers())
    assert dialog._combobox_ignition_layer.count() == 3
    assert dialog._combobox_perimeter_layer.count() == 4
    assert dialog._combobox_land_cover_layer.count() == 4
    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    # Select the different layers in the combobox
    qtbot.keyClicks(dialog._combobox_ignition_layer, 'c')
    qtbot.keyClicks(dialog._combobox_perimeter_layer, 'd')
    qtbot.keyClicks(dialog._combobox_land_cover_layer, 'g')
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(qgis.PyQt.QtWidgets.QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()
    # Get the values
    assert dialog.ignition_layer == vl_c
    assert dialog.perimeter_layer == vl_d
    assert dialog.land_cover_layer == vl_g


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_dialog_04(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                            qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the settings dialog loads correctly the different layers of the project depending on adds to the system a new
    ignition layer

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

    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    QgsProject.instance().addMapLayer(vl_a)
    QgsProject.instance().addMapLayer(vl_b)
    QgsProject.instance().addMapLayer(vl_c)
    vl_d = QgsVectorLayer('Polygon', 'd', 'memory')
    vl_e = QgsVectorLayer('Polygon', 'e', 'memory')
    vl_f = QgsVectorLayer('Polygon', 'f', 'memory')
    vl_g = QgsVectorLayer('Polygon', 'g', 'memory')
    QgsProject.instance().addMapLayer(vl_d)
    QgsProject.instance().addMapLayer(vl_e)
    QgsProject.instance().addMapLayer(vl_f)
    QgsProject.instance().addMapLayer(vl_g)

    dialog: SettingsDialog = SettingsDialog(layers=QgsProject.instance().mapLayers())
    assert dialog._combobox_ignition_layer.count() == 3
    assert dialog._combobox_perimeter_layer.count() == 4
    assert dialog._combobox_land_cover_layer.count() == 4

    def on_timer():
        assert dialog._dlg.isVisible()
        qtbot.keyClicks(dialog._dlg._lineedit_layer_name, 'ignition_new')
        buttons_new_layer: QDialogButtonBox = dialog._dlg._button_box
        button_ok_new_layer: QPushButton = buttons_new_layer.button(qgis.PyQt.QtWidgets.QDialogButtonBox.Ok)
        qtbot.mouseClick(button_ok_new_layer, qgis.QtCore.Qt.LeftButton)
        assert not dialog._dlg.isVisible()

    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    assert len(QgsProject.instance().mapLayers()) == 7
    QTimer.singleShot(100, on_timer)
    qtbot.mouseClick(dialog._button_create_new_ignition_layer, qgis.QtCore.Qt.LeftButton)
    assert len(QgsProject.instance().mapLayers()) == 8
    assert dialog.ignition_layer.name() == 'ignition_new'
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(qgis.PyQt.QtWidgets.QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_dialog_05(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                            qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the settings dialog loads correctly the different layers of the project depending on adds to the system a new
    ignition layer

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

    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    QgsProject.instance().addMapLayer(vl_a)
    QgsProject.instance().addMapLayer(vl_b)
    QgsProject.instance().addMapLayer(vl_c)
    vl_d = QgsVectorLayer('Polygon', 'd', 'memory')
    vl_e = QgsVectorLayer('Polygon', 'e', 'memory')
    vl_f = QgsVectorLayer('Polygon', 'f', 'memory')
    vl_g = QgsVectorLayer('Polygon', 'g', 'memory')
    QgsProject.instance().addMapLayer(vl_d)
    QgsProject.instance().addMapLayer(vl_e)
    QgsProject.instance().addMapLayer(vl_f)
    QgsProject.instance().addMapLayer(vl_g)

    dialog: SettingsDialog = SettingsDialog(layers=QgsProject.instance().mapLayers())
    assert dialog._combobox_ignition_layer.count() == 3
    assert dialog._combobox_perimeter_layer.count() == 4
    assert dialog._combobox_land_cover_layer.count() == 4

    def on_timer():
        assert dialog._dlg.isVisible()
        qtbot.keyClicks(dialog._dlg._lineedit_layer_name, 'perimeter_new')
        buttons_new_layer: QDialogButtonBox = dialog._dlg._button_box
        button_ok_new_layer: QPushButton = buttons_new_layer.button(qgis.PyQt.QtWidgets.QDialogButtonBox.Ok)
        qtbot.mouseClick(button_ok_new_layer, qgis.QtCore.Qt.LeftButton)
        assert not dialog._dlg.isVisible()

    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    assert len(QgsProject.instance().mapLayers()) == 7
    QTimer.singleShot(100, on_timer)
    qtbot.mouseClick(dialog._button_create_new_perimeter_layer, qgis.QtCore.Qt.LeftButton)
    assert len(QgsProject.instance().mapLayers()) == 8
    assert dialog.perimeter_layer.name() == 'perimeter_new'
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(qgis.PyQt.QtWidgets.QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_dialog_06(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                            qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the settings dialog loads correctly the different layers of the project depending on adds to the system a new
    ignition layer

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

    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    project: QgsProject = QgsProject()
    project.instance().addMapLayer(vl_a)
    project.instance().addMapLayer(vl_b)
    project.instance().addMapLayer(vl_c)
    vl_d = QgsVectorLayer('Polygon', 'd', 'memory')
    vl_e = QgsVectorLayer('Polygon', 'e', 'memory')
    vl_f = QgsVectorLayer('Polygon', 'f', 'memory')
    vl_g = QgsVectorLayer('Polygon', 'g', 'memory')
    project.instance().addMapLayer(vl_d)
    project.instance().addMapLayer(vl_e)
    project.instance().addMapLayer(vl_f)
    project.instance().addMapLayer(vl_g)

    dialog: SettingsDialog = SettingsDialog(layers=QgsProject.instance().mapLayers())
    assert dialog._combobox_ignition_layer.count() == 3
    assert dialog._combobox_perimeter_layer.count() == 4
    assert dialog._combobox_land_cover_layer.count() == 4

    def on_timer():
        assert dialog._dlg.isVisible()
        qtbot.keyClicks(dialog._dlg._lineedit_layer_name, 'perimeter_new')
        buttons_new_layer: QDialogButtonBox = dialog._dlg._button_box
        button_ok_new_layer: QPushButton = buttons_new_layer.button(QDialogButtonBox.Ok)
        qtbot.mouseClick(button_ok_new_layer, qgis.QtCore.Qt.LeftButton)
        assert not dialog._dlg.isVisible()

    qtbot.addWidget(dialog)
    dialog.show()
    assert dialog.isVisible()
    assert len(project.instance().mapLayers()) == 7
    QTimer.singleShot(100, on_timer)
    qtbot.mouseClick(dialog._button_create_new_perimeter_layer, qgis.QtCore.Qt.LeftButton)
    buttons: QDialogButtonBox = dialog._button_box
    button_cancel: QPushButton = buttons.button(QDialogButtonBox.Cancel)
    qtbot.mouseClick(button_cancel, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()
    assert len(project.instance().mapLayers()) == 7


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_application_01(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                 qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests Load the settings dialog and is cancelled without any modification

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis.utils.plugins['gisfire_spread_simulation']
    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    project_instance.addMapLayer(vl_a)
    project_instance.addMapLayer(vl_b)
    project_instance.addMapLayer(vl_c)
    vl_d = QgsVectorLayer('Polygon', 'd', 'memory')
    vl_e = QgsVectorLayer('Polygon', 'e', 'memory')
    vl_f = QgsVectorLayer('Polygon', 'f', 'memory')
    vl_g = QgsVectorLayer('Polygon', 'g', 'memory')
    project_instance.addMapLayer(vl_d)
    project_instance.addMapLayer(vl_e)
    project_instance.addMapLayer(vl_f)
    project_instance.addMapLayer(vl_g)
    project_instance.writeEntry('gisfire_spread_simulation', 'ignition_layer_id', vl_a.id())
    project_instance.writeEntry('gisfire_spread_simulation', 'perimeter_layer_id', vl_d.id())
    project_instance.writeEntry('gisfire_spread_simulation', 'land_cover_layer_id', vl_g.id())

    # noinspection DuplicatedCode
    def on_timer():
        dlg: SettingsDialog = plugin._dlg
        assert vl_a == dlg._combobox_ignition_layer.currentLayer()
        assert vl_d == dlg._combobox_perimeter_layer.currentLayer()
        assert vl_g == dlg._combobox_land_cover_layer.currentLayer()
        qtbot.mouseClick(dlg._button_box.button(QDialogButtonBox.Cancel), qgis.QtCore.Qt.LeftButton)

    QTimer.singleShot(100, on_timer)
    plugin._toolbar_actions['setup'].trigger()

    ignition_layer_id: str
    ignition_type_ok: bool
    ignition_layer_id, ignition_type_ok = project_instance.readEntry('gisfire_spread_simulation', 'ignition_layer_id',
                                                                     '')
    assert ignition_type_ok
    assert ignition_layer_id == vl_a.id()
    perimeter_layer_id: str
    perimeter_type_ok: bool
    perimeter_layer_id, perimeter_type_ok = project_instance.readEntry('gisfire_spread_simulation',
                                                                       'perimeter_layer_id', '')
    assert perimeter_type_ok
    assert perimeter_layer_id == vl_d.id()
    land_cover_layer_id: str
    land_cover_type_ok: bool
    land_cover_layer_id, land_cover_type_ok = project_instance.readEntry('gisfire_spread_simulation',
                                                                         'land_cover_layer_id', '')
    assert land_cover_type_ok
    assert land_cover_layer_id == vl_g.id()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_application_02(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                 qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests Load the settings dialog, layers are changed and is cancelled without any modification

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis.utils.plugins['gisfire_spread_simulation']
    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    project_instance.addMapLayer(vl_a)
    project_instance.addMapLayer(vl_b)
    project_instance.addMapLayer(vl_c)
    vl_d = QgsVectorLayer('Polygon', 'd', 'memory')
    vl_e = QgsVectorLayer('Polygon', 'e', 'memory')
    vl_f = QgsVectorLayer('Polygon', 'f', 'memory')
    vl_g = QgsVectorLayer('Polygon', 'g', 'memory')
    project_instance.addMapLayer(vl_d)
    project_instance.addMapLayer(vl_e)
    project_instance.addMapLayer(vl_f)
    project_instance.addMapLayer(vl_g)
    project_instance.writeEntry('gisfire_spread_simulation', 'ignition_layer_id', vl_a.id())
    project_instance.writeEntry('gisfire_spread_simulation', 'perimeter_layer_id', vl_d.id())
    project_instance.writeEntry('gisfire_spread_simulation', 'land_cover_layer_id', vl_g.id())

    # noinspection DuplicatedCode
    def on_timer():
        dlg: SettingsDialog = plugin._dlg
        assert vl_a == dlg._combobox_ignition_layer.currentLayer()
        assert vl_d == dlg._combobox_perimeter_layer.currentLayer()
        assert vl_g == dlg._combobox_land_cover_layer.currentLayer()
        qtbot.keyClicks(dlg._combobox_ignition_layer, 'b')
        qtbot.keyClicks(dlg._combobox_perimeter_layer, 'e')
        qtbot.keyClicks(dlg._combobox_land_cover_layer, 'f')
        assert vl_b == dlg._combobox_ignition_layer.currentLayer()
        assert vl_e == dlg._combobox_perimeter_layer.currentLayer()
        assert vl_f == dlg._combobox_land_cover_layer.currentLayer()
        qtbot.mouseClick(dlg._button_box.button(QDialogButtonBox.Cancel), qgis.QtCore.Qt.LeftButton)

    QTimer.singleShot(100, on_timer)
    plugin._toolbar_actions['setup'].trigger()

    ignition_layer_id: str
    ignition_type_ok: bool
    ignition_layer_id, ignition_type_ok = project_instance.readEntry('gisfire_spread_simulation', 'ignition_layer_id',
                                                                     '')
    assert ignition_type_ok
    assert ignition_layer_id == vl_a.id()
    perimeter_layer_id: str
    perimeter_type_ok: bool
    perimeter_layer_id, perimeter_type_ok = project_instance.readEntry('gisfire_spread_simulation',
                                                                       'perimeter_layer_id', '')
    assert perimeter_type_ok
    assert perimeter_layer_id == vl_d.id()
    land_cover_layer_id: str
    land_cover_type_ok: bool
    land_cover_layer_id, land_cover_type_ok = project_instance.readEntry('gisfire_spread_simulation',
                                                                         'land_cover_layer_id', '')
    assert land_cover_type_ok
    assert land_cover_layer_id == vl_g.id()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_settings_application_03(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                 qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests Load the settings dialog, layers are changed and is committed modifying the project values

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QT settings fixture with a user locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis.utils.plugins['gisfire_spread_simulation']
    vl_a = QgsVectorLayer('Point', 'a', 'memory')
    vl_b = QgsVectorLayer('Point', 'b', 'memory')
    vl_c = QgsVectorLayer('Point', 'c', 'memory')
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    project_instance.addMapLayer(vl_a)
    project_instance.addMapLayer(vl_b)
    project_instance.addMapLayer(vl_c)
    vl_d = QgsVectorLayer('Polygon', 'd', 'memory')
    vl_e = QgsVectorLayer('Polygon', 'e', 'memory')
    vl_f = QgsVectorLayer('Polygon', 'f', 'memory')
    vl_g = QgsVectorLayer('Polygon', 'g', 'memory')
    project_instance.addMapLayer(vl_d)
    project_instance.addMapLayer(vl_e)
    project_instance.addMapLayer(vl_f)
    project_instance.addMapLayer(vl_g)
    project_instance.writeEntry('gisfire_spread_simulation', 'ignition_layer_id', vl_a.id())
    project_instance.writeEntry('gisfire_spread_simulation', 'perimeter_layer_id', vl_d.id())
    project_instance.writeEntry('gisfire_spread_simulation', 'land_cover_layer_id', vl_g.id())

    # noinspection DuplicatedCode
    def on_timer():
        dlg: SettingsDialog = plugin._dlg
        assert vl_a == dlg._combobox_ignition_layer.currentLayer()
        assert vl_d == dlg._combobox_perimeter_layer.currentLayer()
        assert vl_g == dlg._combobox_land_cover_layer.currentLayer()
        qtbot.keyClicks(dlg._combobox_ignition_layer, 'b')
        qtbot.keyClicks(dlg._combobox_perimeter_layer, 'e')
        qtbot.keyClicks(dlg._combobox_land_cover_layer, 'f')
        qtbot.mouseClick(dlg._button_box.button(QDialogButtonBox.Ok), qgis.QtCore.Qt.LeftButton)
        assert vl_b == dlg._combobox_ignition_layer.currentLayer()
        assert vl_e == dlg._combobox_perimeter_layer.currentLayer()
        assert vl_f == dlg._combobox_land_cover_layer.currentLayer()

    QTimer.singleShot(100, on_timer)
    plugin._toolbar_actions['setup'].trigger()

    ignition_layer_id: str
    ignition_type_ok: bool
    ignition_layer_id, ignition_type_ok = project_instance.readEntry('gisfire_spread_simulation', 'ignition_layer_id',
                                                                     '')
    assert ignition_type_ok
    assert ignition_layer_id == vl_b.id()
    perimeter_layer_id: str
    perimeter_type_ok: bool
    perimeter_layer_id, perimeter_type_ok = project_instance.readEntry('gisfire_spread_simulation',
                                                                       'perimeter_layer_id', '')
    assert perimeter_type_ok
    assert perimeter_layer_id == vl_e.id()
    land_cover_layer_id: str
    land_cover_type_ok: bool
    land_cover_layer_id, land_cover_type_ok = project_instance.readEntry('gisfire_spread_simulation',
                                                                         'land_cover_layer_id', '')
    assert land_cover_type_ok
    assert land_cover_layer_id == vl_f.id()
