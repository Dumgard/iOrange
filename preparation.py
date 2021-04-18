import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer

data_students = pd.read_csv("grads.csv")
data_vacancies = pd.read_csv("books.csv")
print(data_vacancies.head())
print(data_students.head())

names = data_vacancies["Имя"]
specializations = ['Программист_JavaScript', 'HTML-верстальщик', 'Программист_Python', 'Программист_C#', 'DevOps',
                   'Системный_аналитик']

special_cost = []
for i in specializations:
    special_cost.append(i+"_low")
    special_cost.append(i+"_medium")
    special_cost.append(i+"_high")

special_cost.append("прочее")

data_full = pd.DataFrame(columns = special_cost)
print(data_full.columns)

for name in names:
    if name in data_students["Имя"].to_list():
        grad = data_students.loc[data_students['Имя'] == name]
        book = data_vacancies.loc[data_vacancies['Имя'] == name]
        print(grad)
        print(book["Специализация"].item())
        if book["Специализация"].item() in specializations:
            univ = grad['Высшее_учебное_заведение'].item()+"_"+grad['Факультет_Направление'].item()
            spec = book["Специализация"].item()+"_"+book["Зарплата"].item()
            print(univ, spec)
            if univ in data_full.index:
                print("YES")
                print(data_full.loc[univ, spec])
                data_full.loc[univ, spec] = data_full[spec][univ] + 1
            else:
                print("NO")
                new_row = pd.Series(data={i: 0 for i in special_cost}, name=univ)
                print(new_row)
                data_full = data_full.append(new_row, ignore_index=False)
                print(data_full)
                data_full.loc[univ, spec] = 1
        else:
            univ = grad['Высшее_учебное_заведение'].item()+"_"+grad['Факультет_Направление'].item()
            if univ in data_full.index:
                data_full.loc[univ, 'прочее'] = data_full['прочее'][univ] + 1
            else:
                new_row = pd.Series(data={i: 0 for i in special_cost}, name=univ)
                data_full = data_full.append(new_row, ignore_index=False)
                data_full.loc[univ, 'прочее'] = 1

print(data_full.sum().sum())
data_full.iloc[:,:] = Normalizer(norm='l1').fit_transform(data_full.iloc[:,:])

print(data_full)
print(data_full.describe())
print(data_full.sum().sum())
data_full.to_csv("data.csv")