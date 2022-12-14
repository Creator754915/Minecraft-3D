import time
from random import randint, choice
from ursina import *
from ursina import curve
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
import numpy as np

app = Ursina()
window.borderless = False
window.exit_button.enabled = False

Sky()
player = FirstPersonController(has_pickup=False)
player.cursor.enabled = True


texture = ['assets/stone', 'assets/wood', 'assets/brick']
map_size = int(randint(15, 30))
boxes = []
bedrock = []

for o in range(4):
    for n in range(map_size):
        for k in range(map_size):
            box = Button(
                color=color.white,
                model='cube',
                position=(k, -o, n),
                texture='grass',
                shader=basic_lighting_shader,
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)

for n in range(map_size):
    for k in range(map_size):
        box = Button(
            color=color.white,
            model='cube',
            position=(k, -4, n),
            texture='bedrock',
            shader=basic_lighting_shader,
            parent=scene,
            origin_y=0.5
        )
        bedrock.append(box)


def tree():
    for n in range(3):
        global x
        x= int(randint(1, map_size))
        global z
        z = int(randint(1, map_size))
        for t in range(5):
            box = Button(
                color=color.white,
                model='cube',
                position=(x, t, z),
                texture='wood',
                shader=basic_lighting_shader,
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)
        for l in range(2):
            box = Button(
                color=color.white,
                model='cube',
                position=(x, 5 + l, z),
                texture='leaves',
                shader=basic_lighting_shader,
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)
        for l1 in range(2):
            box = Button(
                color=color.white,
                model='cube',
                position=(x + l1, 5, z),
                texture='leaves',
                shader=basic_lighting_shader,
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)
        for l1 in range(2):
            box = Button(
                color=color.white,
                model='cube',
                position=(x - l1, 5, z),
                texture='leaves',
                shader=basic_lighting_shader,
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)
        for l2 in range(2):
            box = Button(
                color=color.white,
                model='cube',
                position=(x, 5, z + l2),
                texture='leaves',
                shader=basic_lighting_shader,
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)
        for l2 in range(2):
            box = Button(
                color=color.white,
                model='cube',
                position=(x, 5, z - l2),
                texture='leaves',
                shader=basic_lighting_shader,
                parent=scene,
                origin_y=0.5
            )
            boxes.append(box)


def ignore():
    all_version.visible = False
    all_version.y = 10


hand = Entity(model='cube', texture='hand', rotation=(-30, -45),
              position=(0.25, -0.6), parent=camera.ui, scale=(0.2, 0.2))

pickup = Entity(model='sphere', position=(10, 1, 5))

camera.z = 0
tree()

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

txt_chat_info = Text(text='', scale=2, color='#fc0000', x=-.85, y=-0.27)
txt_save_code = Text(text='', scale=1.5, color='#fc0000', x=-.85, y=-0.37)

chat_input = InputField()
chat_input.x = -0.62
chat_input.y = -0.47
chat_input.visible = False

all_version = Button(
    text="Pay just 0.99$ for the all version",
    color=color.black,
    scale=2
)

all_version.on_click = ignore

number_of_particles = 1000   # keep this as low as possible
points = np.array([Vec3(0,0,0) for i in range(number_of_particles)])
directions = np.array([Vec3(random.random()-.5,random.random()-.5,random.random()-.5)*.05 for i in range(number_of_particles)])
frames = []

# simulate the particles once and cache the positions in a list.
for i in range(60*1):
    points += directions
    frames.append(copy(points))


class ParticleSystem(Entity):
    def __init__(self, **kwargs):
        super().__init__(model=Mesh(vertices=points, mode='point', static=False, render_points_in_3d=True, thickness=.1), t=0, duration=1, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.t += time.dt
        if self.t >= self.duration:
            destroy(self)
            return

        self.model.vertices = frames[floor(self.t * 60)]
        self.model.generate()


def update():
    if player.y == -10 or player.y < -10:
        txt_dead = Text(text='Your are dead', scale=4, color='#fc0000', x=-.40, y=0)
        dead_punch.play()
        player.y = 1
        player.x = randint(0, map_size)
        player.z = randint(0, map_size)

    if player.y == 15 or player.y > 149:
        player.y = 15

    if not player.has_pickup and distance(player, pickup) < pickup.scale_x / 2:
        player.has_pickup = True
        pickup.animate_scale(0, duration=.1)
        destroy(pickup, delay=.1)

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
                    position=box.position + mouse.normal,
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
                p = ParticleSystem(position=Vec2(box.position, mouse.normal),
                                   color=color.green, rotation_y=random.random() * 360)
                p.fade_out(duration=.2, delay=1 - .2, curve=curve.linear)

    if held_keys['tab']:
        if camera.z == -5:
            camera.z = 0.05
            hand.visible = True
        else:
            camera.z = -5
            hand.visible = False
    if held_keys['left mouse']:
        hand.position = (0.45, -0.5)
    elif held_keys['right mouse']:
        hand.position = (0.45, -0.5)
    else:
        hand.position = (0.5, -0.6)
    if held_keys['t']:
        chat_input.visible = True
    if held_keys['enter']:
        print(chat_input.text)
        time.sleep(0.5)
        if chat_input.text == '("forme":"sphere")':
            print("true")
        else:
            txt_chat_info.text = 'Error'

    # save map with code

    if held_keys['c']:
        code = map_size + x + z
        txt_save_code.text = f"{code}"

    # admin option

    if held_keys['l']:
        print(boxes)
        print(bedrock)
        player.cursor.enabled = True
        wp = WindowPanel(
            title='Admin Window',
            content=(
                Text('Name:'),
                InputField(name='admin_name'),
                Text('Password:'),
                InputField(name='admin_password'),
                Button(text='Submit', color=color.azure),
                ButtonGroup(('test', 'reload', 'quit'))
            ),
        )
        wp.y = wp.panel.scale_y / 2 * wp.scale_y


app.run()
