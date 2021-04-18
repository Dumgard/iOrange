import pandas as pd
import random

a1 = ['Иванов', 'Петров', 'Фролов', 'Сидоров', 'Игнатьев', 'Николаев']
b1 = ['Андрей', 'Юрий', 'Григорий', 'Василий', 'Максим']
c1 = ['Семёнович', 'Евгеньевич', 'Михайлович', 'Егорович', 'Аркадьевич']
book_names = [x + '_' + y + '_' + z for x in a1 for y in b1 for z in c1]

a2 = ['Иванов', 'Спиридонов', 'Фролов', 'Сидоров', 'Игнатьев', 'Николаев']
b2 = ['Андрей', 'Юрий', 'Григорий', 'Василий', 'Алексей']
c2 = ['Семёнович', 'Игнатьевич', 'Михайлович', 'Егорович', 'Аркадьевич']
graduate_names = [x + '_' + y + '_' + z for x in a2 for y in b2 for z in c2]

specializations = ['Программист_JavaScript', 'HTML-верстальщик', 'Программист_Python', 'Программист_C#', 'DevOps',
                   'Системный_аналитик', 'Сварщик_3_разряд', 'Преподаватель_информатики', 'Менеджер_по_продажам']
rank = ('low', 'medium', 'high')
# columns = ['Вуз_Факультет_Направление']
# columns = []
# for name in specializations:
#     for i in range(len(rank)):
#         columns.append(name + '_' + rank[i])
# columns.append('остальное')

books = pd.DataFrame(columns=['Имя', 'Специализация', 'Зарплата'], index=list(map(str, range(len(book_names)))))
# books['Имя'] = books['Имя'].apply(lambda x: book_names[random.randint(0, len(book_names)-1)])
books['Имя'] = book_names
books['Специализация'] = books['Специализация'].apply(lambda x: specializations[random.randint(0, len(specializations)-1)])
books['Зарплата'] = books['Зарплата'].apply(lambda x: rank[random.randint(0, len(rank)-1)])

print(books)
books.to_csv('books.csv')


universities = ['МГУ_им_МВЛомоносова', 'МГТУ_им_НЭБаумана', 'МИСиС', 'Университет_Синергия', 'НГУ']
faculties = ['fac1_dir1', 'fac1_dir2', 'fac2_dir1', 'fac2_dir3', 'fac3_dir2', 'fac3_dir1', 'fac3_dir4']

grads = pd.DataFrame(columns=['Имя', 'Высшее_учебное_заведение', 'Факультет_Направление'], index=list(map(str, range(len(graduate_names)))))
# grads['Имя'] = grads['Имя'].apply(lambda x: graduate_names[random.randint(0, len(graduate_names)-1)])
grads['Имя'] = graduate_names
grads['Высшее_учебное_заведение'] = grads['Высшее_учебное_заведение'].apply(lambda x: universities[random.randint(0, len(universities)-1)])
grads['Факультет_Направление'] = grads['Факультет_Направление'].apply(lambda x: faculties[random.randint(0, len(faculties)-1)])

print(grads)
grads.to_csv('grads.csv')
