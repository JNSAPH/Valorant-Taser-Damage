import cv2
import pytesseract
import pyautogui
import serial
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Define the serial port and baud rate
serial_port = 'COM4'  # Change this to the appropriate COM port
baud_rate = 9600

# Initialize serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Tesseract Config
custom_config = r'--oem 3 --psm 6'

# Specify the region to capture (left, top, width, height)
region = (572, 1000, 80, 50)

def main():
    global last_health
    global is_dead
    is_dead = False
    last_health = 100

    # take a screenshot every 1 second
    while True:
        # Take a screenshot of the specified region
        screenshot = pyautogui.screenshot(region=region)

        # Save the screenshot to a file
        screenshot.save("screenshot.png")

        # Read the image
        image = cv2.imread("screenshot.png")

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to enhance text
        _, thresh = cv2.threshold(gray, 0, 120, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # save the thresholded image
        cv2.imwrite("thresh.png", thresh)

        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(thresh, config=custom_config)

        # Print the text and its datatype
        text = text.strip()  # Remove leading/trailing whitespace, including newlines

        # Convert text to integer if it's not empty
        if text and text.isdigit():
            is_dead = False
            if int(text) < last_health and int(text) <= 100:
                #print("Health decreased from {} to {}".format(last_health, text))
                last_health = int(text)
                send_command('0')
                time.sleep(0.5)
                send_command('1')
            else:
                #print("Health increased from {} to {}".format(last_health, text))
                last_health = int(text)

        
        if text == "" and not is_dead:
            print("Dead")
            #send_command('0')
            #time.sleep(0.5)
            ##send_command('1')
            is_dead = True




        # Wait for 1 second
        time.sleep(0.5)

def send_command(command):
    ser.write(command.encode())  # Send command to ESP32

if __name__ == "__main__":
    main()
