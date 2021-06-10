from .pgzanimation import PgzAnimation
from pgzanimation import AnimBulletText
from .slide import Slide

class SlideBullets(Slide):
    
    # bullet spacing is distance between bullets (including the bullet)
    def __init__(self, size, title, bullets, bulletstartpos=(50,220), bulletspacing=80):
        super().__init__(size, title)
        self._bullets = []
        # bullet position is always top left
        self._bullet_pos = bulletstartpos
        # to prevent crashing must be at least one bullet - set to blank
        if len(bullets) == 0:
            bullets.append("")
        # Bullets must have their position defined when created so work out here
        this_y_pos = self._bullet_pos[1]
        for this_bullet in bullets:
            self._bullets.append(AnimBulletText(this_bullet, (self._bullet_pos[0],this_y_pos)))
            this_y_pos += bulletspacing
            
    def draw(self):
        if (super().draw() == False):
            return
        for this_bullet in self._bullets:
            this_bullet.draw()