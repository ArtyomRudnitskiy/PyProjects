import numpy
import matplotlib.pyplot as plt
import numexpr as ne

function1 = "sin(2x)cos(3x)-cos(x)^2"
function2 = "(1+x)/(1+2x^3)"

expression1 = "sin(2*x)*cos(3*x)-(cos(x))**2"
expression2 = "(1+x)/(1+2*x**3)"

plt.title(f"Graph of the functions\n y = {function1}\n"
          f"z = {function2}")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid()

x = numpy.arange(-2, 2, 0.1)

plt.plot(x, ne.evaluate(expression1))

x = numpy.arange(1, 2, 0.1)
plt.plot(x, ne.evaluate(expression2))
plt.show()