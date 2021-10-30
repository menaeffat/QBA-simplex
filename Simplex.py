# TODO: check the case where in Z one of the coefficients is negative or has a constant
from fraction import Fraction


def printProblem(xs, z, m):
    # 0 for max, 1 for min
    # 0  for <=, 1 for =, 2 for >=
    sign = ["≤", "=", "⩾"]
    eqs = []
    xas = 0
    maxLetters = 0
    for eq in xs:
        x_elements = [f"{eq[i]}x_{i + 1}" if eq[i] not in [0, 1] else f"x_{i + 1}" if eq[i] == 1 else "0" for i in
                      range(len(eq) - 2)]
        eqs.append([x_elements, sign[eq[-2]], eq[-1]])
        xas += 1 if eq[-2] > 0 else 0
        ll = len(sorted(x_elements, key=len)[-1])
        maxLetters = ll if ll > maxLetters else maxLetters
    print("-" * 20)
    print("Min" if m else "Max", "Z =", " + ".join([f"{z[i]}x_{i + 1}" if z[i] not in [0, 1]
                                                    else f"x_{i + 1}" if z[i] == 1 else "" for i in range(len(z))]))

    print("Subject to:")
    for i, eq in enumerate(eqs):
        print(f"{i + 1})", " + ".join([i.center(maxLetters) for i in eq[0]]), eq[1], eq[2])
    print(",".join([f"x_{i + 1}" for i in range(len(z))]), sign[2], "0")


def printProcessedProblem(xs, z, m):
    # 0 for max, 1 for min
    # 0  for <=, 1 for =, 2 for >=
    sign = ["≤", "=", "⩾"]
    xas, nss, nas = get_num_of_vars(xs)
    heads = get_vars_names(xas, nss, nas)
    maxLetters = len(sorted(heads, key=len)[-1]) + len(sorted([str(j) for i in xs for j in i[:-2]], key=len)[-1])

    print("-" * 20)
    print("Min" if m else "Max", "Z =", " + ".join([f"{z[i]}x_{i + 1}" if z[i] not in [0, 1]
                                                    else f"x_{i + 1}" if z[i] == 1 else "" for i in range(len(z))]),
          ("+" if m else "-") if nas else "", (" + " if m else " - ").join([f"MA_{i + 1}" for i in range(nas)]))
    print("Subject to:")
    nas, nss = 0, 0
    for i, eq in enumerate(xs):
        # sign = ["≤", "=", "⩾"]
        # S        S    0   -S
        # A        0    A    A
        nas += 0 if eq[-2] == 0 else 1
        nss += 0 if eq[-2] == 1 else 1
        print(f"{i + 1})", " + ".join(
            [f"{co}{heads[i]}".center(maxLetters) if co not in [0, 1] else
             f"{heads[i]}".center(maxLetters) if co == 1 else "0".center(maxLetters) for i, co in enumerate(eq[:-2])]
            + ([] if eq[-2] == 1 else [f"S_{nss}"] if eq[-2] == 0 else [f" - S_{nss}"])
            + ([] if eq[-2] == 0 else [f"A_{nas}"])
        ).replace("+  -", "-"), "=", eq[-1])
    print("*)", ",".join(
        [f"x_{i + 1}" for i in range(len(z))]
        + [f"S_{s + 1}" for s in range(nss)]
        + [f"A_{a + 1}" for a in range(nas)]
    ), sign[2], "0")


def get_vars_names(xas, nss, nas):
    heads = [f"x_{i + 1}" for i in range(xas)] \
            + [f"S_{i + 1}" for i in range(nss)] \
            + [f"A_{i + 1}" for i in range(nas)]
    return heads


def get_num_of_vars(xs):
    # 0 for max, 1 for min
    # 0  for <=, 1 for =, 2 for >=
    xas, nas, nss = len(xs[0]) - 2, 0, 0
    for i, eq in enumerate(xs):
        # sign = ["≤", "=", "⩾"]
        # S        S    0   -S
        # A        0    A    A
        nas += 0 if eq[-2] == 0 else 1
        nss += 0 if eq[-2] == 1 else 1
    return xas, nss, nas


