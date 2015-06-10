from cocos.actions import Move
from cocos.collision_model import AARectShape
from cocos.director import director
from cocos.sprite import Sprite
from pyglet.window import key
from game import utils


from game.resources import resources

class Flappy(Sprite):
    is_event_handler = True
    def __init__(self,
                 position = (200, 200),
                 velocity = (0, 0), 
                 speed = 170,    
                 gravity = -350,
                 *args,
                 **kwargs):
        kwargs['position'] = position

        super(Flappy, self).__init__(resources.flapy, *args, **kwargs)
        self.cshape = AARectShape(self.position, self.width//2, self.height//2)
        self.gravity = gravity
        self.speed = speed #velikost hitrosti
        self.velocity = velocity #vektor hitrosti
        self.do(Move())
        self.schedule_interval(self.update,1/60)

    def update(self, dt):
        
        self.cshape.center = self.position
        
    def jump(self):
        print("aaa")
        self.velocity = 0, self.speed

        
