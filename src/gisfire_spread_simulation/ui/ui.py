# -*- coding: utf-8 -*-

from qgis.PyQt import uic
import os.path
from typing import Any


def get_ui_class(plugin_dir: str, ui_file_name: str) -> Any:
    """
    Loads a UI QT5 graphical interface file to pass it to the final object constructor

    :param plugin_dir: Path of the file to load
    :type plugin_dir: str
    :param ui_file_name: Filename of the UI definition file
    :type ui_file_name: str
    :return: The UI class
    :rtype: Any
    """
    ui_file_path = plugin_dir + '/' + ui_file_name
    if os.path.exists(ui_file_path):
        return uic.loadUiType(ui_file_path)[0]
    else:
        return None  # pragma: no cover
