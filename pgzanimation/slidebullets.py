from .pgzanimation import PgzAnimation
from pgzanimation import AnimBulletText
from .slide import Slide

class SlideBullets(Slide):
    
    def __init__(self, size, title, bullets, bulletstarty=220, bulletendy=1070, bulletstartx=50 ):
        super().__init__(size, title)
        self._bullets = []
        self._bullet_start_x = bulletstartx
        self._bullet_start_y = bulletstarty
        self._bullet_end_y = bulletendy
        # check bullet end is not bigger than height of screen
        if (self._bullet_end_y > self._size[1]):
            self._bullet_end_y = self._size[1] - 50
        # to prevent crashing must be at least one bullet - set to blank
        if len(bullets) == 0:
            bullets.append(" ")
        # Bullets must have their position defined when created so work out here
        bullet_delta_y = (self._bullet_end_y - self._bullet_start_y) / len (bullets)
        this_y_pos = self._bullet_start_y
        for this_bullet in bullets:
            self._bullets.append(AnimBulletText(this_bullet, (self._bullet_start_x,this_y_pos)))
            this_y_pos += bullet_delta_y
            
    def draw(self):
        if (super().draw() == False):
            return
        for this_bullet in self._bullets:
            this_bullet.draw()