#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union
from enum import Enum


class FuelModelType(Enum):
    STATIC = 1
    DYNAMIC = 2


class FuelModel:
    TONS_ACRE_TO_LB_FT2 = 2000.0 / 43560.0
    METER_SECOND_TO_FEET_MINUTE = 3.28084 * 60
    FEET_TO_METER = 0.3048

    def __init__(self, code: Union[str, None] = None, name: Union[str, None] = None,
                 fuel_load_1_h: Union[float, None] = None, fuel_load_10_h: Union[float, None] = None,
                 fuel_load_100_h: Union[float, None] = None, fuel_load_live_herb: Union[float, None] = None,
                 fuel_load_live_wood: Union[float, None] = None, sav_ratio_1_h: Union[float, None] = None,
                 sav_ratio_10_h: Union[float, None] = None, sav_ratio_100_h: Union[float, None] = None,
                 sav_ratio_live_herb: Union[float, None] = None, sav_ratio_live_wood: Union[float, None] = None,
                 fuel_bed_depth: Union[float, None] = None, moisture_of_extinction: Union[float, None] = None,
                 sav_ratio: Union[float, None] = None, bulk_density: Union[float, None] = None,
                 relative_packing_ratio: Union[float, None] = None, model_type: Union[FuelModelType, None] = None):
        """
        TODO

        :param code:
        :type code:
        :param name:
        :type name:
        :param fuel_load_1_h:
        :type fuel_load_1_h:
        :param fuel_load_10_h:
        :type fuel_load_10_h:
        :param fuel_load_100_h:
        :type fuel_load_100_h:
        :param fuel_load_live_herb:
        :type fuel_load_live_herb:
        :param fuel_load_live_wood:
        :type fuel_load_live_wood:
        :param sav_ratio_1_h:
        :type sav_ratio_1_h:
        :param sav_ratio_10_h:
        :type sav_ratio_10_h:
        :param sav_ratio_100_h:
        :type sav_ratio_100_h:
        :param sav_ratio_live_herb:
        :type sav_ratio_live_herb:
        :param sav_ratio_live_wood:
        :type sav_ratio_live_wood:
        :param fuel_bed_depth:
        :type fuel_bed_depth:
        :param moisture_of_extinction:
        :type moisture_of_extinction:
        :param sav_ratio:
        :type sav_ratio:
        :param bulk_density:
        :type bulk_density:
        :param relative_packing_ratio:
        :type relative_packing_ratio:
        :param model_type:
        :type model_type:
        """
        self._particle_density = 32.
        self._heat_content = 8000.
        self._effective_mineral_content = 0.01
        self._mineral_content = 0.055
        self._code = code
        self._name = name
        self._fuel_load_1_h = fuel_load_1_h
        self._fuel_load_10_h = fuel_load_10_h
        self._fuel_load_100_h = fuel_load_100_h
        self._fuel_load_live_herb = fuel_load_live_herb
        self._fuel_load_live_wood = fuel_load_live_wood
        self._sav_ratio_1_h = sav_ratio_1_h
        self._sav_ratio_10_h = sav_ratio_10_h
        self._sav_ratio_100_h = sav_ratio_100_h
        self._sav_ratio_live_herb = sav_ratio_live_herb
        self._sav_ratio_live_wood = sav_ratio_live_wood
        self._fuel_bed_depth = fuel_bed_depth
        self._moisture_of_extinction = moisture_of_extinction
        self._sav_ratio = sav_ratio
        self._bulk_density = bulk_density
        self._relative_packing_ratio = relative_packing_ratio
        self._model_type = model_type

    @property
    def particle_density(self) -> float:
        return self._particle_density

    @particle_density.setter
    def particle_density(self, pd: float) -> None:
        self._particle_density = pd

    @property
    def heat_content(self) -> float:
        return self._heat_content

    @heat_content.setter
    def heat_content(self, hc: float) -> None:
        self._heat_content = hc

    @property
    def effective_mineral_content(self) -> float:
        return self._effective_mineral_content

    @effective_mineral_content.setter
    def effective_mineral_content(self, emc: float) -> None:
        self._effective_mineral_content = emc

    @property
    def mineral_content(self) -> float:
        return self._mineral_content

    @mineral_content.setter
    def mineral_content(self, mc: float) -> None:
        self._mineral_content = mc

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str) -> None:
        self._code = code

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def fuel_load_1_h(self) -> float:
        return self._fuel_load_1_h

    @fuel_load_1_h.setter
    def fuel_load_1_h(self, fuel_load_1_h: float) -> None:
        self._fuel_load_1_h = fuel_load_1_h

    @property
    def fuel_load_10_h(self) -> float:
        return self._fuel_load_10_h

    @fuel_load_10_h.setter
    def fuel_load_10_h(self, fuel_load_10_h: float) -> None:
        self._fuel_load_10_h = fuel_load_10_h

    @property
    def fuel_load_100_h(self) -> float:
        return self._fuel_load_100_h

    @fuel_load_100_h.setter
    def fuel_load_100_h(self, fuel_load_100_h: float) -> None:
        self._fuel_load_100_h = fuel_load_100_h

    @property
    def fuel_load_live_herb(self) -> float:
        return self._fuel_load_live_herb

    @fuel_load_live_herb.setter
    def fuel_load_live_herb(self, fuel_load_live_herb: float) -> None:
        self._fuel_load_live_herb = fuel_load_live_herb

    @property
    def fuel_load_live_wood(self) -> float:
        return self._fuel_load_live_wood

    @fuel_load_live_wood.setter
    def fuel_load_live_wood(self, fuel_load_live_wood: float) -> None:
        self._fuel_load_live_wood = fuel_load_live_wood

    @property
    def sav_ratio_1_h(self) -> float:
        return self._sav_ratio_1_h

    @sav_ratio_1_h.setter
    def sav_ratio_1_h(self, sav_ratio_1_h: float) -> None:
        self._sav_ratio_1_h = sav_ratio_1_h

    @property
    def sav_ratio_10_h(self) -> float:
        return self._mineral_content

    @sav_ratio_10_h.setter
    def sav_ratio_10_h(self, sav_ratio_10_h: float) -> None:
        self._sav_ratio_10_h = sav_ratio_10_h

    @property
    def sav_ratio_100_h(self) -> float:
        return self._mineral_content

    @sav_ratio_100_h.setter
    def sav_ratio_100_h(self, sav_ratio_100_h: float) -> None:
        self._sav_ratio_100_h = sav_ratio_100_h

    @property
    def sav_ratio_live_herb(self) -> float:
        return self._sav_ratio_live_herb

    @sav_ratio_live_herb.setter
    def sav_ratio_live_herb(self, sav_ratio_live_herb: float) -> None:
        self._sav_ratio_live_herb = sav_ratio_live_herb

    @property
    def sav_ratio_live_wood(self) -> float:
        return self._sav_ratio_live_wood

    @sav_ratio_live_wood.setter
    def sav_ratio_live_wood(self, sav_ratio_live_wood: float) -> None:
        self._sav_ratio_live_wood = sav_ratio_live_wood

    @property
    def fuel_bed_depth(self) -> float:
        return self._fuel_bed_depth

    @fuel_bed_depth.setter
    def fuel_bed_depth(self, fuel_bed_depth: float) -> None:
        self._fuel_bed_depth = fuel_bed_depth

    @property
    def moisture_of_extinction(self) -> float:
        return self._moisture_of_extinction

    @moisture_of_extinction.setter
    def moisture_of_extinction(self, moisture_of_extinction: float) -> None:
        self._moisture_of_extinction = moisture_of_extinction

    @property
    def sav_ratio(self) -> float:
        return self._sav_ratio

    @sav_ratio.setter
    def sav_ratio(self, sav_ratio: float) -> None:
        self._sav_ratio = sav_ratio

    @property
    def bulk_density(self) -> float:
        return self._bulk_density

    @bulk_density.setter
    def bulk_density(self, bulk_density: float) -> None:
        self._bulk_density = bulk_density

    @property
    def relative_packing_ratio(self) -> float:
        return self._relative_packing_ratio

    @relative_packing_ratio.setter
    def relative_packing_ratio(self, relative_packing_ratio: float) -> None:
        self._relative_packing_ratio = relative_packing_ratio

    @property
    def model_type(self) -> FuelModelType:
        return self._model_type

    @model_type.setter
    def model_type(self, model_type: FuelModelType) -> None:
        self._model_type = model_type

