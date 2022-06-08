from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import QgsVectorDataProvider
from qgis.core import QgsField
from qgis.core import QgsPointXY
from qgis.core import QgsPoint
from qgis.core import QgsMarkerSymbol
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsLayerTree
from qgis.core import QgsLayerTreeLayer
from qgis.core import QgsLayerTreeNode
from qgis.core import QgsFeature

from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor

from typing import List

import datetime


# noinspection DuplicatedCode
def create_ignition_layer(name: str) -> QgsVectorLayer:
    """
    Creates a QGis vector layer with the attributes needed by the Spread simulation process. Attributes are:
    - fid: Feature ID, integer
    - datetime: Ignition time of the point, string ISO formatted

    :param name: name of the layer that will be shown in the QGis legend
    :type name: string
    :return: the function returns the newly created layer
    :rtype: QgsVectorLayer
    """
    vector_layer: QgsVectorLayer = QgsVectorLayer('Point', name, 'memory')
    provider: QgsVectorDataProvider = vector_layer.dataProvider()
    # Add fields
    attributes: List[QgsField] = [QgsField('fid',  QVariant.Int),
                                  QgsField('datetime',  QVariant.String)]
    provider.addAttributes(attributes)
    # Tell the vector layer to fetch changes from the provider
    vector_layer.updateFields()
    # Assign current project CRS
    crs: QgsCoordinateReferenceSystem = QgsProject.instance().crs()
    vector_layer.setCrs(crs, True)
    # Create a default symbology
    symbol = QgsMarkerSymbol.createSimple({'name': 'circle',
                                           'color': 'red',
                                           'size_unit': 'MM',
                                           'size': '2'})
    # noinspection PyUnresolvedReferences
    vector_layer.renderer().setSymbol(symbol)
    # Update layer's extent because change of extent in provider is not propagated to the layer
    vector_layer.updateExtents()
    return vector_layer


# noinspection DuplicatedCode
def create_perimeter_layer(name: str) -> QgsVectorLayer:
    """
    Creates a QGis vector layer with the attributes needed by the Spread simulation process. Attributes are:
    - fid: Feature ID, integer
    - datetime: Ignition time of the point, string ISO formatted

    :param name: name of the layer that will be shown in the QGis legend
    :type name: string
    :return: the function returns the newly created layer
    :rtype: QgsVectorLayer
    """
    vector_layer: QgsVectorLayer = QgsVectorLayer('Polygon', name, 'memory')
    provider: QgsVectorDataProvider = vector_layer.dataProvider()
    # Add fields
    attributes: List[QgsField] = [QgsField('fid',  QVariant.Int),
                                  QgsField('datetime',  QVariant.String)]
    provider.addAttributes(attributes)
    # Tell the vector layer to fetch changes from the provider
    vector_layer.updateFields()
    # Assign current project CRS
    crs: QgsCoordinateReferenceSystem = QgsProject.instance().crs()
    vector_layer.setCrs(crs, True)
    # Create a default symbology
    # noinspection PyUnresolvedReferences
    vector_layer.renderer().symbol().symbolLayers()[0].setStrokeColor(QColor(255, 0, 0, 255))
    # noinspection PyUnresolvedReferences
    vector_layer.renderer().symbol().symbolLayers()[0].setFillColor(QColor(255, 0, 0, 10))
    # Update layer's extent because change of extent in provider is not propagated to the layer
    vector_layer.updateExtents()
    return vector_layer


def add_layer_in_position(layer: QgsVectorLayer, position: int) -> None:
    """
    Add a data layer in a certain position in the QGis legend. It is one indexed, being the number 1 the top position
    of the legend.

    :param layer: Data layer to be added in the QGIS legend
    :type layer: QgsVectorLayer
    :param position: Position in the project legend were the layer wil be located
    :type position: int
    :return: Nothing
    :rtype: None
    """
    # Inset the layer into the legend
    QgsProject.instance().addMapLayer(layer, True)
    # Find the inserted layer
    root: QgsLayerTree = QgsProject.instance().layerTreeRoot()
    node_layer: QgsLayerTreeLayer = root.findLayer(layer.id())
    node_clone: QgsLayerTreeLayer = node_layer.clone()
    # Insert new clone and remove old (API don't allow to directly insert into position nor move to position)
    parent: QgsLayerTreeNode = node_layer.parent()
    parent.insertChildNode(position, node_clone)
    parent.removeChildNode(node_layer)


def add_ignition_point(point: QgsPoint, date: datetime.datetime, layer: QgsVectorLayer) -> bool:
    """
    Adds a point to the provider layer. The point is an ignition point, so a datetime and a point are needed

    :param point: Point in the CRS of the layer to be set as an ignition source
    :type point: QgsPoint
    :param date: Date when the ignition phase starts
    :type date: datetime.datetime
    :param layer: Ignition layer where the point will be added
    :type layer: QgsVectorLayer
    :return: Success or failure in insertion
    :rtype: bool
    """
    feature: QgsFeature = QgsFeature(layer.fields())
    feature.setAttribute('datetime', date.strftime("%Y-%m-%dT%H:%M:%S%Z"))
    feature.setGeometry(point)
    result: bool
    result, _ = layer.dataProvider().addFeatures([feature])
    layer.updateExtents()
    layer.triggerRepaint()
    return result

