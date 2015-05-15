import pyglet
import color_2048
import random
from pyglet.window import key

class block:
    def __init__(self,value,x=40,y=40,width=40,height=40):
        self.value = value
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = pyglet.text.Label(str(value),
                                       x=self.x+self.width/2, y=self.y+self.height/2,
                                       anchor_x='center', anchor_y='center',
                                       color=color_2048.get_font_color())
        
    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', [self.x, self.y, self.x+self.width, self.y,
                                      self.x+self.width, self.y+self.height, self.x, self.y+self.height]),
                             ('c3f', color_2048.get_block_color(self.value) * 4))
        self.label.draw()

window = pyglet.window.Window()

blocks = [[None]*4,[None]*4,[None]*4,[None]*4]

i, j = random.randrange(0, 4), random.randrange(0, 4)
blocks[i][j] = block(random.randrange(1,3)*2, x=i*40, y=j*40)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        print("left")

@window.event
def on_draw():
    window.clear()
    for col in blocks:
        for b in col:
            if b is not None:
                b.draw()

pyglet.app.run()
