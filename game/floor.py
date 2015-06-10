
from cocos.actions import Move
from cocos.collision_model import AARectShape
from cocos.director import director
from cocos.sprite import Sprite
from game.resources import resources
from random import randint

class Floor(Sprite):

	def __init__(
			self,				
			position = (0, 0),
			velocity = (-150, 0),
			speed = 50,
			*args,
			**kwargs):
		kwargs['position'] = position
		
		super(Floor, self).__init__(resources.floor, *args, **kwargs)
		self.speed = speed
		self.velocity = velocity
		self.do(Move())
		self.schedule(self.update) #vsak 'frame' pokliče funkcijo self.update
		self.cshape = AARectShape(self.position, self.width//2, self.height//2)

	def update(self, dt):
		self.cshape.center = self.position
		if self.position[0] <= -308:
			self.position = 1231, 0
		

		
		