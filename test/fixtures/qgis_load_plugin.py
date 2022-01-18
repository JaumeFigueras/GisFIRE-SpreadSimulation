import pytest
import sys
import qgis.utils
from typing import Union
from typing import List
from typing import Dict
from _pytest.fixtures import SubRequest


@pytest.fixture(scope='session')
def qgis_plugin(request: SubRequest) -> Dict[str, object]:
    """
    TODO

    :param request:
    :type request: SubRequest
    :return:
    :rtype: Dict[str, object]
    """
    paths: Union[str, List[str]] = request.param['paths'] if 'paths' in request.param else None
    names: Union[str, List[str]] = request.param['names'] if 'names' in request.param else None
    if (names is None) or (paths is None):
        return
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


