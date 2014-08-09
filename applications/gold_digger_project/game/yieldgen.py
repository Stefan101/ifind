import random
import math

m = -6  # m is the slope of the linear function


class YieldGenerator(object):
    def __init__(self, depth, max=50, min=0):
        self.depth = depth
        self.max = max
        self.min = min


    def make_yields(self):
        pass


class RandomYieldGenerator(YieldGenerator):

    def make_yields(self):
        """ return a list of Blocks with random yields,
         of length equal to depth
        """
        random_yield_array = []
        for index in range(self.depth):
            random_yield_array.append(random.randint(self.min, self.max))

        return random_yield_array


class ConstantYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) of the same number picked at random in a range

        """
        constant_yield_array = []
        yield_constant = random.randint(self.min, self.max)

        for index in range(self.depth):
            constant_yield_array.append(yield_constant)

        return constant_yield_array

class LinearYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a linear function
        (linear_function(x))
        """
        linear_yield_array = []

        for index in range(self.depth):
            linear_yield_array.append(LinearYieldGenerator.linear_function(index, self.max))

        return linear_yield_array

    @staticmethod
    def linear_function(x, b):
        y = (m*x) + b  # This is the linear yield function

        return y


class QuadraticYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a quadratic function
        (quadratic_function(x, depth))
        """
        quadratic_yield_array = []

        for index in range(self.depth):
            quadratic_yield_array.append(QuadraticYieldGenerator.quadratic_function(index, self.depth))

        return quadratic_yield_array

    @staticmethod
    def quadratic_function(x, x2):
        a = -1.8  # The steepness of the curve
        x1 = 0
        y = a*(x - x1)*(x-x2)

        rounded = int(round(y))
        return rounded


class ExponentialYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to an exponential function
        (exponential_function(x, a))
        """

        exponential_yield_array = []

        for index in range(self.depth):
            exponential_yield_array.append(ExponentialYieldGenerator.exponential_function(index, self.max))

        return exponential_yield_array

    @staticmethod
    def exponential_function(x, a):

        if x == 0:
            y = 0
        else:
            y = a/x

        return y

class CubicYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a cubic function
        (cubic_function(x))
        """

        cubic_yield_array = []

        for index in range(self.depth):
            cubic_yield_array.append(CubicYieldGenerator.cubic_function(index))

        return cubic_yield_array

    @staticmethod
    def cubic_function(x):
        a = 0.5
        c = 0
        y = int(round(pow((a*x), 3) + c*x))

        if y < 0:
            f = 0
            return f

        else:
            return y


class CaliforniaQuadraticYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a quadratic function
        (quadratic_function(x, depth))
        """
        quadratic_yield_array = []

        a = -1*(random.uniform(0.06, 0.09))   # The steepness of the curve
        k = random.randint(10, 18)
        for index in range(self.depth):
            quadratic_yield_array.append(CaliforniaQuadraticYieldGenerator.cali_quadratic_function(index, a, k))

        return quadratic_yield_array

    @staticmethod
    def cali_quadratic_function(x, a, k):

        y = a*(pow((x - 0), 2)) + k

        rounded = int(round(y))
        return rounded


class YukonQuadraticYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a quadratic function
        (quadratic_function(x, depth))
        """
        quadratic_yield_array = []

        a = -1*(random.uniform(0.2, 0.5))   # The steepness of the curve
        k = random.randint(2, 4)

        for index in range(self.depth):
            quadratic_yield_array.append(YukonQuadraticYieldGenerator.yuki_quadratic_function(index, a, k))

        return quadratic_yield_array

    @staticmethod
    def yuki_quadratic_function(x, a, k):

        y = a*(pow((x - k), 2)) + 20

        rounded = int(round(y))
        return rounded


class BrazilQuadraticYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a quadratic function
        (quadratic_function(x, depth))
        """
        quadratic_yield_array = []

        a = -1*(random.uniform(0.8, 1))   # The steepness of the curve
        k = random.randint(30, 34)

        for index in range(self.depth):
            quadratic_yield_array.append(BrazilQuadraticYieldGenerator.brazi_quadratic_function(index, a, k))

        return quadratic_yield_array

    @staticmethod
    def brazi_quadratic_function(x, a, k):


        y = a*(pow((x - 5), 2)) + k

        rounded = int(round(y))
        return rounded


class ScotlandQuadraticYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a quadratic function
        (quadratic_function(x, depth))
        """
        quadratic_yield_array = []

        a = -1*(random.uniform(0.1, 0.2))   # The steepness of the curve
        k = random.randint(35, 39)


        for index in range(self.depth):
            quadratic_yield_array.append(ScotlandQuadraticYieldGenerator.scoti_quadratic_function(index, a, k))

        return quadratic_yield_array

    @staticmethod
    def scoti_quadratic_function(x, a, k):


        y = a*(pow((x - 8), 2)) + k

        rounded = int(round(y))
        return rounded


class SouthAfricaQuadraticYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a quadratic function
        (quadratic_function(x, depth))
        """
        quadratic_yield_array = []

        a = -1*(random.uniform(0.03, 0.05))   # The steepness of the curve
        k = random.randint(25, 28)

        for index in range(self.depth):
            quadratic_yield_array.append(SouthAfricaQuadraticYieldGenerator.sa_quadratic_function(index, a, k))

        return quadratic_yield_array

    @staticmethod
    def sa_quadratic_function(x, a, k):


        y = a*(pow((x - 5), 2)) + k

        rounded = int(round(y))
        return rounded


class VictoriaQuadraticYieldGenerator(YieldGenerator):

    def make_yields(self):
        """
        Returns an array of length (depth) ov values according to a quadratic function
        (quadratic_function(x, depth))
        """
        quadratic_yield_array = []

        a = -1*(random.uniform(0.06, 0.8))   # The steepness of the curve
        k = random.randint(40, 42)

        for index in range(self.depth):
            quadratic_yield_array.append(VictoriaQuadraticYieldGenerator.viki_quadratic_function(index, a, k))

        return quadratic_yield_array

    @staticmethod
    def viki_quadratic_function(x, a, k):

        y = a*(pow((x - 3), 2)) + k

        rounded = int(round(y))
        return rounded