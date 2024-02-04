import random

def while_as_for():
    for i in range(20,0,-2):
        print(i)

def lanca_dado(n):
    dado = [1,2,3,4,5,6]
    c = 0
    for _ in range(n):
        if dado[random.randint(0,5)]%2 == 0:
            c+=1
    return round(c/n,2)*100

def padrao(n):
    ref = list(range(1,n+1))
    for i in range(n+1):
        print(*ref[:i])
    return ''

def padrao2(n):
    ref = list(range(1,n+1))
    for i in range(-(n+1),0,-1):
        print(*ref[:i])
    return ''

# while_as_for()
# print(lanca_dado(5))
print(padrao2(5))