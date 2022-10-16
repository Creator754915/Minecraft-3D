import time
from random import randint, choice
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader

app = Ursina()

Sky()
player = FirstPersonController()
player.y = 1

Cursor(texture='sword', color=color.gold)

texture = ['assets/stone', 'assets/wood', 'assets/brick']
map_size = int(randint(15, 40))
boxes = []

for n in range(map_size):
    for k in range(map_size):
        box = Button(
          color=color.white,
          model='cube',
          position=(k,1,n),
          texture='grass',
          shader=basic_lighting_shader,
          parent=scene,
          origin_y=0.5
        )
        boxes.append(box)

for o in range(2):
    for n in range(map_size):
        for k in range(map_size):
            box = Button(
              color=color.white,
              model='cube',
              position=(k,-o,n),
              texture='assets/stone',
              shader=basic_lighting_shader,
              parent=scene,
              origin_y=0.5
            )
            boxes.append(box)


sword = Entity(model='cube', texture='grass', rotation=(-30, -45),
               position=(0.25, -0.6), parent=camera.ui, scale=(0.2, 0.2))

dead_punch = Audio(
    "assets\\dead_sound.mp3",
    loop=False,
    autoplay=False
)


slider_x = ThinSlider(text="X: ", min=0, max=50, default=0, x=-.65, dynamic=True)
slider_x.scale *= .75
slider_y = ThinSlider(text="Y: ", min=0, max=50, default=0, x=-.65, y=-.04, dynamic=True)
slider_y.scale *= .75
slider_z = ThinSlider(text="Z: ", min=0, max=50, default=0, x=-.65, y=-.08, dynamic=True)
slider_z.scale *= .75

txt_chat_info = Text(text='', scale=2, color='#fc0000', x=-.80, y=-0.27)

chat_input = InputField()
chat_input.x = -0.62
chat_input.y = -0.47
chat_input.visible = False


def update():
    if player.y == -10 or player.y < -10:
        txt_dead = Text(text='Your are dead', scale=4, color='#fc0000', x=-.40, y=0)
        dead_punch.play()
        player.y = 1
        player.x = randint(0, map_size)
        player.z = randint(0, map_size)

    slider_x.value = player.x
    slider_y.value = player.y
    slider_z.value = player.z


def input(key):
    block_texture = choice(texture)
    for box in boxes:
        if box.hovered:
            if key == 'right mouse down':
                new = Button(
                    color=color.white,
                    model='cube',
                    position=box.position+
                    mouse.normal,
                    highlight_color=color.light_gray,
                    texture=block_texture,
                    shader=basic_lighting_shader,
                    parent=scene,
                    origin_y=0.5
                )
                boxes.append(new)
            if key == 'left mouse down':
                boxes.remove(box)
                destroy(box)

    if held_keys['left mouse']:
        sword.position = (0.45, -0.5)
    elif held_keys['right mouse']:
        sword.position = (0.45, -0.5)
    else:
        sword.position = (0.5, -0.6)
    if held_keys['t']:
        chat_input.visible = True
    if held_keys['enter']:
        print(chat_input.text)
        time.sleep(0.5)
        if chat_input.text == '("forme":"sphere")':
            print("true")
        else:
            txt_chat_info.text = 'Error'


app.run()