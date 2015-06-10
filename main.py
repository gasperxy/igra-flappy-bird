import cocos
import pyglet
from game import flappy
from game import utils
from game import pipe
from game import floor as f
from game.resources import resources
from pyglet.window import key
import pyglet.clock
from random import randint
import cocos.collision_model as cm
import time

class Game(cocos.layer.ColorLayer):
    is_event_handler = True
    def __init__(self):
        super(Game, self).__init__(255,255,255,255)
        self.mimo = False     

        self.collision_manager = cm.CollisionManagerBruteForce()
        self.flapy = flappy.Flappy()
        self.add(self.flapy, z=1)
        self.collision_manager.add(self.flapy)
        self.score = 0
        self.label = cocos.text.Label('{0}'.format(self.score),
            font_name = 'Times New Roman',
            font_size = 30,
            anchor_x = 'center', anchor_y = 'center',
            position = (50, 450),
            color = (0,0,0,255)
            )
        self.add(self.label,z=1)
        self.add(BackgroundLayer(), z=0)

        self.batch = cocos.batch.BatchNode()
        self.create_pipes()
        self.add(self.batch)

        self.batch1 = cocos.batch.BatchNode()
        self.create_floor()
        self.add(self.batch1, z=1)
        self.schedule_interval(self.update, 1/60)
        
    def create_pipes(self):
        
        self.pipes = [(pipe.Pipe(1), pipe.Pipe(0)) for i in range(4)]      

        positions = []
        x = 800
        for i in range(4):
            y = randint(-100, 120)
            positions.append(((x, y), (x, 550 + y)))
            x += 250

        
        for i, pip in enumerate(self.pipes):
            pip[0].position = positions[i][0] 
            pip[1].position = positions[i][1]          

            self.batch.add(pip[0])
            self.batch.add(pip[1])

            self.collision_manager.add(pip[0])
            self.collision_manager.add(pip[1])
    def create_floor(self):

        positions = ((0,0),(308,0),(616,0),(924,0),(1232,0))
        self.floor =[f.Floor() for i in range(5)]

        for i, flor in enumerate(self.floor):
            flor.position = positions[i]
            self.batch1.add(flor)
            self.collision_manager.add(flor)

    def save_high_score(self):
        datum = time.strftime("%d/%m/%Y")
        cas = time.strftime("%H:%M:%S")

        with open("highscores.txt", 'a') as hightscores:
            hightscores.write('Dan: {0} Čas: {1} Score: {2} \n'.format(datum, cas, self.score))
            

    def update(self, dt):
        first_pipe = self.pipes[0][0]

        if first_pipe.position[0] < 0: #preveri če je pipa 'pobegnila' iz zaslona
            self.pipes.pop(0)                #ter naredi novo še izven zaslona
            new_pipe = pipe.Pipe(1)
            new_pipe1 = pipe.Pipe(2)

            y = randint(-100, 150)
            new_pipe.position = 1000, y
            new_pipe1.position = 1000, y + 550

            self.add(new_pipe, z=0)
            self.add(new_pipe1, z=0)

            self.collision_manager.add(new_pipe)
            self.collision_manager.add(new_pipe1)

            self.mimo = False

            self.pipes.append((new_pipe, new_pipe1))
        if first_pipe.position[0] < self.flapy.position[0] and not self.mimo:
            self.score += 1
            self.mimo = True
            self.remove(self.label)
            self.label = cocos.text.Label('{0}'.format(self.score),
                font_name = 'Times New Roman',
                font_size = 30,
                anchor_x = 'center', anchor_y = 'center',
                position = (50, 450),
                color = (0,0,0,255)
                )
            self.add(self.label)




   ######################################     
        # for obstacle in self.pipes:            
        #     if obstacle[0].position[0] < 0:
        #         y = randint(-100,150)
        #         print(y)
        #         obstacle[0].position = 1000, y
        #         obstacle[1].position = 1000, y + 550                

        #     if 65.5 < self.flapy.position[0] - obstacle[0].position[0] <= 70:
        #         print(self.flapy.position[0] - obstacle[0].position[0])
        #         self.score += 1
        #         self.remove(self.label)
        #         self.label = cocos.text.Label('{0}'.format(self.score),
        #         font_name = 'Times New Roman',
        #         font_size = 30,
        #         anchor_x = 'center', anchor_y = 'center',
        #         position = (50, 450),
        #         color = (0,0,0,255)
        #         )
        #         self.add(self.label)

        collisions = self.collision_manager.objs_colliding(self.flapy)

        if collisions:
            print("zadet")           
            self.save_high_score()
            scene = cocos.scene.Scene()
            scene.add(YouLostMenu(), z=1)
            scene.add(BackgroundLayer(), z=0)
            cocos.director.director.run(scene)
            
                                   

    def on_key_press(self, symbol, modifires):
        if symbol == key.UP:
            self.flapy.jump()
            
