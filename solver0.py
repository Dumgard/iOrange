import numpy as np
import pandas as pd

def S_pred(P, K):
    return K @ P

def Error(P, K, S):
    t = (S_pred(P, K) - S)**2
    return np.dot(t, t.transpose())

def Error_deriv(P, K, S):
    return 2.*(P @ (S_pred(P, K) - S))

def Error_lin(P, K, S):
    t = S_pred(P, K) - S
    return np.dot(t, t.transpose())

def Error_lin_deriv(P, K, S):
    t = S_pred(P, K) - S
    for i in range(len(t)):
        if t[i] < 0.:
            t[i] = -1.
        else:
            t[i] = 1.
    return P @ t

def evaluation(x, x_low, x_max, dx):
    for i in range(len(x)):
        if dx[i] > 0.0:
            x[i] -= dx[i]*(x[i] - x_low[i])/(dx[i] + (x[i] - x_low[i]))
        else:
            x[i] -= dx[i]*(x[i] - x_max[i])/(dx[i] + (x[i] - x_max[i]))

ERROR = 1

#data_vac = pd.read_csv("test_data.csv")
data_vac = pd.read_csv("test_vacancies.csv")
data_univ = pd.read_csv("test_data.csv")
bound_low = np.array(data_univ["low_bound"], dtype="float64")
bound_high = np.array(data_univ["high_bound"], dtype="float64")
S = np.array(data_vac[data_vac.columns[1]], dtype="float64")
#S = np.array(data_vac, dtype="float64")
I = len(data_vac)
print(I)
J = len(data_univ)
P_list = []
for col in data_univ.columns[3:I+3]:
    P_list.extend(data_univ[col].to_list())
P = np.array(P_list, dtype="float64")
P = P.reshape(J, I)
K = (bound_low + bound_high)/2.
#print(I, J, P, K, S)
learning_rate = 1
steps = 10000
for i in range(steps):
    if ERROR == 2:
        evaluation(K, bound_low, bound_high, learning_rate*Error_deriv(P, K, S))
    else:
        evaluation(K, bound_low, bound_high, learning_rate * Error_lin_deriv(P, K, S))
    print("Error of {} step is {}".format(i+1, Error(P, K, S)))
print("\nK is:")
print(K)
print("\nOn vacantions {} goes {}".format(S, S_pred(P, K)))

#for i in range(len(K)):
#    if abs(S[i] > S_pred(P, K)[i]) < 20:
#        print("We have enough vacantions for " + data_univ.columns[i+3] + "")