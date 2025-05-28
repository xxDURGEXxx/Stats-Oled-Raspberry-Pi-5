import pygame
import sys
import random
from enum import Enum
# Constants for colors
BGCOLOR = (0, 0, 0)           # Black background
MAINCOLOR = (255, 255, 255)   # White drawings

# Mood Types
class Mood (Enum):
    DEFAULT = 0
    TIRED = 1
    ANGRY = 2
    HAPPY = 3

# Predefined Positions
class Position(Enum):
    N = 1    # North, top center
    NE = 2   # North-east, top right
    E = 3    # East, middle right
    SE = 4   # South-east, bottom right
    S = 5    # South, bottom center
    SW = 6   # South-west, bottom left
    W = 7    # West, middle left
    NW = 8   # North-west, top left



EYES_SIZE= 30
EYES_RADIOUS =7
CURIOSITY_HEIGHT = 6
CURIOSITY_TRASHHOLD = 24
EYES_GAP=15

class RoboEyes:
    def __init__(self, draw_surface, width=320, height=240, frame_rate=50):
        """
        Initialize the RoboEyes class.

        :param draw_surface: Pygame surface to draw on.
        :param width: Screen width in pixels (unrotated).
        :param height: Screen height in pixels (unrotated).
        :param frame_rate: Maximum frames per second.
        """
        self.surface = draw_surface
        self.screen_width = width
        self.screen_height = height
        self.frame_interval = 1000 / frame_rate  # in milliseconds
        self.fps_timer = pygame.time.get_ticks()

        # Mood and expressions
        self.tired = False
        self.angry = False
        self.happy = False
        self.curious = False
        self.cyclops = False
        self.eyeL_open = False
        self.eyeR_open = False

        # Eye Geometry
        self.space_between_default = EYES_GAP  # Reduced space for larger eyes
        self.space_between_current = self.space_between_default
        self.space_between_next = self.space_between_default

        # Left Eye
        self.eyeLwidth_default =  EYES_SIZE  # Increased size proportionally
        self.eyeLheight_default = EYES_SIZE
        self.eyeLwidth_current = self.eyeLwidth_default
        self.eyeLheight_current = 1  # start with closed eye
        self.eyeLwidth_next = self.eyeLwidth_default
        self.eyeLheight_next = self.eyeLheight_default
        self.eyeLheight_offset = 0

        self.eyeLborder_radius_default = EYES_RADIOUS  # Increased radius for larger eyes
        self.eyeLborder_radius_current = self.eyeLborder_radius_default
        self.eyeLborder_radius_next = self.eyeLborder_radius_default

        # Right Eye
        self.eyeRwidth_default = self.eyeLwidth_default
        self.eyeRheight_default = self.eyeLheight_default
        self.eyeRwidth_current = self.eyeRwidth_default
        self.eyeRheight_current = 1  # start with closed eye
        self.eyeRwidth_next = self.eyeRwidth_default
        self.eyeRheight_next = self.eyeRheight_default
        self.eyeRheight_offset = 0

        self.eyeRborder_radius_default = EYES_RADIOUS
        self.eyeRborder_radius_current = self.eyeRborder_radius_default
        self.eyeRborder_radius_next = self.eyeRborder_radius_default

        # Coordinates
        self.eyeLx_default = (self.screen_width - (self.eyeLwidth_default + self.space_between_default + self.eyeRwidth_default)) // 2
        self.eyeLy_default = (self.screen_height - self.eyeLheight_default) // 2
        self.eyeLx = self.eyeLx_default
        self.eyeLy = self.eyeLy_default
        self.eyeLx_next = self.eyeLx
        self.eyeLy_next = self.eyeLy

        self.eyeRx_default = self.eyeLx + self.eyeLwidth_current + self.space_between_default
        self.eyeRy_default = self.eyeLy
        self.eyeRx = self.eyeRx_default
        self.eyeRy = self.eyeRy_default
        self.eyeRx_next = self.eyeRx
        self.eyeRy_next = self.eyeRy

        # Both Eyes
        self.eyelids_height_max = self.eyeLheight_default // 2
        self.eyelids_tired_height = 0
        self.eyelids_tired_height_next = self.eyelids_tired_height
        self.eyelids_angry_height = 0
        self.eyelids_angry_height_next = self.eyelids_angry_height
        self.eyelids_happy_bottom_offset_max = (self.eyeLheight_default // 2) + 6  # Adjusted for larger eyes
        self.eyelids_happy_bottom_offset = 0
        self.eyelids_happy_bottom_offset_next = 0
        self.eyes_same_y =True

        # Macro Animations
        self.hFlicker = False
        self.hFlicker_alternate = False
        self.hFlicker_amplitude = 4  # Increased amplitude for larger screen

        self.vFlicker = False
        self.vFlicker_alternate = False
        self.vFlicker_amplitude = 20  # Increased amplitude for larger screen

        self.autoblinker = False
        self.blink_interval = 2000  # in milliseconds (2 seconds)
        self.blink_interval_variation = 4000  # in milliseconds
        self.blink_timer = pygame.time.get_ticks()

        self.idle = False
        self.idle_interval = 5000  # in milliseconds (5 seconds)
        self.idle_interval_variation = 5000  # in milliseconds
        self.idle_animation_timer = pygame.time.get_ticks()

        self.confused = False
        self.confused_animation_timer = 0
        self.confused_animation_duration = 500  # in milliseconds
        self.confused_toggle = True

        self.laugh = False
        self.laugh_animation_timer = 0
        self.laugh_animation_duration = 500  # in milliseconds
        self.laugh_toggle = True

    # General Setup
    def begin(self):
        self.clear_display()
        self.eyeLheight_current = 1
        self.eyeRheight_current = 1

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.fps_timer >= self.frame_interval:
            self.drawEyes()
            self.fps_timer = current_time

    # Setter Methods
    def setFramerate(self, fps):
        self.frame_interval = 1000 / fps

    def setWidth(self, leftEye, rightEye):
        self.eyeLwidth_next = leftEye
        self.eyeRwidth_next = rightEye
        self.eyeLwidth_default = leftEye
        self.eyeRwidth_default = rightEye

    def setHeight(self, leftEye=None, rightEye=None):
        self.eyeLheight_next = self.eyeLheight_default if leftEye is None else leftEye
        self.eyeRheight_next = self.eyeRheight_default if rightEye is None else rightEye

    def setBorderradius(self, leftEye, rightEye):
        self.eyeLborder_radius_next = leftEye
        self.eyeRborder_radius_next = rightEye
        self.eyeLborder_radius_default = leftEye
        self.eyeRborder_radius_default = rightEye

    def setSpacebetween(self, space):
        self.space_between_next = space
        self.space_between_default = space
    
    def getSpacebetween(self):
        return self.space_between_default

    def setMood(self, mood):
        self.tired = False
        self.angry = False
        self.happy = False
        if mood == Mood.TIRED : self.tired = True
        elif mood == Mood.ANGRY : self.angry = True
        elif mood == Mood.HAPPY : self.happy = True

    def setPosition(self, position="center"):
        if position == Position.N:
            self.eyeLx_next = self.getScreenConstraint_X() // 2
            self.eyeLy_next = 0
        elif position == Position.NE:
            self.eyeLx_next = self.getScreenConstraint_X()
            self.eyeLy_next = 0
        elif position == Position.E:
            self.eyeLx_next = self.getScreenConstraint_X()
            self.eyeLy_next = self.getScreenConstraint_Y() // 2
        elif position == Position.SE:
            self.eyeLx_next = self.getScreenConstraint_X()
            self.eyeLy_next = self.getScreenConstraint_Y()
        elif position == Position.S:
            self.eyeLx_next = self.getScreenConstraint_X() // 2
            self.eyeLy_next = self.getScreenConstraint_Y()
        elif position == Position.SW:
            self.eyeLx_next = 0
            self.eyeLy_next = self.getScreenConstraint_Y()
        elif position == Position.W:
            self.eyeLx_next = 0
            self.eyeLy_next = self.getScreenConstraint_Y() // 2
        elif position == Position.NW:
            self.eyeLx_next = 0
            self.eyeLy_next = 0
        else:
            # Default: Middle center
            self.eyeLx_next = self.getScreenConstraint_X() // 2
            self.eyeLy_next = self.getScreenConstraint_Y() // 2

    def setAutoblinker(self, active, interval=2, variation=4):
        """
        Set automated eye blinking.

        :param active: Boolean to activate/deactivate autoblinker.
        :param interval: Basic interval between each blink in seconds.
        :param variation: Interval variation range in seconds.
        """
        self.autoblinker = active
        self.blink_interval = interval * 1000  # convert to milliseconds
        self.blink_interval_variation = variation * 1000  # convert to milliseconds

    def setIdleMode(self, active, interval=5, variation=5):
        """
        Set idle mode for automated eye repositioning.

        :param active: Boolean to activate/deactivate idle mode.
        :param interval: Basic interval between each repositioning in seconds.
        :param variation: Interval variation range in seconds.
        """
        self.idle = active
        self.idle_interval = interval * 1000  # convert to milliseconds
        self.idle_interval_variation = variation * 1000  # convert to milliseconds

    def setCuriosity(self, curious_bit):
        self.curious = curious_bit

    def setCyclops(self, cyclops_bit):
        self.cyclops = cyclops_bit

    def setHFlicker(self, flicker_bit, amplitude=4):
        self.hFlicker = flicker_bit
        self.hFlicker_amplitude = amplitude

    def setVFlicker(self, flicker_bit, amplitude=20):
        self.vFlicker = flicker_bit
        self.vFlicker_amplitude = amplitude

    # Getter Methods
    def getScreenConstraint_X(self):
        return self.screen_width - self.eyeLwidth_current - self.space_between_current - self.eyeRwidth_current
        

    def getScreenConstraint_Y(self):
        return self.screen_height - self.eyeLheight_default  # Using default height

    # Blinking Methods
    def close(self, left=True, right=True):
        if left:
            self.eyeLheight_next = 1
            self.eyeL_open = False
        if right:
            self.eyeRheight_next = 1
            self.eyeR_open = False

    def open_eyes(self, left=True, right=True):
        if left:
            self.eyeL_open = True
        if right:
            self.eyeR_open = True

    def blink(self, left=True, right=True):
        self.close(left, right)
        self.open_eyes(left, right)

    # Macro Animation Methods
    def anim_confused(self):
        self.confused = True

    def anim_laugh(self):
        self.laugh = True

    # Drawing Methods
    def drawEyes(self):
        current_time = pygame.time.get_ticks()

        # Pre-Calculations
        if self.curious:
            if self.eyeLx_next <= CURIOSITY_TRASHHOLD:  # Adjusted threshold for larger screen
                self.eyeLheight_offset = CURIOSITY_HEIGHT
            elif self.eyeLx_next >= (self.getScreenConstraint_X() - 20) and self.cyclops:
                self.eyeLheight_offset = CURIOSITY_HEIGHT
            else:
                self.eyeLheight_offset = 0  # left eye

            if self.eyeRx_next >= self.screen_width - self.eyeRwidth_current - 20:
                self.eyeRheight_offset = CURIOSITY_HEIGHT
            else:
                self.eyeRheight_offset = 0  # right eye
        else:
            self.eyeLheight_offset = 0
            self.eyeRheight_offset = 0

        # Left eye height
        self.eyeLheight_current = (self.eyeLheight_current + self.eyeLheight_next + self.eyeLheight_offset) // 2
        self.eyeLy += ((self.eyeLheight_default - self.eyeLheight_current) // 2)
        self.eyeLy -= self.eyeLheight_offset // 2

        # Right eye height
        self.eyeRheight_current = (self.eyeRheight_current + self.eyeRheight_next + self.eyeRheight_offset) // 2
        self.eyeRy += ((self.eyeRheight_default - self.eyeRheight_current) // 2)
        self.eyeRy -= self.eyeRheight_offset // 2

        # Open eyes again after closing them
        if self.eyeL_open:
            if self.eyeLheight_current <= 1 + self.eyeLheight_offset:
                self.eyeLheight_next = self.eyeLheight_default

        if self.eyeR_open:
            if self.eyeRheight_current <= 1 + self.eyeRheight_offset:
                self.eyeRheight_next = self.eyeRheight_default

        # Left eye width
        self.eyeLwidth_current = (self.eyeLwidth_current + self.eyeLwidth_next) // 2

        # Right eye width
        self.eyeRwidth_current = (self.eyeRwidth_current + self.eyeRwidth_next) // 2

        # Space between eyes
        self.space_between_current = (self.space_between_current + self.space_between_next) // 2

        # Left eye coordinates
        self.eyeLx = (self.eyeLx + self.eyeLx_next) // 2
        self.eyeLy = (self.eyeLy + self.eyeLy_next) // 2

        # Right eye coordinates
        self.eyeRx_next = self.eyeLx_next + self.eyeLwidth_current + self.space_between_current
        self.eyeRy_next = self.eyeLy_next if self.eyes_same_y  else self.eyeRy_next
        self.eyeRx = (self.eyeRx + self.eyeRx_next) // 2
        self.eyeRy = (self.eyeRy + self.eyeRy_next) // 2

        # Left eye border radius
        self.eyeLborder_radius_current = (self.eyeLborder_radius_current + self.eyeLborder_radius_next) // 2

        # Right eye border radius
        self.eyeRborder_radius_current = (self.eyeRborder_radius_current + self.eyeRborder_radius_next) // 2

        # Apply Macro Animations
        if self.autoblinker and (current_time >= self.blink_timer):
            self.blink()
            variation = random.randint(0, self.blink_interval_variation)
            self.blink_timer = current_time + self.blink_interval + variation

        # Laugh Animation
        if self.laugh:
            if self.laugh_toggle:
                self.setVFlicker(True, 10)  # Increased amplitude for larger screen
                self.laugh_animation_timer = current_time
                self.laugh_toggle = False
            elif current_time >= self.laugh_animation_timer + self.laugh_animation_duration:
                self.setVFlicker(False, 0)
                self.laugh_toggle = True
                self.laugh = False

        # Confused Animation
        if self.confused:
            if self.confused_toggle:
                self.setHFlicker(True, 40)  # Increased amplitude for larger screen
                self.confused_animation_timer = current_time
                self.confused_toggle = False
            elif current_time >= self.confused_animation_timer + self.confused_animation_duration:
                self.setHFlicker(False, 0)
                self.confused_toggle = True
                self.confused = False

        # Idle Animation
        if self.idle and (current_time >= self.idle_animation_timer):
            self.eyeLx_next = random.randint(0, self.getScreenConstraint_X())
            self.eyeLy_next = random.randint(0, self.getScreenConstraint_Y())
            variation = random.randint(0, self.idle_interval_variation)
            self.idle_animation_timer = current_time + self.idle_interval + variation

        # Horizontal Flicker
        if self.hFlicker:
            if self.hFlicker_alternate:
                self.eyeLx += self.hFlicker_amplitude
                self.eyeRx += self.hFlicker_amplitude
            else:
                self.eyeLx -= self.hFlicker_amplitude
                self.eyeRx -= self.hFlicker_amplitude
            self.hFlicker_alternate = not self.hFlicker_alternate

        # Vertical Flicker
        if self.vFlicker:
            if self.vFlicker_alternate:
                self.eyeLy += self.vFlicker_amplitude
                self.eyeRy += self.vFlicker_amplitude
            else:
                self.eyeLy -= self.vFlicker_amplitude
                self.eyeRy -= self.vFlicker_amplitude
            self.vFlicker_alternate = not self.vFlicker_alternate

        # Cyclops Mode
        if self.cyclops:
            self.eyeRwidth_current = 0
            self.eyeRheight_current = 0
            self.space_between_current = 0

        # Clear Display
        self.clear_display()

        # Draw Eyes
        self.draw_eye(self.eyeLx, self.eyeLy, self.eyeLwidth_current, self.eyeLheight_current,
                     self.eyeLborder_radius_current, MAINCOLOR)
        if not self.cyclops:
            self.draw_eye(self.eyeRx, self.eyeRy, self.eyeRwidth_current, self.eyeRheight_current,
                         self.eyeRborder_radius_current, MAINCOLOR)

        # Mood Transitions
        if self.tired:
            self.eyelids_tired_height_next = self.eyeLheight_current // 2
            self.eyelids_angry_height_next = 0
        else:
            self.eyelids_tired_height_next = 0

        if self.angry:
            self.eyelids_angry_height_next = self.eyeLheight_current // 2
            self.eyelids_tired_height_next = 0
        else:
            self.eyelids_angry_height_next = 0

        if self.happy:
            self.eyelids_happy_bottom_offset_next = self.eyeLheight_current // 2
        else:
            self.eyelids_happy_bottom_offset_next = 0

        # Draw Tired Eyelids
        self.eyelids_tired_height = (self.eyelids_tired_height + self.eyelids_tired_height_next) // 2
        if not self.cyclops:
            # Left Eye
            points_left = [
                (self.eyeLx, self.eyeLy - 1),
                (self.eyeLx + self.eyeLwidth_current, self.eyeLy - 1),
                (self.eyeLx, self.eyeLy + self.eyelids_tired_height - 1)
            ]
            pygame.draw.polygon(self.surface, BGCOLOR, points_left)

            # Right Eye
            points_right = [
                (self.eyeRx, self.eyeRy - 1),
                (self.eyeRx + self.eyeRwidth_current, self.eyeRy - 1),
                (self.eyeRx + self.eyeRwidth_current, self.eyeRy + self.eyelids_tired_height - 1)
            ]
            pygame.draw.polygon(self.surface, BGCOLOR, points_right)
        else:
            # Cyclops Tired Eyelids
            half_width = self.eyeLwidth_current // 2
            points_left = [
                (self.eyeLx, self.eyeLy - 1),
                (self.eyeLx + half_width, self.eyeLy - 1),
                (self.eyeLx, self.eyeLy + self.eyelids_tired_height - 1)
            ]
            pygame.draw.polygon(self.surface, BGCOLOR, points_left)

            points_right = [
                (self.eyeLx + half_width, self.eyeLy - 1),
                (self.eyeLx + self.eyeLwidth_current, self.eyeLy - 1),
                (self.eyeLx + self.eyeLwidth_current, self.eyeLy + self.eyelids_tired_height - 1)
            ]
            pygame.draw.polygon(self.surface, BGCOLOR, points_right)

        # Draw Angry Eyelids
        self.eyelids_angry_height = (self.eyelids_angry_height + self.eyelids_angry_height_next) // 2
        if not self.cyclops:
            # Left Eye
            points_left = [
                (self.eyeLx, self.eyeLy - 1),
                (self.eyeLx + self.eyeLwidth_current, self.eyeLy - 1),
                (self.eyeLx + self.eyeLwidth_current, self.eyeLy + self.eyelids_angry_height - 1)
            ]
            pygame.draw.polygon(self.surface, BGCOLOR, points_left)

            # Right Eye
            points_right = [
                (self.eyeRx, self.eyeRy - 1),
                (self.eyeRx + self.eyeRwidth_current, self.eyeRy - 1),
                (self.eyeRx, self.eyeRy + self.eyelids_angry_height - 1)
            ]
            pygame.draw.polygon(self.surface, BGCOLOR, points_right)
        else:
            # Cyclops Angry Eyelids
            half_width = self.eyeLwidth_current // 2
            points_left = [
                (self.eyeLx, self.eyeLy - 1),
                (self.eyeLx + half_width, self.eyeLy - 1),
                (self.eyeLx + half_width, self.eyeLy + self.eyelids_angry_height - 1)
            ]
            pygame.draw.polygon(self.surface, BGCOLOR, points_left)

            points_right = [
                (self.eyeLx + half_width, self.eyeLy - 1),
                (self.eyeLx + self.eyeLwidth_current, self.eyeLy - 1),
                (self.eyeLx + half_width, self.eyeLy + self.eyelids_angry_height - 1)
            ]
            pygame.draw.polygon(self.surface, BGCOLOR, points_right)

        # Draw Happy Eyelids
        self.eyelids_happy_bottom_offset = (self.eyelids_happy_bottom_offset + self.eyelids_happy_bottom_offset_next) // 2
        pygame.draw.rect(self.surface, BGCOLOR,
                         (self.eyeLx - 2, (self.eyeLy + self.eyeLheight_current) - self.eyelids_happy_bottom_offset + 2,
                          self.eyeLwidth_current + 4, self.eyeLheight_default))
        if not self.cyclops:
            pygame.draw.rect(self.surface, BGCOLOR,
                             (self.eyeRx - 2, (self.eyeRy + self.eyeRheight_current) - self.eyelids_happy_bottom_offset + 2,
                              self.eyeRwidth_current + 4, self.eyeRheight_default))

        # Update Display (Handled externally)
        # pygame.display.flip()  # Removed to handle rotation externally

    def draw_eye(self, x, y, width, height, border_radius, color):
        # Draw a rounded rectangle representing an eye
        eye_rect = pygame.Rect(x, y, width, height)
        if border_radius > 0:
            pygame.draw.rect(self.surface, color, eye_rect, border_radius=border_radius)
        else:
            pygame.draw.rect(self.surface, color, eye_rect)

    def clear_display(self):
        self.surface.fill(BGCOLOR)