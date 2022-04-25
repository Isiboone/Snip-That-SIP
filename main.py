# Isis Boone AI contest, AI Processing pictures and turning into code
# Isiboone@uat.edu Last Tested: March 25th 2022 11:37PM
# This is the librarys for the CV processings and making the GUI and VOICE
import os.path
from tkinter import *
import pyautogui
import datetime
import cv2
import pytesseract
from cv_processing import CV_Processing
import pyttsx3

# This is the Text to speech for the AI and how she will speak to people
converter = pyttsx3.init()
speaking_rate = 200
converter.setProperty('rate', speaking_rate)
converter.setProperty('volume', .6)
voice = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
converter.setProperty('voice', voice)


# This is for the introduction to speak what it is saying to you.
def texttospeech(text):
    print(text)
    converter.say(text)
    converter.runAndWait()


def introduction():
    texttospeech("Hello, this is SNIP THAT!")
    texttospeech("This application will help you snip code and copying it down for you to remember!")
    texttospeech("You will try this now! Good luck and have fun! ")


# this is making the snipping tool GUI and making it where you can take a picture of anything to get the text
class Application():
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        # root.configure(background = 'red')
        # root.attributes("-transparentcolor","red")

        root.attributes("-transparent", "blue")
        root.geometry('400x500')  # set new geometry
        root.title('~~~SNIP THAT~~~')
        self.menu_frame = Frame(master, bg="blue")
        self.menu_frame.pack(fill=BOTH, expand=YES)

        self.buttonBar = Frame(self.menu_frame, bg="")
        self.buttonBar.pack(fill=BOTH, expand=YES)

        self.snipButton = Button(self.buttonBar, width=3, command=self.createScreenCanvas, background="purple")
        self.snipButton.pack(expand=YES)

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "white")
        self.picture_frame = Frame(self.master_screen, background="pink")
        self.picture_frame.pack(fill=BOTH, expand=YES)

    # This is making the Ocr image and processing what it is seeing on the image
    def ocr_image(self, image_path: str):
        img = cv2.imread(image_path)

        # processing
        gray = CV_Processing.unsharp_mask(img)
        # denoise = CV_Processing.remove_noise(gray)
        # thresh = CV_Processing.thresholding(gray)
        # opening = CV_Processing.opening(thresh)
        # canny = CV_Processing.canny(opening)

        processed_image = gray
        abs_path = os.path.abspath(image_path)
        cv2.imwrite(abs_path, processed_image)
        # Adding custom options
        # custom_config = r'--oem 3 --psm 6'
        custom_config = r'-l eng'

        output_text = pytesseract.image_to_string(processed_image, config=custom_config)
        print(output_text)

    # This is taking the screenshots and saving them into your folder for safe keeping
    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        screenshot = pyautogui.screenshot(region=(x1, y1, x2, y2))
        time_now = datetime.datetime.now()
        formatted_time = time_now.strftime("%f")
        filename = "snips/" + formatted_time + ".png"
        screenshot.save(filename)
        self.ocr_image(filename)

    # This is creating the GUI for the snipping tool and making sure you can use the UI
    def createScreenCanvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    # This is programming the button that is taking the screenshot
    def on_button_release(self, event):
        self.recPosition()

        if self.start_x <= self.curX and self.start_y <= self.curY:
            # print("right down")
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            # print("left down")
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            # print("right up")
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            # print("left up")
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.exitScreenshotMode()
        return event

    # This is the exiting screenshot mode
    def exitScreenshotMode(self):
        print("Screenshot mode exited")
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    # This is for exiting the application
    def exit_application(self):
        print("Application exit")
        root.quit()

    # This is the on button and when you drag the screenshot to the dimensions
    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=3, fill="blue")

    # This is expanding the rectangle for the screenshot
    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    # This is the position of the screenshot.
    def recPosition(self):
        print(self.start_x)
        print(self.start_y)
        print(self.curX)
        print(self.curY)

    # This is to run the whole application


if __name__ == '__main__':
    introduction()
    root = Tk()
    app = Application(root)
    root.mainloop()
