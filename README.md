Hardware Required:
Raspberry Pi (any model with GPIO pins)
MQ-2 Gas Sensor
Breadboard and jumper wires
(Optional) Analog-to-Digital Converter (ADC) like MCP3008, as the MQ-2 outputs analog signals and the Raspberry Pi GPIO pins only read digital signals.
Wiring:
MQ-2 Sensor to MCP3008 ADC:

MQ-2 VCC to MCP3008 VDD (3.3V)
MQ-2 GND to MCP3008 GND
MQ-2 AO (Analog Output) to MCP3008 CH0 (Channel 0)
MCP3008 ADC to Raspberry Pi:

MCP3008 VDD to Raspberry Pi 3.3V
MCP3008 GND to Raspberry Pi GND
MCP3008 CLK to Raspberry Pi GPIO11 (SCLK)
MCP3008 DOUT to Raspberry Pi GPIO9 (MISO)
MCP3008 DIN to Raspberry Pi GPIO10 (MOSI)
MCP3008 CS/SHDN to Raspberry Pi GPIO8 (CE0)
Python Code:
You'll need the spidev library for SPI communication and the time library for delay.

Install the spidev library:


sudo apt-get update
sudo apt-get install python3-spidev
Python Script to Read Gas Sensor Data:


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
Explanation:
spidev.SpiDev() initializes the SPI device.
spi.open(0, 0) opens SPI bus 0 and device 0 (CE0).
spi.max_speed_hz sets the SPI communication speed.
read_adc(channel) function reads the ADC value from the specified channel.
The loop continuously reads the sensor value every second and prints it.
