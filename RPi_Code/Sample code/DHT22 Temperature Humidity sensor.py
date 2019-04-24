# DHT22 or 11 Link: https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

print(humidity, temperature)
