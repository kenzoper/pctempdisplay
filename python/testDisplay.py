import serial
import time

ser = serial.Serial('COM7', 9600)  

MIN_TEMP=0
MAX_TEMP=120

if __name__ == "__main__":

    counter = MIN_TEMP;

    try:
        while True:
            buffer = bytearray()
            buffer.append(counter)
            buffer.append(0x80 | MAX_TEMP-counter)
            ser.write(buffer)
            time.sleep(0.25)


            counter = counter + 1
            if counter > MAX_TEMP:
                counter = MIN_TEMP
    
    except KeyboardInterrupt:
        print("Ctrl-C was pressed. Closing port cleanly...")    
        ser.close()







