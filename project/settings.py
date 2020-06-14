from qgis.core import QgsProject

class Settings:
    PLUGIN_NAME = 'gis_fire_spread_simulator'
    PREFIX = PLUGIN_NAME + '_'
    NONE = 'None'
    IGNITION_POINTS = 'Ignition Points'
    FIRE_PERIMETER = 'Fire Perimeter'

    VERSION = '0.2'
    SETTING_VERSION = 'version'
    SETTING_IGNITION_LAYER_NAME = 'ignition_layer'
    SETTING_PERIMETER_LAYER_NAME = 'perimeter_layer'

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

    @property
    def ignition_layer_name(self):
        project = QgsProject.instance()
        name, ok = project.readEntry(self.PLUGIN_NAME, self.SETTING_IGNITION_LAYER_NAME, self.NONE)
        if name != 'None' and ok:
            return name
        return None

    @ignition_layer_name.setter
    def ignition_layer_name(self, value):
        project = QgsProject.instance()
        project.writeEntry(self.PLUGIN_NAME, self.SETTING_IGNITION_LAYER_NAME, value)

    @property
    def perimeter_layer_name(self):
        project = QgsProject.instance()
        name, ok = project.readEntry(self.PLUGIN_NAME, self.SETTING_PERIMETER_LAYER_NAME, self.NONE)
        if name != 'None' and ok:
            return name
        return None

    @perimeter_layer_name.setter
    def perimeter_layer_name(self, value):
        project = QgsProject.instance()
        project.writeEntry(self.PLUGIN_NAME, self.SETTING_PERIMETER_LAYER_NAME, value)
