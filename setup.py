from distutils.core import setup
from Cython.Build import cythonize

setup(name='Data Utils Cython',
      ext_modules=cythonize('utils_cython/data_utils_c.pyx'))