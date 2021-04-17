import random
import pandas as pd
import math
from sklearn.preprocessing import Normalizer

specializations = ['Программист_JavaScript', 'HTML-верстальщик', 'Программист_Python', 'Программист_C#', 'DevOps',
                   'Системный_аналитик']
rank = ('low', 'medium', 'high')
# columns = ['Вуз_Факультет_Направление']
columns = ['low_bound', 'high_bound']
for name in specializations:
    for i in range(len(rank)):
        columns.append(name + '_' + rank[i])
columns.append('остальное')

universities = ['МГУ_им_МВЛомоносова', 'МГТУ_им_НЭБаумана', 'МИСиС', 'Университет_Синергия', 'НГУ']
faculties = ['fac1_dir1', 'fac1_dir2', 'fac2_dir1', 'fac2_dir3', 'fac3_dir2', 'fac3_dir1', 'fac3_dir4']
index = []
for name in universities:
    for i in range(len(faculties)):
        index.append(name + '_' + faculties[i])
df = pd.DataFrame(columns=columns, index=index)
for col in df.columns:
    df[col] = df[col].apply(lambda x: random.random())

df.iloc[:, 2:] = Normalizer(norm='l1').fit_transform(df.iloc[:, 2:])

# for col in (df.columns[0], df.columns[1]):
df[df.columns[0]] = df[df.columns[0]].apply(lambda x: random.randint(10, 120))
df[df.columns[1]] = df[df.columns[0]].apply(lambda x: 2 * x)

pd.set_option('display.max_columns', 5)

print(df)

df.to_csv('test_data.csv')


sum1 = df.iloc[:, 0].sum() / df.shape[0]
print(sum1)

sr = pd.Series([(lambda x: random.randint(math.ceil(sum1 * 0.8), math.ceil(sum1 * 1.2)))(i) for i in range(len(index))], index=index)
print(sr)

sr.to_csv('test_vacancies.csv')
