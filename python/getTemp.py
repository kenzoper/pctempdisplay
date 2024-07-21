import wmi
import serial
import time

ser = serial.Serial('COM3', 9600)  

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

def send_temp(sensor, temp):
    value_to_send = 8 * [0]

    if sensor == 'CPU':
        value_to_send[0] = 1
    if sensor == 'GPU':
        value_to_send[0] = 0



if __name__ == "__main__":

    try:
        while True: 
            gpu_temp = get_gpu_temp()
            cpu_temp = get_cpu_temp()

            print(f"GPU Temperature: {gpu_temp} °C")
            print(f"CPU Temperature: {cpu_temp} °C")

            # send_temp('CPU',int(cpu_temp))
            ser.write(f"C {cpu_temp}\n".encode())
            time.sleep(0.05)
            ser.write(f"G {gpu_temp}\n".encode())
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("Ctrl-C was pressed. Closing port cleanly...")    
        ser.close()







