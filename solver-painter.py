import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
K1 = K
K2= K1.copy()
P1 = P
P2 = P1.copy()
S1 = S
S2= S1.copy()
steps = 10000
chk=0
lstError = 0
for i in range(steps):
    evaluation(K1, bound_low, bound_high, learning_rate*Error_deriv(P1, K1, S1))
    print("Error of {} step is {}".format(i+1, Error(P1, K1, S1)))
    if lstError == Error(P1,K1,S1):
        chk = chk+1
    lstError= Error(P1, K1, S1)
    if chk >=5:
        break
steps = 10000
chk=0
lstError = 0
for i in range(steps):
    evaluation(K2, bound_low, bound_high, learning_rate * Error_lin_deriv(P2, K2, S2))
    print("Error of {} step is {}".format(i+1, Error(P2, K2, S2)))
    if lstError == Error(P2,K2,S2):
        chk = chk+1
    lstError= Error(P2, K2, S2)
    if chk >=5:
        break 
print("\nK1 is:")
print(K1)
print("\nK2 is:")
print(K2)

print("\nOn vacantions {} goes {}".format(S1, S_pred(P1, K1)))
print("\nOn vacantions {} goes {}".format(S2, S_pred(P2, K2)))

print(type(data_univ))
print(data_univ)
print(data_vac)
unives = data_univ.columns[0]

univ_realization = pd.DataFrame({'University,faculty,direction':data_univ[unives].to_list(),
                             'Расчет_Квот_Квадратичный':K1,
                             'Расчет_Квот_Линейный':K2},
                            index =data_univ[unives].to_list() )





vac_compare = pd.DataFrame ({'Vacansies':S1,
                             'Specialists_quad':S_pred(P1, K1),
                             'Specialists_line':S_pred(P2, K2)},
                            index =data_vac[data_vac.columns[0]].to_list())


vac_comp = pd.DataFrame ({'Jobs':data_vac[data_vac.columns[0]].to_list(),
                          'Спрос_на_рынке_труда_':S1,
                          'Расчет_специалистов_квадратичный':S_pred(P1, K1),
                          'Расчет_специалистов_линейный':S_pred(P2, K2)})


print (univ_realization)
print (vac_compare)

#F = plt.figure(figsize=(5,3))
F, ax1 = plt.subplots(figsize=(12,6))
sns.set()
vac_comp.set_index('Jobs').plot(kind='bar', stacked=False, grid=False, ax=ax1)
F.show()
F.savefig('F.png')

#sns.barplot(data=vac_compare)
#sns.scatterplot(data=vac_compare)
#plt.xticks(rotation=90)
#F.set_xticklabels(rotation=90)
G, ax2 = plt.subplots(figsize=(12,6))
univ_realization.set_index('University,faculty,direction').plot(kind='bar', stacked=False, grid=False, ax=ax2)
plt.xticks(rotation=90)
G.show()
G.savefig('G.png')


print(type(S1))
print(type(S_pred(P2, K2)))

Izb_quad=(S_pred(P1, K1)-S1)
Izb_lin=S_pred(P2, K2)-S2
vac_over = pd.DataFrame ({'Jobs':data_vac[data_vac.columns[0]].to_list(),
                          'Избыток_специалистов_квадратичный':Izb_lin,
                          'Избыток_специалистов_линейный':Izb_quad})
H, ax3 = plt.subplots(figsize=(12,6))
vac_over.set_index('Jobs').plot(kind='bar', stacked=False, grid=False, ax=ax3)
plt.xticks(rotation=90)
H.show()
H.savefig('H.png')


vac_dif = ((S_pred(P1, K1) / S_pred(P2, K2)) - 1) * 100
Vac_met = pd.DataFrame ({'Jobs':data_vac[data_vac.columns[0]].to_list(),
                         'Относительная_разница_мер_(лин-квадр, %)':vac_dif})
FF = plt.figure(figsize=(12,6))
sns.barplot(data=Vac_met, x='Jobs', y='Относительная_разница_мер_(лин-квадр, %)')
plt.xticks(rotation=90)
FF.show()
FF.savefig('FF.png')

qote_dif = K1-K2
univ_met = pd.DataFrame({'University,faculty,direction':data_univ[unives].to_list(),
                             'Разность_между_методами_для_квот':qote_dif})

GG = plt.figure(figsize=(12,6))
sns.barplot(data=univ_met, x='University,faculty,direction', y='Разность_между_методами_для_квот')
plt.xticks(rotation=90)
GG.show()
GG.savefig('GG.png')

#for i in range(len(K)):
#    if abs(S[i] > S_pred(P, K)[i]) < 20:
#        print("We have enough vacantions for " + data_univ.columns[i+3] + "")
