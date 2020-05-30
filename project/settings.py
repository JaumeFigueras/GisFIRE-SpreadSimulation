from qgis.core import QgsProject

class Settings:
    PLUGIN_NAME = 'gis_fire_spread_simulator'
    PREFIX = PLUGIN_NAME + '_'
    NONE = 'None'

    VERSION = '0.2'
    SETTING_VERSION = 'version'

    @property
    def gis_fire_version(self):
        project = QgsProject.instance()
        version, ok = project.readEntry(self.PLUGIN_NAME, self.SETTING_VERSION, self.NONE)
        if version != 'None' and ok:
            return version
        return None

    @gis_fire_version.setter
    def gis_fire_version(self, value):
        project = QgsProject.instance()
        project.writeEntry(self.PLUGIN_NAME, self.SETTING_VERSION, value)
