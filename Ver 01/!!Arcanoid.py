import pgzrun

def draw():
    paddle.draw()

TITLE = "Arkanoid clone"
WIDTH = 800
HEIGHT = 500

paddle = Actor("paddleblue.png")
paddle.x = 200
paddle.y = 420
 
pgzrun.go()