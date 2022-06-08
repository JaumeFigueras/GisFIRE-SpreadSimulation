#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
# For linux
sys.path.append('/usr/share/qgis/python/plugins')
# For Windows
sys.path.append('C:\\QGIS\\apps\\qgis\\python\\plugins')


# noinspection PyPep8Naming
def classFactory(iface):
    """
    Loads the GisFIRESpreadSimulation class. It is needed by the qgis.utils module in charge of loadin plugins into QGIS

    :param iface: A QGIS interface instance.
    :type iface: qgis.gui.QgisInterface
    """
    from .gisfire_spread_simulation import GisFIRESpreadSimulation
    return GisFIRESpreadSimulation(iface)
