import sympy as sy
sy.init_printing()

th, dth, d2th, phi, dphi, d2phi = sy.symbols('\\theta \\dot\\theta \\ddot\\theta \\phi \\dot\\phi \\ddot\\phi')
mw, mb, Iw, Ib, l, d, g = sy.symbols('m_w m_b I_w I_b \ell d g')
# assume rotational inertial are negligible

q = sy.Matrix([th, phi])
dq = sy.Matrix([dth, dphi])
d2q = sy.Matrix([d2th, d2phi])

T = 0.5 * mw * (dphi * sy.pi * d)**2 + 0.5 * mb * ((dphi * sy.pi * d)**2 + 2 * l * (dphi * sy.pi * d) * dth * sy.cos(th) + l**2 * dth**2) + 0.5 * 1 / (sy.pi**2 * d**2) * Iw * (dphi * sy.pi * d)**2 + 0.5 * Ib * dth**2
V = mb * g * l * sy.cos(th)
L = sy.Matrix([T - V])

L_dq = L.jacobian(dq)
eom = sy.simplify(L_dq.jacobian(dq) * d2q + L_dq.jacobian(q) * dq - L.jacobian(q).transpose())


mass_matrix, RHS = sy.linear_eq_to_matrix(eom, [d2th, d2phi])
remainder_matrix = -RHS
