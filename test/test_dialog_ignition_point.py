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
    Tests the labels and data provided is shown (with floats)

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

    dialog: IgnitionDateTimeDialog = IgnitionDateTimeDialog()
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    crs: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem('EPSG:4326')
    project_instance.setCrs(crs)
    project_crs: QgsCoordinateReferenceSystem = project_instance.crs()
    dialog.crs = project_crs.authid()
    dialog.point_x = 3.69
    dialog.point_y = 2.58
    current_utc = datetime.datetime.utcnow()
    dialog.ignition_datetime = current_utc
    dialog.show()
    assert dialog.isVisible()
    assert dialog._datetime_ignition.dateTime().toPyDateTime() == current_utc.replace(microsecond=0)
    assert dialog._label_crs.text() == 'EPSG:4326'
    assert dialog._label_x.text() == '3.69'
    assert dialog._label_y.text() == '2.58'
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_dialog_02(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                  qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the labels and data provided is shown (with integers)

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

    dialog: IgnitionDateTimeDialog = IgnitionDateTimeDialog()
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    crs: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem('EPSG:4326')
    project_instance.setCrs(crs)
    project_crs: QgsCoordinateReferenceSystem = project_instance.crs()
    dialog.crs = project_crs.authid()
    dialog.point_x = 3
    dialog.point_y = 2
    current_utc = datetime.datetime.utcnow()
    dialog.ignition_datetime = current_utc
    dialog.show()
    assert dialog.isVisible()
    assert dialog._datetime_ignition.dateTime().toPyDateTime() == current_utc.replace(microsecond=0)
    assert dialog._label_crs.text() == 'EPSG:4326'
    assert dialog._label_x.text() == '3'
    assert dialog._label_y.text() == '2'
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_dialog_03(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                  qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the labels and data provided is shown (with strings)

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

    dialog: IgnitionDateTimeDialog = IgnitionDateTimeDialog()
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    crs: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem('EPSG:4326')
    project_instance.setCrs(crs)
    project_crs: QgsCoordinateReferenceSystem = project_instance.crs()
    dialog.crs = project_crs.authid()
    dialog.point_x = '3.69'
    dialog.point_y = '2.58'
    current_utc = datetime.datetime.utcnow()
    dialog.ignition_datetime = current_utc
    dialog.show()
    assert dialog.isVisible()
    assert dialog._datetime_ignition.dateTime().toPyDateTime() == current_utc.replace(microsecond=0)
    assert dialog._label_crs.text() == 'EPSG:4326'
    assert dialog._label_x.text() == '3.69'
    assert dialog._label_y.text() == '2.58'
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_dialog_04(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                  qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the labels and data provided is shown (with local TZ)

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

    dialog: IgnitionDateTimeDialog = IgnitionDateTimeDialog()
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    crs: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem('EPSG:4326')
    project_instance.setCrs(crs)
    project_crs: QgsCoordinateReferenceSystem = project_instance.crs()
    dialog.crs = project_crs.authid()
    dialog.point_x = 3.69
    dialog.point_y = 2.58
    current_datetime = datetime.datetime.now()
    dialog.ignition_datetime = current_datetime
    dialog.show()
    assert dialog.isVisible()
    assert dialog._datetime_ignition.dateTime().toPyDateTime() == current_datetime.replace(microsecond=0)
    assert dialog._label_crs.text() == 'EPSG:4326'
    assert dialog._label_x.text() == '3.69'
    assert dialog._label_y.text() == '2.58'
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


# noinspection DuplicatedCode
@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_dialog_05(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                  qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None):
    """
    Tests the labels and data provided is shown (with local TZ)

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

    dialog: IgnitionDateTimeDialog = IgnitionDateTimeDialog()
    dialog.show()
    assert dialog.isVisible()
    dt: datetime.datetime = datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('CET'))
    dt_str: str = dt.strftime("%d/%m/%Y %H:%M:%S")
    qtbot.keyClicks(dialog._datetime_ignition, dt_str)
    assert dialog.ignition_datetime == datetime.datetime(2021, 12, 31, 23, 0, 0, tzinfo=pytz.UTC)
    buttons: QDialogButtonBox = dialog._button_box
    button_ok: QPushButton = buttons.button(QDialogButtonBox.Ok)
    qtbot.mouseClick(button_ok, qgis.QtCore.Qt.LeftButton)
    assert not dialog.isVisible()


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_application_01(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                       qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None) -> None:
    """
    Tests the Map point tool is created when the menu is triggered

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QSettings fixture this the current QGIS application locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    :param qgis_bot: QGIS UI Test Bot
    :type qgis_bot: QgisBot
    :param qtbot: QT UI Test Bot
    :type qtbot: QtBot
    :param qgis_new_project: Ensures a new project is created for the current test
    :type qgis_new_project: None
    :return: Nothing
    :rtype: None
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'

    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    plugin._menu_actions['new_ignition'].trigger()
    assert plugin._pointTool is not None


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_application_02(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                       qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None,
                                       qgis_canvas: QgsMapCanvas) -> None:
    """
    Tests the Map point tool is destroyed when there is a Right Click

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QSettings fixture this the current QGIS application locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    :param qgis_bot: QGIS UI Test Bot
    :type qgis_bot: QgisBot
    :param qtbot: QT UI Test Bot
    :type qtbot: QtBot
    :param qgis_new_project: Ensures a new project is created for the current test
    :type qgis_new_project: None
    :return: Nothing
    :rtype: None
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'

    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    plugin._menu_actions['new_ignition'].trigger()
    assert plugin._pointTool is not None
    qtbot.mouseClick(qgis_canvas.viewport(), qgis.QtCore.Qt.RightButton, pos=QPoint(10, 10))
    assert plugin._pointTool is None


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_application_03(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                       qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None,
                                       qgis_canvas: QgsMapCanvas) -> None:
    """
    Tests the Ignition Point dialog is shown when there is a Left Click (the appearing dialog is cancelled)

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QSettings fixture this the current QGIS application locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    :param qgis_bot: QGIS UI Test Bot
    :type qgis_bot: QgisBot
    :param qtbot: QT UI Test Bot
    :type qtbot: QtBot
    :param qgis_new_project: Ensures a new project is created for the current test
    :type qgis_new_project: None
    :return: Nothing
    :rtype: None
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'

    def on_timer():
        dlg: IgnitionDateTimeDialog = plugin._dlg
        assert dlg.isVisible()
        qtbot.mouseClick(dlg._button_box.button(QDialogButtonBox.Cancel), qgis.QtCore.Qt.LeftButton)

    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    plugin._menu_actions['new_ignition'].trigger()
    assert plugin._pointTool is not None
    QTimer.singleShot(100, on_timer)
    qtbot.mouseClick(qgis_canvas.viewport(), qgis.QtCore.Qt.LeftButton, pos=QPoint(10, 10))


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_application_04(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                       qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None,
                                       qgis_canvas: QgsMapCanvas) -> None:
    """
    Tests the Ignition Point dialog is shown when there is a Left Click (the appearing dialog is cancelled) so the tests
    checks that the ignition points layer is unchanged

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QSettings fixture this the current QGIS application locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    :param qgis_bot: QGIS UI Test Bot
    :type qgis_bot: QgisBot
    :param qtbot: QT UI Test Bot
    :type qtbot: QtBot
    :param qgis_new_project: Ensures a new project is created for the current test
    :type qgis_new_project: None
    :return: Nothing
    :rtype: None
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    vl_a: QgsVectorLayer = QgsVectorLayer('Point', 'a', 'memory')
    provider: QgsVectorDataProvider = vl_a.dataProvider()
    attributes: List[QgsField] = [QgsField('fid', QVariant.Int), QgsField('datetime', QVariant.String)]
    provider.addAttributes(attributes)
    vl_a.updateFields()
    crs: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem('EPSG:25831')
    vl_a.setCrs(crs, True)
    vl_a.updateExtents()
    plugin._ignition_layer = vl_a
    assert vl_a.featureCount() == 0

    def on_timer():
        dlg: IgnitionDateTimeDialog = plugin._dlg
        assert dlg.isVisible()
        qtbot.mouseClick(dlg._button_box.button(QDialogButtonBox.Cancel), qgis.QtCore.Qt.LeftButton)

    plugin._menu_actions['new_ignition'].trigger()
    assert plugin._pointTool is not None
    QTimer.singleShot(100, on_timer)
    qtbot.mouseClick(qgis_canvas.viewport(), qgis.QtCore.Qt.LeftButton, pos=QPoint(10, 10))

    assert vl_a.featureCount() == 0


@pytest.mark.parametrize('qgis_plugin', [{
    'paths': str(Path(__file__).parent.parent) + '/src',
    'names': 'gisfire_spread_simulation'
}], indirect=True)
def test_ignition_point_application_05(qgis_app: QgsApplication, qgis_locale: QSettings, qgis_plugin: Dict[str, Any],
                                       qgis_bot: QgisBot, qtbot: QtBot, qgis_new_project: None,
                                       qgis_canvas: QgsMapCanvas) -> None:
    """
    Tests the Ignition Point dialog is shown when there is a Left Click (the appearing dialog is cancelled) so the tests
    checks that the ignition points layer is unchanged

    :param qgis_app: QGIS application fixture
    :type qgis_app: QgsApplication
    :param qgis_locale: QSettings fixture this the current QGIS application locale
    :type qgis_locale: QSettings
    :param qgis_plugin: QGIS loading and unloading fixture for plugins
    :type qgis_plugin: dict of Any
    :param qgis_bot: QGIS UI Test Bot
    :type qgis_bot: QgisBot
    :param qtbot: QT UI Test Bot
    :type qtbot: QtBot
    :param qgis_new_project: Ensures a new project is created for the current test
    :type qgis_new_project: None
    :return: Nothing
    :rtype: None
    """
    assert type(qgis.utils.plugins['gisfire_spread_simulation']).__name__ == 'GisFIRESpreadSimulation'
    plugin: GisFIRESpreadSimulation = qgis_plugin['gisfire_spread_simulation']
    vl_a: QgsVectorLayer = QgsVectorLayer('Point', 'a', 'memory')
    provider: QgsVectorDataProvider = vl_a.dataProvider()
    attributes: List[QgsField] = [QgsField('fid', QVariant.Int), QgsField('datetime', QVariant.String)]
    provider.addAttributes(attributes)
    vl_a.updateFields()
    crs: QgsCoordinateReferenceSystem = QgsCoordinateReferenceSystem('EPSG:25831')
    vl_a.setCrs(crs, True)
    vl_a.updateExtents()
    plugin._ignition_layer = vl_a
    assert vl_a.featureCount() == 0
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    project_instance.setCrs(crs)

    def on_timer():
        dlg: IgnitionDateTimeDialog = plugin._dlg
        assert dlg.isVisible()
        qtbot.mouseClick(dlg._button_box.button(QDialogButtonBox.Ok), qgis.QtCore.Qt.LeftButton)

    plugin._menu_actions['new_ignition'].trigger()
    assert plugin._pointTool is not None
    QTimer.singleShot(100, on_timer)
    qtbot.mouseClick(qgis_canvas.viewport(), qgis.QtCore.Qt.LeftButton, pos=QPoint(10, 10))

    assert vl_a.featureCount() == 1
