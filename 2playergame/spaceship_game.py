from ursina import *
import random

app = Ursina()

offset = 0
background = Entity(model="quad", scale=(20,10), texture="background.png", z=.1)

asteroid_entities = []  # Create a list to store asteroid entities.

def spawn_rectangle():
    global asteroid_entities

    for i in range(len(asteroid_entities)):
        # Reset the position of existing asteroids
        asteroid_entities[i].position = (random.uniform(-1, 1), random.uniform(-4, 4), 0)

    # If there are fewer asteroids than expected, create new ones
    for _ in range(5 - len(asteroid_entities)):
        asteroid = Entity(model="quad", scale=(0.8, 0.8, 0.8), texture="asteroid.png")
        asteroid.collider = 'box'
        random_x = random.uniform(-1, 1)
        random_y = random.uniform(-4, 4)
        asteroid.position = (random_x, random_y, 0)
        asteroid_entities.append(asteroid)

def input(key):
    if key=="x":
        left_bullet.position = (left_ship.x+.7, left_ship.y)
        left_bullet.enabled = True
    
    if key=="m":
        right_bullet.position = (right_ship.x-.7, right_ship.y)
        right_bullet.enabled = True

def update():
    global speed, entity, offset, Rcollis_counter, Lcollis_counter

    offset+=time.dt*.1
    setattr(background, "texture_offset", (offset, 0))

    left_bullet.x += time.dt * speed
    right_bullet.x -= time.dt * speed

    left_ship.y += held_keys['w'] * time.dt *speed
    left_ship.y -= held_keys['s'] * time.dt *speed
    left_ship.x += held_keys['d'] * time.dt *speed
    left_ship.x -= held_keys['a'] * time.dt *speed

    right_ship.y += held_keys['i'] * time.dt *speed
    right_ship.y -= held_keys['k'] * time.dt *speed
    right_ship.x += held_keys['l'] * time.dt *speed
    right_ship.x -= held_keys['j'] * time.dt *speed

    Lcollis_top = left_ship.intersects(top_barrier)
    if Lcollis_top.hit:
        left_ship.y = top_barrier.y - top_barrier.scale_y / 2 - left_ship.scale_y / 2

    Lcollis_bottom = left_ship.intersects(bottom_barrier)
    if Lcollis_bottom.hit:
        left_ship.y = bottom_barrier.y + bottom_barrier.scale_y / 2 + left_ship.scale_y / 2

    Lcollis_left = left_ship.intersects(left_barrier)
    if Lcollis_left.hit:
        left_ship.x = left_barrier.x + left_barrier.scale_x / 2 + left_ship.scale_x / 2
    
    Lcollis_left_middle = left_ship.intersects(left_middle_barrier)
    if Lcollis_left_middle:
        left_ship.x = left_middle_barrier.x - left_middle_barrier.scale_x / 2 - left_ship.scale_x / 2

    Rcollis_top = right_ship.intersects(top_barrier)
    if Rcollis_top.hit:
        right_ship.y = top_barrier.y - top_barrier.scale_y / 2 - right_ship.scale_y / 2

    Rcollis_bottom = right_ship.intersects(bottom_barrier)
    if Rcollis_bottom.hit:
        right_ship.y = bottom_barrier.y + bottom_barrier.scale_y / 2 + right_ship.scale_y / 2

    Rcollis_right = right_ship.intersects(right_barrier)
    if Rcollis_right.hit:
        right_ship.x = right_barrier.x - right_barrier.scale_x / 2 - right_ship.scale_x / 2
        
    Rcollis_right_middle = right_ship.intersects(right_middle_barrier)
    if Rcollis_right_middle.hit:
        right_ship.x = right_middle_barrier.x + right_middle_barrier.scale_x / 2 +  right_ship.scale_x / 2

    for asteroid in asteroid_entities:
        collis_lbullet_asteroid = left_bullet.intersects(asteroid)
        if collis_lbullet_asteroid.hit:
            left_bullet.enabled = False
    for asteroid in asteroid_entities:
        collis_rbullet_asteroid = right_bullet.intersects(asteroid)
        if collis_rbullet_asteroid.hit:
            right_bullet.enabled = False

    if left_bullet.enabled:
        collis_lbullet_rship = left_bullet.intersects(right_ship)
        if collis_lbullet_rship.hit:
            Rcollis_counter+=1
            rship_hit_animation.start()
            left_bullet.enabled=False

    if Rcollis_counter ==2:
        right_ship.enabled=False
        print_on_screen("LEFT SIDE WINS")

    if right_bullet.enabled:
        collis_rbullet_lship = right_bullet.intersects(left_ship)
        if collis_rbullet_lship.hit:
            Lcollis_counter+=1
            lship_hit_animation.start()
            right_bullet.enabled=False

    if Lcollis_counter ==2:
        left_ship.enabled=False
        print_on_screen("RIGHT SIDE WINS")
                   
def spawn_timer():
    spawn_rectangle()
    invoke(spawn_timer, delay=6)  # Call spawn_timer again after 10 seconds.

spawn_timer()

speed = 3
Rcollis_counter = 0
Lcollis_counter = 0

left_ship = Entity(model="quad", scale=1, x=-4.5, y=0, texture="left_spaceship.png", enabled=True)
right_ship = Entity(model="quad", scale=1, x=4.5, y=0, texture="right_spaceship.png", enabled=True)
left_ship.collider = 'box'
right_ship.collider = 'box'

top_barrier = Entity(model="quad", scale_x=14, scale_y=.5, color=color.dark_gray, position=(0,4.5,0), visible=False)
bottom_barrier = Entity(model="quad", scale_x=14, scale_y=.5, color=color.dark_gray, position=(0,-4.5,0), visible=False)
top_barrier.collider = 'box'
bottom_barrier.collider = 'box'

right_middle_barrier = Entity(model="quad", scale_x=.5, scale_y=14, color=color.dark_gray, position=(2,0,0), visible=False)
left_middle_barrier = Entity(model="quad", scale_x=.5, scale_y=14, color=color.dark_gray, position=(-2,0,0), visible=False)
left_middle_barrier.collider = 'box'
right_middle_barrier.collider = 'box'

right_barrier = Entity(model="quad", scale_x=.5, scale_y=14, color=color.dark_gray, position=(7.5,0,0), visible=False)
left_barrier = Entity(model="quad", scale_x=.5, scale_y=14, color=color.dark_gray, position=(-7.5,0,0), visible=False)
left_barrier.collider = 'box'
right_barrier.collider = 'box'

left_bullet = Entity(model="quad", enabled=False, scale_x=.6, scale_y=.4, texture="left_bullet.png")
right_bullet = Entity(model="quad", enabled=False, scale_x=.6, scale_y=.4, texture="right_bullet.png")
left_bullet.collider = 'box'
right_bullet.collider = 'box'

rship_hit_animation = Sequence(1, Func(right_ship.blink, duration=1), loop=False)
lship_hit_animation = Sequence(1, Func(left_ship.blink, duration=1), loop=False)

app.run()
