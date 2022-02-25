#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from _pytest.fixtures import SubRequest
from qgis.PyQt.QtCore import QSettings


@pytest.fixture(scope='function')
def qgis_locale(request: SubRequest) -> QSettings:
    """
    A fixture that assigns to the application QSettings the locale parameters needed to load the plugins

    :param request: Fixture parameter, the fixture accepts a parameter called 'locale' with a full locale string, such
    as 'en_GB' or 'ca_ES'
    :type request: SubRequest
    :return: A QSettings object with the locale settings strings used in QGIS
    :rtype: QSettings
    """
    global_settings = QSettings()
    global_settings.setValue('locale/overrideFlag', False)
    if hasattr(request, 'param'):
        if 'locale' in request.param:
            locale = request.param['locale']
            global_settings.setValue('locale/overrideFlag', True)
        else:
            locale = 'en_GB'
    else:
        locale = 'en_GB'
    global_settings.setValue('locale/userLocale', locale)

    yield global_settings

    global_settings.remove('locale/overrideFlag')
    global_settings.remove('locale/userLocale')
