#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pytest
import qgis.utils
from _pytest.fixtures import SubRequest
from qgis.PyQt.QtWidgets import QMenu
from qgis.gui import QgisInterface


@pytest.fixture(scope='function')
def qgis_plugin(request: SubRequest) -> Dict[str, Any]:
    """
    Load the plugins provided by the request parameters. The parameters are two lists with the names of the plugins to
    load and the location paths of the plugins to load. The parameters can be a single values or a list. Parameters are
    named 'paths' and 'names'

    :param request: Request object that contains the parameters passes to the fixture
    :type request: SubRequest
    :return: A dictionary with the name, loaded plugin object association
    :rtype: Dict[str, Any]
    """
    paths: Union[str, List[str]] = request.param['paths'] if 'paths' in request.param else None
    names: Union[str, List[str]] = request.param['names'] if 'names' in request.param else None
    if (names is None) or (paths is None):
        return  # pragma: no cover
    if not isinstance(paths, list):
        paths: List[str] = [paths]
    if not isinstance(names, list):
        names: List[str] = [names]
    for path in paths:
        qgis.utils.plugin_paths.append(path)
        if path not in sys.path:
            sys.path.insert(0, path)
    qgis.utils.updateAvailablePlugins()
    plugins = dict()
    for name in names:
        assert qgis.utils.loadPlugin(name)
        assert qgis.utils.startPlugin(name)
        plugins[name] = qgis.utils.plugins[name]

    yield plugins

    for name in names:
        qgis.utils.unloadPlugin(name)
        del qgis.utils.plugin_times[name]
    for path in paths:
        sys.path.remove(path)
        qgis.utils.plugin_paths.remove(path)
    qgis.utils.updateAvailablePlugins()


@pytest.fixture(scope='function')
def qgis_iface_menu(qgis_iface: QgisInterface) -> QgisInterface:
    menu: QMenu = qgis_iface.mainWindow().menuBar()
    """
    Add menus to the QgisInterface. By default, the interface mock create only an empty menu.

    :param qgis_iface: The mocked interface provided by the qgis-pytest fixtures
    :type qgis_iface: QgisInterface
    :return: The same QgisInterface mock with three menus in the menu bar
    :rtype: QgisInterface
    """
    menu_a: QMenu = QMenu('A', menu)
    menu_b: QMenu = QMenu('B', menu)
    menu_c: QMenu = QMenu('C', menu)
    menu.addMenu(menu_a)
    menu.addMenu(menu_b)
    menu.addMenu(menu_c)

    yield qgis_iface

    qgis_iface.mainWindow().menuBar().removeAction(menu_a.menuAction())
    qgis_iface.mainWindow().menuBar().removeAction(menu_b.menuAction())
    qgis_iface.mainWindow().menuBar().removeAction(menu_c.menuAction())
    menu_a.deleteLater()
    menu_b.deleteLater()
    menu_c.deleteLater()
