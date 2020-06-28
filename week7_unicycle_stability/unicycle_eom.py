import sympy as sy
sy.init_printing()

th, dth, d2th, phi, dphi, d2phi = sy.symbols('\\theta \\dot\\theta \\ddot\\theta \\phi \\dot\\phi \\ddot\\phi')
mw, mb, Iw, Ib, l, d, g = sy.symbols('m_w m_b I_w I_b \ell d g')
# assume rotational inertial are negligible

q = sy.Matrix([th, phi])
dq = sy.Matrix([dth, dphi])
d2q = sy.Matrix([d2th, d2phi])

wheel_vel = [dphi * d, 0] # cartesian
body_vel = [dphi * d + l * dth * sy.cos(th), -l * dth * sy.sin(th)] # cartesian

T = 0.5 * mw * (wheel_vel[0]**2 + wheel_vel[1]**2) + 0.5 * mb * (body_vel[0]**2 + body_vel[1]**2) +  0.5 * Iw * dphi**2 + 0.5 * Ib * dth**2
V = mb * g * l * sy.cos(th)
L = sy.Matrix([T - V])

L_dq = L.jacobian(dq)
eom = sy.simplify(L_dq.jacobian(dq) * d2q + L_dq.jacobian(q) * dq - L.jacobian(q).transpose())

mass_matrix, RHS = sy.linear_eq_to_matrix(eom, [d2th, d2phi])
remainder_matrix = -RHS
