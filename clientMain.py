import pickle
import socket
import time
import openai
import pygame
import pygame_gui
import pyaudio
import wave
import queue
import threading
import re
from clientKeys import OPENAI_API_KEY, ELEVEN_API_KEY, USE_TTS, SYNC_PORT, PUSH_ASYNC_PORT, GET_ASYNC_PORT
import win32com.client as wincl
from elevenlabs import generate, play
from elevenlabs import set_api_key
set_api_key(ELEVEN_API_KEY)


openai.api_key = OPENAI_API_KEY

messages = []

outputLinkText = ""
outputTextConversation = ""

iteration = 0

background_image = None
running = True

updateUI = False
sendTextIsAllowed = False


audio_frames = []
is_recording = False




# Initialize queues for threads
syncQueue = queue.Queue()
pushQueue = queue.Queue()

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen_width = 1152
screen_height = 768
window_size = (screen_width, screen_height)
image_size = (384,768)
screen = pygame.display.set_mode(window_size)

# Initialize the pygame_gui UIManager
UI_MANAGER = pygame_gui.UIManager(window_size, 'themes/themes.json')

# Initialize the sockets
syncSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pushAsyncSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
getAsyncSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#TODO IMPORT HOST AND PORTS

# Sync Socket
sync_host = ''
sync_port = SYNC_PORT

# Async Socket
push_async_host = ''
push_async_port = PUSH_ASYNC_PORT

# Picture Socket
get_async_host = ''
get_async_port = GET_ASYNC_PORT


#Enter pressed feedback sound
feedbackSound = pygame.mixer.Sound('sounds/Click.mp3')

# Set the title of the window
pygame.display.set_caption("User_LivePrototyping")

# Setup Background 
background = pygame.Surface(window_size)
background.fill(UI_MANAGER.ui_theme.get_colour('dark_bg'))

# Set up the game clock
CLOCK = pygame.time.Clock()

# create a TTS engine using Windows 10 integrated TTS
tts_engine = wincl.Dispatch("SAPI.SpVoice")
for voice in tts_engine.GetVoices():
    if voice.GetDescription().startswith('Microsoft Zira'):
        tts_engine.Voice = voice
        break
tts_engine.Rate = 0
tts_engine.Volume = 100

# Set up audio recording parameters
chunk = 1024
format = pyaudio.paInt16
channels = 1
rate = 44100
filename = 'sounds/output.wav'

#-------------------------------------FUNCTIONS--------------------------------------------------------
def extract_text(input_string):
    # Find all matches of the pattern
    matches = re.findall(r'label=\"findme\">(.*?)</a>', input_string)


    # If there are matches, return the last one
    if matches:
        return matches[-1]

    # Otherwise, return None to indicate there were no matches
    return None

# TTS Windows:
def tts_thread(output):
    if(USE_TTS):
        audio = generate(
            text=output,
            voice="Bella",
            model="eleven_multilingual_v1"
        )
        play(audio)
    else:
        tts_engine.Speak(output)


def stablediff_thread(iteration):
    #call function to create image
    print("Image is loading...")
    loadImage("output_"+str(iteration))

# Load an image:
def loadImage(image_data):
    image_path = f'images/output_{iteration}.png'

    with open(image_path, 'wb') as file:
        file.write(image_data)
        
    print(f'Image received and saved as {image_path}')

    global background_image
    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, image_size)
    print("Image is loaded")
    #pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)
    screen.blit(background_image, (0, 0))
    pygame.display.update()

def loadExampleImage():
    global background_image
    image_path = f'images/black.png'

    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, image_size)
    print("Image is loaded")
    screen.blit(background_image, (0, 0))
    pygame.display.update()
    

def recordAudio():
        global audio_frames, is_recording
        audio_frames = []
        p = pyaudio.PyAudio()

        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        while is_recording:
            data = stream.read(chunk)
            audio_frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

def saveAudioToFile():
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(audio_frames))
    wf.close()

