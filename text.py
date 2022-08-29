import pygame

class TextHandler():
    def __init__(self,path,color,text,size,antialias=True):
        self.path = path
        self.color=color
        self.text=text
        self.size=size
        self.ref_size=size
        self.antialias=antialias
        self.font=pygame.font.Font(self.path,int(self.size))
        self.text_obj = self.font.render(self.text,self.antialias,self.color)
        self.rect=self.text_obj.get_rect()
        self.switch=False
        self.timer=0
    def shrink_pop(self,timer):
        if self.switch==False:
            if self.timer!=timer:
                self.size-=.1
                self.timer+=1
            else:
                self.timer=0
                self.switch=True
        else:
            if self.timer<timer:
                self.size+=.1
                self.timer+=1
            # elif self.timer<timer*1.75:###pop feature needs work###
            #     self.size+=.25
            #     self.timer+=1
            else:
                self.timer=0
                self.size=self.ref_size
                self.switch=False
        self.update()

    def update(self):
        self.font=pygame.font.Font(self.path,int(self.size))
        self.text_obj = self.font.render(self.text,self.antialias,self.color)

    @property
    def x(self):
        return self.rect.x
    @property
    def y(self):
        return self.rect.y
    @property
    def width(self):
        return self.rect.width
    @property
    def height(self):
        return self.rect.height

def draw_text(surface, text, color, font, aa=False, bkg=None):
    '''Draw some text into an area of a surface.
    Automatically wraps words;
    Returns any text that didn't get blitted
    '''
    rect = surface.get_rect()
    rect.topleft=(5,5)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1
        new_line=False

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            nl=text.rfind('\n',0,i)
            if nl == -1:
                i = text.rfind(" ", 0, i) + 1
            else:
                new_line=True
                i = text.rfind("\n", 0, i)

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

        if new_line:
            image = font.render('', aa, color)
            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            text = text[1:]

    return text