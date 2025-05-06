import pygame, sys, time

pygame.init()
pygame.display.set_caption("Towers of Hanoi")
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

game_done = False
framerate = 10
font = pygame.font.SysFont('sans serif', 25)

# game vars:
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0
n = 0

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78, 162, 196)
grey = (170, 170, 170)
green = (77, 206, 145)
bright_green = (0, 255, 0)
dark_green = (0, 150, 0)
brown = (160, 82, 45)

# some testing vars
gtuple = ()
animation = False
que = []


class Button():
    def __init__(self, x, y, w, h, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'inactive': gold,
            'hover': grey,
            'active': green,
        }

        self.buttonSurface = pygame.Surface((self.w, self.h))
        self.buttonRect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

    def draw(self):
        mousePos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if click[0] == 1 and self.onclickFunction != None:
                self.buttonSurface.fill(self.fillColors['active'])
                self.onclickFunction()
        else:
            self.buttonSurface.fill(self.fillColors['inactive'])

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])

        screen.blit(self.buttonSurface, self.buttonRect)

    # def check_click():


def blit_text(screen, text, midtop, aa=True, font=None, font_name=None, size=None, color=(255, 0, 0)):
    if font is None:  # font option is provided to save memory if font is
        font = pygame.font.SysFont(font_name, size)  # already loaded and needs to be reused many times
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(font_surface, font_rect)


def menu_screen():  # to be called before starting actual game loop
    global screen, n_disks, game_done
    menu_done = False
    while not menu_done:  # every screen/scene/level has its own loop
        screen.fill(white)
        blit_text(screen, 'Towers of Hanoi', (323, 122), font_name='sans serif', size=90, color=grey)
        blit_text(screen, 'Towers of Hanoi', (320, 120), font_name='sans serif', size=90, color=gold)
        blit_text(screen, 'Use arrow keys to select difficulty:', (320, 220), font_name='sans serif', size=30,
                  color=black)
        blit_text(screen, str(n_disks), (320, 260), font_name='sans serif', size=40, color=blue)
        blit_text(screen, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=black)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 6:
                        n_disks = 6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip()
        clock.tick(60)


def game_over():  # game over screen
    global screen, steps
    screen.fill(white)
    min_steps = 2 ** n_disks - 1
    blit_text(screen, 'You Won!', (320, 200), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'You Won!', (322, 202), font_name='sans serif', size=72, color=gold)
    blit_text(screen, 'Your Steps: ' + str(steps), (320, 360), font_name='mono', size=30, color=black)
    blit_text(screen, 'Minimum Steps: ' + str(min_steps), (320, 390), font_name='mono', size=30, color=red)
    if min_steps == steps:
        blit_text(screen, 'You finished in minumum steps!', (320, 300), font_name='mono', size=26, color=green)
    pygame.display.flip()
    time.sleep(5)  # wait for 2 secs
    pygame.quit()  # pygame exit
    sys.exit()  # console exit


def draw_towers():
    global screen
    for xpos in range(40, 460 + 1, 200):
        pygame.draw.rect(screen, blue, pygame.Rect(xpos, 400, 160, 20))
        pygame.draw.rect(screen, brown, pygame.Rect(xpos + 75, 200, 10, 200))
    blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)

    btn = Button(50, 50, 50, 50, "Solve", lambda: toh(n_disks, 0, 2, 1))
    btn.draw()


def left():
    global floating
    global pointing_at, floater
    if not floating:  # up
        for disk in disks[::-1]:
            if disk['tower'] == pointing_at:
                floating = True
                floater = disks.index(disk)
                disk['rect'].midtop = (towers_midx[pointing_at], 100)
                break
    time.sleep(0.5)

    if floating:
        pointing_at = (pointing_at - 1) % 3
        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
        disks[floater]['tower'] = pointing_at
    time.sleep(0.5)