def sendToWhisper(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript 
    except Exception as e:
        print(f"WISPER ERROR: {str(e)}.\nRetrying after 5 seconds...")
        time.sleep(5)
        return sendToWhisper(audio_file)

#---------------------SOCKET THREADS----------------------------------

def syncSocket_thread():
    global running 
    global sendTextIsAllowed
    global syncSocket
    global outputTextConversation
    global updateUI

    syncSocket.listen(1)
    print(f'Server listening on {sync_host}:{sync_port}...')
    prototyper_socket, address = syncSocket.accept()
    print(f'Connected to client: {address[0]}:{address[1]}')

    while running:
        try:
            messageFromPrototyper = prototyper_socket.recv(50000).decode()  # Receive the message from the client

            if(messageFromPrototyper == "restart"):
                print("Loading example picture")
                loadExampleImage()
                time.sleep(2)
                answer = "ok"
                prototyper_socket.send(answer.encode())
                continue

            print(f"The message from the prototyper is: {messageFromPrototyper}")

            outputTextConversation = messageFromPrototyper
            #Write into Textbox_Output
            updateUI = True

            if(messageFromPrototyper != ''):
                sendTextIsAllowed = True

            #TODO Voice output
            lastSentence = extract_text(messageFromPrototyper)
            if lastSentence != None:
                print(f"Last AI sentence was {lastSentence}")

                ttsThread = threading.Thread(target=tts_thread, args=(lastSentence,))
                ttsThread.start()

            # wait for user input from syncQueue
            response = syncQueue.get()
            if response is None:
                break

            print(f'Processing (sync) queue element.')
            syncQueue.task_done()

            prototyper_socket.send(response.encode())
      
        except Exception as e:
            print(f'Socket error: {str(e)}') 
            prototyper_socket.close()
            time.sleep(2)
            prototyper_socket, address = syncSocket.accept()
            print(f'Connected to client: {address[0]}:{address[1]}')

def pushAsyncSocket_thread():
    global running
    global pushAsyncSocket
    global outputTextConversation
    global updateUI
    
    pushAsyncSocket.listen(1)
    print(f'Server listening on {push_async_host}:{push_async_port}...')
    prototyper_socket, address = pushAsyncSocket.accept()
    print(f'Connected to client: {address[0]}:{address[1]}')

    while running:
        try:
            htmlConversationFromPrototyper = prototyper_socket.recv(50000).decode()  # Receive the message from the client

            if(htmlConversationFromPrototyper != "ready"):
                updateUI = True
                outputTextConversation = htmlConversationFromPrototyper
            
            # wait for user input from pushQueue
            asyncEventFromUser = pushQueue.get()
            if asyncEventFromUser is None:
                break

            print(f'Processing (push_async) queue element: {asyncEventFromUser}')
            pushQueue.task_done()

            prototyper_socket.send(asyncEventFromUser.encode())
      
        except Exception as e:
            print(f'Socket error: {str(e)}') 
            prototyper_socket.close()
            time.sleep(2)
            prototyper_socket, address = pushAsyncSocket.accept()
            print(f'Connected to client: {address[0]}:{address[1]}')

def getAsyncSocket_thread():
    global running
    global getAsyncSocket
    global outputTextConversation
    global updateUI

    getAsyncSocket.listen(1)
    print(f'Server listening on {get_async_host}:{get_async_port}...')
    prototyper_socket, address = getAsyncSocket.accept()
    print(f'Connected to client: {address[0]}:{address[1]}')

    while running:
        try:
            bytesSize = int.from_bytes(prototyper_socket.recv(4), byteorder='big')
            raw_data = b''
            while len(raw_data) < bytesSize:
                part = prototyper_socket.recv(1024)
                if not part:
                  break
                raw_data += part

            instructionFromPrototyper = pickle.loads(raw_data)
            print(f"Instruction from Prototyper is: {str(instructionFromPrototyper)}")
            
            if(isinstance(instructionFromPrototyper, dict) and instructionFromPrototyper != None):
                if instructionFromPrototyper["label"] == "image":
                    # change image
                    print("Prototyper instructed to change the image")
                    loadImage(instructionFromPrototyper["content"])

                elif instructionFromPrototyper["label"] == "conversation":
                    print("Prototyper instructed to change the conversation text")
                    # change conversation:
                    outputTextConversation = instructionFromPrototyper["content"]
                    # Write into Textbox_Output
                    updateUI = True
                elif instructionFromPrototyper["label"] == "test":
                    print("Prototyper send the test case")
                else: 
                    print("Label of Instruction unclear")

            response = "instruction received"
            prototyper_socket.send(response.encode())
      
        except Exception as e:
            print(f'Get async socket error: {str(e)}') 
            prototyper_socket.close()
            time.sleep(2)
            prototyper_socket, address = getAsyncSocket.accept()
            print(f'Connected to client: {address[0]}:{address[1]}')

#---------------------------UI------------------------------

# Create a "Record" button
button_size = (80, 80)

TEXT_INPUT_HEIGHT = 50
TEXT_INPUT_WIDTH = (screen_width / 3)*2

TEXT_INPUT_X = (screen_width) / 3
TEXT_INPUT_Y = (screen_height - button_size[1]) - 20-TEXT_INPUT_HEIGHT
button_x = (TEXT_INPUT_X + (TEXT_INPUT_WIDTH/2) - (button_size[0]/2))
button_y = (screen_height - button_size[1]) - 10
TEXT_OUTPUT_Y = -10 

TEXT_OUTPUT_HEIGHT = TEXT_INPUT_Y - TEXT_OUTPUT_Y

PANEL_HEIGHT = screen_height
PANEL_WIDTH = TEXT_INPUT_X

PANEL_X = 0
PANEL_Y = TEXT_OUTPUT_Y

# Create a Textfield
TEXT_OUTPUT = pygame_gui.elements.UITextBox("",
                                            relative_rect=pygame.Rect((TEXT_INPUT_X, TEXT_OUTPUT_Y+10), 
                                                                        (TEXT_INPUT_WIDTH, TEXT_OUTPUT_HEIGHT)),
                                                manager=UI_MANAGER, 
                                                object_id='#text_output')

# Create a Textfield
TEXT_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((TEXT_INPUT_X, TEXT_INPUT_Y+5),
                                                                            (TEXT_INPUT_WIDTH, TEXT_INPUT_HEIGHT)),
                                                                            manager=UI_MANAGER, object_id='#text_entry')



