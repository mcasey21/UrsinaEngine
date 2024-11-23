from ursina import *
import random as r

# Create a replay button and initially hide it
replay_b = Button(model="quad", text="REPLAY", color=color.red, scale=0.5, y=-.4, origin=(0, 0), enabled=False)

def replay_game():
    # Reset the game when the replay button is pressed
    start_game()

def end_of_game():
    global replay_b
    
    cube.disable()
    Title.disable()
    control_1.disable()
    control_2.disable()
    control_3.disable()
    control_4.disable()
    control_5.disable()

    shift_q = Text(text="Shift + Q to exit", color=color.red, scale=2, y=-0.2, origin=(0, 0))
    the_end = Text(text="THE END", color=color.red, scale=8, origin=(0, 0))

    # Show the replay button
    replay_b.enabled = True

def start_game():
    global replay_b, cube, rside, lside, right_barrier, left_barrier

    # Hide the replay button
    replay_b.enabled = False

    cube.enable()
    Title.enable()
    control_1.enable()
    control_2.enable()
    control_3.enable()
    control_4.enable()
    control_5.enable()

    # Reset cube and other variables
    cube.x = 0
    cube.color = color.white
    cube.rotation = (0, 0, 0)
    cube.enable()

    # Reset the sides and barriers
    rside.color = color.green
    rside.texture = "block1.png"
    lside.color = color.green
    lside.texture = "block1.png"
    rside.enable()
    lside.enable()

    right_barrier.enable()
    left_barrier.enable()

app = Ursina()

speed = 2
x = 0
collision_count_right = 0
collision_count_left = 0
rdisable = False
ldisable = False

replay_b.on_click = replay_game

cube = Entity(model="cube", texture="white_cube")
rside = Entity(model="cube", scale_y=2, scale_x=0.5, scale_z=3, color=color.green, position=(4, 0, 0), texture="block1.png")
lside = Entity(model="cube", scale_y=2, scale_x=0.5, scale_z=3, color=color.green, position=(-4, 0, 0), texture="block1.png")
right_barrier = Entity(model="cube", scale_y=12, scale_x=0.25, position=(5.25, 0, 0), color=color.dark_gray)
left_barrier = Entity(model="cube", scale_y=12, scale_x=0.25, position=(-5.25, 0, 0), color=color.dark_gray)

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

def update():
    global x, speed, collision_count_right, collision_count_left, rdisable, ldisable

    collis_right = cube.intersects(rside)
    if collis_right.hit:   
        speed = -speed
        collision_count_right += 1

    collis_left = cube.intersects(lside)
    if collis_left.hit:
        speed = -speed
        collision_count_left += 1

    collis_right_barrier = cube.intersects(right_barrier)
    if collis_right_barrier.hit:   
        speed = -speed

    collis_left_barrier = cube.intersects(left_barrier)
    if collis_left_barrier.hit:   
        speed = -speed

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
        red = r.randint(0, 255)
        green = r.randint(0, 255)
        blue = r.randint(0, 255)
        cube.color = color.rgb(red, green, blue)

    if collision_count_right == 4 and collision_count_left == 4:
        end_of_game()

    if rdisable == True and ldisable == True:
        end_of_game()

    cube.x += held_keys['d'] * time.dt * speed
        
    if held_keys["r"]:
        cube.rotation_x = cube.rotation_x + time.dt * 100
        cube.rotation_y = cube.rotation_y + time.dt * 100
        cube.rotation_z = cube.rotation_z + time.dt * 100

    camera.position = (cube.x, 0, -20)

app.run()

