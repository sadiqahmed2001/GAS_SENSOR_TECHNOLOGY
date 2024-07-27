import Rpi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.IN)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(12,False)
while True:
    button_state=GPIO.input(12)
    if button_state==False:
        GPIO.output(12,True)
        while GPIO.input(14)== False:
            time.sleep(0.2)
    else:
        GPIO.output(12,False)



import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CS) 0
spi.max_speed_hz = 1350000

# Function to read ADC value from a specific channel
def read_adc(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")
    # Start with a byte of 1, followed by 7 bits of channel number, then 1 more bit
    # in a 3-byte frame.
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    # The ADC value is in the last 10 bits of the response
    adc_value = ((r[1] & 3) << 8) + r[2]
    return adc_value

try:
    while True:
        # Read from channel 0
        gas_value = read_adc(0)
        print(f"Gas Sensor Value: {gas_value}")
        time.sleep(1)  # Read every second
except KeyboardInterrupt:
    print("Program terminated")
finally:
    spi.close()
