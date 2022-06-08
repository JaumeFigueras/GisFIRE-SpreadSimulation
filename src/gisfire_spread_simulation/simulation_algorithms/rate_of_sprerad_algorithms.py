#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gisfire_spread_simulation.fuel_models.fuel_model import FuelModel
from typing import Tuple
from typing import Union
from typing import List
from math import exp
from math import pow
from math import tan
from math import cos
from math import sin
from math import atan2


class RateOfSpread:
    FEET_TO_METER = 0.3048
    METER_SECOND_TO_FEET_MINUTE = 3.28084 * 60

    # noinspection SpellCheckingInspection
    @staticmethod
    def rothermel(fuel_model: Union[FuelModel, None] = None,
                  moisture: Union[Tuple[Tuple[float, float, float], Tuple[float, float]], None] = None,
                  wind: Union[Tuple[float, float], float, None] = None, slope: Union[float, None] = None) \
            -> Union[float, Tuple[float, float, float]]:
        """
        TODO
        :param fuel_model:
        :type fuel_model: FuelModel
        :param moisture: Fuel moisture content for the different fuel classes
        :type moisture: Tuple[Tuple[float, float, float], Tuple[float, float]]
        :param wind:
        :type wind:
        :param slope:
        :type slope:
        :return:
        :rtype:
        """
        # Vectorice the "Surface to Volume Ratio" of the fire model provided. This value is sigma in the formulation
        sav_ratio: Tuple[Tuple[float, float, float], Tuple[float, float]] = \
            ((fuel_model.sav_ratio_1_h, fuel_model.sav_ratio_10_h, fuel_model.sav_ratio_100_h),
             (fuel_model.sav_ratio_live_herb, fuel_model.sav_ratio_live_wood))
        # Vectorice the "Oven Dry Fuel Load" of the provided model. This value is w sub 0
        fuel_load: Tuple[Tuple[float, float, float], Tuple[float, float]] = \
            ((fuel_model.fuel_load_1_h, fuel_model.fuel_load_10_h, fuel_model.fuel_load_100_h),
             (fuel_model.fuel_load_live_herb, fuel_model.fuel_load_live_wood))
        # Mean total surface area per unit fuel cell of each size class within each category. (Andrews 2018, pg. 17)
        # Although the formula uses the particle density for each categoru (ro sub i, j) the fire models consider it
        # constant for all categories and equal to 32 lb/ft³
        a_ij: List[List[float]] = [[0] * 3, [0] * 2]
        for i in range(0, 2):
            for j in range(0, len(a_ij[i])):
                a_ij[i][j] = (sav_ratio[i][j] * fuel_load[i][j]) / fuel_model.particle_density
        # Mean total surface area of the live and dead categories. (Andrews 2018, pg. 17)
        a_i: Tuple[float, float] = (sum(a_ij[0]), sum(a_ij[1]))
        # Mean total surface area of the fuel. (Andrews 2018, pg. 17)
        a_t: float = sum(a_i)
        # Weighting factor for characteristic dead and live heat content, effective mineral content, moisture content,
        # and surface-area-to-volume ratio. (Andrews 2018, pg. 17)
        f_ij: List[List[float]] = [[0] * 3, [0] * 2]
        for i in range(0, 2):
            for j in range(0, len(f_ij[i])):
                f_ij[i][j] = a_ij[i][j] / a_i[i] if a_i[i] > 0 else 0
        # Weighting factor for characteristic fuel bed surface-area-to-volume ratio. (Andrews 2018, pg. 17)
        f_i: Tuple[float, float] = (a_i[0] / a_t, a_i[1] / a_t)
        # Surface-area-to-volume ratio (ft²/ft³). (Andrews 2018, pg. 18)
        # In the formulation is identified by sigma sub i
        # noinspection DuplicatedCode
        sav_ratio_i: Tuple[float, float] = (
            f_ij[0][0] * sav_ratio[0][0] + f_ij[0][1] * sav_ratio[0][1] + f_ij[0][2] * sav_ratio[0][2],
            f_ij[1][0] * sav_ratio[1][0] + f_ij[1][1] * sav_ratio[1][1])
        # Surface-area-to-volume ratio (ft²/ft³). (Andrews 2018, pg. 18)
        # In the formulation is identified by sigma
        mean_sav_ratio: float = f_i[0] * sav_ratio_i[0] + f_i[1] * sav_ratio_i[1]
        # Mean bulk density (lb/ft³). (Andrews 2018, pg. 18)
        # The formulation says that is the sum of the sum all the Oven-dry fuel load (w sub 0) divided by delta, the
        # fuel bed depth
        mean_bulk_density: float = (sum(fuel_load[0]) + sum(fuel_load[1])) / fuel_model.fuel_bed_depth
        # Mean packing ratio. (Andrews 2018, pg. 18)
        # As all classes have the same particle density it can be moved out of the sumations simplifying the formula
        mean_packing_ratio: float = mean_bulk_density / fuel_model.particle_density
        # Propagating flux ratio. (Andrews 2018, pg. 19)
        propagating_flux_ratio: float = exp((0.792 + 0.681 * pow(mean_sav_ratio, 0.5)) * (0.1 + mean_packing_ratio)) *\
            pow((192 + 0.2595 * mean_sav_ratio), -1)
        # Optimum reaction velocity (min⁻¹) A exponent. (Andrews 2018, pg. 19)
        a: float = 133 * pow(mean_sav_ratio, -0.7913)
        # Optimum packing ratio. (Andrews 2018, pg. 18)
        # Beta sub opt in the formulation
        mean_optimal_packing_ratio: float = 3.348 * pow(mean_sav_ratio, -0.8189)
        # Maximum reaction velocity (min⁻¹). (Andrews 2018, pg. 19)
        # Capital Gamma prima max in the formulation
        mean_maximum_reaction_velocity: float = pow(mean_sav_ratio, 1.5) / (495 + 0.0594 * pow(mean_sav_ratio, 1.5))
        # Optimum reaction velocity (min⁻¹). (Andrews 2018, pg. 19)
        # Capital Gamma prima in the formulation
        mean_optimal_reaction_velocity: float = mean_maximum_reaction_velocity * \
            pow((mean_packing_ratio / mean_optimal_packing_ratio), a) * \
            exp(a * (1 - (mean_packing_ratio / mean_optimal_packing_ratio)))
        # Net fuel load (lb/ft²). (Andrews 2018, pg. 18)
        net_fuel_load: List[List[float]] = [[0] * 3, [0] * 2]
        for i in range(0, len(net_fuel_load)):
            for j in range(0, len(net_fuel_load[i])):
                net_fuel_load[i][j] = fuel_load[i][j] * (1 - fuel_model.mineral_content)
        # Dead fraction net fuel load (lb/ft²). (Andrews 2018, pg. 18)
        # In Andrews explain the g_ij categorization of the f_ij, but as for dead always each of the 3 possible values
        # fall in different categories for all models it is not necesdsary to calculate g and use directly f
        net_fuel_load_dead: float = f_ij[0][0] * net_fuel_load[0][0] + f_ij[0][1] * net_fuel_load[0][1] + f_ij[0][2] * \
            net_fuel_load[0][2]
        # Live fraction net fuel load (lb/ft²). (Andrews 2018, pg. 18)
        # In Andrews explain the g_ij categorization of the f_ij, but as for life always each of the 2 possible values
        # fall in the same categories for all models it is not necesdsary to calculate g because it wil be always 1 (the
        # sum of f weights of live fuels)
        net_fuel_load_live: float = net_fuel_load[1][0] + net_fuel_load[1][1]
        # Heat content (Btu/lb). (Andrews 2018, pg. 18)
        heat_content_i: Tuple[float, float] = (fuel_model.heat_content * sum(f_ij[0]),
                                               fuel_model.heat_content * sum(f_ij[1]))
        # Moisture content (fraction). (Andrews 2018, pg. 18)
        # noinspection DuplicatedCode
        fuel_moisrute_i: Tuple[float, float] = (f_ij[0][0] * moisture[0][0] + f_ij[0][1] * moisture[0][1] +
                                                f_ij[0][2] * moisture[0][2],
                                                f_ij[1][0] * moisture[1][0] + f_ij[1][1] * moisture[1][1])
        # Live fuel moisture of extinction (fraction). Dead-to-live load ratio W numerator part calculation.
        # (Andrews 2018, pg. 17)
        w_num: float = 0
        for j in range(0, len(sav_ratio[0])):
            if sav_ratio[0][j] > 0:
                w_num += fuel_load[0][j] * exp(-138 / sav_ratio[0][j])
        # Live fuel moisture of extinction (fraction). Dead-to-live load ratio W denominator part calculation.
        # (Andrews 2018, pg. 17)
        w_den: float = 0
        for j in range(0, len(sav_ratio[1])):
            if sav_ratio[1][j] > 0:
                w_den += fuel_load[1][j] * exp(-500 / sav_ratio[1][j])
        # Live fuel moisture of extinction (fraction). Dead-to-live load ratio W calculation. (Andrews 2018, pg. 17)
        w: float = w_num / w_den if w_den > 0 else 0
        # Live fuel moisture of extinction (fraction). "Fine" dead fuel moisture M sub f dead calculation.
        # (Andrews 2018, pg. 17)
        mf_dead: float = ((moisture[0][0] * fuel_load[0][0] * exp(-138 / sav_ratio[0][0])) +
                          (moisture[0][1] * fuel_load[0][1] * exp(-138 / sav_ratio[0][1])) +
                          (moisture[0][2] * fuel_load[0][2] * exp(-138 / sav_ratio[0][2]))) / \
                         ((fuel_load[0][0] * exp(-138 / sav_ratio[0][0])) +
                          (fuel_load[0][1] * exp(-138 / sav_ratio[0][1])) +
                          (fuel_load[0][2] * exp(-138 / sav_ratio[0][2])))
        # Live fuel moisture of extinction (fraction). (Andrews 2018, pg. 17)
        live_moisture_of_extinction: float = max(2.9 * w * (1 - (mf_dead / fuel_model.moisture_of_extinction)) - 0.226,
                                                 fuel_model.moisture_of_extinction)
        # Moisture damping coefficient (part 1). (Andrews 2018, pg. 18)
        moisture_relation_i: Tuple[float, float] = (min(1.0, fuel_moisrute_i[0] / fuel_model.moisture_of_extinction),
                                                    min(1.0, fuel_moisrute_i[1] / live_moisture_of_extinction))
        # Moisture damping coefficient (part 2). (Andrews 2018, pg. 18)
        moisture_damping_i: List[float] = [0] * 2
        for i in range(0, 2):
            moisture_damping_i[i] = 1 - 2.59 * moisture_relation_i[i] + 5.11 * pow(moisture_relation_i[i], 2) - \
                                    3.52 * pow(moisture_relation_i[i], 3)
        # Mineral damping coefficient. (Andrews 2018, pg. 18)
        mineral_damping: float = min(1.0, 0.174 * pow(fuel_model.effective_mineral_content, -0.19))
        # Reaction intensity (dead fuel). (Andrews 2018, pg. 19)
        intensity_reaction_a: float = net_fuel_load_dead * heat_content_i[0] * moisture_damping_i[0] * mineral_damping
        # Reaction intensity (live fuel). (Andrews 2018, pg. 19)
        intensity_reaction_b: float = net_fuel_load_live * heat_content_i[1] * moisture_damping_i[1] * mineral_damping
        # Reaction intensity (Btu/ft -min). (Andrews 2018, pg. 19)
        intensity_reaction: float = mean_optimal_reaction_velocity * (intensity_reaction_a + intensity_reaction_b)
        # Heat of preignition for each size class, live and dead (Btu/lb). (Andrews 2018, pg. 19)
        heat_of_preignition_ij: List[List[float]] = [[0] * 3, [0] * 2]
        for i in range(0, 2):
            for j in range(0, len(heat_of_preignition_ij[i])):
                heat_of_preignition_ij[i][j] = 250 + 1116 * moisture[i][j]
        # Heat sink (Btu/ft³) summation. (Andrews 2018, pg. 19)
        heat_number_tmp: List[float] = [0] * 2
        for i in range(0, len(heat_number_tmp)):
            heat_number_tmp[i] = f_i[i] * sum([a * (exp(-138 / b) if b > 0 else 0) * c for a, b, c in
                                              zip(f_ij[i], sav_ratio[i], heat_of_preignition_ij[i])])
        # Heat sink (Btu/ft³). (Andrews 2018, pg. 19)
        heat_sink: float = mean_bulk_density * sum(heat_number_tmp)
        # Wind factor pre-calculations. (Andrews 2018, pg. 18)
        c: float = 7.47 * exp(-0.133 * pow(mean_sav_ratio, 0.55))
        b: float = 0.02526 * pow(mean_sav_ratio, 0.54)
        e: float = 0.715 * exp(-3.59e-4 * mean_sav_ratio)
        # Slope factor. (Andrews 2018, pg. 18)
        slope_factor: float = 5.275 * pow(mean_packing_ratio, -0.3) * pow(tan(slope), 2)
        # If the wind is a scalar it means that the wind blows in the same direction as the slope and therefore no
        # vector calculations are needed to determine the final fire direction. If the wind is a tuple or list with 2
        # elements, then the first element is the magnitude and the second the angle, and the vector product with the
        # ROS has to be calculated
        if isinstance(wind, (int, float)):
            # Convert from m/s to imperial units
            wind = wind * RateOfSpread.METER_SECOND_TO_FEET_MINUTE
            # Add the wind limit. (Andrews 2018, pg. 25)
            limited_wind = min(wind, 96.8 * pow(intensity_reaction, 1/3))
            # Wind factor. (Andrews 2018, pg. 18)
            wind_factor = c * pow(limited_wind, b) * pow(mean_packing_ratio / mean_optimal_packing_ratio, -e)
            # Finally, compute the rate of spread. (Andrews 2018, pg. 19)
            rate_of_spread = (intensity_reaction * propagating_flux_ratio * (1 + wind_factor + slope_factor)) / (
                heat_sink)
            return rate_of_spread * RateOfSpread.FEET_TO_METER
        else:
            # Convert from m/s to imperial units
            wind_feet_minute: float = wind[0] * RateOfSpread.METER_SECOND_TO_FEET_MINUTE
            # Add the wind limit. (Andrews 2018, pg. 25)
            limited_wind = min(wind_feet_minute, 96.8 * pow(intensity_reaction, 1 / 3))
            # Wind factor. (Andrews 2018, pg. 18)
            wind_factor = c * pow(limited_wind, b) * pow(mean_packing_ratio / mean_optimal_packing_ratio, -e)
            # Finally, compute the rate of spread. (Andrews 2018, pg. 19)
            rate_of_spread = (intensity_reaction * propagating_flux_ratio) / heat_sink
            # Compute the compound product of two vectors. (Andrews 2018, pg. 85-88)
            d_s = rate_of_spread * slope_factor
            d_w = rate_of_spread * wind_factor
            d_h = pow((d_s + d_w * cos(wind[1])) ** 2 + (d_w * sin(wind[1]) ** 2), 0.5)
            composite_rate_of_spread = rate_of_spread + d_h
            # Calculate the resulting angle. (Andrews 2018, pg. 85-88)
            alpha = atan2(d_w * sin(wind[1]), d_s + d_w * cos(wind[1]))
            # Calculate the effective wind factor. (Andrews 2018, pg. 85-88)
            effective_wind_factor = (composite_rate_of_spread / rate_of_spread) - 1
            effective_wind_speed = pow(effective_wind_factor *
                                       pow(mean_packing_ratio / mean_optimal_packing_ratio, e) / c,
                                       1 / b)
            return (composite_rate_of_spread * RateOfSpread.FEET_TO_METER,
                    alpha,
                    effective_wind_speed * (1 / RateOfSpread.METER_SECOND_TO_FEET_MINUTE))
