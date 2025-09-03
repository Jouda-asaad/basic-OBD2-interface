import obd
import pygame
import argparse
import sys
import time

# --- Configuration Constants ---
# Connection settings
DEFAULT_PORT = "/dev/rfcomm99"
BAUDRATE = 9600
CONNECTION_TIMEOUT = 30

# Unit conversion
KPH_TO_MPH = 0.621371

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Classes for Organization ---

class CarState:
    """A class to hold and manage the car's real-time data."""
    def __init__(self):
        self.speed = 0
        self.rpm = 0
        self.load = 0

    def update_speed(self, s):
        """Callback for SPEED command."""
        if not s.is_null():
            # Convert from kph to mph
            self.speed = int(s.value.magnitude * KPH_TO_MPH)

    def update_rpm(self, r):
        """Callback for RPM command."""
        if not r.is_null():
            self.rpm = int(r.value.magnitude)

    def update_load(self, l):
        """Callback for ENGINE_LOAD command."""
        if not l.is_null():
            self.load = int(l.value.magnitude)

class Display:
    """A class to manage all Pygame display elements."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("OBD-II Dashboard")
        pygame.mouse.set_visible(False)

        # Initialize fonts once for efficiency
        self.label_font = pygame.font.SysFont(None, 50)
        self.value_font = pygame.font.SysFont(None, 75)
        self.unit_font = pygame.font.SysFont(None, 50)

    def draw_dashboard(self, state: CarState):
        """Draws the entire dashboard, both static and dynamic elements."""
        self.screen.fill(BLACK)

        # --- Draw static UI elements ---
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(5, 5, 150, 150), 2)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(270, 5, 150, 150), 2)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(155, 100, 115, 115), 2)

        speed_label = self.label_font.render("Speed", True, WHITE)
        self.screen.blit(speed_label, (15, 160))

        rpm_label = self.label_font.render("RPM", True, WHITE)
        self.screen.blit(rpm_label, (310, 160))

        load_label = self.label_font.render("Load", True, WHITE)
        self.screen.blit(load_label, (175, 60))

        # --- Draw dynamic data values ---
        speed_text = self.value_font.render(str(state.speed), True, WHITE)
        speed_unit = self.unit_font.render("mph", True, WHITE)
        self.screen.blit(speed_text, (22, 50))
        self.screen.blit(speed_unit, (22, 100))


        rpm_text = self.value_font.render(str(state.rpm), True, WHITE)
        self.screen.blit(rpm_text, (285, 50))

        load_text = self.value_font.render(f"{state.load}%", True, WHITE)
        self.screen.blit(load_text, (172, 130))

        # Update the full display
        pygame.display.flip()

    def quit(self):
        """Shuts down Pygame."""
        pygame.quit()

def connect_obd(port: str):
    """
    Establishes and validates the OBD connection.
    Returns a connection object or None if failed.
    """
    print(f"Attempting to connect to OBD-II adapter at {port}...")
    try:
        connection = obd.Async(
            port,
            protocol="6",
            baudrate=str(BAUDRATE),
            fast=False,
            timeout=CONNECTION_TIMEOUT
        )
        
        # Give the connection a moment to initialize
        time.sleep(2)

        # Check if the connection is successful by querying supported commands
        if not connection.is_connected() or len(connection.supported_commands) == 0:
            print("Error: Could not establish a stable connection. Check adapter and port.", file=sys.stderr)
            connection.close()
            return None

        print("Connection successful.")
        return connection
    except Exception as e:
        print(f"Error connecting to OBD-II adapter: {e}", file=sys.stderr)
        return None

def main(args):
    """Main function to run the dashboard application."""
    connection = connect_obd(args.port)
    if not connection:
        sys.exit(1)

    car_state = CarState()
    display = Display()

    # Register callbacks to update the car's state
    connection.watch(obd.commands.SPEED, callback=car_state.update_speed)
    connection.watch(obd.commands.RPM, callback=car_state.update_rpm)
    connection.watch(obd.commands.ENGINE_LOAD, callback=car_state.update_load)

    # Start the asynchronous connection
    connection.start()

    running = True
    try:
        while running:
            # Event handling (e.g., for quitting)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            
            # Draw the screen with the latest data
            display.draw_dashboard(car_state)
            
            # Limit the loop to a reasonable refresh rate
            pygame.time.Clock().tick(30)

    finally:
        # This block will run whether the loop exits cleanly or via an error
        print("Closing connection and shutting down.")
        if connection and connection.is_connected():
            connection.stop()
            connection.close()
        display.quit()

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="OBD-II Real-time Dashboard")
    parser.add_argument(
        "--port",
        default=DEFAULT_PORT,
        help=f"Serial port for the OBD-II adapter (default: {DEFAULT_PORT})"
    )
    args = parser.parse_args()
    
    # Configure OBD logging
    obd.logger.setLevel(obd.logging.DEBUG)
    
    main(args)