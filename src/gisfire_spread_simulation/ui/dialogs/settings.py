# -*- coding: utf-8 -*-

import os.path
from typing import Dict
from typing import List
from typing import Union

from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtWidgets import QWidget
from qgis.core import QgsMapLayer
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import QgsWkbTypes
from qgis.gui import QgsMapLayerComboBox

from .layer_name import LayerNameDialog
from ..ui import get_ui_class
from ...qgis_helper_functions.layer import add_layer_in_position
from ...qgis_helper_functions.layer import create_ignition_layer
from ...qgis_helper_functions.layer import create_perimeter_layer

FORM_CLASS = get_ui_class(os.path.dirname(__file__), 'settings.ui')


class SettingsDialog(QDialog, FORM_CLASS):
    """
    Dialog box to collect or modify the settings needed by the GisFIRE Spread simulation plugin. The settings are:
    - Ignition Layer
    - Perimeter Layer
    - Land Cover Layer

    """

    def __init__(self, parent: QWidget = None, layers: Union[Dict[str, QgsMapLayer], None] = None):
        """
        Constructor

        :param parent: UI Parent
        :type parent: QWidget
        """
        self._combobox_ignition_layer: Union[QgsMapLayerComboBox, None] = None
        self._combobox_perimeter_layer: Union[QgsMapLayerComboBox, None] = None
        self._combobox_land_cover_layer: Union[QgsMapLayerComboBox, None] = None
        self._button_create_new_ignition_layer: Union[QPushButton, None] = None
        self._button_create_new_perimeter_layer: Union[QPushButton, None] = None
        self._button_box: Union[QDialogButtonBox, None] = None
        self._layers: Union[Dict[str, QgsMapLayer], None] = layers
        self._dlg: Union[LayerNameDialog, None] = None
        self._excepted_ignition_layers: List[QgsMapLayer]
        self._excepted_perimeter_layers: List[QgsMapLayer]
        self._excepted_land_cover_layers: List[QgsMapLayer]
        QDialog.__init__(self, parent)
        self.setupUi(self)
        if layers is not None:
            self._excepted_ignition_layers: List[QgsMapLayer] = [lyr for lyr in layers.values() if
                                                                 isinstance(lyr, QgsVectorLayer) and
                                                                 lyr.geometryType() != QgsWkbTypes.PointGeometry]
            self._excepted_perimeter_layers: List[QgsMapLayer] = [lyr for lyr in layers.values() if
                                                                  isinstance(lyr, QgsVectorLayer) and
                                                                  lyr.geometryType() != QgsWkbTypes.PolygonGeometry]
            self._excepted_land_cover_layers: List[QgsMapLayer] = [lyr for lyr in layers.values() if
                                                                   isinstance(lyr, QgsVectorLayer) and
                                                                   lyr.geometryType() != QgsWkbTypes.PolygonGeometry]
            self._combobox_ignition_layer.setExceptedLayerList(self._excepted_ignition_layers)
            self._combobox_perimeter_layer.setExceptedLayerList(self._excepted_perimeter_layers)
            self._combobox_land_cover_layer.setExceptedLayerList(self._excepted_land_cover_layers)
        # noinspection PyUnresolvedReferences
        self._button_create_new_ignition_layer.clicked.connect(self._on_click_new_ignition_layer)
        # noinspection PyUnresolvedReferences
        self._button_create_new_perimeter_layer.clicked.connect(self._on_click_new_perimeter_layer)
        buttons: QDialogButtonBox = self._button_box
        button_cancel: QPushButton = buttons.button(QDialogButtonBox.Cancel)
        # noinspection PyUnresolvedReferences
        button_cancel.clicked.connect(self._on_cancel)
        self._created_layers: List[QgsVectorLayer] = list()

    def _on_click_new_ignition_layer(self):
        self._dlg: LayerNameDialog = LayerNameDialog(parent=self, layers=self._layers)
        result = self._dlg.exec_()
        if result == QDialog.Accepted:
            layer: QgsVectorLayer = create_ignition_layer(self._dlg.layer_name)
            add_layer_in_position(layer, 1)
            self._combobox_ignition_layer.setLayer(layer)
            self._created_layers.append(layer)
            self._excepted_perimeter_layers.append(layer)
            self._excepted_land_cover_layers.append(layer)
            self._combobox_perimeter_layer.setExceptedLayerList(self._excepted_perimeter_layers)
            self._combobox_land_cover_layer.setExceptedLayerList(self._excepted_land_cover_layers)

    def _on_click_new_perimeter_layer(self):
        self._dlg: LayerNameDialog = LayerNameDialog(parent=self, layers=self._layers)
        result = self._dlg.exec_()
        if result == QDialog.Accepted:
            layer: QgsVectorLayer = create_perimeter_layer(self._dlg.layer_name)
            add_layer_in_position(layer, 1)
            self._combobox_perimeter_layer.setLayer(layer)
            self._created_layers.append(layer)
            self._excepted_ignition_layers.append(layer)
            self._combobox_ignition_layer.setExceptedLayerList(self._excepted_ignition_layers)

    def _on_cancel(self):
        for layer in self._created_layers:
            QgsProject.instance().removeMapLayer(layer)

    @property
    def ignition_layer(self) -> QgsVectorLayer:
        return self._combobox_ignition_layer.currentLayer()

    @ignition_layer.setter
    def ignition_layer(self, layer: QgsVectorLayer):
        self._combobox_ignition_layer.setLayer(layer)

    @property
    def perimeter_layer(self) -> QgsVectorLayer:
        return self._combobox_perimeter_layer.currentLayer()

    @perimeter_layer.setter
    def perimeter_layer(self, layer: QgsVectorLayer):
        self._combobox_perimeter_layer.setLayer(layer)

    @property
    def land_cover_layer(self) -> QgsVectorLayer:
        return self._combobox_land_cover_layer.currentLayer()

    @land_cover_layer.setter
    def land_cover_layer(self, layer: QgsVectorLayer):
        self._combobox_land_cover_layer.setLayer(layer)
