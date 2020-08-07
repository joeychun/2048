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
        self.label = pyglet.text.Label(str(value),
                                       x=self.x, y=self.y,
                                       anchor_x='center', anchor_y='center',
                                       color=color_2048.get_font_color())
        self.merged = False
        self.moved = False
        
        self.set_index(i, j)

    def set_index(self, i, j):
        self.i = i
        self.j = j
        self.x = GS + BS/2 + (GS + BS) * self.j
        self.y = GS + BS/2 + (GS + BS) * self.i
        self.label.x = self.x
        self.label.y = self.y

    def set_value(self, value):
        self.value = value
        self.label.text = str(value)
    
    def draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', [self.x-BS/2, self.y-BS/2,
                                      self.x+BS/2, self.y-BS/2,
                                      self.x+BS/2, self.y+BS/2,
                                      self.x-BS/2, self.y+BS/2]),
                             ('c3f', color_2048.get_block_color(self.value) * 4))
        self.label.draw()

class board:
    def __init__(self):
        self._grid = grid()
        self.blocks = [[None]*4,[None]*4,[None]*4,[None]*4]
        self.generate()

    def generate(self):
        empty = self.get_empty()
        if len(empty) > 0:
            i, j = empty[random.randrange(0, len(empty))]
            self.blocks[i][j] = block(random.randrange(1,3)*2, i, j)

    def get_empty(self):
        lst = []
        for p in range(4):
            for q in range(4):
                if self.blocks[p][q] is None:
                    lst.append((p,q))
        return lst

    def merge(self, pos1, pos2):
        # pos1 is already moved
        # pos is tuple (i, j)
        if pos1[0] < 0 or pos1[0] > 3:
            return False
        if pos1[1] < 0 or pos1[1] > 3:
            return False
        prev = self.blocks[pos1[0]][pos1[1]]
        curr = self.blocks[pos2[0]][pos2[1]]
        if prev.value is curr.value and not prev.merged:
            curr.set_value(curr.value * 2)
            curr.set_index(pos1[0], pos1[1])
            self.blocks[pos1[0]][pos1[1]] = curr
            self.blocks[pos2[0]][pos2[1]] = None
            del prev
            curr.merged = True
            return True
        return False
    
    def move_x(self, symbol):
        if symbol == key.LEFT:
            filled_init = -1
            ran = range(4)
        elif symbol == key.RIGHT:
            filled_init = 4
            ran = range(3,-1,-1)
        
        for p in range(4):
            filled = filled_init
            for q in ran:
                if self.blocks[p][q] is None:
                    pass
                else:
                    b = self.blocks[p][q]
                    if self.merge((p, filled), (p, q)):
                        continue
                    filled += (1 if symbol == key.LEFT else -1)
                    b.set_index(p, filled)
                    self.blocks[p][filled] = b
                    if symbol == key.LEFT and q > filled:
                        self.blocks[p][q] = None
                    if symbol == key.RIGHT and q < filled:
                        self.blocks[p][q] = None
        self.generate()
        
    def move_y(self, symbol):
        if symbol == key.DOWN:
            filled_init = -1
            ran = range(4)
        elif symbol == key.UP:
            filled_init = 4
            ran = range(3,-1,-1)
        
        for q in range(4):
            filled = filled_init
            for p in ran:
                if self.blocks[p][q] is None:
                    pass
                else:
                    b = self.blocks[p][q]
                    if self.merge((filled, q), (p, q)):
                        continue
                    filled += (1 if symbol is key.DOWN else -1)
                    b.set_index(filled, q)
                    self.blocks[filled][q] = b
                    if symbol == key.DOWN and p > filled:
                        self.blocks[p][q] = None
                    if symbol == key.UP and p < filled:
                        self.blocks[p][q] = None
        self.generate()
        
    def draw(self):
        self._grid.draw()
        for col in self.blocks:
            for b in col:
                if b is not None:
                    b.draw()

    def merge_false(self):
        for col in self.blocks:
            for b in col:
                if b is not None:
                    b.merged = False

    def check_gameover(self):
        for col in self.blocks:
            for b in col:
                if b is None:
                    return False
        for p in range(4):
            for q in range(3):
                if self.blocks[p][q].value is self.blocks[p][q+1].value:
                    return False
        for p in range(3):
            for q in range(4):
                if self.blocks[p][q].value is self.blocks[p+1][q].value:
                    return False
        return True

window = pyglet.window.Window(WS, WS)
gameboard = board()

game_over = False
game_over_text = pyglet.text.Label("",
                          font_name='Times New Roman',
                          font_size=36,
                          anchor_x="center",
                          x=WS//2, y=WS//2)

@window.event
def on_key_press(symbol, modifiers):
    global gameboard
    if symbol == key.LEFT or symbol == key.RIGHT:
        gameboard.move_x(symbol)
    if symbol == key.UP or symbol == key.DOWN:
        gameboard.move_y(symbol)
    gameboard.merge_false()
    if gameboard.check_gameover():
        print("GAME OVER")
        game_over = True
        if game_over:
            game_over_text.text = "GAME OVER!"
        game_over_text.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    print(x, y)

@window.event
def on_draw():
    window.clear()
    gameboard.draw()
    if game_over:
        game_over_text.text = "GAME OVER!"
    game_over_text.draw()


pyglet.app.run()
