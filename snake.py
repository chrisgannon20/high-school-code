from random import *
from Tkinter import *

class SnakeGame(Frame):

    def __init__(self, world, snake, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.world = world
        self.snake = snake

    def setCanvas(self, canvas):
        self.canv = canvas

    def myLoop(self):
        self.drawWorld()
        self.doLogic()
        self.after(GAME_SPEED, self.myLoop)

    def drawWorld(self):
        self.canv.delete("all")

        # grid
        cell_size = WORLD_SIZE / self.world.width
        for x in range(self.world.width):
            for y in range(self.world.height):
                self.canv.create_rectangle(x * cell_size, y * cell_size, x * cell_size + cell_size,
                                           y * cell_size + cell_size)

        # food
        self.canv.create_oval(world.foodpos[0] * cell_size + 3, world.foodpos[1] * cell_size + 3,
                              world.foodpos[0] * cell_size + cell_size - 3,
                              world.foodpos[1] * cell_size + cell_size - 3, fill="red")

        # snake
        for part in self.snake.body:
            self.canv.create_rectangle(part.x * cell_size, part.y * cell_size, part.x * cell_size + cell_size,
                                       part.y * cell_size + cell_size, fill="blue")

    def doLogic(self):
        if(self.snake.dir == "up"):
            self.snake.last_dir = "up"
            newPart = SnakeBodyPiece(self.snake.body[0].x, self.snake.body[0].y - 1)
            self.snake.body.insert(0, newPart)
        elif (self.snake.dir == "left"):
            self.snake.last_dir = "left"
            newPart = SnakeBodyPiece(self.snake.body[0].x - 1, self.snake.body[0].y)
            self.snake.body.insert(0, newPart)
        elif (self.snake.dir == "right"):
            self.snake.last_dir = "right"
            newPart = SnakeBodyPiece(self.snake.body[0].x + 1, self.snake.body[0].y)
            self.snake.body.insert(0, newPart)
        elif (self.snake.dir == "down"):
            self.snake.last_dir = "down"
            newPart = SnakeBodyPiece(self.snake.body[0].x, self.snake.body[0].y + 1)
            self.snake.body.insert(0, newPart)


        xHead = self.snake.body[0].x
        yHead = self.snake.body[0].y

        xFood = self.world.foodpos[0]
        yFood = self.world.foodpos[1]

        if(xHead == xFood and yHead == yFood):
            self.world.newFoodPos()
        else:
            self.snake.body.pop()

        if(xHead >= world.width or xHead < 0 or yHead >= world.height or yHead < 0):
            self.snake = Snake()

        bodyIter = iter(self.snake.body)
        next(bodyIter)
        for part in bodyIter:
            if(xHead == part.x and yHead == part.y):
                self.snake = Snake()

    def upKey(self, event):
        if(self.snake.last_dir != "down"):
            self.snake.dir = "up"
    def downKey(self, event):
        if(self.snake.last_dir != "up"):
            self.snake.dir = "down"
    def rightKey(self, event):
        if(self.snake.last_dir != "left"):
            self.snake.dir = "right"
    def leftKey(self, event):
        if(self.snake.last_dir != "right"):
            self.snake.dir = "left"


class World:

    width = 20
    height = 20
    foodpos = (1,1)

    def __init__(self, snake):
        self.snake = snake
        self.width = CELL_COUNT
        self.height = CELL_COUNT
        self.newFoodPos()

    def newFoodPos(self):
        self.foodpos = (randint(1, self.width - 1), randint(1, self.height - 1))

        x = self.foodpos[0]
        y = self.foodpos[1]

        for part in self.snake.body:
            if(x == part.x and y == part.y):
                self.newFoodPos()

class Snake:

    def __init__(self):
        origin = (CELL_COUNT/2, CELL_COUNT/2)

        part1 = SnakeBodyPiece(origin[0],origin[1])
        part2 = SnakeBodyPiece(origin[0], origin[1]+1)
        part3 = SnakeBodyPiece(origin[0], origin[1]+2)

        self.body = [part1,part2,part3]

        self.dir = "up"
        self.last_dir = "up"

class SnakeBodyPiece:
    def __init__(self, x, y):
        self.x = x
        self.y = y

WORLD_SIZE = 800
CELL_COUNT = 20
GAME_SPEED = 100

snake = Snake()
world = World(snake)

game = SnakeGame(world, snake)
game.master.title("Snake")
game.master.minsize(WORLD_SIZE,WORLD_SIZE)
game.master.maxsize(WORLD_SIZE,WORLD_SIZE)

game.master.bind("<Down>", game.downKey)
game.master.bind("<Up>", game.upKey)
game.master.bind("<Left>", game.leftKey)
game.master.bind("<Right>", game.rightKey)

canv = Canvas(game.master, width=WORLD_SIZE, height=WORLD_SIZE)
canv.pack()

game.setCanvas(canv)
game.drawWorld()
game.myLoop()
game.mainloop()