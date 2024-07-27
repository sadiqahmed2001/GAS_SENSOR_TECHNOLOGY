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

import RPi.GPIO as GPIO
import time

# Set up GPIO mode and warnings
GPIO.setmode(GPIO.BCM)  # Use Broadcom (BCM) GPIO numbering
GPIO.setwarnings(False)  # Disable GPIO warnings

# Set up GPIO pins
GPIO.setup(14, GPIO.IN)  # Set GPIO pin 14 as an input (for button)
GPIO.setup(12, GPIO.OUT)  # Set GPIO pin 12 as an output (for LED)
GPIO.setup(12, False)    # Initialize GPIO pin 12 to LOW (turn off LED)

while True:
    button_state = GPIO.input(14)  # Read the state of GPIO pin 14 (button)
    if button_state == False:  # If button is pressed (button_state is LOW)
        GPIO.output(12, True)  # Turn on the LED (set GPIO pin 12 HIGH)
        # Wait until the button is released
        while GPIO.input(14) == False:
            time.sleep(0.2)  # Sleep for 200 milliseconds
    else:
        GPIO.output(12, False)  # Turn off the LED (set GPIO pin 12 LOW)
Explanation:
Import Libraries:


import RPi.GPIO as GPIO
import time
RPi.GPIO: Provides an interface to control the GPIO pins on the Raspberry Pi.
time: Used for adding delays in the code.
GPIO Setup:


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM): Sets the GPIO pin numbering mode to Broadcom (BCM). BCM mode uses the pin numbers based on the Broadcom SOC channel numbers.
GPIO.setwarnings(False): Disables GPIO warnings that can occur when GPIO pins are used.
Pin Configuration:


GPIO.setup(14, GPIO.IN)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(12, False)
GPIO.setup(14, GPIO.IN): Configures GPIO pin 14 as an input, which is typically connected to a button.
GPIO.setup(12, GPIO.OUT): Configures GPIO pin 12 as an output, which is connected to an LED.
GPIO.setup(12, False): Initializes GPIO pin 12 to LOW (False), which means the LED is turned off initially.
Main Loop:


while True:
    button_state = GPIO.input(14)
    if button_state == False:
        GPIO.output(12, True)
        while GPIO.input(14) == False:
            time.sleep(0.2)
    else:
        GPIO.output(12, False)
while True:: Creates an infinite loop that continuously checks the button state.
button_state = GPIO.input(14): Reads the state of the button connected to GPIO pin 14. If the button is pressed, GPIO.input(14) returns False (LOW); if not pressed, it returns True (HIGH).
if button_state == False:: Checks if the button is pressed.
GPIO.output(12, True): Turns on the LED connected to GPIO pin 12.
while GPIO.input(14) == False:: Enters another loop that keeps the LED on while the button is pressed. The time.sleep(0.2) adds a short delay to avoid rapidly toggling the LED due to button bouncing.
else:: If the button is not pressed.
GPIO.output(12, False): Turns off the LED.
Summary:
The code continuously monitors the state of a button connected to GPIO pin 14. When the button is pressed, it turns on an LED connected to GPIO pin 12. The LED stays on while the button remains pressed and turns off when the button is released. This is achieved using a loop to check the button state and controlling the LED accordingly.
