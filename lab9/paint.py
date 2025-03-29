import pygame as pg

pg.init()

W = 1000
H = 600
screen = pg.display.set_mode((W, H))


# Current activities
active_size = 0
active_color = 'white'
active_shape = 0
painting = []


clock = pg.time.Clock()
FPS = 2400
pg.display.set_caption("Paint!")

def draw_menu():
    # Draw menu bar
    pg.draw.rect(screen, 'gray', [0, 0, W, 100])
    pg.draw.line(screen, 'black', (0, 100), (W, 100), 2)

    # Draw all brushs blocks 
    xl_brush = pg.draw.rect(screen, 'black', [25,25,50,50])
    pg.draw.circle(screen, 'white', (50,50), 20)
    l_brush = pg.draw.rect(screen, 'black', [90,25,50,50])
    pg.draw.circle(screen, 'white', (115,50), 15)
    m_brush = pg.draw.rect(screen, 'black', [155,25,50,50])
    pg.draw.circle(screen, 'white', (180,50), 10)
    s_brush = pg.draw.rect(screen, 'black', [220,25,50,50])
    pg.draw.circle(screen, 'white', (245,50), 5)

    # List of all brushes blocks positions
    brush_list = [xl_brush,l_brush,m_brush,s_brush]


    # Draw al colors blocks
    blue = pg.draw.rect(screen, (0,0,255), [W - 50, 25, 25,25])
    green = pg.draw.rect(screen, (0,255,0), [W - 75, 25, 25,25])
    red = pg.draw.rect(screen, (255,0,0), [W - 50, 50, 25,25])
    yellow = pg.draw.rect(screen, (255,255,0), [W - 75 , 50, 25,25])
    pg.draw.rect(screen, 'black', [W - 200, 25, 50,50])
    white = pg.draw.rect(screen, (255,255,255), [W - 195, 30, 40,40])

    # List of all colors RGBs and blocks
    rgb_list = [(0,0,255), (0,255,0), (255,0,0), (255,255,0), (255,255,255)]
    color_list = [blue, green, red, yellow, white]

    # Draw all shapes blocks
    rectangel = pg.draw.rect(screen, 'black', [400,25,50,50])
    pg.draw.rect(screen, 'white', [405, 35, 40, 30])
    circle = pg.draw.rect(screen, 'black', [455,25,50,50])
    pg.draw.circle(screen, 'white', (480 ,50), 20)
    square = pg.draw.rect(screen, 'black', [510,25,50,50])
    pg.draw.rect(screen, 'white', [515, 30, 40, 40])
    right_triangle = pg.draw.rect(screen, 'black', [565,25,50,50])
    pg.draw.polygon(screen, 'white', ((570,30),(570,70),(610,70)))
    equilateral_triangle = pg.draw.rect(screen, 'black', [620,25,50,50])
    pg.draw.polygon(screen, 'white', ((645,30),(625,70),(665,70)))
    rhombus = pg.draw.rect(screen, 'black', [675,25,50,50])
    pg.draw.polygon(screen, 'white', ((700, 30), (680, 50), (700, 70), (720, 50)))

    # List of all blocks positions and names
    shape_list = [rectangel, circle, square, right_triangle, equilateral_triangle, rhombus]
    shape_name = ["rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]


    return brush_list, color_list, rgb_list, shape_list, shape_name



def draw_painting(paint):
    for i in range(len(paint)):
        pg.draw.circle(screen, paint[i][0], paint[i][1], paint[i][2])



drawing = False
drawingshape = False

drawed_shapes = []

run = True
while run:
    screen.fill("white")

    # Get all postions of all blocks and featers in menu
    brushes, colors, rgbs, shapes, shapename = draw_menu()

    # Check all clicked mouse buttons
    mouse = pg.mouse.get_pos()
    clicked = pg.mouse.get_pressed()[0]

    # To don't draw on the menu bar
    if mouse[1] > 100 + active_size:
        pg.draw.circle(screen, active_color, mouse, active_size)
        if clicked and not drawingshape:
            painting.append((active_color, mouse, active_size))
    
    

    # Draw all shapes in the list
    for sh in drawed_shapes:
        match sh[0]:
            case "rect": #drawing rectangle
                pg.draw.rect(screen, sh[1], [sh[2][0], sh[2][1], sh[3], sh[4]])
            case "circle": # Drawomg Circle
                pg.draw.circle(screen, sh[1], sh[5], sh[6])
            case "square": # Drawing Square
                pg.draw.rect(screen, sh[1], [sh[2][0], sh[2][1], sh[3], sh[3]])
            case "right_triangle": # Drawing Right Triangle
                pg.draw.polygon(screen, sh[1], ((sh[5]), (sh[5][0], sh[7][1]), (sh[7])))
            case "equilateral_triangle": # Drawing Equilateral Triangle
                pg.draw.polygon(screen, sh[1],(((sh[6]/2 + sh[5][0], sh[5][1]), (sh[5][0], sh[5][1] + sh[6]), (sh[5][0] + sh[6], sh[5][1] + sh[6]))))
            case "rhombus": # Drawing Rhombus
                pg.draw.polygon(screen, sh[1], (((sh[5][0] + sh[7][0]) / 2, sh[5][1]), (sh[5][0] , (sh[5][1] + sh[7][1]) / 2), ((sh[5][0] + sh[7][0]) / 2, sh[7][1]), (sh[7][0] , (sh[5][1] + sh[7][1]) / 2)))

    draw_painting(painting)

    if drawingshape:
        if clicked and not drawing:
            drawing = True
            start_pos = mouse
        elif not clicked and drawing:
            end_pos = mouse

            # Get both start and end points position's
            x1, y1 = start_pos
            x2, y2 = end_pos

            # To stop on bottom of the menu
            if y2 < 100:
                y2 = 102
            if y1 < 100:
                y1 = 102

            left = min(x1, x2)
            top = min(y1,y2)
            width = abs(x2-x1)
            height = abs(y2-y1)

            # Distance between two points
            d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            
            # Added to list of shapes to lock on the screen
            drawed_shapes.append((active_shape, active_color, (left, top), width, height, (x1, y1), d, (x2, y2)))


            drawing = False
        
        

        if drawing:
            # Get both start and end points position's
            x1, y1 = start_pos
            x2, y2 = mouse


            # To stop on bottom of the menu
            if y2 < 100:
                y2 = 102
            if y1 < 100:
                y1 = 102



            left = min(x1, x2)
            top = min(y1,y2)
            width = abs(x2-x1)
            height = abs(y2-y1)

            # Distance between two points
            d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

            # Drawing while holding 
            match active_shape:
                case "rect": #drawing rectangle
                    pg.draw.rect(screen, active_color, (left, top, width, height))
                case "circle": # Drawomg Circle
                    if y1 - d < 100:
                        d = y1 - 102
                    pg.draw.circle(screen, active_color,(x1,y1) , d)
                case "square": # Drawing Square
                    pg.draw.rect(screen, active_color, (left,top, width, width))
                case "right_triangle": # Drawing Right Triangle
                    pg.draw.polygon(screen, active_color, ((x1, y1), (x1,y2), (x2,y2)))
                case "equilateral_triangle": # Drawing Equilateral Triangle
                    pg.draw.polygon(screen, active_color, ((d/2 + x1, y1), (x1, y1 + d), (x1+d, y1+d)))
                case "rhombus":
                    pg.draw.polygon(screen, active_color, (((x1+x2)/2, y1), (x1, (y1 + y2)/2), ((x1+x2)/2, y2), (x2, (y1 + y2)/2) ))
                    
        
    # Check all pressed buttons
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in range(len(brushes)):
                if brushes[i].collidepoint(event.pos):
                    drawingshape = False
                    active_size = 20 - (i * 5)
    
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in range(len(colors)):
                if colors[i].collidepoint(event.pos):
                    active_color = rgbs[i]
    
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in range(len(shapes)):
                if shapes[i].collidepoint(event.pos):
                    drawingshape = True
                    active_shape = shapename[i]
    

    pg.display.update()
    clock.tick(FPS)
pg.quit()
exit()