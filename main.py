import Simplex

m = 1  # 0 for max, 1 for min
z = [3, 1, 4]
# 0  for <=, 1 for =, 2 for >=
xs = [
    [1, 1, 1, 1, 1000],
    [2, 1, 0, 2, 200],
    [0, 1, 2, 0, 800]
]

# m = 0
# z = [1, 2, 4]
# xs = [
#     [1, 1, 1, 0, 400],
#     [0, 2, 1, 0, 300],
#     [1, 1, 0, 0, 200]
# ]

if __name__ == "__main__":
    print("Starting...")

    Simplex.printProblem(xs, z, m)

    Simplex.printProcessedProblem(xs, z, m)

    heads, eqs, RHS, bv, z_row = Simplex.create_tableau(xs, z, m)

    pc = Simplex.get_pivot_column(z_row, m)
    pr = Simplex.get_pivot_row(eqs, RHS, pc)

    Simplex.print_tableau(heads, eqs, RHS, bv, z_row, pc, pr)
