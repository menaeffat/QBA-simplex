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
# z = [2, 4]
# xs = [
#     [1,1,2,50],
#     [1,1,0,100],
#     [-1,1,2,25]
# ]

# m = 0
# z = [1, 2, 4]
# xs = [
#     [1, 1, 1, 0, 400],
#     [0, 2, 1, 0, 300],
#     [1, 1, 0, 0, 200]
# ]

# m = 0
# z = [2, 1]
# xs = [
#     [3, 2, 0, 300],
#     [1, 1, 0, 200]
# ]

# m = 0
# z = [4, 1, 3]
# xs = [
#     [2,1,3,0,400],
#     [0,2,1,0,200],
#     [1,0,2,0,300]
# ]

# m = 1
# z = [2, 2, 3]
# xs = [
#     [1, 1, 1, 1, 180],
#     [0, 1, 0, 0, 60],
#     [0, 2, 1, 2, 50]
# ]

m = 0  # 0 for max, 1 for min
z = [2,4]
# 0  for <=, 1 for =, 2 for >=
xs = [
    [1,1,0,3],
    [0.5,1,0,2.5]
]


if __name__ == "__main__":
    print("Starting...")

    # problem initialization
    Simplex.printProblem(xs, z, m)

    Simplex.printProcessedProblem(xs, z, m)
    xas, nss, nas = Simplex.get_num_of_vars(xs)
    heads, eqs, RHS, bv, z_row = Simplex.create_initial_tableau(xs, z, m)

    # check status
    status = Simplex.get_status(heads, nas, RHS, bv, z_row, m)

    # for III in range(5):
    while not status[3]:
        pc = Simplex.get_pivot_column(z_row, m)
        pr = Simplex.get_pivot_row(eqs, RHS, pc, heads, bv)
        status = Simplex.get_status(heads, nas, RHS, bv, z_row, m)
        Simplex.print_tableau(heads, eqs, RHS, bv, z_row, pc if not status[3] else None,
                              pr if not status[3] or pr is None else None)
        Simplex.print_status(status)

        if pr is None:
            print("Unbound solution")
            break

        bv[pr] = pc

        eqs, RHS, z_row = Simplex.iterate(eqs, RHS, z_row, pc, pr)