BUTTON_RECORD = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((button_x, button_y), button_size),
                                            text="",
                                            object_id='#record_button',
                                            manager=UI_MANAGER)

## Define the color of the line (in RGB format)
#line_color = (255, 255, 255)  # White color
#
## Define the start and end points of the line
#start_pos = (TEXT_INPUT_X, 0)
#end_pos = (TEXT_INPUT_X, screen_height)
#
## Define the width of the line
#line_width = 1
#
## Draw the line
#pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)

pygame.display.flip()


#--------------------------SOCKETS-------------------------------

# Binding sync socket
syncSocket.bind((sync_host, sync_port))

syncThread = threading.Thread(target=syncSocket_thread)
syncThread.start()

# Binding pushAsyncSocket socket
pushAsyncSocket.bind((push_async_host, push_async_port))

pushAsyncThread = threading.Thread(target=pushAsyncSocket_thread)
pushAsyncThread.start()

# Binding getAsyncSocket socket
getAsyncSocket.bind((get_async_host, get_async_port))

getAsyncThread = threading.Thread(target=getAsyncSocket_thread)
getAsyncThread.start()


#---------------------------WHILE-------------------------------------
screen.blit(background, (0, 0))
#pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)

while running:
    UI_REFRESH_RATE = CLOCK.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Sending Text (sync)
        if(sendTextIsAllowed):
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#text_entry' and event.text):

                if event.text == "":
                    print("Empty input is skipped")
                else:
                    print("Answer is triggerd")

                    outputText = event.text

                    feedbackSound.play()
                    TEXT_INPUT.set_text("")
                    TEXT_INPUT.redraw()

                    userInput = "\n<font color=\"#FF0000\">YOU:</font>" +" "+ "<font color=\"#ffeeee\">" + "<a href=\"pL\">"+ outputText +"</a></font>"
                    
                    outputTextConversation += userInput
                    updateUI = True
                    #TEXT_OUTPUT.set_text(outputTextConversation) #Write into Textbox_Output

                    UI_MANAGER.draw_ui(screen) 
                    pygame.display.update()

                    if event.text == "stop":
                        running = False
                        break
                    
                    # Put conversation text to syncThread
                    syncQueue.put(outputText)

                    # Disable sending
                    sendTextIsAllowed = False

        #TODO how disabled text entry else:
            #Grey out UI element

        # Record Button
        if ((event.type == pygame_gui.UI_BUTTON_PRESSED and
            event.ui_object_id == '#record_button')):

            # Button pressed, perform the desired action
            if not is_recording:
                #BUTTON_RECORD.set_text("STOP")
                BUTTON_RECORD.select()
                is_recording = True
                recording_thread = threading.Thread(target=recordAudio)
                recording_thread.start()
            else:
                #BUTTON_RECORD.set_text("Record")
                is_recording = False
                recording_thread.join()
                saveAudioToFile()

                duration = 0
                with wave.open("sounds/output.wav") as currentA:
                    duration = currentA.getnframes() / currentA.getframerate()
                
                #send file to whisper
                audio_file = open("sounds/output.wav", "rb")
                if  duration > 1:
                    
                    transcript = sendToWhisper(audio_file)

                    if(transcript != None):
                        TEXT_INPUT.set_text(transcript.text)
                        TEXT_INPUT.focus()
                        print(transcript.text)
                else:
                    print("Audio duration under limit")
            
        # Click Text (push_async)
        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            if event.ui_element is TEXT_OUTPUT:

                linkText = event.link_target
                
                pushQueue.put(linkText)

                #External Window
                #notepad_window = UIWindow(pygame.Rect(50, 20, 300, 400), window_display_title="English translation:")
                #text_output_box = UITextBox(
                #    relative_rect=pygame.Rect((0, 0), notepad_window.get_container().get_size()),
                #    html_text="",
                #    container=notepad_window)
                #text_output_box.set_text(translation)
                

                #translation = str(translateWithDeepLAPI(linkText.replace('_', ' ')))
                #outputTextConversation += "\n\n\n<font color=\"#d77aff\">" + "Translation: "+translation+"</font>"
                #TEXT_OUTPUT.set_text(outputTextConversation) #Write into Textbox_Output

                #UI_MANAGER.draw_ui(screen)  # Draw the UI elements
                #pygame.display.update()  # Update the display

        UI_MANAGER.process_events(event)
    
    #Write into Textbox_Output
    if(updateUI):
        print(f"Output for TextBox: {outputTextConversation}")
        for i in range(6):
            TEXT_OUTPUT.set_text(outputTextConversation)
            UI_MANAGER.draw_ui(screen) 
            pygame.display.update()

        updateUI = False

    UI_MANAGER.update(UI_REFRESH_RATE)

    #if background_image is None:
    #    screen.blit(background, (0, 0))
    #    pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)
    #else:
    #    screen.blit(background_image, (0, 0))
    #    pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)

    UI_MANAGER.draw_ui(screen) 

    pygame.display.update()

# Wait for sockets to close
syncThread.join()
pushAsyncThread.join()
getAsyncThread.join()

syncSocket.close()
pushAsyncSocket.close()
getAsyncSocket.close()

# Quit Pygame
pygame.mixer.quit()
pygame.quit()