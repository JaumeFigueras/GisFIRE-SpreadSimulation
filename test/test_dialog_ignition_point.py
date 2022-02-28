#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Union

import pytest
import pytz
import qgis.utils
from PyQt5.QtCore import QTimer
from pytest_qgis.qgis_bot import QgisBot
from pytestqt.qtbot import QtBot
from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QLineEdit
from qgis.core import QgsApplication
from qgis.core import QgsMapLayer
from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
from qgis.core import QgsCoordinateReferenceSystem
from PyQt5.QtGui import QPalette
from PyQt5.QtGui import QColor

from src.gisfire_spread_simulation.gisfire_spread_simulation import GisFIRESpreadSimulation
from src.gisfire_spread_simulation.ui.dialogs.ignition_datetime import IgnitionDateTimeDialog
import datetime


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

