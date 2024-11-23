from ursina import *
import random as r


def end_of_game():
    global shift_q, the_end
    B.y=-.35 
    cube.disable()
    Title.disable()
    control_1.disable()
    control_2.disable()
    control_3.disable()
    control_4.disable()
    control_5.disable()

    shift_q = Text(text="Shift + Q to exit",color=color.red,scale=2,y=-.2,origin=(0, 0))
    the_end = Text(text="THE END",color=color.red,scale=8,origin=(0, 0))
    
def update():
    global x, speed, collision_count_right, collision_count_left, rdisable, ldisable

    collis_right = cube.intersects(rside)
    if collis_right.hit:   
        speed= -speed
        collision_count_right += 1

    collis_left = cube.intersects(lside)
    if collis_left.hit:
        speed= -speed
        collision_count_left += 1

    collis_right_barrier = cube.intersects(right_barrier)
    if collis_right_barrier.hit:   
        speed= -speed

    collis_left_barrier = cube.intersects(left_barrier)
    if collis_left_barrier.hit:   
        speed= -speed

    if collision_count_right == 1:
        rside.color = color.yellow
        rside.texture = "block2.png"
    elif collision_count_right == 2:
        rside.color = color.orange
        rside.texture = "block3.png"
    elif collision_count_right == 3:
        rside.color = color.red
        rside.texture = "block4.png"
    elif collision_count_right == 4:
        rdisable = True
        rside.disable()

    if collision_count_left == 1:
        lside.color = color.yellow
        lside.texture = "block2.png"
    elif collision_count_left == 2:
        lside.color = color.orange
        lside.texture = "block3.png"
    elif collision_count_left == 3:
        lside.color = color.red
        lside.texture = "block4.png"
    elif collision_count_left == 4:
        ldisable = True
        lside.disable()
        
    if held_keys["c"]:
        red=r.randint(0,255)
        green=r.randint(0,255)
        blue=r.randint(0,255)
        cube.color=color.rgb(red,green,blue)

    if collision_count_right == 4 and collision_count_left == 4:
        end_of_game()

    if rdisable == True and ldisable == True:
        end_of_game()

    cube.x += held_keys['d'] * time.dt *speed
        
    if held_keys["r"]:
        cube.rotation_x=cube.rotation_x+time.dt*100
        cube.rotation_y=cube.rotation_y+time.dt*100
        cube.rotation_z=cube.rotation_z+time.dt*100

    camera.position=(cube.x,0,-20)

app = Ursina()

B=Button(text="replay", color=color.red, scale=(.25, .1), y=1)
#B.on_mouse_enter=reset

speed = 2
x=0
collision_count_right = 0
collision_count_left = 0
rdisable = False
ldisable = False

cube = Entity(model="cube", texture="white_cube")
rside = Entity(model="cube", scale_y=2, scale_x=0.5, scale_z =3, color=color.green, position=(4,0,0), texture="block1.png")
lside = Entity(model="cube", scale_y=2, scale_x=0.5, scale_z =3, color=color.green, position=(-4,0,0), texture="block1.png")
right_barrier = Entity(model="cube", scale_y=12, scale_x=0.25, position=(5.25,0,0), color=color.dark_gray)
left_barrier = Entity(model="cube", scale_y=12, scale_x=0.25, position=(-5.25,0,0), color=color.dark_gray)

Title = Text(text="Spiny Colourful Cube", color=color.red, scale=3, y= +.4, x= -.365)
control_1 = Text(text="CONTROLS", color=color.red, scale=1.5, y= +.4, x= -.8)
control_2 = Text(text="rotate cube [r]", color=color.red, scale=1, y= +.365, x= -.8)
control_3 = Text(text="change colour [c]", color=color.red, scale=1, y= +.340, x= -.8)
control_4 = Text(text="movement [d]", color=color.red, scale=1, y= +.315, x= -.8)
control_5 = Text(text="exit [Shift+Q]", color=color.red, scale=1, y= +.290, x= -.8)

rside.collider = 'box'
lside.collider = 'box' 
cube.collider = 'box'
right_barrier.collider = 'box'
left_barrier.collider = 'box'

app.run()