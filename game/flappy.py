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
                 speed = 120,    
                 gravity = -200,
                 *args,
                 **kwargs):
        kwargs['position'] = position

        super(Flappy, self).__init__(resources.flapy, *args, **kwargs)
        self.cshape = AARectShape(self.position, self.width//2, self.height//2)
        self.gravity = gravity
        self.speed = speed #velikost hitrosti
        self.velocity = velocity #vektor hitrosti
        self.do(Move())
        self.schedule(self.update)

    def update(self, dt):
        width, height = director.get_window_size()
        self.cshape.center = self.position
        
    def jump(self):
        print("aaa")
        self.velocity = 0, self.speed

        
