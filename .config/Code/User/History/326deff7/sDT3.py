import turtle

def square(turtle,l):
    for i in range(4):
        turtle.fd(l)
        turtle.lt(90)

def draw_chess_board(turtle,size,l):
    for i in range(size):
        for i in range(size):
            square(turtle,l)
            turtle.fd(l)
        turtle.lt(90)
        turtle.fd(l)
        turtle.rt(90)
        turtle.fd(-1*(l*size))


def main():
    t = turtle.Turtle()
    draw_chess_board(t,5,50)
    turtle.mainloop()

if __name__ == "__main__":
    main()