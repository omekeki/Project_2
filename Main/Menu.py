import pygame, sys

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Globals
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
FONT_COLOR = (0, 0, 100)

click_sound = True
main_music = pygame.mixer.music.load("../sounds/menu_music.wav")
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound("../sounds/click.wav")

def load_image(filename: str) -> pygame.Surface:
    surface = pygame.image.load(filename).convert()
    return surface


class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=10,
                 font_color=FONT_COLOR, pos_x=0, pos_y=0):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y
        self.is_selected = False

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

    def is_mouse_selection(self, posx, posy):
        global click_sound
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
                (posy >= self.pos_y and posy <= self.pos_y + self.height):
            return True
        if not (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
                    (posy >= self.pos_y and posy <= self.pos_y + self.height):
            click_sound = True
            return False


class GameMenu():
    def __init__(self, screen, items, bg_color=BLACK, font=None, font_size=30,
                 font_color=FONT_COLOR):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.pressed = False
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, 38, FONT_COLOR)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_item_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
            item.set_font_color(FONT_COLOR)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pygame.K_UP and \
                            self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                            self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                            self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                            self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(BLUE)
        click.play(loops=0, maxtime=0, fade_ms=0)

        # Finally check if Enter or Space is pressed
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            mainloop = False
            self.pressed = True
            return text

    def set_mouse_selection(self, item, mpos):
        """Marks the MenuItem the mouse cursor hovers on."""

        global click_sound
        if item.is_mouse_selection(mpos[0],mpos[1]):
            item.set_font_color(BLUE)
            item.set_italic(True)
            if click_sound:
                click.play(loops = 0, maxtime = 0, fade_ms = 0)
                click_sound = False
        else:
            item.set_font_color(FONT_COLOR)
            item.set_italic(False)


    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 60 FPS
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_item_selection(event.key)
                    if self.pressed:
                        return self.set_item_selection(event.key)
                        self.pressed = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos[0], mpos[1]):
                            return item.text

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            # Redraw the background
            self.screen.fill(self.bg_color)
            screen.blit(menu_bg, (0, 0))

            for item in self.items:
                if self.mouse_is_visible:
                    mpos = pygame.mouse.get_pos()
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()

# Creating the screen
screen = pygame.display.set_mode((930, 580), 0, 32)
menu_bg = load_image('../images/battleship.jpg')
menu_items = ('Start', 'Instructions', 'Highscore','Settings', 'Quit')
pygame.display.set_caption('Game Menu')
gm = GameMenu(screen, menu_items)
