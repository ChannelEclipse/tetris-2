class Block(object):
   def __init__(self, pygame ,canvas ,name , color, rect):
      self.pygame = pygame
      self.canvas = canvas
      self.name   = name
      self.color  = color
      self.rect   = rect
      

      self.visible = True

   def update(self):
      if(self.visible):
        self.pygame.draw.rect(self.canvas, self.color, self.rect) 
