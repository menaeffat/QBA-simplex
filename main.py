import Simplex

##z = [2,-1]
##xs = [
##    [1,0,100],
##    [-1,0,10],
##    [0,1,100],
##    [0,-1,10],
##    [1,1,110]
##    ]

##z = [1,3]
##xs = [
##    [1,2,180],
##    [2,1,180],
##    [1,-1,45],
##    [-1,1,45]
##    ]

##z=[1,2,4]
##xs=[
##    [1,1,1,400],
##    [0,1,2,300],
##    [1,1,0,200]
##    ]

# z = [7, 10, 12]
# xs = [
#     [1, 0, 0, 400],
#     [0, 1, 0, 200],
#     [0, 0, 1, 100],
#     [2, 3, 7, 1000],
#     [1, 0, 1, 400],
#     [3, 5, 10, 2000],
#     [0, -2, 1, 0],
#     [2, 4, 6, 10000]
# ]
# z = [5, 6, 6]
# xs = [
#     [1, 0, 0, 400],
#     [0, 1, 0, 200],
#     [0, 0, 1, 100],
#     [2, 3, 7, 1000],
#     [1, 0, 1, 400],
#     [3, 5, 10, 2000],
#     [-2, 1, 0, 0],
#     [2, 4, 6, 10000]
# ]

m = 1  # 0 for max, 1 for min
z = [3, 1, 4]
# 0  for <=, 1 for =, 2 for >=
xs = [
    [1, 1, 1, 1, 1000],
    [2, 1, 0, 2, 200],
    [0, 1, 2, 0, 800]
]

if __name__ == "__main__":
    print("Starting...")
    # Simplex.printProblem(xs, z, m)
    Simplex.printProcessedProblem(xs, z, m)
    # Simplex.getTableauVars(xs, z, m)
    # t, bv = Simplex.createTableau(xs, z)
    # optimal = False
    # print(bv)
    # Simplex.printTableau(t, bv, xs, z, m)
# # while not optimal:
#     pc, pr = Simplex.findPivot(t, m)
#     optimal = Simplex.isOptimal(t, m)
#     Simplex.printTableau(t, bv, xs, z, m, pc, pr)
#     Simplex.printStatus(xs, z, t, bv, m)
#     if not optimal:
#         bv[pr] = pc
#         t = Simplex.iterate(xs, z, t, bv, pc, pr)
