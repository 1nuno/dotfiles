import turtle

def square(turtle,l):
    for i in range(4):
        turtle.fd(l)
        turtle.lt(90)

def draw_chess_board(turtle,size,l,fill='black'):
    turtle.fillcolor(fill)
    for j in range(size):
        for i in range(size):
            if (i+j)%2 == 0:
                turtle.begin_fill()
                square(turtle,l)
                turtle.fd(l)
                turtle.end_fill()
            else:
                square(turtle,l)
                turtle.fd(l)
        turtle.lt(90)
        turtle.fd(l)
        turtle.rt(90)
        turtle.fd(-1*(l*size))


def main():
    t = turtle.Turtle()
    draw_chess_board(t,3,50)
    turtle.mainloop()

if __name__ == "__main__":
    main()