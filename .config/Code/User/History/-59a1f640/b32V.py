import random
import turtle

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

def padrao2(n):
    for i in range(n+1,1,-1):
        print(*list(range(1,i)))

def padrao3(n):
    ref = list(range(1,n+1))
    for i in range(1,n+1):
        aux = ref[:i]
        aux.extend([' ' for _ in range(n-i)])
        print(*aux[::-1])

def draw_square(t,lado):
    for i in range(4):
        t.fd(lado)
        t.lt(90)

def grelha(t,lado):
    for i in range():
        
        pass

# while_as_for()
# print(lanca_dado(5))
# padrao(5)
# print()
# padrao2(5)
# print()
# padrao3(5)

def desenha_estrela(t,lado,n):
    for i in range(n):
        t.fd(lado)
        t.lt(360/n)


if __name__ == '__main__':
    t = turtle.Turtle()
    desenha_estrela(t,100,4)
    x = 75
    myfunc()
    print(x)