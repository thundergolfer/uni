"""
Pure-Python3 implementation of Gradient Descent (https://en.wikipedia.org/wiki/Gradient_descent).
Written for educational/learning purposes and not performance.

Completed as part of the UTS course '35512 - Modelling Change' (https://handbook.uts.edu.au/subjects/35512.html).
"""
import random
from typing import List, Mapping, Optional, Dict, Set, Tuple


# Used to make chars like 'x' resemble typical mathematical symbols.
def _italic_str(text: str) -> str:
    return f"\x1B[3m{text}\x1B[23m"


def _superscript_exp(n: str) -> str:
    return "".join(["⁰¹²³⁴⁵⁶⁷⁸⁹"[ord(c) - ord('0')] for c in str(n)])


class Variable:
    """
    A object representing a mathematical variable, for use in building expressions.

    Usage: `x = Variable("x")`
    """
    def __init__(self, var: str):
        if len(var) != 1 or (not var.isalpha()):
            raise ValueError("Variable must be single alphabetical character. eg. 'x'")
        self.var = var

    def __repr__(self):
        return _italic_str(self.var)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Variable):
            return self.var == other.var
        return False

    def __key(self):
        return self.var

    def __hash__(self):
        return hash(self.__key())


# An element of some set called a space. Here, that 'space' will be the domain of a multi-variable function.
Point = Dict[Variable, float]


class Expression:
    def diff(self, ref_var: Optional[Variable] = None) -> Optional["Expression"]:
        raise NotImplementedError

    def evaluate(self, point: Point) -> float:
        raise NotImplementedError


class ConstantExpression(Expression):
    """
    ConstantExpression is a single real-valued number.
    It cannot be parameterised and it's first-derivative is always 0 (None).
    """

    def __init__(self, real: float):
        super().__init__()
        self.real = real

    def diff(self, ref_var: Optional[Variable] = None) -> Optional[Expression]:
        return None

    def evaluate(self, point: Point) -> float:
        return self.real

    def __repr__(self):
        return str(self.real)


class PolynomialExpression(Expression):
    """
    An expression object that support evaluation and differentiation of single-variable polynomials.
    """
    def __init__(
            self,
            variable: Variable,
            coefficient: float,
            exponent: int
    ):
        super().__init__()
        self.var = variable
        self.coefficient = coefficient
        self.exp = exponent

    def diff(self, ref_var: Optional[Variable] = None) -> Optional[Expression]:
        if ref_var and ref_var != self.var:
            return None
        if self.exp == 1:
            return ConstantExpression(real=self.coefficient)
        return PolynomialExpression(
            variable=self.var,
            coefficient=self.coefficient * self.exp,
            exponent=self.exp - 1,
        )

    def evaluate(self, point: Point) -> float:
        return (
                self.coefficient *
                point[self.var] ** self.exp
        )

    def __repr__(self):
        return f"{self.coefficient}{self.var}{_superscript_exp(str(self.exp))}"


class Multiply(Expression):
    def __init__(self, a: PolynomialExpression, b: PolynomialExpression):
        self.a = a
        self.b = b

    def diff(self, ref_var: Optional[Variable] = None) -> Optional["Expression"]:
        if not ref_var:
            raise RuntimeError("Must pass ref_var when differentiating Multiply expression")
        if self.a.var == ref_var:
            diff_a = self.a.diff(ref_var=ref_var)
            if not diff_a:
                return None
            else:
                return Multiply(a=diff_a, b=self.b)
        elif self.b.var == ref_var:
            diff_b = self.b.diff(ref_var=ref_var)
            if not diff_b:
                return None
            else:
                return Multiply(a=self.a, b=diff_b)
        else:
            return None  # diff with respect to some non-involved variable is 0

    def evaluate(self, point: Point) -> float:
        return self.a.evaluate(point) * self.b.evaluate(point)

    def __repr__(self):
        return f"({self.a})({self.b})"


GradientVector = Dict[Variable, "MultiVariableFunction"]


class MultiVariableFunction:
    """
    MultiVariableFunction support the composition of expressions by addition into a
    function of multiple real-valued variables.

    Partial differentiation with respect to a single variable is supported, as is
    evaluation at a Point, and gradient finding.
    """

    def __init__(self, variables: Set[Variable], expressions: List[Expression]):
        self.vars = variables
        self.expressions = expressions

    def gradient(self) -> GradientVector:
        grad_v: GradientVector = {}
        for v in self.vars:
            grad_v[v] = self.diff(ref_var=v)
        return grad_v

    def diff(self, ref_var: Variable) -> "MultiVariableFunction":
        first_partial_derivatives: List[Expression] = []
        for expression in self.expressions:
            first_partial_diff = expression.diff(ref_var=ref_var)
            if first_partial_diff:
                first_partial_derivatives.append(first_partial_diff)
        return MultiVariableFunction(
            variables=self.vars,
            expressions=first_partial_derivatives,
        )

    def evaluate(self, point: Point) -> float:
        return sum(
            expression.evaluate(point)
            for expression
            in self.expressions
        )

    def __repr__(self):
        return " + ".join([str(e) for e in self.expressions])


