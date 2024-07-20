import wmi
import serial

##ser = serial.Serial('COM3', 9600)  

def get_gpu_temp():

    w = wmi.WMI(namespace="root\OpenHardwareMonitor")

    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
            if sensor.SensorType == u'Temperature' and 'GPU' in sensor.Name:
                return sensor.Value

def get_cpu_temp():

    w = wmi.WMI(namespace="root\OpenHardwareMonitor")

    temperature_infos = w.Sensor()
    for sensor in temperature_infos:
            if sensor.SensorType == u'Temperature' and 'CPU' in sensor.Name:
                return sensor.Value

def send_temp(sensor, temp):
    value_to_send = 8 * [0]

    if sensor == 'CPU':
        value_to_send[0] = 1
    if sensor == 'GPU':
        value_to_send[0] = 0



if __name__ == "__main__":
    gpu_temp = get_gpu_temp()
    cpu_temp = get_cpu_temp()

    print(f"GPU Temperature: {gpu_temp} °C")
    print(f"CPU Temperature: {cpu_temp} °C")

    send_temp('CPU',int(cpu_temp))

    ##ser.write(f"{value_to_send}\n".encode())  

    ##ser.close()







