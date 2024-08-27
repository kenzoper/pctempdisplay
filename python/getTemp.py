import wmi
import serial
import time

ser = serial.Serial('COM7', 9600)  

def get_gpu_temp() -> int:

    w = wmi.WMI(namespace="root\OpenHardwareMonitor")

    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
            if sensor.SensorType == u'Temperature' and 'GPU' in sensor.Name:
                return int(round(sensor.Value))

def get_cpu_temp() -> int:

    w = wmi.WMI(namespace="root\OpenHardwareMonitor")

    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
            if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
                return int(round(sensor.Value))

def clamp(temp):
    if temp > 127:
         temp = 127
    elif temp < 0:
         temp = 0
    return temp

def send_temps(cpu, gpu):
    cpu = clamp(cpu)
    gpu = clamp(gpu)
    buffer = bytearray()
    buffer.append(0x7F & cpu)
    buffer.append(0x80 | gpu)
    ser.write(buffer)

if __name__ == "__main__":

    try:
        while True: 
            gpu_temp = get_gpu_temp()
            cpu_temp = get_cpu_temp()

            print(f"CPU Temperature: {cpu_temp} °C")
            print(f"GPU Temperature: {gpu_temp} °C")

            send_temps(int(cpu_temp), int(gpu_temp))
            time.sleep(0.5)

            # ser.write(f"C {cpu_temp}\n".encode())
            # time.sleep(0.05)
            # ser.write(f"G {gpu_temp}\n".encode())
            # time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("Ctrl-C was pressed. Closing port cleanly...")    
        ser.close()







