import numpy
import matplotlib.pyplot as plt
import numexpr as ne

function = "-0.00185x^5+0.008x^4+0.27x^3-1.01x^2-4.8x+3.56"
expression = "-0.00185*x**5+0.008*x**4+0.27*x**3-1.01*x**2-4.8*x+3.56"
A = -5
B = 5

plt.title("Graph of the function y = " + function)
plt.xlabel("x")
plt.ylabel("y")
plt.grid()

x = numpy.arange(A, B, 0.1)

plt.plot(x, ne.evaluate(expression))
plt.show()