class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__()

        self.font_title['font_name'] = 'Edit Undo Line BRK'
        self.font_title['font_size'] = 52
        self.font_title['color'] = (240, 0, 220, 255)
        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (240, 0, 220, 255)

        items = []
        items.append(cocos.menu.MenuItem('New game', self.on_new_game))
        items.append(cocos.menu.MenuItem('Options', self.on_options))
        items.append(cocos.menu.MenuItem('Quit', self.on_quit))
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_new_game(self):       
        scene = cocos.scene.Scene()
        scene.add(cocos.layer.MultiplexLayer(Game(),BackgroundLayer()), z=1)
        scene.add(BackgroundLayer(), z=0)       
        cocos.director.director.run(scene)

    def on_options(self):
        self.parent.switch_to(1)

    def on_quit(self):
        pyglet.app.exit()

class OptionsMenu(cocos.menu.Menu):
    def __init__(self):
        super(OptionsMenu, self).__init__("two_runner")

        self.font_title["font_name"] = "Edit Undo Line BRK"
        self.font_title["font_size"] = 52
        self.font_title["color"] = (240, 0, 220, 255)

        self.font_item["color"] = (255, 255, 255, 255)
        self.font_item_selected["color"] = (240, 0, 220, 255)

        items = []
        items.append(cocos.menu.MenuItem("Fullscreen", self.on_fullscreen))
        items.append(cocos.menu.MenuItem("Back", self.on_quit))
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_fullscreen(self):
        cocos.director.director.window.set_fullscreen(
            not cocos.director.director.window.fullscreen
        )

    def on_quit(self):
        self.parent.switch_to(0)

class YouLostMenu(cocos.menu.Menu):
    def __init__(self):
        super(YouLostMenu, self).__init__("YOU LOST")

        self.font_title["font_name"] = "Edit Undo Line BRK"
        self.font_title["font_size"] = 52
        self.font_title["color"] = (240, 0, 220, 255)

        self.font_item["color"] = (255, 255, 255, 255)
        self.font_item_selected["color"] = (240, 0, 220, 255)

        items = []
        items.append(cocos.menu.MenuItem("High Scores", self.on_high_scores))
        items.append(cocos.menu.MenuItem("New Game", self.on_new_game))
        items.append(cocos.menu.MenuItem("Main Menu", self.on_main_menu))
        items.append(cocos.menu.MenuItem("Quit", self.on_quit))
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_high_scores(self):
        pass

    def on_quit(self):
        pyglet.app.exit()

    def on_new_game(self):
        scene = cocos.scene.Scene()
        scene.add(cocos.layer.MultiplexLayer(Game()), z=1)
        scene.add(BackgroundLayer(), z=0)       
        cocos.director.director.run(scene)

    def on_main_menu(self):
        scene = cocos.scene.Scene()
        scene.add(cocos.layer.MultiplexLayer(MainMenu()), z=1)
        scene.add(BackgroundLayer(), z=0)       
        cocos.director.director.run(scene)

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.image = cocos.sprite.Sprite(resources.bg)
        self.image.position = 400, 250
        self.add(self.image, z=0)

      


if __name__ == '__main__':
    cocos.director.director.init(width=800, height=500)
    cocos.director.director.show_FPS = True
   
    cocos.director.director.window.push_handlers(utils.keys)
    scene = cocos.scene.Scene()
    scene.add(cocos.layer.MultiplexLayer(MainMenu(), OptionsMenu()), z=1)
    scene.add(BackgroundLayer(), z=0)
    cocos.director.director.run(scene)
