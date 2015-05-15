import pyglet
import color_2048
import random

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

blocks = [[],[],[],[]]

for i in range(16):
    e = random.randrange(1, 12)
    value = pow(2, e)
    blocks[i//4].append(block(value, x=(i//4)*40, y=(i%4)*40))


@window.event
def on_draw():
    window.clear()
    for col in blocks:
        for b in col:
            b.draw()

pyglet.app.run()
