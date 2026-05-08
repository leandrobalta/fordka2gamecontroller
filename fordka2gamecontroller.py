import can
import pywinctl as pwc
import time
from pynput.keyboard import Key, Controller
from dataclasses import dataclass
from threading import Thread

@dataclass
class CarController:
	# Controller state object
	throttle: int = 0
	brake: int = 0
	steering: int = 0

	def AsDictionary(this):
		return {
			"throttle": this.throttle,
			"brake":	this.brake,
			"steering": this.steering
		}

def CANThread(car: CarController):
	# MACOS:                       or 'serial'
	#with can.ThreadSafeBus(channel='fordka', interface='socketcan') as bus:
	with can.interface.Bus(interface='slcan', 
								channel='/dev/cu.usbserial-5B060119651', 
								tty_baudrate=115200, 
								bitrate=500000) as bus:
		for msg in bus:
			msg_handle(car, msg)	

	
def msg_handle(car: CarController, msg):
	# volante: 
	# can id => 07e 
	# tudo pra direita => 6D
	# reto => 80
	# tudo pra esquerda => 93
	# meio pra direita => menor ou igual a 7E
	# meio pra esquerda => maior ou igual a 82

	# update dia 08/05/2026:
	# reto => 7C
	# direita => menor ou igual a 7A
	# esquerda => maior ou igual a 7E

	if msg.arbitration_id == 0x07e:
		#print(f"steering data: [{msg.data}]")
		steer=msg.data[0]
		#print(f"steer: [{steer:02x}]")
		#print(f"{steer:02x}")
		if steer >= 0x7d:
			car.steering=-1
		elif steer <= 0x7b:
			car.steering=1
		else:
			car.steering=0

	
	# FREIO FORD KA
	# CAN ID => 165
	# FREIO DESATIVADO => 10 C0
	# FREIO ATIVADO => 20 C0
 
	#update dia 08/05/2026:
	# FREIO E ACELERADOR MESMO ID => 165
	# PEDALS OFF => 10 C0
	# FREIO ATIVADO => 20 C0
	# ACELERADOR ATIVADO => 50 C0
	# FREIO E ACELERADOR ATIVADOS => 60 C0
	if msg.arbitration_id == 0x165:
		#print(f"brake data: [{msg.data}]")
  
		if msg.data[0] == 0x20:
			car.brake = 1
		else:
			car.brake = 0

		if msg.data[0] == 0x50:
			car.throttle = 1
		elif msg.data[0] == 0x60:
			car.throttle = 1
			car.brake = 1
		else:
			car.throttle = 0

	# ACELERADOR FORD KA
	# CAN ID => 167 
	# ACELERADOR ACIONADO    => 72 7F FF 00 00 1A XX 00
	# ACELERADOR DESACIONADO => 72 7F FF 00 00 19 XX 00
	# if msg.arbitration_id == 0x167:
	# 	#print(f"throttle data [{msg.data}]")
	# 	if msg.data[5] == 0x1a:
	# 		car.throttle = 1
	# 	else:
	# 		car.throttle = 0


keyboard = Controller()
#input("Ready?")
#app = pygetwindow.getWindowsWithTitle("SuperTuxKart")
#app[0].activate()

# app = pwc.getWindowsWithTitle('SuperTuxKart')

# if app:
#     # 2. Pick the first window found
#     app[0].activate()
    
# else:
# 	print("app not found.")
# 	exit(1)
	

# Instance the state object
car = CarController()

# run the CAN handler in a separate thread
can_thread = Thread(target=CANThread, args=(car,))
can_thread.daemon = True
can_thread.start()
 
# Now poll for keys
while True:
	time.sleep(1 / 20)
	state=car.AsDictionary()
	if state["throttle"]:
		keyboard.press(Key.up)
	else:
		keyboard.release(Key.up)
	if state["brake"]:
		keyboard.press(Key.down)
	else:
		keyboard.release(Key.down)		
	if state["steering"] == -1:
		keyboard.press(Key.left)
	else:
		keyboard.release(Key.left)
	if state["steering"] == 1:
		keyboard.press(Key.right)
	else:
		keyboard.release(Key.right)
	
	#print(f"throttle: [{state["throttle"]}] | brake: [{state["brake"]}] | steering: [{state["steering"]}]")
	# make the same print above but without f statement
	print("throttle: [{}] | brake: [{}] | steering: [{}]".format(state["throttle"], state["brake"], state["steering"]))
	


