from if3_game.engine import init, Game, Layer
from random import randint, choice
from asteroid import SpaceObject, RESOLUTION, Spaceship, Asteroid, Bullet  #Spaceobject a toutes les capacités du sprite

#RESOLUTION = (800, 600)

init(RESOLUTION, "ASTRO-LITCHI")

spaceship = Spaceship((400, 300)) 

main_layer = Layer()

main_layer.add(spaceship)


for _ in range(6):
    x = randint(64, 736)     #128/2 = 64 et 800-64=736
    y = randint(64, 536)     #600-64=536

    while y > 136 and y < 464 and x < 614 and x > 186 :  #pour que l'asteroid touche le bord de la fusée quand meme on fait 250-64=186 et 550+64=614
        x = randint(64, 736)                           #200-64 et 400+64
        y = randint(64, 536)

    asteroid_position = (x, y)
    asteroid_speed = randint(-50, 100), randint(-50, 50)
    rotation_speed =(randint(-50, 50))
    asteroid = Asteroid(asteroid_position, asteroid_speed, rotation_speed)
   
    main_layer.add(asteroid)


    
game = Game()
game.add(main_layer)
game.debug =True
game.run()


