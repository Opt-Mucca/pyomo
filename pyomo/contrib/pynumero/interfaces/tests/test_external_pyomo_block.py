#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import itertools
import pyomo.common.unittest as unittest
from pyomo.common.collections import ComponentSet, ComponentMap
import pyomo.environ as pyo

from pyomo.contrib.pynumero.dependencies import (
    numpy as np, numpy_available, scipy, scipy_available
)

if not (numpy_available and scipy_available):
    raise unittest.SkipTest("Pynumero needs scipy and numpy to run NLP tests")

from pyomo.common.dependencies.scipy import sparse as sps

from pyomo.contrib.pynumero.asl import AmplInterface
if not AmplInterface.available():
    raise unittest.SkipTest(
        "Pynumero needs the ASL extension to run cyipopt tests")

from pyomo.contrib.pynumero.algorithms.solvers.cyipopt_solver import (
    cyipopt_available,
)
from pyomo.contrib.pynumero.interfaces.external_pyomo_model import (
    ExternalPyomoModel,
    get_hessian_of_constraint,
)
from pyomo.contrib.pynumero.interfaces.external_grey_box import (
    ExternalGreyBoxBlock,
    ScalarExternalGreyBoxBlock,
    IndexedExternalGreyBoxBlock,
)

if not pyo.SolverFactory("ipopt").available():
    raise unittest.SkipTest(
        "Need IPOPT to run ExternalPyomoModel tests"
        )


def make_external_model():
    m = pyo.ConcreteModel()
    m.a = pyo.Var()
    m.b = pyo.Var()
    m.r = pyo.Var()
    m.x = pyo.Var()
    m.y = pyo.Var()
    m.x_out = pyo.Var()
    m.y_out = pyo.Var()
    m.c_out_1 = pyo.Constraint(expr=m.x_out == m.x)
    m.c_out_2 = pyo.Constraint(expr=m.y_out == m.y)
    m.c_ex_1 = pyo.Constraint(expr=
            m.a + m.b ==
            1 + 0.5*m.x + 3*m.x**2 - 2*m.x**3 + 0.1*m.x**4 - 0.1*m.x**5
            )
    m.c_ex_2 = pyo.Constraint(expr=m.r == m.x*m.y)
    return m


class TestExternalGreyBoxBlock(unittest.TestCase):

    def test_construct_scalar(self):
        block = ExternalGreyBoxBlock(concrete=True)
        self.assertIs(type(block), ScalarExternalGreyBoxBlock)

        m = make_external_model()
        input_vars = [m.a, m.b, m.r, m.x_out, m.y_out]
        external_vars = [m.x, m.y]
        residual_cons = [m.c_out_1, m.c_out_2]
        external_cons = [m.c_ex_1, m.c_ex_2]
        ex_model = ExternalPyomoModel(
                input_vars,
                external_vars,
                residual_cons,
                external_cons,
                )
        block.set_external_model(ex_model)

        self.assertEqual(len(block.inputs), len(input_vars))
        self.assertEqual(len(block.outputs), 0)
        self.assertEqual(len(block._equality_constraint_names), 2)

#    def test_construct_indexed(self):
#        block = ExternalGreyBoxBlock([0, 1, 2], concrete=True)
#        self.assertIs(type(block), IndexedExternalGreyBoxBlock)
#
#        m = make_external_model()
#        input_vars = [m.a, m.b, m.r, m.x_out, m.y_out]
#        external_vars = [m.x, m.y]
#        residual_cons = [m.c_out_1, m.c_out_2]
#        external_cons = [m.c_ex_1, m.c_ex_2]
#        ex_model = ExternalPyomoModel(
#                input_vars,
#                external_vars,
#                residual_cons,
#                external_cons,
#                )
#
#        for i in block:
#            b = block[i]
#            b.set_external_model(ex_model)
#            self.assertEqual(len(b.inputs), len(input_vars))
#            self.assertEqual(len(b.outputs), 0)
#            self.assertEqual(len(b._equality_constraint_names), 2)

"""
The ExternalGreyBoxModel doesn't do much with the external model. It
is mostly an intermediate between the external model and the NLP, which
is created by the CyIpopt solver?
^ This work is done during the cyipopt solver's solve method, which is
unfortunate. It makes this somewhat hard to test...

What data from the ExternalGreyBoxBlock is used where?
"""


if __name__ == '__main__':
    unittest.main()
