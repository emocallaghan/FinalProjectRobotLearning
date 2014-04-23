# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 15:57:54 2014

@author: cbeery
"""

if __name__ == '__main__':
    pygame.init()

    size = (1000,700)
    screen = pygame.display.set_mode(size)

    model = Model(size)
    
    
    
     """---Nothing Below has been updated to the new architecture---"""
    
    view = PyGameWindowView(model,screen)

    KeyBoardcontroller = PyGameKeyboardController(model)
    collisionController = CollisionController(model)    
    running = True
    
    startTime = time.time()
    xTime = time.time()
    
    
    while running:
        collisionController.checkCollisions()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            KeyBoardcontroller.handle_keyboard_event(event)
            collisionController.checkCollisions()
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
    
        
        