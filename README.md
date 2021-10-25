# Solving Linear problems using the Simplex Method/Big M Method
This project solves linear programming problems to optimality as taught to us by **Prof. Assad El Nidani** in the Quantitative Business Analysis course as part of the MBA program.
I want to thank him personally for tolerating my endless questions and thoroughly answering them.
## Disclaimer
This code is not a clean code, it's just something that I threw together in my spare time because I was bored and curious :D and was tested on very limited cases. so use it at your own risk

## Example

### Objective function and constraints
![image](https://user-images.githubusercontent.com/5011250/138702810-18fe6be0-aca6-4579-be3e-382d6c3cb0a4.png)

### Entering the problem data
we need to set 3 variables: \
**m**: determines wether our problem is a maximization of a minimization problem \
**z**: used to assign the cooficients of the variables in the objective function \
**xs**: used to define the constraint functions, by entering the cooficients of the variables in each function, then a number that represents the separator between the right hand side and the left hand side of the function, where 0  for <=, 1 for =, and 2 for >= , then the last item is the value of the right hand side\
![image](https://user-images.githubusercontent.com/5011250/138703099-9775ac75-3c53-4a2b-9bf2-495e29d9a191.png)

### Result
![image](https://user-images.githubusercontent.com/5011250/138704434-d4a06a40-f12a-4d1d-849e-e64ffca826f7.png)
![image](https://user-images.githubusercontent.com/5011250/138704537-a8577204-cfe9-4320-8d1f-c42db3d8cab9.png)
![image](https://user-images.githubusercontent.com/5011250/138704579-bd293b04-be5f-460a-b910-127cc4148d70.png)
