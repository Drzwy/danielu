import serial
import time

# Configura el puerto serie (ajusta el puerto según tu configuración)
puerto_serie = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

try:
    while True:
        # Lee una línea de datos desde el puerto serie
        linea = puerto_serie.readline().decode('utf-8').strip()
        
        # Convierte la línea a un número entero (si es un número válido)
        try:
            valor_sensor = int(linea)
            print(f'Valor del sensor: {valor_sensor}')
        except ValueError:
            print('Error al convertir el valor a entero.')

        # Espera un segundo (ajusta según sea necesario)
        time.sleep(1)

except KeyboardInterrupt:
    print('Programa detenido manualmente.')

finally:
    # Cierra el puerto serie al salir
    puerto_serie.close()