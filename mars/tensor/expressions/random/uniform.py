#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2018 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

from .... import operands
from .core import TensorRandomOperandMixin, handle_array


class TensorUniform(operands.Uniform, TensorRandomOperandMixin):
    __slots__ = '_low', '_high', '_size'
    _input_fields_ = ['_low', '_high']

    def __init__(self, size=None, state=None, dtype=None, gpu=None, **kw):
        dtype = np.dtype(dtype) if dtype is not None else dtype
        super(TensorUniform, self).__init__(_size=size, _state=state, _dtype=dtype,
                                            _gpu=gpu, **kw)

    def __call__(self, low, high, chunks=None):
        return self.new_tensor([low, high], None, raw_chunks=chunks)


def uniform(random_state, low=0.0, high=1.0, size=None, chunks=None, gpu=None, **kw):
    r"""
    Draw samples from a uniform distribution.

    Samples are uniformly distributed over the half-open interval
    ``[low, high)`` (includes low, but excludes high).  In other words,
    any value within the given interval is equally likely to be drawn
    by `uniform`.

    Parameters
    ----------
    low : float or array_like of floats, optional
        Lower boundary of the output interval.  All values generated will be
        greater than or equal to low.  The default value is 0.
    high : float or array_like of floats
        Upper boundary of the output interval.  All values generated will be
        less than high.  The default value is 1.0.
    size : int or tuple of ints, optional
        Output shape.  If the given shape is, e.g., ``(m, n, k)``, then
        ``m * n * k`` samples are drawn.  If size is ``None`` (default),
        a single value is returned if ``low`` and ``high`` are both scalars.
        Otherwise, ``mt.broadcast(low, high).size`` samples are drawn.
    chunks : int or tuple of int or tuple of ints, optional
        Desired chunk size on each dimension
    gpu : bool, optional
        Allocate the tensor on GPU if True, False as default

    Returns
    -------
    out : Tensor or scalar
        Drawn samples from the parameterized uniform distribution.

    See Also
    --------
    randint : Discrete uniform distribution, yielding integers.
    random_integers : Discrete uniform distribution over the closed
                      interval ``[low, high]``.
    random_sample : Floats uniformly distributed over ``[0, 1)``.
    random : Alias for `random_sample`.
    rand : Convenience function that accepts dimensions as input, e.g.,
           ``rand(2,2)`` would generate a 2-by-2 array of floats,
           uniformly distributed over ``[0, 1)``.

    Notes
    -----
    The probability density function of the uniform distribution is

    .. math:: p(x) = \frac{1}{b - a}

    anywhere within the interval ``[a, b)``, and zero elsewhere.

    When ``high`` == ``low``, values of ``low`` will be returned.
    If ``high`` < ``low``, the results are officially undefined
    and may eventually raise an error, i.e. do not rely on this
    function to behave when passed arguments satisfying that
    inequality condition.

    Examples
    --------
    Draw samples from the distribution:

    >>> import mars.tensor as mt

    >>> s = mt.random.uniform(-1,0,1000)

    All values are within the given interval:

    >>> mt.all(s >= -1).execute()
    True
    >>> mt.all(s < 0).execute()
    True

    Display the histogram of the samples, along with the
    probability density function:

    >>> import matplotlib.pyplot as plt
    >>> count, bins, ignored = plt.hist(s.execute(), 15, normed=True)
    >>> plt.plot(bins, mt.ones_like(bins).execute(), linewidth=2, color='r')
    >>> plt.show()
    """
    if 'dtype' not in kw:
        kw['dtype'] = np.random.RandomState().uniform(
            handle_array(low), handle_array(high), size=(0,)).dtype
    size = random_state._handle_size(size)
    op = TensorUniform(size=size, state=random_state._state, gpu=gpu, **kw)
    return op(low, high, chunks=chunks)