import can

def main():
    # Tente adicionar o bitrate (ex: 500k) além do baudrate da porta
    try:
        with can.interface.Bus(interface='slcan', 
                               channel='/dev/cu.usbserial-5B060119651', 
                               tty_baudrate=115200, 
                               bitrate=500000) as bus:
            for msg in bus:
                #)
                if msg.arbitration_id == 0x07e:
                    #print(f"steering data: [{msg.data}]")
                    steer = msg.data[0]
                    print(f"steer: [{steer:02x}]")
                    if steer >= 0x7D:
                        print("STEERING LEFT")
                    elif steer <= 0x7A:
                        print("STEERING RIGHT")
                    else:
                        print("STEERING CENTER")
                # if msg.arbitration_id == 0x165:
                #     print(f"brake data: [{msg.data}]")
                #     brake = msg.data[0]
                #     print(f"brake: [{brake:02x}]")
                #     print(f"BRAKE {'ON' if brake == 0x20 else 'OFF'}")
                if msg.arbitration_id == 0x167:
                    print(f"throttle data [{msg.data}]")
                    throttle = msg.data[5]
                    print(f"throttle: [{throttle:02x}]")
                    print(f"THROTTLE {'ON' if throttle == 0x1a else 'OFF'}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()