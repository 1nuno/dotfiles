import turtle

#def square(turtle_instance,size):
#    for i in range(4):
#        turtle_instance.fd(size)
#        turtle_instance.lt(90)
#
#def concentric_squares(turtle_instance,size,number,padding,outer=False):
#    if outer:
#        for i in range(number):
#            square(turtle_instance,size)
#            turtle_instance.pu()
#            for _ in range(2):
#                turtle_instance.rt(90)
#                turtle_instance.fd(padding)
#            turtle_instance.pd()
#            turtle_instance.lt(180) 
#            size += padding*2
#    else:
#        for i in range(number):
#            square(turtle_instance,size)
#            turtle_instance.pu()
#            for _ in range(2):
#                turtle_instance.fd(padding)
#                turtle_instance.lt(90)
#            turtle_instance.pd()
#            turtle_instance.lt(180) 
#            size -= padding*2

def s(turtle_instance,radius):
    turtle_instance.circle(-radius,180)
    turtle_instance.circle(-radius,-180)
    

def main():
    t = turtle.Turtle()
    #t.pensize(5)
    #concentric_squares(t,200,6,20,outer=True)
    s(t,50)
    turtle.mainloop()

if __name__ == "__main__":
    main()