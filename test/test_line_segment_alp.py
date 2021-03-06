# -*- coding: utf-8 -*-
#
from __future__ import division

import matplotlib.pyplot as plt
import numpy
import pytest
import sympy

import orthopy


def exact_natural(x):
    sqrt = numpy.vectorize(sympy.sqrt)
    sqrt1mx2 = sqrt(1 - x ** 2)

    p0_0 = 1
    #
    p1p1 = -sqrt1mx2
    p1_0 = x
    p1m1 = -p1p1 / 2
    #
    p2p2 = 3 * (1 - x ** 2)
    p2p1 = -3 * sqrt1mx2 * x
    p2_0 = (3 * x ** 2 - 1) / 2
    p2m1 = -p2p1 / 6
    p2m2 = p2p2 / 24
    #
    p3p3 = -15 * sqrt1mx2 ** 3
    p3p2 = 15 * x * (1 - x ** 2)
    p3p1 = -3 * sqrt1mx2 * (5 * x ** 2 - 1) / 2
    p3_0 = (5 * x ** 3 - 3 * x) / 2
    p3m1 = -p3p1 / 12
    p3m2 = +p3p2 / 120
    p3m3 = -p3p3 / 720
    #
    p4p4 = 105 * (1 - x ** 2) ** 2
    p4p3 = -105 * sqrt1mx2 ** 3 * x
    p4p2 = 15 * (7 * x ** 2 - 1) * (1 - x ** 2) / 2
    p4p1 = -5 * sqrt1mx2 * (7 * x ** 3 - 3 * x) / 2
    p4_0 = (35 * x ** 4 - 30 * x ** 2 + 3) / 8
    p4m1 = -p4p1 / 20
    p4m2 = +p4p2 / 360
    p4m3 = -p4p3 / 5040
    p4m4 = +p4p4 / 40320

    return [
        [p0_0],
        [p1m1, p1_0, p1p1],
        [p2m2, p2m1, p2_0, p2p1, p2p2],
        [p3m3, p3m2, p3m1, p3_0, p3p1, p3p2, p3p3],
        [p4m4, p4m3, p4m2, p4m1, p4_0, p4p1, p4p2, p4p3, p4p4],
    ]


numpy.random.seed(10)


def ff(l, m):
    """factorial(l-m) / factorial(l+m)
    """
    if m > 0:
        return sympy.S(1) / sympy.prod([l - m + 1 + i for i in range(2 * m)])
    return sympy.prod([l - abs(m) + 1 + i for i in range(2 * abs(m))])


@pytest.mark.parametrize(
    "x",
    [
        sympy.S(1) / 10,
        sympy.S(1) / 1000,
        numpy.array([sympy.S(3) / 7, sympy.S(1) / 13]),
    ],
)
@pytest.mark.parametrize(
    "standardization,factor",
    [
        ("natural", lambda L, m: 1),
        (
            "spherical",
            # sqrt((2*L+1) / 4 / pi * factorial(l-m) / factorial(l+m))
            lambda L, m: sympy.sqrt(sympy.S(2 * L + 1) / (4 * sympy.pi) * ff(L, m)),
        ),
        ("normal", lambda L, m: sympy.sqrt(sympy.S(2 * L + 1) / 2 * ff(L, m))),
        ("schmidt", lambda L, m: 2 * sympy.sqrt(ff(L, m))),
    ],
)
def test_exact(x, standardization, factor):
    """Test for the exact values.
    """
    L = 4
    vals = orthopy.line_segment.tree_alp(x, L, standardization, symbolic=True)

    exacts = exact_natural(x)
    exacts = [
        [val * factor(L, m - L) for m, val in enumerate(ex)]
        for L, ex in enumerate(exacts)
    ]

    for val, ex in zip(vals, exacts):
        for v, e in zip(val, ex):
            assert numpy.all(v == e)
    return


def test_plot():
    L = 3
    x = numpy.linspace(-1.0, +1.0, 500)
    vals = orthopy.line_segment.tree_alp(
        x, L, standardization="normal", with_condon_shortley_phase=True, symbolic=False
    )

    for val in vals[L]:
        plt.plot(x, val)

    plt.xlim(-1, +1)
    # plt.ylim(-2, +2)
    plt.tick_params(
        axis="both",
        which="both",
        bottom="off",
        top="off",
        left="off",
        right="off",
        labelbottom="off",
        labelleft="off",
    )
    plt.grid()
    return


if __name__ == "__main__":
    # x_ = 0.43
    # x_ = numpy.random.rand(3, 2)
    # test_unnormalized(x=x_)
    # test_full(x=x_)
    test_plot()
    # plt.show()
    plt.savefig("alp.png", transparent=True)
