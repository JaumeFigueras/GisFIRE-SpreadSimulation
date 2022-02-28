# -*- coding: utf-8 -*-

import os.path
from typing import Dict
from typing import List
from typing import Union

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QLineEdit
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QWidget
from qgis.core import QgsMapLayer

from ..ui import get_ui_class

FORM_CLASS = get_ui_class(os.path.dirname(__file__), 'layer_name.ui')


class LayerNameDialog(QDialog, FORM_CLASS):
    """
    Dialog box to set a name for a new layer. It shows in red that the name of the new layer does not exist. It disables
    the Ok button accordingly
    """

    def __init__(self, parent: QWidget = None, layers: Union[Dict[str, QgsMapLayer], None] = None):
        """
        Constructor
        :param parent: UI Parent
        :type parent: QWidget
        :param layers: Available layers in the project to check the new name does not exist
        :type layers: dict of (str, QgsMapLayer)
        """
        self._lineedit_layer_name: Union[QLineEdit, None] = None
        self._text_color: Union[QColor, None] = None
        self._button_box: Union[QDialogButtonBox, None] = None
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._layer_names: List[str] = list()
        if layers is not None:
            self._layer_names = [lyr.name() for lyr in layers.values()]
        self._text_color = self._lineedit_layer_name.palette().color(QPalette.WindowText)
        self._lineedit_layer_name.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        buttons: QDialogButtonBox = self._button_box
        button_ok: QPushButton = buttons.button(QDialogButtonBox.Ok)
        if self._lineedit_layer_name.text() in self._layer_names:
            self._lineedit_layer_name.setStyleSheet('color: red')
            button_ok.setEnabled(False)
        else:
            self._lineedit_layer_name.setStyleSheet('color: {}'.format(self._text_color.name()))
            button_ok.setEnabled(True)

    @property
    def layer_name(self) -> str:
        return self._lineedit_layer_name.text()
