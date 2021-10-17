def calcValue(o_r, o_c, p_i, o_i):
    return (o_i - (o_r * o_c) / p_i)


def calcItem(t, pc, pr, r, c):
    p_i = t[pr][pc]
    o_i = t[r][c]
    o_c = t[r][pc]
    o_r = t[pr][c]
    return calcValue(o_r, o_c, p_i, o_i)


def createTableau(xs, z):
    # I need columns to cover the Xs, Ss, As and RHS
    # I need rows equal to the number of constraints
    tableau = [None for r in range(len(xs) + 1)]
    # create identity matrix
    identity = [[1 if c == r else 0 for c in range(len(xs))] for r in range(len(xs))]

    # fill tableau
    for i in range(len(xs)):
        tableau[i] = xs[i][:-2] + identity[i] + [xs[i][-1]]
    tableau[-1] = [-j for j in z] + [0 for i in range(len(xs) + 1)]
    bv = [i for i in range(len(z), len(z) + len(xs))]
    return tableau, bv


def isOptimal(t, m):
    if m:  # max, count negative values
        return sum(1 for i in t[-1][:-1] if i > 0) == 0
    else:  # min, count positive values
        return sum(1 for i in t[-1][:-1] if i < 0) == 0


def findPivot(t, m):
    optimal = isOptimal(t, m)
    pc, pr = None, None
    if not optimal:
        val, pc = min((val, idx) for (idx, val) in enumerate(t[-1][:-1]))
        val, pr = min((val, idx) for (idx, val) in enumerate([float('inf') if xx is None or xx < 0 else xx for xx in
                                                              [float('inf') if r[pc] <= 0 else r[-1] / r[pc] for r in
                                                               t]]))
    return pc, pr


def printTableau(t, bv, xs, z, m=0, pc=None, pr=None):
    heads = ['x_' + str(i + 1) for i in range(len(z))] + ['S_' + str(i + 1) for i in range(len(xs))]

    if not pc is None:
        print(" ", " " * (10 + pc * 6) + "↓")

    header = ' BV    | ' + ' | '.join(heads) + ' | RHS  '
    print(" ", header)
    hr = ''.join(["|" if i == "|" else "-" for i in header])
    print(" ", hr)
    for i in range(len(xs)):
        row = '{0}) {1} |'.format(i + 1, heads[bv[i]]) + "|".join([str(x).center(5) for x in t[i]])
        print(" " if (pr is None or pr != i) else "→", row)

    print(" ", hr)
    Z_row = "    Z  |" + "|".join([str(x).center(5) for x in t[-1]])
    print(" ", Z_row)
    print(" ", ''.join(["|" if i == "|" else "=" for i in hr]))


def iterate(xs, z, t, bv, pc, pr):
    nt = [[None for c in range(len(xs) + len(z) + 1)] for r in range(len(xs) + 1)]
    # pivot item
    p_i = t[pr][pc]
    # set pivot column in new tableau
    for r in range(len(t)):
        nt[r][pc] = 0 if r != pr else 1
    # set pivot row in new tableau
    for c in range(len(t[pr])):
        nt[pr][c] = 1 if c == pc else t[pr][c] / p_i
    # set the rest
    for r in range(len(t)):
        for c in range(len(t[pr])):
            if nt[r][c] is None:
                nt[r][c] = calcItem(t, pc, pr, r, c)

    return nt


def printStatus(xs, z, t, bv, m):
    print("Optimal" if isOptimal(t, m) else "Not optimal")
    heads = ['x_' + str(i + 1) for i in range(len(z))] + ['S_' + str(i + 1) for i in range(len(xs))] + ['Z']
    vals = [0] * len(heads)
    for i in range(len(bv)):
        vals[bv[i]] = t[i][-1]
    vals[-1] = t[-1][-1]
    print("\t".join([heads[i] + " = " + str(vals[i]) for i in range(len(heads))]))


def printProblem(xs, z, m):
    # 0 for max, 1 for min
    # 0  for <=, 1 for =, 2 for >=
    sign = ["≤", "=", "⩾"]
    eqs = []
    xas = 0
    maxLetters = 0
    for eq in xs:
        xelements = [f"{eq[i]}x_{i + 1}" if eq[i] not in [0, 1] else f"x_{i + 1}" if eq[i] == 1 else "0" for i in
                     range(len(eq) - 2)]
        eqs.append([xelements, sign[eq[-2]], eq[-1]])
        xas += 1 if eq[-2] > 0 else 0
        ll = len(sorted(xelements, key=len)[-1])
        maxLetters = ll if ll > maxLetters else maxLetters
    print("-" * 20)
    print("Min" if m else "Max", "Z =", " + ".join([f"{z[i]}x_{i + 1}" for i in range(len(z))]))
    print("Subject to:")
    for i, eq in enumerate(eqs):
        print(f"{i + 1})", " + ".join([i.center(maxLetters) for i in eq[0]]), eq[1], eq[2])
    print(",".join([f"x_{i + 1}" for i in range(len(z))]), sign[2], "0")


def printProcessedProblem(xs, z, m):
    # 0 for max, 1 for min
    # 0  for <=, 1 for =, 2 for >=
    sign = ["≤", "=", "⩾"]
    xas, nss, nas = getTableauVars(xs, z, m)
    heads = getVariablesNames(xas, nss, nas)
    maxLetters = len(sorted(heads, key=len)[-1]) + len(sorted([str(j) for i in xs for j in i[:-2]], key=len)[-1])

    print(xs)
    print("-" * 20)
    print("Min" if m else "Max", "Z =", " + ".join([f"{z[i]}x_{i + 1}" for i in range(len(z))]),
          ("+" if m else "-"), (" + " if m else " - ").join([f"MA_{i + 1}" for i in range(nas)]))
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


def getVariablesNames(xas, nss, nas):
    heads = [f"x_{i+1}" for i in range(xas)] \
            + [f"S_{i+1}" for i in range(nss)] \
            + [f"A_{i+1}" for i in range(nas)]
    return heads


def getTableauVars(xs, z, m):
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
