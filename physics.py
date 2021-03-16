import pygame
import math
pygame.init()
window_d = 800
window = pygame.display.set_mode((window_d,window_d))
pygame.display.set_caption('Physics')
Icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(Icon)

#font init
font = pygame.font.Font('freesansbold.ttf', 20)
font_small = pygame.font.Font('freesansbold.ttf', 13)

#reference: all units are in meters, 1 meter = 1 pixel * pixel to meter ratio
pixel_to_meter_ratio = 40
bodies = []
gravity = 9.8#m/s^2
fps = 60
aiming = False
arrowStart = [0,0]
arrowEnd = [0,0]
radius = .5
elasticity = 1

#UItext
key = font.render(str(round(200/pixel_to_meter_ratio,3)) + ' Meters', True, (255,255,255))
zoom_txt = font_small.render('Zoom: ' + str(int(round(pixel_to_meter_ratio/40,2)*100)) +'%', True, (255,255,255))
radius_txt = font_small.render('Radius: ' + str(radius) + 'M', True, (255,255,255))
elasticity_txt = font_small.render('Elasticity: ' + str(elasticity), True, (255,255,255))
fps_txt = font_small.render('RefreshRate: ' + str(fps) + '/s', True, (255,255,255))
gravity_txt = font_small.render('Gravity: ' + str(gravity) + 'm/s^2', True, (255,255,255))

class body():
    def __init__(self, x, y, v_x, v_y):
        self.x = x
        self.y = y
        self.v_x = v_x 
        self.v_y = v_y * 2
        bodies.append(self)

class button():
    def __init__(self, x, y, plus):
        self.x = x
        self.y = y
        if plus:
            self.sign = '+'
        else:
            self.sign = '-'
    
    def draw(self):
        pygame.draw.rect(window, (255,255,255), (self.x, self.y, 25,25))
        txt = font.render(self.sign, True, (0,0,0))
        window.blit(txt, (self.x+8, self.y + 2))

#------------------PhysicsFunctions----------------

#shoots an object using the aiming tool
def createBody():
    v_x = (arrowEnd[0] - arrowStart[0])/pixel_to_meter_ratio
    v_y = (arrowEnd[1] - arrowStart[1])/pixel_to_meter_ratio
    clearArea = False
    while not(clearArea):
        clearArea = True
        for ibody in bodies:
            distance = math.sqrt((ibody.x-arrowStart[0])**2+(ibody.y - arrowStart[1])**2)
            if distance < radius*pixel_to_meter_ratio*2:
                arrowStart[1] -= 5
                clearArea = False
                break
    body(arrowStart[0], arrowStart[1], v_x, v_y)

#simulates motion of all bodies
def motion():
    out_of_range = None
    for i in range(len(bodies)):
        body = bodies[i]
        body.v_y += gravity/fps  # gravity
        body.x += (body.v_x/fps) * pixel_to_meter_ratio  # velocity in x direction
        body.y += (body.v_y/fps) * pixel_to_meter_ratio  # velocity in y direction
        pygame.draw.circle(window, (240,240,240),(body.x, body.y), radius*pixel_to_meter_ratio)
        if body.y > window_d:
            out_of_range = i    #bodies that are to far and need to be deleted
    if out_of_range or out_of_range == 0:
        del bodies[out_of_range]   

#detects intersecting objects and simulates collisions
def collisions():
    for i in range(len(bodies)):
        for j in range(i+1,len(bodies)):
            body1 = bodies[i]
            body2 = bodies[j]
            distance = math.sqrt((body1.x-body2.x)**2+(body1.y - body2.y)**2) #calculates distance between objects
            if distance < 2*radius*pixel_to_meter_ratio:
                b1x = body1.v_x  #data holders
                b1y = body1.v_y 
                #objects switch velocities because of equal mass
                body1.v_x = body2.v_x * elasticity
                body1.v_y = body2.v_y * elasticity
                body2.v_x = b1x * elasticity
                body2.v_y = b1y * elasticity

#--------------------UI/buttons--------------------

