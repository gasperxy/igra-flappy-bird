
from cocos.actions import Move
from cocos.collision_model import AARectShape
from cocos.director import director
from cocos.sprite import Sprite
from game.resources import resources
from random import randint

class Pipe(Sprite):

	def __init__(
			self,
			mode,			
			position = (600, 50),
			velocity = (-150, 0),
			speed = 50,
			*args,
			**kwargs):
		kwargs['position'] = position
		
		#self.position = position
		self.score = 0
		self.mode = mode
		if self.mode == 1:
			super(Pipe, self).__init__(resources.pipe, *args, **kwargs)
		else:
			super(Pipe, self).__init__(resources.pipe1, *args, **kwargs)
		self.speed = speed
		self.velocity = velocity
		self.do(Move())
		self.schedule(self.update) #vsak 'frame' pokliče funkcijo self.update
		self.cshape = AARectShape(self.position, self.width//2, self.height//2)

	def update(self, dt):
		self.cshape.center = self.position
		if self.position[0] < 200:
			self.score += 1
		

		
		


