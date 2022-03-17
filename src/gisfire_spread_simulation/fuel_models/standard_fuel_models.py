#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fuel_model import FuelModel
from fuel_model import FuelModelType

model_1 = FuelModel(
    code='1',
    name='Short grass',
    fuel_load_1_h=0.74 * FuelModel.TONS_ACRE_TO_LB_FT2,
    fuel_load_10_h=0 * FuelModel.TONS_ACRE_TO_LB_FT2,
    fuel_load_100_h=0 * FuelModel.TONS_ACRE_TO_LB_FT2,
    fuel_load_live_herb=0 * FuelModel.TONS_ACRE_TO_LB_FT2,
    fuel_load_live_wood=0 * FuelModel.TONS_ACRE_TO_LB_FT2,
    sav_ratio_1_h=3500,
    sav_ratio_10_h=109,
    sav_ratio_100_h=30,
    sav_ratio_live_herb=0,
    sav_ratio_live_wood=0,
    fuel_bed_depth=1,
    moisture_of_extinction=0.12,
    sav_ratio=3500,
    bulk_density=0.03,
    relative_packing_ratio=0.25,
    model_type=FuelModelType.STATIC
)

model_2 = FuelModel(
    code='1',
    name='Timber grass and understory',
    fuel_load_1_h=2 * FuelModel.TONS_ACRE_TO_LB_FT2,
    fuel_load_10_h=1 * FuelModel.TONS_ACRE_TO_LB_FT2,
    fuel_load_100_h=0.5 * FuelModel.TONS_ACRE_TO_LB_FT2,
    fuel_load_live_herb=0.5 * FuelModel.TONS_ACRE_TO_LB_FT2,
    fuel_load_live_wood=0 * FuelModel.TONS_ACRE_TO_LB_FT2,
    sav_ratio_1_h=3000,
    sav_ratio_10_h=109,
    sav_ratio_100_h=30,
    sav_ratio_live_herb=1500,
    sav_ratio_live_wood=0,
    fuel_bed_depth=1,
    moisture_of_extinction=0.15,
    sav_ratio=2784,
    bulk_density=0.18,
    relative_packing_ratio=1.14,
    model_type=FuelModelType.STATIC
)

fuel_models = {
    model_1.code: model_1,
    model_2.code: model_2,
}
