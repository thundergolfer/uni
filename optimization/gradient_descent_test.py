from optimization.gradient_descent import gradient_descent
from optimization.gradient_descent import ConstantExpression
from optimization.gradient_descent import Multiply
from optimization.gradient_descent import MultiVariableFunction
from optimization.gradient_descent import PolynomialExpression
from optimization.gradient_descent import Variable

# TODO(Jonathon): This is a quick and dirty, and weird, way to test. Use unittest to be normal.
def test_gradient_descent() -> None:
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
    test_gradient_descent()