import pyglet
import color_2048
import random
from pyglet.window import key

WS = 450
BS = 100
GS = 10

class grid:
    def __init__(self):
        pass
    def draw(self):
        for i in range(4):
            for j in range(4):
                pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                                     ('v2f', [GS+(GS+BS)*i, GS+(GS+BS)*j,
                                              GS+(GS+BS)*i+BS, GS+(GS+BS)*j,
                                              GS+(GS+BS)*i+BS, GS+(GS+BS)*j+BS,
                                              GS+(GS+BS)*i, GS+(GS+BS)*j+BS]),
                                     ('c3f', color_2048.get_bg_color() * 4))

class block:
    def __init__(self,value,i=0,j=0):
        self.value = value
        self.x = 0
        self.y = 0
        self.set_index(i, j)
        self.label = pyglet.text.Label(str(value),
                                       x=self.x, y=self.y,
                                       anchor_x='center', anchor_y='center',
                                       color=color_2048.get_font_color())

    def set_index(self, i, j):
        self.i = i
        self.j = j
        self.x = GS + BS/2 + (GS + BS) * self.j
        self.y = GS + BS/2 + (GS + BS) * self.i
    
    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', [self.x-BS/2, self.y-BS/2,
                                      self.x+BS/2, self.y-BS/2,
                                      self.x+BS/2, self.y+BS/2,
                                      self.x-BS/2, self.y+BS/2]),
                             ('c3f', color_2048.get_block_color(self.value) * 4))
        self.label.draw()

window = pyglet.window.Window(WS, WS)

blocks = [[None]*4,[None]*4,[None]*4,[None]*4]
grids = grid()

i, j = random.randrange(0, 4), random.randrange(0, 4)
blocks[i][j] = block(random.randrange(1,3)*2, i, j)
print(i, j)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        print("left")

@window.event
def on_mouse_press(x, y, button, modifiers):
    print(x, y)

@window.event
def on_draw():
    window.clear()
    grids.draw()
    for col in blocks:
        for b in col:
            if b is not None:
                b.draw()

pyglet.app.run()
