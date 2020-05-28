from .settings import Settings

from qgis.core import QgsProject
from qgis.core import QgsExpressionContextUtils

def isAGisFireProject():
    project = QgsProject.instance()
    version, ok = project.readEntry(Settings.PLUGIN_NAME, Settings.SETTING_VERSION, "None")
    if version != "None" and ok:
        return True
    return False

def getProjectName():
    project = QgsProject.instance()
    scope = QgsExpressionContextUtils.projectScope(project)
    return scope.variable('project_basename')