def create_initial_tableau(xs, z, m):
    # 0 for max, 1 for min
    # 0  for <=, 1 for =, 2 for >=
    t_xas, t_nss, t_nas = get_num_of_vars(xs)
    nas, nss = 0, 0
    eqs = []
    bv = [0] * len(xs)
    RHS = []
    z_rhs = (0, 0)
    z_row = [(0, 0)] * (t_xas + t_nss + t_nas + 1)
    heads = get_vars_names(t_xas, t_nss, t_nas)
    for i, eq in enumerate(xs):
        # sign = ["≤", "=", "⩾"]
        # S        S    0   -S
        # A        0    A    A
        # BV       S    A    A
        S = [0] * t_nss
        A = [0] * t_nas

        if eq[-2] == 0:
            S[nss] = 1
            bv[i] = t_xas + nss
            nss += 1
        elif eq[-2] == 1:
            A[nas] = 1
            bv[i] = t_xas + t_nss + nas
            nas += 1
        elif eq[-2] == 2:
            S[nss] = -1
            A[nas] = 1
            bv[i] = t_xas + t_nss + nas
            nas += 1
            nss += 1
        line_eq = eq[:-2] + S + A
        eqs.append(line_eq)
        RHS.append(eq[-1])
        # 0 for max, 1 for min
        # print(z_row, line_eq)
        if eq[-2]:
            z_row = [(z_row[ii][0] + line_eq[ii] if m else z_row[ii][0] - line_eq[ii], z_row[ii][1])
                     for ii in range(len(heads))] + [(z_row[-1][0] + (eq[-1] if m else -eq[-1]), z_rhs[1])]

    for i, zz in enumerate(z):
        z_row[i] = (z_row[i][0], -zz)
    if nas:
        z_row = z_row[:-nas - 1] + [(0, 0)] * nas + [z_row[-1]]
    # print(z_row)
    return heads, eqs, RHS, bv, z_row


def print_tableau(heads, eqs, rhs, bv, z_row, pc=None, pr=None):
    max_letters = 7
    if pc is not None:
        print(" ", " " * (11 + (max_letters + 1) * pc) + "↓".center(max_letters))
    header = ("|".join(["BV".center(10)] + [h.center(max_letters) for h in heads] + ["RHS".center(10)]))
    hr = ''.join(["|" if i == "|" else "-" for i in header])
    print(" ", header)
    print(" ", hr)

    for i, line in enumerate(eqs):
        print_line = f"{i:02d})" + f" {heads[bv[i]]}".center(7) + "|" \
                     + "|".join([format_number(e).center(max_letters) for e in line]) + "|" \
                     + format_number(rhs[i]).center(10)
        print("→" if i == pr else " ", print_line)
    print(" ", hr)

    zl1 = [z_row[i_z][0] for i_z in range(len(z_row))]
    zl2 = [z_row[i_z][1] for i_z in range(len(z_row))]
    zl1_nz = zl1 != [0] * len(zl1)
    zl2_nz = zl2 != [0] * len(zl2)
    if not zl1_nz and zl2_nz:
        z_line = ["Z".center(10)] + [format_number(z).center(max_letters) for z in zl2]
        print(" ", "|".join(z_line))
    else:
        z_line = ["Z".center(10)] + [i.center(max_letters) for i in [
            format_number(z, "M") for z in
            zl1]]
        print(" ", "|".join(z_line))
        if zl1_nz and zl2_nz:
            z_line = ["".center(10)] + [format_number(z).center(max_letters) for z in zl2]
            print(" ", "|".join(z_line))
    print(" ", ''.join(["|" if i == "|" else "=" for i in hr]))


def get_pivot_column(z_row, m):
    # 0 for max,            1 for min
    # look for most -ve     look for most positive
    m_power = max([abs(i[0]) for i in z_row[:-1]] + [abs(i[1]) for i in z_row[:-1]])
    big_m = 100 ** m_power
    z_comp = [z[0] * big_m + z[1] for z in z_row[:-1]]
    if m:
        pc = max((val, idx) for (idx, val) in enumerate(z_comp))
    else:
        pc = min((val, idx) for (idx, val) in enumerate(z_comp))
    return pc[1]


def get_pivot_row(eqs, rhs, pc, heads, bv):
    ratio = []
    for i, eq in enumerate(eqs):
        if eq[pc] <= 0:
            ratio.append(float("inf"))
        else:
            ratio.append(rhs[i] / eq[pc])
    # check to see if it is an unbound solution
    if ratio == [float("inf")] * len(ratio):
        # Solution is unbound
        return None
    else:
        # apply Bland rules to avoid degenerate solutions
        min_val = min((val, idx) for (idx, val) in enumerate(ratio))
        indices_of_min_val = [i for i, v in enumerate(ratio) if v == min_val[0]]
        indices_of_BV = [bv[i] for i, v in enumerate(ratio) if v == min_val[0]]
        pr = indices_of_min_val[min((val, idx) for (idx, val) in enumerate(indices_of_BV))[1]]
        return pr


