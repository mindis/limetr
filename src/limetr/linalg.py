# -*- coding: utf-8 -*-
"""
    limetr.linalg
    ~~~~~~~~~~~~~

    Linear algebra class for limetr object
"""
import numpy as np


class LinearMap:
    """Linear map class, conduct dot product when do not have function form
    only support matrix vector multiplication
    """
    def __init__(self, shape, mv_dot, trans_mv_dot=None):
        self.shape = shape
        self.mv_dot = mv_dot
        self.trans_mv_dot = trans_mv_dot

    def dot(self, x):
        return self.mv_dot(x)

    @property
    def mat(self):
        return np.vstack([self.dot(np.eye(1, np.shape[1], i))
                          for i in range(self.shape[1])]).T

    @property
    def T(self):
        if self.trans_mv_dot is None:
            return None
        else:
            return LinearMap((self.shape[1], self.shape[0]),
                             self.trans_mv_dot,
                             trans_mv_dot=self.mv_dot)


class SmoothFunction:
    """Smooth function class, include function mapping and
    Jacobian matrix or its LinearMap object
    """
    def __init__(self, shape, fun, jac_mat=None, jac_fun=None):
        # check the input
        assert jac_mat is not None or jac_fun is not None
        # pass in the data
        self.shape = shape
        self.fun = fun
        self.jac_mat = jac_mat
        self.jac_fun = jac_fun
        if self.jac_mat is not None:
            self.jac_type = 'jac_mat'
            self.jac = self.jac_mat
        else:
            self.jac_type = 'jac_fun'
            self.jac = self.jac_fun

    def check(self):
        """check the output dimension"""
        x = np.zeros(self.shape[1])
        fun_result = self.fun(x)
        jac_result = self.jac(x)
        assert type(fun_result) == np.ndarray
        assert fun_result.shape == (self.shape[0],)
        if self.jac_type == 'jac_mat':
            assert type(jac_result) == np.ndarray
            assert jac_result.shape == self.shape
        else:
            assert type(jac_result) == LinearMap
            assert jac_result.shape == self.shape
