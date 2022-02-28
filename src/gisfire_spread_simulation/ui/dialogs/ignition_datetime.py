# -*- coding: utf-8 -*-
import datetime
import os.path
from typing import Dict
from typing import List
from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QLabel
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QWidget
from qgis.PyQt.QtWidgets import QDateTimeEdit
from qgis.core import QgsMapLayer
from PyQt5.QtCore import QDateTime

from ..ui import get_ui_class

import datetime
import pytz

FORM_CLASS = get_ui_class(os.path.dirname(__file__), 'ignition_datetime.ui')
LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


class IgnitionDateTimeDialog(QDialog, FORM_CLASS):
    """
    Dialog box to set the starting date and time of an ignition in a wildfire. The date time is always set and stores in
    UTC time, but it will be displayed in local time
    """

    def __init__(self, parent: QWidget = None):
        """
        Constructor
        :param parent: UI Parent
        :type parent: QWidget
        """
        self._label_crs: Union[QLabel, None] = None
        self._label_x: Union[QLabel, None] = None
        self._label_y: Union[QLabel, None] = None
        self._datetime_ignition: Union[QDateTimeEdit, None] = None
        self._button_box: Union[QDialogButtonBox, None] = None
        QDialog.__init__(self, parent)
        self.setupUi(self)

    @property
    def crs(self) -> str:
        return self._label_crs.text()

    @crs.setter
    def crs(self, value: str) -> None:
        self._label_crs.setText(value)

    @property
    def point_x(self) -> str:
        return self._label_x.text()

    @point_x.setter
    def point_x(self, value: Union[str, int, float]) -> None:
        text: str = ''
        if isinstance(value, str):
            text = value
        elif isinstance(value, int) or isinstance(value, float):
            text = str(value)
        self._label_x.setText(text)

    @property
    def point_y(self) -> str:
        return self._label_y.text()

    @point_y.setter
    def point_y(self, value: Union[str, int, float]) -> None:
        text: str = ''
        if isinstance(value, str):
            text = value
        elif isinstance(value, int) or isinstance(value, float):
            text = str(value)
        self._label_y.setText(text)

    @property
    def ignition_datetime(self) -> datetime.datetime:
        qt_dt: QDateTime = self._datetime_ignition.dateTime()
        dt: datetime.datetime = qt_dt.toPyDateTime().replace(microsecond=0)
        dt_utc: datetime.datetime = dt.astimezone(pytz.UTC)
        return dt_utc

    @ignition_datetime.setter
    def ignition_datetime(self, dt_utc: datetime.datetime) -> None:
        dt: datetime.datetime = dt_utc.astimezone(LOCAL_TIMEZONE).replace(microsecond=0)
        qt_dt: QDateTime = QDateTime(dt)
        self._datetime_ignition.setDateTime(qt_dt)
