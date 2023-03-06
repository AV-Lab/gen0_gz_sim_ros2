import pygame
import can
import time

class VehicleControl:
    def __init__(self):

        # Configuration
        self.desiredSpeedForward= 0.2 # m/s
        self.desiredSpeedBackward= -0.2 # m/s
        self.desiredSpeedAcceleration= 0.2 # m/s^2
        self.desiredSpeedDeceleration= -0.2 # m/s^2

        # Development purpose dont modify
        self.current_front_step = 0
        self.current_rear_step = 0
        self.front_steer_lsb='00'
        self.front_steer_msb='00'
        self.rear_steer_lsb='00'
        self.rear_steer_msb='00'
        self.speed_lsb='00'
        self.speed_msb='00'
        self.acceleration_lsb='00'
        self.acceleration_msb='00'
        self.bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)

        # Draw the layout
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))

        self.w_button_pos = (125, 50)
        self.w_button_size = (50, 50)
        self.a_button_pos = (50, 150)
        self.a_button_size = (50, 50)
        self.s_button_pos = (125, 150)
        self.s_button_size = (50, 50)
        self.d_button_pos = (200, 150)
        self.d_button_size = (50, 50)
        self.x_button_pos = (125, 250)
        self.x_button_size = (50, 50)

        self.w_button = pygame.Rect(self.w_button_pos[0], self.w_button_pos[1], self.w_button_size[0], self.w_button_size[1])
        self.a_button = pygame.Rect(self.a_button_pos[0], self.a_button_pos[1], self.a_button_size[0], self.a_button_size[1])
        self.s_button = pygame.Rect(self.s_button_pos[0], self.s_button_pos[1], self.s_button_size[0], self.s_button_size[1])
        self.d_button = pygame.Rect(self.d_button_pos[0], self.d_button_pos[1], self.d_button_size[0], self.d_button_size[1])
        self.x_button = pygame.Rect(self.x_button_pos[0], self.x_button_pos[1], self.x_button_size[0], self.x_button_size[1])

        self.screen.fill((0, 0, 0)) # Fill the screen with black color
        # Draw the buttons on the screen
        pygame.draw.rect(self.screen, (255, 0, 0), self.w_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.a_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.s_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.d_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.x_button)
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface_w = myfont.render('w', False, (255, 255, 255))
        textsurface_a = myfont.render('a', False, (255, 255, 255))
        textsurface_s = myfont.render('s', False, (255, 255, 255))
        textsurface_d = myfont.render('d', False, (255, 255, 255))
        textsurface_x = myfont.render('x', False, (255, 255, 255))
        self.screen.blit(textsurface_w, (self.w_button_pos[0] + 20,self.w_button_pos[1] + 10))
        self.screen.blit(textsurface_a, (self.a_button_pos[0] + 20,self.a_button_pos[1] + 10))
        self.screen.blit(textsurface_s, (self.s_button_pos[0] + 20,self.s_button_pos[1] + 10))
        self.screen.blit(textsurface_d, (self.d_button_pos[0] + 20,self.d_button_pos[1] + 10))
        self.screen.blit(textsurface_x, (self.x_button_pos[0] + 20,self.x_button_pos[1] + 10))
        
    def steerFrontRadToDecimal(self, step):
        hex_number = hex(step & int("1"*16, 2))
        extended_hex = "{:04x}".format(int(hex_number, 16))
        return extended_hex[2:4], extended_hex[0:2]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                if self.current_front_step == 3060:
                    print("max reached: " + str(self.current_front_step))
                else:
                    self.current_front_step= self.current_front_step + 60
                    self.front_steer_lsb, self.front_steer_msb = self.steerFrontRadToDecimal(self.current_front_step)
                    self.current_rear_step= self.current_rear_step - 60
                    self.rear_steer_lsb, self.rear_steer_msb = self.steerFrontRadToDecimal(self.current_rear_step)
                    print("Input is left => Current front step is: " + str(self.current_front_step) + ", Current rear step is: " + str(self.current_rear_step))
            if keys[pygame.K_d]:
                if self.current_front_step == -3060:
                    print("max reached: " + str(self.current_front_step))
                else:
                    self.current_front_step = self.current_front_step - 60
                    self.front_steer_lsb, self.front_steer_msb = self.steerFrontRadToDecimal(self.current_front_step)
                    self.current_rear_step = self.current_rear_step + 60
                    self.rear_steer_lsb, self.rear_steer_msb = self.steerFrontRadToDecimal(self.current_rear_step)
                    print("Input is right => Current front step is: " + str(self.current_front_step) + ", Current rear step is: " + str(self.current_rear_step))
            if keys[pygame.K_w]:
                self.speed_lsb, self.speed_msb = self.steerFrontRadToDecimal(int(self.desiredSpeedForward * 1000))
                self.acceleration_lsb, self.acceleration_msb = self.steerFrontRadToDecimal(int(self.desiredSpeedAcceleration * 1000))
                print("Setting the speed to => " + str(self.desiredSpeedForward) + " Acceleration is => " + str(self.desiredSpeedAcceleration))

            if keys[pygame.K_s]:
                self.speed_lsb, self.speed_msb = self.steerFrontRadToDecimal(0)
                self.acceleration_lsb, self.acceleration_msb = self.steerFrontRadToDecimal(int(self.desiredSpeedDeceleration * 1000))
                print("Setting the speed to => " + '0' + " Deceleration is => " + str(self.desiredSpeedDeceleration))

            if keys[pygame.K_x]:
                self.speed_lsb, self.speed_msb = self.steerFrontRadToDecimal(int(self.desiredSpeedBackward * 1000))
                self.acceleration_lsb, self.acceleration_msb = self.steerFrontRadToDecimal(int(self.desiredSpeedAcceleration * 1000))
                print("Setting the speed to => " + str(self.desiredSpeedBackward) + " Acceleration is => " + str(self.desiredSpeedAcceleration))
            
            try:
                msg_steering = can.Message(arbitration_id=0x193, data=[int(self.acceleration_lsb, 16), int(self.acceleration_msb, 16), int(self.speed_lsb, 16), int(self.speed_msb, 16), int(self.front_steer_lsb, 16), int(self.front_steer_msb, 16), int(self.rear_steer_lsb, 16), int(self.rear_steer_msb, 16)],is_extended_id=False)
                self.bus.send(msg_steering)
            except can.CanError:
                print("Message NOT sent")
            
            time.sleep(0.02)
            # Update the screen
            pygame.display.flip()


vehicle_control = VehicleControl()
vehicle_control.run()


