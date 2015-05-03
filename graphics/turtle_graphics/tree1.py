import turtle # Import turtle graphics.

def drawBranch(size, angle): # Recursive function to draw a part of the tree.
    turtle.fd(size)
    if size>5:
        turtle.rt(angle/2)
        drawBranch(size*0.75, angle)
        turtle.lt(angle)
        drawBranch(size*0.75, angle)
        turtle.rt(angle/2)
    turtle.bk(size)

# This is the main program.       
size=180 # Base element size for the tree.
angle=60 # Angle between the branches.
turtle.tracer(8,0) # Speed up the drawing...a lot. Replace 8 with 16 or 32 for even faster drawing.
turtle.mode('logo') # Use LOGO language orientation: turtle faces upward.
turtle.pu() # Pull up the pen to pre-position the turtle.
turtle.bk(size*2)
turtle.pd() # Then put the pen back down to draw.
drawBranch(size, angle) # Draw the tree.
