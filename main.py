'''
#TODO - Error handling
#TODO - Replace CV live commands with Voice commands instead 
References:
https://www.thepythoncode.com/article/control-keyboard-python
Color Detection Component
https://github.com/nrsyed/computer-vision/blob/master/get_video_pixel/get_video_pixel.py
https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
Audio Input Component:
https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
Audio Output Component:
https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/
'''
# Import libraries for visual recognition, audio input and output, timing commands and math functions
import cv2
import time
import math
import speech_recognition as sr
import pyttsx3

#create a function to take in verbal audio from the user and convert it to text
def audio_input():
    # use a try statement to test a possible solution and if not functioning, let the user know that their input is invalid. 
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak...")
            r.adjust_for_ambient_noise(source)
            my_audio = r.listen(source) 
            text = r.recognize_google(my_audio)       
    except:
        error_message = "Sorry, please repeat what you said"
        audio_output(error_message)
        audio_input()
    # continue the function with the else component 
    else:
        return text

# Define a function that converts strings to audio output that the user can hear
def audio_output(phrase):
    engine = pyttsx3.init()
    engine.say(phrase)
    engine.runAndWait()

#define a function to obtain the color detection from a camera  
def video_detection(list_colors, list_burnt):
    #creating an object for webcam display
    video_captured = cv2.VideoCapture(0)

    # Get the Center of the camera's display by getting half of the width and height
    WIDTH_WINDOW, HEIGHT_WINDOW = video_captured.get(3), video_captured.get(4)
    CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT = int(WIDTH_WINDOW // 2), int(HEIGHT_WINDOW // 2)

    # Test
    print(time.time())
    counter = 0
    # Attain current epoch time
    initial_time = time.time()

    # Start camera loop and display what the camera captures on a separate window
    while True:
        [frames_read, display] = video_captured.read()
        cv2.imshow('frame', display)

        # Keyboard key detection
        cv_live_command = cv2.waitKey(1) & 0xFF

        # Testing Purposes to determine where the colours are being detected

        # cv2.circle(display, (CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT), 1, (0, 255, 0), -1)
        # cv2.circle(display, (CENTER_SCREEN_WIDTH - 25, CENTER_SCREEN_HEIGHT - 25), 1, (0, 0, 255), -1)
        # cv2.circle(display, (CENTER_SCREEN_WIDTH + 25, CENTER_SCREEN_HEIGHT + 25), 1, (0, 0, 255), -1)
        # cv2.circle(display, (CENTER_SCREEN_WIDTH - 25, CENTER_SCREEN_HEIGHT + 25), 1, (0, 0, 255), -1)
        # cv2.circle(display, (CENTER_SCREEN_WIDTH + 25, CENTER_SCREEN_HEIGHT - 25), 1, (0, 0, 255), -1)
        # cv2.circle(display, (CENTER_SCREEN_WIDTH - 50, CENTER_SCREEN_HEIGHT - 50), 1, (0, 0, 255), -1)
        # cv2.circle(display, (CENTER_SCREEN_WIDTH + 50, CENTER_SCREEN_HEIGHT + 50), 1, (0, 0, 255), -1)
        # cv2.circle(display, (CENTER_SCREEN_WIDTH - 50, CENTER_SCREEN_HEIGHT + 50), 1, (0, 0, 255), -1)
        # cv2.circle(display, (CENTER_SCREEN_WIDTH + 50, CENTER_SCREEN_HEIGHT - 50), 1, (0, 0, 255), -1)

        # Check if the user hits the space bar or terminate automatically after 25 minutes of program execution
        if cv_live_command == ord(' ') or time.time() - initial_time > 1500:
            break
        # Otherwise, execute the following code every 10 seconds
        elif math.floor(time.time()-initial_time) == counter + 10:

            # Take a snapshot of what the webcam is detected
            red_avg, green_avg, blue_avg = 0, 0, 0
            captured_image = display.copy()  
            cv2.imshow('Snapshot', captured_image)  

            # Attain the colours of 5 different central pixels on the snapshot image   
            list_detected_colours = [captured_image[CENTER_SCREEN_HEIGHT, CENTER_SCREEN_WIDTH, [2, 1, 0]],
                                    captured_image[CENTER_SCREEN_HEIGHT - 25, CENTER_SCREEN_WIDTH - 25, [2, 1, 0]],
                                    captured_image[CENTER_SCREEN_HEIGHT + 25, CENTER_SCREEN_WIDTH + 25, [2, 1, 0]],
                                    captured_image[CENTER_SCREEN_HEIGHT - 25, CENTER_SCREEN_WIDTH + 25, [2, 1, 0]],
                                    captured_image[CENTER_SCREEN_HEIGHT + 25, CENTER_SCREEN_WIDTH - 25, [2, 1, 0]]]

            # Attain the average RGB values of the 5 central pixels of the image         
            for color in list_detected_colours:
                red_avg = red_avg + color[0]
                green_avg = green_avg + color[1]
                blue_avg = blue_avg + color[2]

            red_avg = int(red_avg // 5)
            green_avg = int(green_avg // 5)
            blue_avg = int(blue_avg // 5)

            final_color_det = [red_avg, green_avg, blue_avg]
            counter = counter + 10
            print(final_color_det)

            # Check if the detected RGB values are below the threshold determined for a burnt food item
            if final_color_det[0] < list_burnt[0] and final_color_det[1] < list_burnt[1] and final_color_det[2] < list_burnt[2]:
                # Inform the user through audio that the food is burning
                food_burnt = "Careful. The food is burning."
                audio_output(food_burnt) 
            # Otherwise, check if the detected RGB values are above the threshold determined for cooked food items
            elif final_color_det[0] < list_colors[0] and final_color_det[1] < list_colors[1] and final_color_det[2] < list_colors[2]:
                # Inform the user through audio that the food is cooked
                food_ready = "The food is all done"
                audio_output(food_ready) 

    # Terminate the video capturing windows
    video_captured.release()
    cv2.destroyAllWindows()

# Program flow
def main():
    # Default 640x480
    # video_captured.set(3, 1920) # horiz
    # video_captured.set(4, 1080) # vert
    # blue, white / grey, pink

    # Food RGB data
    phrase_introduction = "Hello. Please say the food you would like to cook or say exit to leave."
    audio_output(phrase_introduction)
    food_list = ['grilled cheese']
    food_cooked = [[180, 100, 100]]
    food_burnt = [[50, 50, 50]]
    terminate = False

    # Keep asking for the food that the user would like to cook through audio until he answers
    while True:
        choice = audio_input()
        print(choice)
        if choice in food_list:
            food_item = food_list.index(choice)
            break
        # Terminate the program if the user chooses to exit
        elif choice == 'exit':
            terminate = True
            break
        else:
            audio_output("Please select an item from the list or say exit to leave")

    # If the gave acceptable input (food in the database), inform the user they can start cooking
    # Commence video detection sequence
    if terminate == False:
        start_cook = "You can begin cooking. Press space bar if you would like to stop cooking."
        audio_output(start_cook)
        video_detection(food_cooked[food_item], food_burnt[food_item])
        end_cook = "Enjoy your meal"
        audio_output(end_cook)
    # Otherwise, the user has chosen to exit
    else:
        end_program = "Have a good day"
        audio_output(end_program)
main()

