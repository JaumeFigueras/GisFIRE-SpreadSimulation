import pytest
from _pytest.fixtures import SubRequest
from qgis.PyQt.QtCore import QSettings


@pytest.fixture(scope='session')
def qgis_locale(request: SubRequest):
    if hasattr(request, 'param'):
        locale = request.param['locale'] if 'locale' in request.param else 'EN'
    else:
        locale = 'EN'
    global_settings = QSettings()
    global_settings.setValue('locale/userLocale', locale)
    yield global_settings
