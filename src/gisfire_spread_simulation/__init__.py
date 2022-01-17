#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# noinspection PyPep8Naming
def classFactory(iface):
    """
    Loads the GisFIRESpreadSimulation class. It is needed by the qgis.utils module in charge of loadin plugins into QGIS

    :param iface: A QGIS interface instance.
    :type iface: qgis.gui.QgisInterface
    """
    from .gisfire_spread_simulation import GisFIRESpreadSimulation
    return GisFIRESpreadSimulation(iface)
