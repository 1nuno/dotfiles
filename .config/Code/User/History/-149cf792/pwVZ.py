import turtle


def is_complement(sentence1,sentence2):
    if len(sentence1) != len(sentence2):
        return False
    else:
        ref = ['at','ta','cg','gc']
        for a,b in zip(sentence1,sentence2):
            if a+b not in ref:
                return False
    return True

def is_embbeded(s1,s2):
    if s1 == s2:
        return True
    elif len(s1) >= len(s2):
        return False
    else:
        c=0
        for i in s2:
            if i == s1[c]:
                c+=1
            if c == len(s1):
                return True
        return False

def is_balanced(cadeia):
    c=0
    for i in cadeia:
        if i.lower() in 'at':
            c+=1
    if c == len(cadeia)-c:
        return True
    return False


def is_connected_n(s1,s2,n):
    for j in range(len(s1)):
        s1 = s1[j:]
        for i in range(len(s2)):
            if s2[i:i+n] == s1[:n]:
                return True
    return False


def draw_regular(t,side,n):
    angle = 360/n
    for _ in range(n):
        t.fd(side)
        t.lt(angle)

def draw_star(t,side,n,pointy):
    angle = 360/n
    for _ in range(n):
        t.lt(pointy)
        t.fd(side/2)
        t.rt(120-2*pointy)
        t.fd(side/2)
        t.lt(pointy+angle)

def draw_spiral_regular(t,side,n,m):
    for _ in range(m):
        draw_regular(t,side,n)
        t.lt(20)
        side *= 0.98

# print(is_complement('attg','taag'))
# print(''.join([a+b for a,b in zip('abc','DEF'[::-1])]))
# print(is_embbeded('abc','dddadddbdddcc'))
# print(is_balanced('ATCGCA'))
# print(is_connected_n('abacadabra','aabcadatb',5))

t = turtle.Turtle()
t.speed(5)
draw_star(t,50,4,15)
side = 50
turtle.exitonclick()