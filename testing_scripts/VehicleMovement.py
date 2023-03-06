import can
import time
from pprint import pprint
from can.message import Message

class VehicleMovement:
    def __init__(self):
        self.state = "reset"
        self.bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)
        self.current_front_step=0
        self.current_rear_step=0
    
    def steerFrontRadToDecimal(self, step):
        hex_number = hex(step & int("1"*16, 2))
        extended_hex = "{:04x}".format(int(hex_number, 16))
        return extended_hex[2:4], extended_hex[0:2]
    
    def moveVehicle(self, front_step, rear_step, iterations):
        for i in range(1, iterations * 52):
            self.current_front_step= self.current_front_step + front_step
            front_steer_lsb, front_steer_msb= self.steerFrontRadToDecimal(self.current_front_step)
            self.current_rear_step= self.current_rear_step + rear_step
            rear_steer_lsb, rear_steer_msb= self.steerFrontRadToDecimal(self.current_rear_step)
            try:
                msg_steering = can.Message(arbitration_id=0x193,data=[0, 0, 0, 0, int(front_steer_lsb, 16), int(front_steer_msb, 16), int(rear_steer_lsb, 16), int(rear_steer_msb, 16)],is_extended_id=False)
                self.bus.send(msg_steering)
                time.sleep(0.02)
            except can.CanError:
                print("Message NOT sent")

    def run(self, input):
        if self.state == "reset":
            if input == "right":
                self.state = "turn_right"
                self.moveVehicle(-60, 60, 1)
            elif input == "left":
                self.state = "turn_left"
                self.moveVehicle(60, -60, 1)
        elif self.state == "turn_right":
            if input == "reset":
                self.state = "reset"
                self.moveVehicle(60, -60, 1)
            elif input == "left":
                self.state = "turn_left"
                self.moveVehicle(60, -60, 2)        
        elif self.state == "turn_left":
            if input == "reset":
                self.state = "reset"
                self.moveVehicle(-60, 60, 1)
            elif input == "left":
                self.state = "turn_left"
                self.moveVehicle(-60, 60, 2)

# usage example
vehicle = VehicleMovement()
vehicle.run("right")
time.sleep(2)
vehicle.run("left")
time.sleep(2)
vehicle.run("reset")