#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
from qgis.core import QgsProject


@pytest.fixture(scope='function')
def non_gisfire_project(qgis_new_project: None) -> None:
    """
    Fixture to load a QGIS project with no GisFIRE data

    :param qgis_new_project:
    :type qgis_new_project:
    :return:
    :rtype:
    """
    test_folder = Path(__file__).parent.parent
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    filename = str(test_folder) + '/data/blank_project_no_gisfire.qgz'
    project_instance.read(filename)


@pytest.fixture(scope='function')
def gisfire_blank_project(qgis_new_project: None) -> None:
    """
    Fixture to load a QGIS project with GisFIRE data but no data on the data layers

    :param qgis_new_project:
    :type qgis_new_project:
    :return:
    :rtype:
    """
    test_folder = Path(__file__).parent.parent
    project: QgsProject = QgsProject()
    project_instance: QgsProject = project.instance()
    filename = str(test_folder) + '/data/blank_project.qgz'
    project_instance.read(filename)