def gradient_descent(
    gamma: float,
    max_iterations: int,
    f: MultiVariableFunction,
    initial_point: Optional[Point] = None,
) -> Tuple[float, Point]:
    """
    Implements Gradient Descent (https://en.wikipedia.org/wiki/Gradient_descent) in pure-Python3.6+ with
    no external dependencies.

    :param gamma: 'step size', or 'learning rate'
    :param max_iterations: Maximum number of steps in descent process.
    :param f: A differentiable function off multiple real-valued variables.
    :param initial_point: Optionally, a place to start the descent process
    :return: A tuple of first a local minimum and second the point at which minimum is found.
    """
    if gamma <= 0:
        raise ValueError("gamma value must be a positive real number, γ∈ℝ+")

    iterations_per_logline = 100
    a: Point = {}
    f_grad = f.gradient()

    if not initial_point:
        for v in f.vars:
            a[v] = random.randrange(4)
    else:
        a = initial_point
    for i in range(max_iterations):
        # Calculate function's gradient @ point `a`
        grad_a: Mapping[Variable, float] = {
            var: grad_elem.evaluate(a)
            for var, grad_elem
            in f_grad.items()
        }
        # update estimate of minimum point
        a_next = {
            var: current - (gamma * grad_a[var])
            for var, current
            in a.items()
        }
        a_prev = a
        a = a_next

        if a_prev == a:
            print("Iteration as not changed value. Stopping early.")
            break
        if i % iterations_per_logline == 0:
            print(f"Iteration {i}. Current min estimate: {a}")
    return f.evaluate(a), a


def main() -> None:
    print("hello world")
    x = Variable("x")
    y = Variable("y")
    exp = PolynomialExpression(
        variable=x,
        coefficient=2,
        exponent=4,
    )
    print(exp)
    print(exp.diff())

    test_f = MultiVariableFunction(
        variables={x, y},
        expressions=[
            PolynomialExpression(variable=x, coefficient=1, exponent=2),
            PolynomialExpression(variable=y, coefficient=1, exponent=2),
            PolynomialExpression(variable=x, coefficient=-2, exponent=1),
            PolynomialExpression(variable=y, coefficient=-6, exponent=1),
            ConstantExpression(real=14.0),
        ],
    )
    minimum_val, minimum_point = gradient_descent(
        gamma=0.1,
        max_iterations=5000,
        f=test_f,
    )
    print(f"Min Value: {minimum_val}")
    print(f"Min Location: {minimum_point}")

    # Test variable comparisons
    ##########################
    assert Variable("x") == Variable("x")
    assert Variable("x") != Variable("y")
    assert Variable("y") != Variable("x")
    assert Variable("y") != Variable("z")

    # Test gradient evaluations of Expressions
    ##########################################
    # ConstantExpressions
    assert ConstantExpression(real=0.0).diff() is None
    assert ConstantExpression(real=4.5).diff() is None
    # PolynomialExpression
    poly1 = PolynomialExpression(
        variable=Variable("x"),
        coefficient=2,
        exponent=4,
    )
    poly1_grad1 = poly1.diff()
    assert poly1_grad1.var == Variable("x")
    assert poly1_grad1.coefficient == 8
    assert poly1_grad1.exp == 3
    poly1_grad2 = poly1.diff(ref_var=Variable("y"))
    assert poly1_grad2 is None

    # Test function evaluation
    ##########################
    x = Variable("x")
    y = Variable("y")
    # f = 3x + y^2
    f1 = MultiVariableFunction(
        variables={x, y},
        expressions=[
            PolynomialExpression(variable=x, coefficient=3, exponent=1),
            PolynomialExpression(variable=y, coefficient=1, exponent=2),
        ],
    )
    assert f1.evaluate(point={x: 1.0, y: 1.0}) == 4
    assert f1.evaluate(point={x: 1.0, y: 2.0}) == 7
    # Test function gradient
    g = f1.gradient()
    assert str(g[x]) == "3"

    # Test Multiply
    ##########################
    a = PolynomialExpression(variable=x, coefficient=3, exponent=1)
    b = PolynomialExpression(variable=y, coefficient=1, exponent=2)
    a_times_b = Multiply(a=a, b=b)
    result = a_times_b.evaluate(point={x: 2.0, y: 4.0})
    assert result == (6 * 16)
    result = a_times_b.evaluate(point={x: 3.0, y: 5.0})
    assert result == 225
    # Test diff on multiplication expression
    a_times_b_diff = a_times_b.diff(ref_var=x)
    assert a_times_b_diff.evaluate(point={x: 1.0, y: 5.0}) == 75


if __name__ == "__main__":
    main()
