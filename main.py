import cocos
import pyglet
from game import flappy
from game import utils
from game import pipe
from game import floor as f
from game.resources import resources
from pyglet.window import key
from random import randint
import cocos.collision_model as cm

class Game(cocos.layer.ColorLayer):
    is_event_handler = True
    def __init__(self):
        super(Game, self).__init__(255,255,255,255)     

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
        self.schedule(self.update)
        
    def create_pipes(self):
        
        self.pipes = [(pipe.Pipe(1), pipe.Pipe(0)) for i in range(4)]
        positions = (
            ((800, 0), (800, 530)),
            ((1050, 0), (1050, 530)),
            ((1300, 0), (1300, 530)),
            ((1550, 0), (1550, 530)))
        
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


            

    def update(self, dt):
        
        for obstacle in self.pipes:            
            if obstacle[0].position[0] < 0:
                y = -randint(-100,200)
                obstacle[0].position = 1000, y
                obstacle[1].position = 1000, y + 570
                

            if 69.75 < self.flapy.position[0] - obstacle[0].position[0] <= 70:
                print(self.flapy.position[0] - obstacle[0].position[0])
                self.score += 1
                self.remove(self.label)
                self.label = cocos.text.Label('{0}'.format(self.score),
                font_name = 'Times New Roman',
                font_size = 30,
                anchor_x = 'center', anchor_y = 'center',
                position = (50, 450),
                color = (0,0,0,255)
                )
                self.add(self.label)
        



            
        collisions = self.collision_manager.objs_colliding(self.flapy)


        if collisions:
            print("zadet")
            scene = cocos.scene.Scene()
            scene.add(cocos.layer.MultiplexLayer(YouLostMenu()), z=1)
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
        # game_layer = Game()
        # game_scene = cocos.scene.Scene(game_layer)
        # cocos.director.director.push(game_scene)
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
    cocos.director.director.init(width=800, height=500, vsync = False)
    cocos.director.director.show_FPS = True
    cocos.director.director.window.push_handlers(utils.keys)
    scene = cocos.scene.Scene()
    scene.add(cocos.layer.MultiplexLayer(MainMenu(), OptionsMenu()), z=1)
    scene.add(BackgroundLayer(), z=0)
    cocos.director.director.run(scene)
