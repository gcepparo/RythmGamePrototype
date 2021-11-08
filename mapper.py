import constants as const
import actors as act
import random

def readMapFile():
    pass


class fakeBullet(act.Bullet): # necessary to collision detection
    def __init__(self):
        super().__init__('up',100)
        self.rect[0] = self.position # in the bullet class the rect is initialized as 0,0 and gets repositioned at the first update
    
    def update(self):
        pass



def randomMap(length):
    bullets = list()
    states = ['null','up','down']

    for i in range(length):
        case = states[random.randint(0,2)]
        if case == 'null':
            pass
        elif case == 'up':
            b = act.Bullet(case,i*100)
            bullets.append(b)
        elif case == 'down':
            b = act.Bullet(case, i*100)
            bullets.append(b)

    bullets.append(fakeBullet())
    return bullets