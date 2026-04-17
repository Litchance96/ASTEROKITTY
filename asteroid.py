from if3_game.engine import Sprite
from pyglet.window import key as keyboard
from math import sin, cos, radians, sqrt
from random import randint, choice



RESOLUTION = (800, 600)

class SpaceObject(Sprite):
    def __init__(self, image, position, anchor, speed =(0, 0), rotation_speed=0):
        super().__init__(image, position, anchor=anchor, collision_shape="circle")
        self.speed = speed
        self.rotation_speed = rotation_speed

    def update(self, dt):
        super().update(dt)
        mvt = self.speed[0] * dt, self.speed[1]* dt
        self.position = self.position[0] + mvt[0], self.position[1] + mvt[1]
        self.rotation += self.rotation_speed * dt
        #une rotation (= des degrés) et une vitesse (speed.rotation = vitesse (pixel/s)) = des degres/secondes = angle/temps et donc rotation.speed * dt = des degres (les secondes s'annulent)
         
        x, y = self.position

        if x < -self.width/2:
            x = RESOLUTION[0] + self.width/2
        elif x > RESOLUTION[0] + self.width/2:
            x = -self.width/2

        if y < -self.height/2:
            y = RESOLUTION[1] + self.height/2
        if y > RESOLUTION[1] + self.height/2:
           y = -self.height/2

        self.position = x, y


class Asteroid(SpaceObject):
    def __init__(self, position, speed, rotation_speed, level=3):
        self.level = level
        image = "assets/asteroid128.png"
        anchor = (64, 64)
        if self.level == 2:
            image = "assets/asteroid64.png"
            anchor = (32, 32)
        if self.level == 1:
            image = "assets/asteroid32.png"
            anchor = (16, 16)
        super().__init__(image, position, anchor, speed, rotation_speed)

    def on_collision(self, other):
        if isinstance(other, Bullet): #la fonction isinstance renverra TRUE si other est de type Bullet. ca verifie que other est une instance de Bullet
            print("AIE!!")
            self.destroy()
            other.destroy()

        elif isinstance(other, Spaceship):  #elif = sinon si, si il a dabord été touché par une bullet il va pas chercher a voir si il est touché par le vaisseau
            self.destroy()

    def destroy(self):
        super().destroy()
        
        if self.level > 1:
            for _ in range(3):
                sx = randint(30, 100)*choice([1, -1])
                sy = randint(30, 100)*choice([1, -1])
                speed = sx, sy
                rotation_speed =(randint(-50, 50))
                asteroid = Asteroid(self.position, speed, rotation_speed, self.level-1)
            
                self.layer.add(asteroid)
    

class Spaceship(SpaceObject):

    def __init__(self, position):
        super().__init__("assets/ship2.png", position, (32, 64))
        self.velocity =  0     #pixels/secondes
        self.engine_on = False
#       une vitesse (speed.rotation) = des degres/secondes = angle/temps
        self.acceleration = 250   #   pixels/secondes /secondes   (au carré)
        self.velocity_max = 100
        self.invicibility = False
        self.chrono = 0.
        self.life = 3

    # def collision_ship(self, other):
    #     if isinstance(other, Asteroid):
    #         self.destroy()

    def update(self, dt):
        if self.engine_on:
            angle = radians(-self.rotation+90)
#            self.velocity += self.acceleration * dt  #à quel point on a acceleré (a quel point mon hypothenus augmente)? on doit recalculer la vitesse pour la "caper" (la modifier)

            speed_change_x = cos(angle)*self.acceleration * dt
            speed_change_y = sin(angle)*self.acceleration * dt

            self.speed = self.speed[0] + speed_change_x , self.speed[1] + speed_change_y   #cos(angle)*self.velocity, sin(angle)*self.velocity
        
        if self.invicibility == True:    
            self.chrono += dt
            if self.chrono >= 4.:
                self.opacity = 255
                self.invicibility = False
                self.chrono = 0.

        if self.life == 0:
            self.invicibility = False
            self.destroy()
        
        super().update(dt) #sinon le vaisseau ne bouge plus, important de ne pas oublier d'importer ce qu'on avait dans spaceobject 

    def on_key_press(self, key, _): #"modifier" on est obligé de l'écrire mais pas de l'utiliser est du coup on peut juste mettre un underscore !! 
        if key == keyboard.RIGHT:
            self.rotation_speed = 70 

        elif key == keyboard.LEFT:
            self.rotation_speed = -70

        if key == keyboard.UP:
            self.engine_on = True

        if key == keyboard.SPACE:
            self.create_bullet()
        
               
    def on_key_release(self, key, _):
        if key == keyboard.RIGHT or key == keyboard.LEFT:
            self.rotation_speed = 0 

        if key == keyboard.UP:
            self.engine_on = False


    def create_bullet(self):
        
        angle = radians(-self.rotation+90)
        
        decal = self.height/2
        decal_x = cos(angle)*decal
        decal_y = sin(angle)*decal
        
        bullet_position = self.position[0] + decal_x, self.position[1] + decal_y
        
        bullet_velocity = 450 + sqrt(self.speed[0]**2 + self.speed[1]**2)   #3."sqrt" = square roat : racine carré => on veut l'hypothenus, donc avec pythagore on doit faire la racine carré des carrés des deux côtés
        speed_x = cos(angle)* bullet_velocity       #2. Puis on fait sqrt pour que le balles aillent plus vite que le vaisseau (exemple du train, ou du vaisseau (quand on sort du vaisseau on garde la meme vitesse du vaisseau, et les balles doivent aller plus vite, on rajoute l'intensité et la direction pour que les balles ne soient pas plus lentes que le vaisseau))
        speed_y = sin(angle)* bullet_velocity  #1. Pour que les balles aient la meme vitesse que le vaisseau

        speed = speed_x, speed_y

        bullet = Bullet(bullet_position, speed, 2.)
        self.layer.add(bullet)


    def on_collision(self, other):
        if isinstance (other, Asteroid):
            if self.invicibility == False: #if live>0
                self.opacity = 125
                self.invicibility = True
                self.life -= 1
        

# DEVOIR : si le vaisseau est touché 3x(vies), il disparaît (destroy) !!!! (hors invincibilité "évidemment")

class Bullet(SpaceObject):

    def __init__(self, position, speed, life_time):
        super().__init__("assets/bullet.png", position, (8,8), speed)

        self.chrono =0.
        self.life_time = life_time

    def update(self, dt):
        super().update(dt)
        self.chrono += dt


        if self.chrono >= self.life_time:
            self.destroy()


