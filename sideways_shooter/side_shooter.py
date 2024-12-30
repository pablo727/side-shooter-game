import pygame
import sys
from side_settings import Settings
from ss_ship import Jet
from side_bullet import Bullet
from alien import Alien

class SideShooter():
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Side Shooter')

        self.ship = Jet(self)

        # Create a group for bullets.
        self.bullets = pygame.sprite.Group()

        # Create a group of aliens.
        self.aliens = pygame.sprite.Group()

        # Set the fleet direction before creating the fleet.
        self.fleet_direction = -1 # 1 for right, -1 for left.
        
        # Adjust for the speed of the aliens.
        self.settings.alien_speed

        # Create fleet.
        self._create_fleet()
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()  # Check for events like key presses.
            self.ship.update()  # Update position of the ship.
            self._update_bullets()  # Update the bullets.
            self._split_fleet()  # Check and split the fleet when close to ship
            self._update_aliens()  # Update the position of aliens.
            self._update_screen()  # Redraw the screen.
            self.clock.tick(60)  # Limit frame rate to 60 FPS.
    
    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # Create a bullet when space is pressed.   
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        
    def _check_keyup_events(self, event):
        """Respond to key release."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        """Create two bullets and add them to the bullet group."""
        # Adjust offset for left and right cannon.
        new_bullet_left = Bullet(self, offset_x=20, offset_y=15) # Left.
        new_bullet_right = Bullet(self, offset_x=20, offset_y=80) # Right.  

        self.bullets.add(new_bullet_left)  # Add it to the group
        self.bullets.add(new_bullet_right)
    
    def _update_bullets(self):
        """Update the position of bullets and remove off-screen ones."""
        self.bullets.update()  # Update all bullets in the group.

        # Remove bullets that are off the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.right < 0:
                self.bullets.remove(bullet)
    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self, self.fleet_direction)
        alien_width, alien_height = alien.rect.size

        # Add padding values.
        top_padding = 20  # Padding from the top.
        bottom_padding = 150  # Padding from the bottom.
        right_padding = 20  # Padding from the right.

        # Set a fixed amount of space between aliens.
        horizontal_spacing = alien_width * 1.2 # Larger than alien width.
        vertical_spacing = alien_height * 1.8  # Larger than alien height.

        # Starting positions with padding.
        current_x, current_y = alien_width, alien_height + top_padding
        current_x += 4.3 * alien_width  # Start first row bit further from left

        # Adjust to avoid right edge
        while current_x + alien_width <= (self.settings.screen_width 
                                          - right_padding):  # Avoid right edge
            current_y = vertical_spacing + top_padding  # Reset y position.

            # Split fleet in two halves: Top and Bottom.
            while current_y + alien_height <= (self.settings.screen_height 
                                               - bottom_padding): 
                self._create_alien(current_x, current_y)
                current_y += vertical_spacing  # Move down next alien.

            # Move to the next column, adjusting for the width of the alien.
            current_x += horizontal_spacing  # Move right calculated spacing
        
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self, self.fleet_direction)
        new_alien.y = y_position
        new_alien.rect.y = y_position 
        new_alien.rect.x = x_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()  # Update the position of each alien.

        # Move the fleet based on fleet direction.
        for alien in self.aliens.sprites():
            alien.rect.x += self.settings.alien_speed * self.fleet_direction

            # Move aliens vertically if they hit the edge.
            if self.fleet_direction == 1:  # Moving right.
                if alien.rect.right >= self.settings.screen_width:
                    self.fleet_direction = -1  # Move left.
                    for alien in self.aliens.sprites():
                        alien.rect.y += 10  # Move the entire fleet down.
            elif self.fleet_direction == -1:  # Moving left.
                if alien.rect.left <= 0:
                    self.fleet_direction = 1  # Move right.
                    for alien in self.aliens.sprites():
                        alien.rect.y += 10  # Move the entire fleet down.
    def _split_fleet(self):
        """Split the alien fleet into two halves 
        and make them move in opposite directions."""
        # Check if the aliens are close enough to the ship
        # (i.e., below the ship's position).
        ship_rect = self.ship.rect
        for alien in self.aliens.sprites():
            if alien.rect.centery > ship_rect.centery + 140:  # Adjust value.
                # Split the fleet into two parts: 
                # left half goes toward the top,
                # right half goes toward the bottom.
                top_half = []
                bottom_half = []

                # Separate the aliens into top and bottom halves
                #  based on their y-cordinate. 
                for alien in self.aliens.sprites():
                    if alien.rect.centerx < ship_rect.centery:
                        top_half.append(alien)  # Aliens above the ship.
                    else:
                        bottom_half.append(alien)  # Aliens below the ship.

                # Now, move each half in opposite directions.
                for alien in top_half:
                    alien.fleet_direction = 1  # Move the top half upwards 
                                               #(negative y direction).
                    alien.speed = self.settings.alien_speed  # Keep same speed.

                for alien in bottom_half:
                    alien.fleet_direction = -1  # Move the bottom half 
                                            # downwards (positive y direction).
                    alien.speed = self.settings.alien_speed  # Same speed.
                break  # Exit loop when split condition is triggered.                       


    def _check_fleet_edges(self):
        """Respond if any alien hits the edge of the screen."""
        for alien in self.aliens.sprites():
            if (alien.rect.right >= self.settings.screen_width or
                 alien.rect.left <= 0):
                self._change_fleet_direction()
                break  # No need to check other aliens once fleet hits the edge
    
    def _change_fleet_direction(self):
        """Move the entire fleet down and change direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += 1  # Move down(adjust value as needed).
        self.fleet_direction *= -1  # Reverse direction.

    def _update_screen(self):
        """Update images on the screen, and flip to new screen."""
        self.screen.fill(self.settings.bg_color)
        # Draw the ship.
        self.ship.blitme()

        # Draw the bullets.
        self.bullets.draw(self.screen)

        # Draw the aliens.
        self.aliens.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    ss = SideShooter()
    ss.run_game()