def is_optimal(z_row, m):
    # 0 for max,            1 for min
    # no  -ve               no positive
    m_power = max([abs(i[0]) for i in z_row[:-1]] + [abs(i[1]) for i in z_row[:-1]])
    big_m = 100 ** m_power
    z_comp = [z[0] * big_m + z[1] for z in z_row[:-1]]
    optimal = sum([i > 0 if m else i < 0 for i in z_comp]) == 0
    return optimal


def get_status(heads, nas, rhs, bv, z_row, m):
    optimal = is_optimal(z_row, m)
    values = [0] * len(z_row)
    for i in range(len(bv)):
        values[bv[i]] = rhs[i]
    keys = heads + ["Z"]
    values[-1] = z_row[-1]
    feasible = values[-nas - 1:-1] == [0] * nas
    return keys, values, feasible, optimal


def print_status(status):
    z = status[1][-1]
    # print_z0 = f"{z[0]:.2f}M" if z[0] not in [-1, 0, 1] else "0" if z[0] == 0 else "M" if z[0] == 1 else "-M"
    print_z0 = format_number(z[0], "M")
    print_z1 = format_number(z[1])
    print("OT:", status[3], "FT:", status[2],
          "\t".join([f"{status[0][i]} = {format_number(status[1][i])}" for i in range(len(status[0]) - 1)]),
          f"Z = {print_z0} + {print_z1}".replace("+ -", "- ").replace("0 + ", ""))


def format_number(x, var=None) -> str:
    if var is None:
        var = ""
    number = ""
    if x not in [-1, 0, 1]:
        if int(x) == x:
            number = f"{int(x)}{var}"
        else:
            n = Fraction(x)
            if len(str(n.denominator)) < 3:
                number = f"{format_number(n.numerator,var)}/{n.denominator}"
            else:
                number = f"{x:.2f}{var}"
    elif x == 0:
        number = "0"
    elif x == 1:
        number = "1" if var == "" else f"{var}"
    elif x == -1:
        number = "-1" if var == "" else f"-{var}"
    return number


def calcValue(o_r, o_c, p_i, o_i):
    return o_i - (o_r * o_c) / p_i


def calcItem(t, pc, pr, r, c):
    p_i = t[pr][pc]
    o_i = t[r][c]
    o_c = t[r][pc]
    o_r = t[pr][c]
    return calcValue(o_r, o_c, p_i, o_i)


def iterate(eqs, rhs, z_row, pc, pr):
    new_table = [[None for i in range(len(eqs[1]))] for j in range(len(eqs))]
    new_rhs = [None for i in range(len(rhs))]
    new_z_row = [(0, 0) for i in range(len(z_row))]
    # pivot item
    p_i = eqs[pr][pc]
    # set pivot column in new tableau
    for row_index in range(len(eqs)):
        new_table[row_index][pc] = 1 if row_index == pr else 0
    new_z_row[pc] = (0, 0)  # this is useless because It's initially (0, 0)
    # set pivot row in new tableau
    for c in range(len(eqs[pr])):
        new_table[pr][c] = 1 if c == pc else eqs[pr][c] / p_i
    new_rhs[pr] = rhs[pr] / p_i
    # set the rest
    for r in range(len(eqs)):
        for c in range(len(eqs[pr])):
            if new_table[r][c] is None:
                new_table[r][c] = calcItem(eqs, pc, pr, r, c)
    for i in range(len(rhs)):
        if i != pr:
            new_rhs[i] = calcValue(eqs[i][pc], rhs[pr], p_i, rhs[i])
    for i in range(len(z_row) - 1):
        if i != pc:
            z0 = calcValue(z_row[pc][0], eqs[pr][i], p_i, z_row[i][0])
            z1 = calcValue(z_row[pc][1], eqs[pr][i], p_i, z_row[i][1])
            new_z_row[i] = (z0, z1)

    z0 = calcValue(z_row[pc][0], rhs[pr], p_i, z_row[-1][0])
    z1 = calcValue(z_row[pc][1], rhs[pr], p_i, z_row[-1][1])
    new_z_row[-1] = (z0, z1)

    return new_table, new_rhs, new_z_row
