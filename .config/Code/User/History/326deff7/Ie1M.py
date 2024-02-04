import turtle

def square(turtle,l):
    for i in range(4):
        turtle.fd(l)
        turtle.lt(90)
def main():
    t = turtle.Turtle()
    square(t,50)
    turtle.mainloop()

if __name__ == "__main__":
    main()