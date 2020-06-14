from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
from qgis.core import QgsField
from qgis.core import QgsFeature
from qgis.core import QgsMarkerSymbol

from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor

def createIgnitionLayer(name):
    """Create a QGis vector layer with the attributes specified by the meteo.cat
    API definition

    :param name: name of the layer that will be shown in the QGis legend
    :type name: string

    :return: the function returns the newly created layer
    :type return: qgis.core.QgsVectorLayer
    """
    # Check allowed feature types

    vl = QgsVectorLayer('Point', name, 'memory')
    pr = vl.dataProvider()
    # add fields
    attributes = [QgsField('id',  QVariant.Int),
                    QgsField('datetime',  QVariant.String),
                    QgsField('type',  QVariant.Int),
                    QgsField('burned',  QVariant.Int)]
    pr.addAttributes(attributes)
    vl.updateFields() # tell the vector layer to fetch changes from the provider
    # Assign current project CRS
    crs = QgsProject.instance().crs()
    vl.setCrs(crs, True)
    # Create simbology
    symbol = QgsMarkerSymbol.createSimple({'name': 'circle', 'color': 'red', 'size_unit': 'MM', 'size':'2'})
    vl.renderer().setSymbol(symbol)
    # Update layer's extent because change of extent in provider is not
    # propagated to the layer
    vl.updateExtents()
    return vl

def createPerimeterLayer(name):
    """Create a QGis vector layer with the attributes specified by the meteo.cat
    API definition

    :param name: name of the layer that will be shown in the QGis legend
    :type name: string

    :return: the function returns the newly created layer
    :type return: qgis.core.QgsVectorLayer
    """
    # Check allowed feature types

    vl = QgsVectorLayer('Polygon', name, 'memory')
    pr = vl.dataProvider()
    # add fields
    attributes = [QgsField('id',  QVariant.Int),
                    QgsField('datetime',  QVariant.String)]
    pr.addAttributes(attributes)
    vl.updateFields() # tell the vector layer to fetch changes from the provider
    # Assign current project CRS
    crs = QgsProject.instance().crs()
    vl.setCrs(crs, True)
    vl.renderer().symbol().symbolLayers()[0].setStrokeColor(QColor(255, 0, 0, 255))
    vl.renderer().symbol().symbolLayers()[0].setFillColor(QColor(255, 0, 0, 10))
    # Update layer's extent because change of extent in provider is not
    # propagated to the layer
    vl.updateExtents()
    return vl

def addLayerInPosition(layer, position):
    """Add a data layer in a certain position in the QGis legend. It is one
    indexed, beein the number 1 the top position of the legend.

    :param layer: data layer to be added in the QGis legend
    :type type: qgis.core.QgsVectorLayer

    :param name: one-indexed poition to add the layer
    :type name: int
    """
    QgsProject.instance().addMapLayer(layer, True)
    root = QgsProject.instance().layerTreeRoot()
    node_layer = root.findLayer(layer.id())
    node_clone = node_layer.clone()
    parent = node_layer.parent()
    parent.insertChildNode(position, node_clone)
    parent.removeChildNode(node_layer)
