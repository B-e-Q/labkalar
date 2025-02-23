import re

with open('row.txt', "r", encoding='utf-8') as file:
    txt = file.read()


#task 1
pattern = re.findall(r'ab{0,}', txt)
print(pattern)

#task 2
pattern = re.findall(r'ab{2,3}', txt)
print(pattern)

#task 3
pattern = re.findall(r'[a-z]*+_[a-z]*', txt)
print(pattern)

#task 4
pattern = re.findall(r'[A-Z]{1}+[a-z]+', txt)
print(pattern)

#task 5
pattern = re.findall(r'a.*?b', txt)
print(pattern)

#task 6
pattern = re.sub(r'[ ,.]', ':', txt)
print(pattern)

#task 7
pattern = re.findall(r'[A-Za-z]+_[A-Za-z]+', txt)
cc = []
for i in pattern:
    a = i.split('_')
    cc.append(a[0]+''.join(x.capitalize() for x in a[1:]))
print(cc)

#task 8
pattern = re.findall(r'[A-Z][^A-Z]+', txt)
print(pattern)

#task 9
pattern = re.sub(r'(?<!^)(?=[A-Z])', ' ', txt)
print(pattern)

#task 10
pattern = re.findall(r'[A-Za-z]+[A-Z]+', txt)
cc = []
for i in pattern:
    cc.append(re.sub(r'(?<!^)(?=[A-Z])', '_', i).lower())
print(cc)