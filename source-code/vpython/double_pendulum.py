import sympy
from sympy import symbols
from sympy import cos, sin, Derivative, pi

def compute_odes():
    l1, m1 = symbols('l_1 m_1', real=True, positive=True)
    l2, m2 = symbols('l_2 m_2', real=True, positive=True)
    t, g = symbols('t g', real=True, positive=True)

    theta1, theta2 = symbols(r'\theta_1 \theta_2', cls=sympy.Function)
    theta1, theta2 = theta1(t), theta2(t)

    x1, y1 = l1*sin(theta1), -l1*cos(theta1)
    x2, y2 = x1 + l2*sin(theta2), y1 - l2*cos(theta2)

    T = m1*(x1.diff(t)**2 + y1.diff(t)**2)/2 + \
        m2*(x2.diff(t)**2 + y2.diff(t)**2)/2
    U = m1*g*y1 + m2*g*y2
    L = T - U

    theta1_dot, theta2_dot = theta1.diff(t), theta2.diff(t)
    theta1_ddot, theta2_ddot = theta1_dot.diff(t), theta2_dot.diff(t)

    EL_eq1 = (L.diff(theta1) - L.diff(theta1_dot).diff(t)).simplify()
    EL_eq2 = (L.diff(theta2) - L.diff(theta2_dot).diff(t)).simplify()

    rhs = sympy.solve({EL_eq1, EL_eq2}, {theta1_ddot, theta2_ddot})
    
    funcs = x1, y1, x2, y2 = symbols('x_1 y_1 x_2 y_2')
    subst = {
        theta1: x1,
        theta1_dot: y1,
        theta2: x2,
        theta2_dot: y2,
    }

    eqs = [
        y1,
        rhs[theta1_ddot].subs(subst),
        y2,
        rhs[theta2_ddot].subs(subst),
    ]

    jacobian = sympy.Matrix(4, 4, lambda i, j: eqs[i].diff(funcs[j]))

    rhs_funcs = sympy.lambdify((t, x1, y1, x2, y2, g, m1, l1, m2, l2),
                               eqs)
    jac_funcs = sympy.lambdify((t, x1, y1, x2, y2, g, m1, l1, m2, l2),
                               jacobian)

    def sp_funcs(t, Y, g, m1, l1, m2, l2):
        theta1, omega1, theta2, omega2 = Y
        return rhs_funcs(t, theta1, omega1, theta2, omega2,
                         g, m1, l1, m2, l2)

    def sp_jac(t, Y, g, m1, l1, m2, l2):
        theta1, omega1, theta2, omega2 = Y
        return jac_funcs(t, theta1, omega1, theta2, omega2,
                         g, m1, l1, m2, l2)

    return sp_funcs, sp_jac
