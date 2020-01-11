from distutils.core import setup
from Cython.Build import cythonize

setup(name='Data Utils Cython',
      ext_modules=cythonize('utils/preprocessing_c.pyx'))