#draws Buttons/key
def drawUI():
    global key
    global zoom_txt
    global radius_txt
    global fps_txt
    global elasticity_txt
    pygame.draw.line(window, (255,255,255), (20, 20), (220,20), width = 2)
    pygame.draw.line(window, (255,255,255), (20, 10), (20,30), width = 2)
    pygame.draw.line(window, (255,255,255), (220, 10), (220,30), width = 2)
    window.blit(key, (70, 30)) 
    zoom_in.draw()
    zoom_out.draw()
    radius_inc.draw()
    radius_dec.draw()
    fps_up.draw()
    fps_down.draw()
    gravity_up.draw()
    gravity_down.draw()
    window.blit(zoom_txt, (window_d - 165, 16))
    window.blit(radius_txt, (window_d - 165, 51))
    window.blit(fps_txt, (window_d - 380, 16))
    window.blit(gravity_txt, (window_d - 383, 51))

#checks whether a button has been pressed
def buttonPress():
    global pixel_to_meter_ratio
    global radius
    global key
    global zoom_txt
    global radius_txt
    global fps
    global fps_txt
    global elasticity
    global elasticity_txt
    global gravity
    global gravity_txt
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    btnPress = False

    if x > zoom_in.x and x < zoom_in.x + 25 and y > zoom_in.y and y < zoom_in.y + 25:
        pixel_to_meter_ratio += (pixel_to_meter_ratio)*.1      
        btnPress = True
    if x > zoom_out.x and x < zoom_out.x + 25 and y > zoom_out.y and y < zoom_out.y + 25:
        pixel_to_meter_ratio -= (pixel_to_meter_ratio)*.1    
        btnPress = True
    if x > radius_inc.x and x < radius_inc.x + 25 and y > radius_inc.y and y < radius_inc.y + 25:
        radius += .5
        btnPress = True
    if x > radius_dec.x and x < radius_dec.x + 25 and y > radius_dec.y and y < radius_dec.y + 25:
        radius -= .5
        btnPress = True
    if x > fps_up.x and x < fps_up.x + 25 and y > fps_up.y and y < fps_up.y + 25:
        fps += 10
        btnPress = True
    if x > fps_down.x and x < fps_down.x + 25 and y > fps_down.y and y < fps_down.y + 25:
        if fps != 10:
            fps -= 10
        btnPress = True
    if x > gravity_up.x and x < gravity_up.x + 25 and y > gravity_up.y and y < gravity_up.y + 25:
        gravity += .7
        gravity = round(gravity,2)
        btnPress = True
    if x > gravity_down.x and x < gravity_down.x + 25 and y > gravity_down.y and y < gravity_down.y + 25:
        gravity -= .7
        gravity = round(gravity,2)
        btnPress = True

    if btnPress: 
        zoom_txt = font_small.render('Zoom: ' + str(int(round(pixel_to_meter_ratio/40,2)*100)) +'%', True, (255,255,255))
        radius_txt = font_small.render('Radius: ' + str(radius) + 'M', True, (255,255,255))
        key = font.render(str(round(200/pixel_to_meter_ratio,3)) + ' Meters', True, (255,255,255))
        fps_txt = font_small.render('RefreshRate: ' + str(fps) + '/s', True, (255,255,255))
        gravity_txt = font_small.render('Gravity: ' + str(gravity) + 'm/s^2', True, (255,255,255))
        return True
    else:
        return False

#initializes buttons
zoom_in = button(window_d - 60, 10, True)
zoom_out = button(window_d - 220, 10, False)
radius_inc = button(window_d - 60, 45, True)
radius_dec = button(window_d - 220, 45, False)
fps_up = button(window_d - 260, 10, True)
fps_down = button(window_d - 420, 10, False)
gravity_up = button(window_d - 260, 45, True)
gravity_down = button(window_d - 420, 45, False)

#main loop
while True:
    window.fill((0,0,0))
    pygame.time.delay((1000//fps))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        #handles shooting of objects
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not(buttonPress()):
                    aiming = True
                    arrowStart[0] = pygame.mouse.get_pos()[0]
                    arrowStart[1] = pygame.mouse.get_pos()[1]
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if aiming == True:
                    aiming = False
                    arrowEnd[0] = pygame.mouse.get_pos()[0]
                    arrowEnd[1] = pygame.mouse.get_pos()[1]
                    createBody()
                
    #draws aiming arrow
    if aiming:
        pygame.draw.line(window, (255,0,0), (arrowStart[0], arrowStart[1]), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), width = 2)            
    
    #draws motion/data/buttons
    collisions()
    motion()
    drawUI()
    pygame.display.update()