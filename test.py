import csv


# f=open("test.csv", "r")
# if f.mode == 'r':
#     contents =f.read()
#     print(contents)

f=open("data.txt","r")
lines=f.read()
result=[lines]
print(result)
f.close()