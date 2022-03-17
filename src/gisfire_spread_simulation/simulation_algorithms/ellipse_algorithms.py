#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Tuple
from math import exp
from math import pow


class EllipseAlgorithm:

    # noinspection PyPep8Naming
    @staticmethod
    def alexander(ros: float, Ue: float) -> Tuple[float, float, float]:
        """
        TODO
        :param ros:
        :type ros:
        :param Ue:
        :type Ue:
        :return:
        :rtype:
        """
        LB = 0.936 * exp(0.2566 * Ue) + 0.461 * exp(-0.1548 * Ue) - 0.397
        HB = (LB + pow(pow(LB, 2) - 1, 0.5)) / (LB - pow(pow(LB, 2) - 1, 0.5))
        a = 0.5 * (ros + ros / HB) / LB
        b = (ros + ros / HB) / 2
        c = b - ros / HB
        return a, b, c

    # noinspection PyPep8Naming,SpellCheckingInspection
    @staticmethod
    def catchpole(ros: float, Ue: float) -> Tuple[float, float, float]:
        """

        :param ros:
        :type ros:
        :param Ue:
        :type Ue:
        :return:
        :rtype:
        """
        Z = 1 + 0.25 * Ue
        e = pow((Z ** 2 - 1), 0.5) / Z
        Rh = ros
        Rb = Rh * (1 - e) / (1 + e)
        L = Rh + Rb
        W = L / Z
        f = L / 2
        h = W / 2
        g = Rh - f
        return h, f, g
