#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations  # Needed to allow returning type of enclosing class PEP 563

import datetime
from typing import List
from typing import Union
from typing import Any
from typing import Tuple

import math
import numpy
from dateutil import parser
from qgis.core import QgsApplication
from qgis.core import QgsFeature
from qgis.core import QgsVectorLayer
from qgis.core import QgsProject
from qgis.core import edit
from qgis.core import QgsPointXY
from qgis.core import QgsGeometry
from qgis.core import QgsProcessingFeedback

import gisfire_spread_simulation.fuel_models.standard_fuel_models as models
from gisfire_spread_simulation.fuel_models.standard_fuel_models import model_1
from gisfire_spread_simulation.fuel_models.standard_fuel_models import model_0
from gisfire_spread_simulation.fuel_models.fuel_model import FuelModel
from gisfire_spread_simulation.simulation_algorithms.ellipse_algorithms import EllipseAlgorithm
from gisfire_spread_simulation.simulation_algorithms.rate_of_sprerad_algorithms import RateOfSpread

import processing


class SpreadSimulator:
    """
    TODO
    """

    class Point:
        def __init__(self, x: Union[float, None] = None, y: Union[float, None] = None, fuel_model: Union[FuelModel, None] = None):
            self._x = x
            self._y = y
            self._fuel_model = fuel_model

        @property
        def x(self) -> float:
            return self._x

        @x.setter
        def x(self, value: float) -> None:
            self._x = value

        @property
        def y(self) -> float:
            return self._y

        @y.setter
        def y(self, value: float) -> None:
            self._y = value

        @property
        def fuel_model(self) -> FuelModel:
            return self._fuel_model

        @fuel_model.setter
        def fuel_model(self, value: fuel_model) -> None:
            self._fuel_model = value

    class IgnitionPoint(Point):
        def __init__(self, feature: Union[QgsFeature, None] = None, x: Union[float, None] = None,
                     y: Union[float, None] = None, ignition_date: Union[datetime.datetime, None] = None,
                     fuel_model: Union[FuelModel, None] = None) -> None:
            super().__init__(x=x, y=y, fuel_model=fuel_model)
            self._feat = feature
            self._dt = ignition_date
            self._wind_speed: Union[float, None] = None
            self._wind_direction: Union[float, None] = None
            self._fuel_model: Union[FuelModel, None] = None
            self._slope: Union[float, None] = None
            self._aspect: Union[float, None] = None

        def __lt__(self, other: SpreadSimulator.IgnitionPoint) -> bool:
            return self._dt < other._dt

        def __gt__(self, other: SpreadSimulator.IgnitionPoint) -> bool:
            return self._dt > other._dt

        def __le__(self, other: SpreadSimulator.IgnitionPoint) -> bool:
            return self._dt <= other._dt

        def __ge__(self, other: SpreadSimulator.IgnitionPoint) -> bool:
            return self._dt >= other._dt

        @property
        def feature(self) -> QgsFeature:
            return self._feat

        @feature.setter
        def feature(self, value: QgsFeature) -> None:
            self._feat = value

        @property
        def ignition_date(self) -> datetime.datetime:
            return self._dt

        @ignition_date.setter
        def ignition_date(self, value: datetime.datetime) -> None:
            self._dt = value

        @property
        def fuel_model(self) -> FuelModel:
            return self._fuel_model

        @fuel_model.setter
        def fuel_model(self, value: FuelModel) -> None:
            self._fuel_model = value

    default_moisture = ((0.03, 0.03, 0.03), (0.45, 0.82))
    default_wind = (2, 0)
    default_slope = 0

    def __init__(self, time_step: int = 30, initial_sampling: int = 100,
                 ignition_layer: Union[QgsVectorLayer, None] = None,
                 perimeter_layer: Union[QgsVectorLayer, None] = None, fuel_layer: Union[QgsVectorLayer, None] = None,
                 starting_time: Union[datetime.datetime, None] = None) -> None:
        """
        TODO

        :param time_step: Time step of the simulation (i.e. the time the simulator advance in each iteration). The time
        step must be provided in seconds.
        :type time_step: int
        :param initial_sampling: Number of points to discretize the first ellipse of an ignition point
        :type initial_sampling: int
        :param ignition_layer:
        :type ignition_layer: QgsVectorLayer
        :param perimeter_layer:
        :type perimeter_layer: QgsVectorLayer
        :param fuel_layer:
        :type fuel_layer: QgsVectorLayer
        :param starting_time:
        :type starting_time: datetime.datetime
        """
        # Simulation parameters
        self._time_step = time_step
        self._initial_sampling = initial_sampling
        self._ignition_layer = ignition_layer
        self._perimeter_layer = perimeter_layer
        self._fuel_layer = fuel_layer
        self._start_date: datetime.datetime = starting_time
        # Simulation internal state
        self._t_now: Union[datetime.datetime, None] = None
        self._ignition_points: Union[List[SpreadSimulator.IgnitionPoint], None] = None

    @property
    def time_step(self) -> int:
        return self._time_step

    @time_step.setter
    def time_step(self, ts: int) -> None:
        self._time_step = ts

    @property
    def start_date(self) -> datetime.datetime:
        return self._start_date

    @start_date.setter
    def start_date(self, value: datetime.datetime) -> None:
        self._start_date = value

    @property
    def initial_sampling(self) -> int:
        return self._initial_sampling

    @initial_sampling.setter
    def initial_sampling(self, sm: int) -> None:
        self._initial_sampling = sm

    @property
    def ignition_layer(self) -> QgsVectorLayer:
        return self._ignition_layer

    @ignition_layer.setter
    def ignition_layer(self, layer: QgsVectorLayer) -> None:
        self._ignition_layer = layer

    @property
    def perimeter_layer(self) -> QgsVectorLayer:
        return self._perimeter_layer

    @perimeter_layer.setter
    def perimeter_layer(self, layer: QgsVectorLayer) -> None:
        self._perimeter_layer = layer

    @property
    def fuel_layer(self) -> QgsVectorLayer:
        return self._fuel_layer

    @fuel_layer.setter
    def fuel_layer(self, layer: QgsVectorLayer) -> None:
        self._fuel_layer = layer

    def reset_simulation(self):
        """
        Initialize the internal variables to perform a simulation. It clears the perimeter layer in case it has any data
        and the internal time counter to the starting time
        """
        # Initialize simulation time
        self._t_now = self._start_date
        # Clean the perimeter layer
        with edit(self._perimeter_layer):
            feature_ids = [feature.id() for feature in self._perimeter_layer.getFeatures()]
            self._perimeter_layer.deleteFeatures(feature_ids)

    def __ellipse(self, point: Point) -> Union[List[Point], None]:
        """
        TODO
        :param point:
        :type point: SpreadSimulator.Point
        :param model:
        :type model: FuelModel
        :return:
        :rtype:
        """
        if point.fuel_model == model_0:
            return None
        # TODO: Get moisture, wind and slope from layers instead of defaults
        # TODO: rotate the wind according to the aspect of the slope
        (rate, alpha, wind) = RateOfSpread.rothermel(fuel_model=point.fuel_model,
                                                     moisture=SpreadSimulator.default_moisture,
                                                     wind=SpreadSimulator.default_wind,
                                                     slope=SpreadSimulator.default_slope)
        (a, b, c) = EllipseAlgorithm.alexander(rate / 60, wind)

        dt = self._time_step
        ds = (2 * numpy.pi) / self._initial_sampling
        steps = numpy.arange(0, 2 * numpy.pi, ds)
        points: List[SpreadSimulator.Point] = [
            SpreadSimulator.Point(dt * a * math.cos(step), dt * b * math.sin(step) + dt * c) for step in steps]
        points = [SpreadSimulator.Point(p.x * math.cos(alpha) - p.y * math.sin(alpha),
                                        p.x * math.sin(alpha) + p.y * math.cos(alpha)) for p in points]
        points = [SpreadSimulator.Point(p.x + point.x, p.y + point.y) for p in points]
        # TODO: rotate the ellipse to meet the aspect of the slope
        return points

    def __ignite_point(self, ignition_point: Point) -> Union[List[Point], None]:
        """
        TODO
        :param ignition_point:
        :type ignition_point:
        :return:
        :rtype:
        """
        # TODO: Get fuel from fuel layer
        return self.__ellipse(ignition_point)

    @staticmethod
    def __create_memory_layer(layer_type: str, name: str) -> QgsVectorLayer:
        project = QgsProject()
        project_instance = project.instance()
        return QgsVectorLayer(layer_type + '?crs=' + project_instance.crs().authid(), name, 'memory')

    def _propagate_perimeter(self, perimeter: List[SpreadSimulator.Point]):
        ds = (2 * numpy.pi) / len(perimeter)
        dt = self._time_step
        dxij = list()
        dyij = list()
        xijp1_bar = list()
        yijp1_bar = list()
        for i in range(0, len(perimeter)):
            if perimeter[i].fuel_model != model_0:
                (rate, alpha, wind) = RateOfSpread.rothermel(fuel_model=perimeter[i].fuel_model,
                                                             moisture=SpreadSimulator.default_moisture,
                                                             wind=SpreadSimulator.default_wind,
                                                             slope=SpreadSimulator.default_slope)
                alpha = -alpha
                (a, b, c) = EllipseAlgorithm.alexander(rate / 60, wind)
                xij = perimeter[i].x
                yij = perimeter[i].y
                xs = (perimeter[(i+1) % len(perimeter)].x - perimeter[i-1].x) / (2 * ds)
                ys = (perimeter[(i+1) % len(perimeter)].y - perimeter[i-1].y) / (2 * ds)
                (xt, yt) = self.__fg(xs, ys, (a, b, c), alpha)
                dxij.append(dt * xt)
                dyij.append(dt * yt)
                xijp1_bar.append(xij + dt * xt)
                yijp1_bar.append(yij + dt * yt)
            else:
                dxij.append(0)
                dyij.append(0)
                xijp1_bar.append(perimeter[i].x)
                yijp1_bar.append(perimeter[i].y)
        dxij_bar = list()
        dyij_bar = list()
        new_perimeter: List[SpreadSimulator.Point] = list()
        for i in range(0, len(perimeter)):
            if perimeter[i].fuel_model != model_0:
                (rate, alpha, wind) = RateOfSpread.rothermel(fuel_model=perimeter[i].fuel_model,
                                                             moisture=SpreadSimulator.default_moisture,
                                                             wind=SpreadSimulator.default_wind,
                                                             slope=SpreadSimulator.default_slope)
                alpha = -alpha
                (a, b, c) = EllipseAlgorithm.alexander(rate / 60, wind)
                xij = perimeter[i].x
                yij = perimeter[i].y
                xs = (xijp1_bar[(i+1) % len(perimeter)] - xijp1_bar[i-1]) / (2 * ds)
                ys = (yijp1_bar[(i+1) % len(perimeter)] - yijp1_bar[i-1]) / (2 * ds)
                if xs != 0 or ys != 0:
                    (xt, yt) = SpreadSimulator.__fg(xs, ys, (a, b, c), alpha)
                    dxij_bar.append(dt * xt)
                    dyij_bar.append(dt * yt)
                    xijp1 = xij + 0.5 * (dxij[i] + dt * xt)
                    yijp1 = yij + 0.5 * (dyij[i] + dt * yt)
                    new_perimeter.append(SpreadSimulator.Point(x=xijp1, y=yijp1))
                else:
                    print("ERROR")
            else:
                dxij_bar.append(0)
                dyij_bar.append(0)
                new_perimeter.append(SpreadSimulator.Point(x=perimeter[i].x, y=perimeter[i].y))
        return new_perimeter

    @staticmethod
    def __fg(xs: float, ys: float, ellipse: Tuple[float, float, float], theta: float) -> Tuple[float, float]:
        """
        TODO:

        :param xs:
        :type xs:
        :param ys:
        :type ys:
        :param ellipse:
        :type ellipse:
        :param theta:
        :type theta:
        :return:
        :rtype:
        """
        (a, b, c) = ellipse
        part1 = (a ** 2) * (math.cos(theta)) * (xs * math.sin(theta) + ys * math.cos(theta))
        part2 = (b ** 2) * (math.sin(theta)) * (xs * math.cos(theta) - ys * math.sin(theta))
        part3 = (b ** 2) * ((xs * math.cos(theta) - ys * math.sin(theta)) ** 2)
        part4 = (a ** 2) * ((xs * math.sin(theta) + ys * math.cos(theta)) ** 2)
        part5 = c * math.sin(theta)
        part6 = math.sqrt(part3 + part4)
        xt = ((part1 - part2) / part6) + part5
        part1 = (a ** 2) * (math.sin(theta)) * (xs * math.sin(theta) + ys * math.cos(theta))
        part2 = (b ** 2) * (math.cos(theta)) * (xs * math.cos(theta) - ys * math.sin(theta))
        part5 = c * math.cos(theta)
        yt = ((-part1 - part2) / part6) + part5
        return xt, yt

    def _get_fire_model(self, x: float, y: float) -> FuelModel:
        """
        TODO:
        :param x:
        :type x:
        :param y:
        :type y:
        :return:
        :rtype:
        """
        # TODO: Get the land cover element ...
        return model_1

    def simulation_step(self):
        # TODO: Remove print
        print("Step start", self._t_now)
        future_time: datetime.datetime = self._t_now + datetime.timedelta(seconds=self._time_step)
        # Create the ignition points list and sort it by ignition date
        ignition_points: List[SpreadSimulator.IgnitionPoint]
        ignition_points = [SpreadSimulator.IgnitionPoint(feature=feature, x=feature.geometry().asPoint().x(),
                                                         y=feature.geometry().asPoint().y(),
                                                         ignition_date=parser.parse(feature.attributes()[1])) for feature
                           in self._ignition_layer.getFeatures()]
        print(self._ignition_layer, ignition_points[0].ignition_date)
        ignition_points.sort()
        # Delete ignition points that ignited prior to the starting date of the simulation
        while (len(ignition_points) > 0) and (ignition_points[0].ignition_date < self._t_now):
            print("delete", ignition_points[0].ignition_date)
            ignition_points.pop(0)
        ignition_points = [point for point in ignition_points if self._t_now <= point.ignition_date < future_time]
        if len(ignition_points) > 0:
            # Compute the perimeter of the ignition point if it has to burn
            ignition_perimeters: List[List[SpreadSimulator.Point]] = list()
            for ignition_point in ignition_points:
                print(ignition_point.ignition_date)
                ignition_point.fuel_model = self._get_fire_model(ignition_point.x, ignition_point.y)
                perimeter = self.__ignite_point(ignition_point)
                if perimeter is not None:
                    ignition_perimeters.append(perimeter)
            # Move perimeters to a QGIS layer
            fields = self._perimeter_layer.fields()
            raw_perimeters_layer: QgsVectorLayer = SpreadSimulator.__create_memory_layer('Polygon', 'raw_perimeters')
            for perimeter in ignition_perimeters:
                qgis_points: List[QgsPointXY] = [QgsPointXY(point.x, point.y) for point in perimeter]
                qgis_feature: QgsFeature = QgsFeature()
                qgis_geometry: QgsGeometry = QgsGeometry.fromPolygonXY([qgis_points]) # NOQA
                qgis_feature.setGeometry(qgis_geometry)
                qgis_data_provider: QgsVectorLayer = raw_perimeters_layer.dataProvider()
                qgis_data_provider.addFeature(qgis_feature) # NOQA
            # Fix geometries
            params = {'INPUT': raw_perimeters_layer, 'OUTPUT': 'memory:'}
            feedback = QgsProcessingFeedback()
            result = processing.run('native:fixgeometries', params, feedback=feedback, is_child_algorithm=False)
            fixed_layer = result['OUTPUT']
            print(result)
            params = {'INPUT': fixed_layer, 'OUTPUT': 'memory:', 'FIELD': None}
            feedback = QgsProcessingFeedback()
            result = processing.run('native:dissolve', params, feedback=feedback, is_child_algorithm=False)
            dissolved_layer = result['OUTPUT']
            print(result)
            params = {'INPUT': dissolved_layer, 'OUTPUT': 'memory:'}
            feedback = QgsProcessingFeedback()
            result = processing.run('native:multiparttosingleparts', params, feedback=feedback, is_child_algorithm=False)
            single_part_layer = result['OUTPUT']
            params = {'INPUT': single_part_layer, 'OUTPUT': 'memory:'}
            feedback = QgsProcessingFeedback()
            result = processing.run('native:forcerhr', params, feedback=feedback, is_child_algorithm=False)
            del fixed_layer
            del dissolved_layer
            del single_part_layer
            with edit(self._perimeter_layer):
                features = list()
                for feature in result['OUTPUT'].getFeatures():
                    feat = QgsFeature()
                    feat.setGeometry(QgsGeometry.fromPolygonXY(feature.geometry().asPolygon()))
                    feat.setFields(fields)
                    feat['datetime'] = future_time.strftime("%Y-%m-%dT%H:%M:%S%Z")
                    features.append(feat)
                (_, _) = self._perimeter_layer.dataProvider().addFeatures(features)
            del result['OUTPUT']
            del raw_perimeters_layer

        # Calculate the propagation perimeters
        propagation_perimeters: List[List[Any]] = list()
        # Filter the perimeters needed to propagate and convert to simple points
        features_of_perimeters_to_propagate = [feature for feature in self._perimeter_layer.getFeatures() if parser.parse(feature.attributes()[1]) == self._t_now]
        for feature in features_of_perimeters_to_propagate:
            # Get the geometries, if a polygon is a list its points define the polygon, if it is a list of lists the
            # first defines the polygon and the other lists the islands. The islands can have polygons inside and so on.
            # So a recursive function is implemented
            propagation_perimeter: List[Any] = list()
            geometry = feature.geometry().asPolygon()
            points: List[SpreadSimulator.Point] = [SpreadSimulator.Point(x=point.x(), y=point.y()) for point in geometry[0]]
            for point in points:
                point.fuel_model = self._get_fire_model(point.x, point.y)
            propagation_perimeter.append(points)
            if len(geometry) > 1: # Has islands
                # TODO: Recursion
                pass
            propagation_perimeters.append(propagation_perimeter)
        if len(propagation_perimeters) > 0:
            # Propagate the perimeters as points
            propagated_perimeters: List[List[Any]] = list()
            for perimeter in propagation_perimeters:
                propagated_perimeter: List[Any] = list()
                new_perimeter = self._propagate_perimeter(perimeter[0][-2::-1])
                propagated_perimeter.append(new_perimeter)
                if len(perimeter) > 1: # Has islands
                    # TODO: Recursion
                    pass
                propagated_perimeters.append(propagated_perimeter)
            # Move perimeters to a QGIS layer
            fields = self._perimeter_layer.fields()
            raw_perimeters_layer: QgsVectorLayer = SpreadSimulator.__create_memory_layer('Polygon', 'raw_perimeters')
            for perimeter in propagated_perimeters:
                qgis_perimeter: List[List[Any]] = list()
                qgis_points: List[QgsPointXY] = [QgsPointXY(point.x, point.y) for point in perimeter[0]]
                qgis_feature: QgsFeature = QgsFeature()
                qgis_perimeter.append(qgis_points)
                if len(perimeter) > 1:
                    # TODO: Recursion
                    pass
                qgis_geometry: QgsGeometry = QgsGeometry.fromPolygonXY(qgis_perimeter) # NOQA
                qgis_feature.setGeometry(qgis_geometry)
                qgis_data_provider: QgsVectorLayer = raw_perimeters_layer.dataProvider()
                qgis_data_provider.addFeature(qgis_feature) # NOQA
            # Fix geometries
            params = {'INPUT': raw_perimeters_layer, 'OUTPUT': 'memory:'}
            feedback = QgsProcessingFeedback()
            result = processing.run('native:fixgeometries', params, feedback=feedback, is_child_algorithm=False)
            fixed_layer = result['OUTPUT']
            print(result)
            params = {'INPUT': fixed_layer, 'OUTPUT': 'memory:', 'FIELD': None}
            feedback = QgsProcessingFeedback()
            result = processing.run('native:dissolve', params, feedback=feedback, is_child_algorithm=False)
            dissolved_layer = result['OUTPUT']
            print(result)
            params = {'INPUT': dissolved_layer, 'OUTPUT': 'memory:'}
            feedback = QgsProcessingFeedback()
            result = processing.run('native:multiparttosingleparts', params, feedback=feedback, is_child_algorithm=False)
            single_part_layer = result['OUTPUT']
            params = {'INPUT': single_part_layer, 'OUTPUT': 'memory:'}
            feedback = QgsProcessingFeedback()
            result = processing.run('native:forcerhr', params, feedback=feedback, is_child_algorithm=False)
            del fixed_layer
            del dissolved_layer
            del single_part_layer
            with edit(self._perimeter_layer):
                features = list()
                for feature in result['OUTPUT'].getFeatures():
                    feat = QgsFeature()
                    feat.setGeometry(QgsGeometry.fromPolygonXY(feature.geometry().asPolygon()))
                    feat.setFields(fields)
                    feat['datetime'] = future_time.strftime("%Y-%m-%dT%H:%M:%S%Z")
                    features.append(feat)
                (_, _) = self._perimeter_layer.dataProvider().addFeatures(features)
            del result['OUTPUT']
            del raw_perimeters_layer

        # Update time
        self._t_now = future_time
        # TODO: Remove print
        print(self._t_now.strftime("%Y-%m-%dT%H:%M:%S%Z"))