def right():
    global floating
    global pointing_at, floater
    if not floating:  # up
        for disk in disks[::-1]:
            if disk['tower'] == pointing_at:
                floating = True
                floater = disks.index(disk)
                disk['rect'].midtop = (towers_midx[pointing_at], 100)
                break
    time.sleep(0.5)

    if floating:
        pointing_at = (pointing_at + 1) % 3  # RIGHT
        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
        disks[floater]['tower'] = pointing_at
    time.sleep(0.5)


def down():
    global floating
    global pointing_at, floater, steps
    if floating:
        for disk in disks[::-1]:
            if disk['tower'] == pointing_at and disks.index(disk) != floater:
                if disk['val'] > disks[floater]['val']:
                    floating = False
                    disks[floater]['rect'].midbottom = (towers_midx[pointing_at], disk['rect'].top - 1)
                    steps += 1
                break
        else:
            floating = False
            disks[floater]['rect'].midbottom = (towers_midx[pointing_at], 400 - 10)
            steps += 1


def animate(start, end):
    global pointing_at

    pointing_at = start
    if start < end:
        right()
        print(pointing_at)
        if pointing_at != end:
            right()
            print(pointing_at)
            down()
        else:
            down()
    else:
        left()
        print(pointing_at)
        if pointing_at != end:
            left()
            print(pointing_at)
            down()
        else:
            down()


def make_disks():
    global n_disks, disks
    disks = []
    height = 100 / n_disks
    ypos = 390 - height
    width = n_disks * 10
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks - i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height + 1
        width -= 10


def draw_disks():
    global screen, disks
    for disk in disks:
        pygame.draw.rect(screen, green, disk['rect'])
    return


def draw_ptr():
    ptr_points = [(towers_midx[pointing_at] - 7, 440), (towers_midx[pointing_at] + 7, 440),
                  (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(screen, red, ptr_points)
    return


def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(4)
        game_over()


def reset():
    global steps, pointing_at, floating, floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_screen()
    make_disks()


# class Counter(object) :
#     def __init__(self, fun) :
#         self._fun = fun
#         self.counter=0
#     def __call__(self,*args, **kwargs) :
#         self.counter += 1
#         return self._fun(*args, **kwargs)

def incNo():
    global n
    n += 1
    print(n)


def toh(n, start, end, other):
    # has no effect
    global gtuple, que
    global steps
    if (n == 1):

        print(start, '->', end)
        tup = (start, end)
        gtuple += (tup,)
    else:
        toh(n - 1, start, other, end)

        print(start, '->', end)
        tup = (start, end)
        gtuple += (tup,)
        toh(n - 1, other, end, start)
    que = list(gtuple)
    return 0


menu_screen()
make_disks()

# main game loop:
while not game_done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at + 1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at - 1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break
            if event.key == pygame.K_DOWN and floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk) != floater:
                        if disk['val'] > disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midbottom = (towers_midx[pointing_at], disk['rect'].top - 1)
                            steps += 1
                        break
                else:
                    floating = False
                    disks[floater]['rect'].midbottom = (towers_midx[pointing_at], 400 - 10)
                    if animate:  # might be uneccessary
                        steps += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            event_x, event_y = event.pos

            # Check if the event position is inside the bounding box
            if (50 <= event_x <= 50 + 50) and \
                    (50 <= event_y <= 50 + 50):
                toh(n_disks, 0, 2, 1)
                print("Event position is inside the bounding box")
                animation = True
                steps = 0
    if animation:
        sum = 2 ** n_disks - 1
        i = 0
        if sum > i:
            item = que.pop(0)
            a, b = item
            print(item)

            animate(a, b)
            i += 1

        else:

            animation = False

    screen.fill(white)
    draw_towers()
    draw_disks()
    draw_ptr()

    blit_text(screen, 'Steps: ' + str(steps), (320, 20), font_name='mono', size=30, color=black)
    pygame.display.flip()

    if not floating: check_won()
    clock.tick(framerate)

# print(gtuple)