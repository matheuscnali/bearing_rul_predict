import numpy as np    

def derivative(double[:] data, double h):

    # Based on http://web.media.mit.edu/~crtaylor/calculator.html
    cdef int N = len(data)
    cdef double[:] deriv = np.zeros(N-4)
    cdef double den = 12*h

    for i in range(N-4):
        deriv[i] = (-25*data[i]+48*data[i+1]-36*data[i+2]+16*data[i+3]-3*data[i+4])/(den)
    
    return deriv