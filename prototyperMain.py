import pygame
import pygame_gui
import openai
import pickle
import threading
import socket
import time
import prototypingElements
import prototypingUIElements
from prototyper_keys import OPENAI_API_KEY, USER_HOST, SYNC_PORT, PUSH_ASYNC_PORT, GET_ASYNC_PORT, PICTURE_HOST, PICTURE_PORT
sync_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
push_async_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
get_async_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

conversationGPT = []
conversationHTML = ""
conversationRAW = ""

openai.api_key = OPENAI_API_KEY

labelCounter = 0
stableIteration = 0

userHost = USER_HOST
syncPort = SYNC_PORT
pushAsyncPort = PUSH_ASYNC_PORT
getAsyncPort = GET_ASYNC_PORT

instructions = prototypingElements.instructions

visibleSubblock = None
visibleBlock = None

doRestart = False

#-------------------------------BRAIN--------------------------------
def askGPT(prompt):
    task = []
    task.append({"role": "user", "content": prompt})
    try:
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=task)
        output = response["choices"][0]["message"]["content"]
        
        print(f"ASKGPT REQUEST: {prompt} resulted in {output}")
        return output

    except openai.error.RateLimitError as e:
        # Retry the request after waiting for some time
        print(f"ASKGPT ERROR: {str(e)}.\nRetrying after 5 seconds...")
        time.sleep(5)
        return askGPT(prompt)
    
    except Exception as e:
        print(f"ASKGPT ERROR: {str(e)}")

def whileSubblocks(block):
    index = 0

    while index < len(block):
        subblockList = block.get_subblocks()
        subblock = subblockList[index]

        TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, subblock.get_name()))

        if type(subblock) is prototypingElements.Subblock_User_Input:
                print(f"This is a Subblock_User_Input: {subblock.get_name()}.")
                executeUserInput(subblock)
                print(subblock.get_output())

        if type(subblock) is prototypingElements.Subblock_Prototyper_Input:
                print(f"This is a Subblock_Prototyper_Input: {subblock.get_name()}.")
                executePrototyperInput(subblock)
                print(subblock.get_output())

        if type(subblock) is prototypingElements.Subblock_Combine:
                print(f"This is a Subblock_Combine: {subblock.get_name()}.")
                executeCombine(subblock)
                print(subblock.get_output())

        if type(subblock) is prototypingElements.Subblock_SendToGPT:
                print(f"This is a Subblock_SendToGPT: {subblock.get_name()}.")
                executeSendToGPT(subblock)
                print(subblock.get_output())

        if type(subblock) is prototypingElements.Subblock_Image:
                print(f"This is a Subblock_Image: {subblock.get_name()}.")
                executeImage(subblock)

        if type(subblock) is prototypingElements.Subblock_Output:
                print(f"This is a Subblock_Output: {subblock.get_name()}.")
                executeOutput(subblock)
    
        index += 1

def executeUserInput(subblock):
     # send input request text requestVarForUser to user
     # (this has to use the sync code to send the text request ?)
     # write received user input to output var
     subblock.set_output(sendAndReceive(subblock.get_requestVarForUser()))

def executePrototyperInput(subblock):
     # this is text only
     # text input by prototyper is set through GUI
     # we set the output as the text input of the prototyper
     subblock.set_output(subblock.get_prototyper_input())

def executeCombine(subblock):
    # here we receive a text consisting of subblock names, whose text we concatenate
    # split the '+' delimited inputs var
    # look up all names after splitting
    # use getSubblockOutput to take their output
    # concatenate the result in the output variable which makes them available
    subblock.set_output(combineInput(subblock.get_inputs()))

def executeSendToGPT(subblock):
     # we have the input from the UI
     # the input is always an output of another subblock (text), use getSubblockOutput to find it
     # use the input as the prompt parameter for the askGPT function call
     # the return value of the askGPT call gets written to the output of this subblock
     subblock.set_output(askGPT(combineInput(subblock.get_input())))

def executeImage(subblock):
     global stableIteration
     # we are provided with to variables here, positive and negative prompt
     # add positive and negative to the prompt:
     #  to do this call stableDifPayload in prompting.py with these values (must be extended to change negative)
     # call the stablePicture function with the global variable stableIteration and imagePrompt
     # load the image from file (stablePicture isn't finished until it is written to file anyways)
     # increment the stableIteration variable
     #stablePicture(stableIteration, prompting.stableDifpayload(subblock.get_input(), subblock.get_negativeInput()))
     pictureThread = threading.Thread(target=stablePicture, args=(stableIteration, combineInput(subblock.get_input())+"+"+combineInput(subblock.get_negativeInput()),))
     pictureThread.start()
     stableIteration += 1

def executeOutput(subblock):
     subblockInput = subblock.get_input()
     subblock.set_output(combineInput(subblockInput))

def combineInput(sublockInput):
    subblockNames = sublockInput.split('+')
    concatOuts = ""
    for name in subblockNames:
        concatOuts = concatOuts + " " + getSubblockOutput(name)
    return concatOuts
     
def getBlock(blockName):
    for block in instructions:
        if block.get_name() == blockName:
            return block
        
def getSubblock(subblockName):
    for block in instructions:
        for subblock in block:
            if subblock.get_name() == subblockName:
                return subblock

def getSubblockOutput(subblockName):
    # call getBlocks on instructions (list) -> call getSubblocks on blocks (list) -> call getOutput on subblock
    # return the value from getOutput for the one with matching name
    # the subblock we get is only a string with its name
    for block in instructions:
        for subblock in block:
            if subblock.get_name() == subblockName:
                return subblock.get_output()
    return subblockName


def deleteSubblock(subblockToDelete):
    index = 0
    for block in instructions:
        for subblock in block:
            if subblock == subblockToDelete:
                block.subblocks.pop(index)
            index += 1
        index = 0

def deleteBlock(blockToDelete):
    index = 0
    for block in instructions:
        if block == blockToDelete:
            instructions.blocks.pop(index)
        index += 1
    index = 0

def moveSubblockUp(subblockToMove):
    index = 0
    for block in instructions:
        for subblock in block:
            if subblock == subblockToMove:
                if(index != 0):
                    block.subblocks.insert(index-1,block.subblocks.pop(index))
                    return
            index += 1
        index = 0

def moveSubblockDown(subblockToMove):
    index = 0
    for block in instructions:
        for subblock in block:
            if subblock == subblockToMove:
                if(index != (len(block.subblocks)-1)):
                    block.subblocks.insert(index+1,block.subblocks.pop(index))
                    return
            index += 1
        index = 0

def moveBlockUp(blockToMove):
    index = 0
    for block in instructions:
        if block == blockToMove:
            if(index != 0):
                instructions.blocks.insert(index-1,instructions.blocks.pop(index))
                return
        index += 1
    index = 0

def moveBlockDown(blockToMove):
    index = 0
    for block in instructions:
        if block == blockToMove:
            if(index != (len(instructions.blocks)-1)):
                instructions.blocks.insert(index+1,instructions.blocks.pop(index))
                return
        index += 1
    index = 0



def disableContainers():
    global instructions

    for block in instructions:
        block.uiInstance.block_container.disable()
        block.uiInstance.block_container.hide()
        for subblock in block:
            subblock.uiInstance.subblock_container.disable()
            subblock.uiInstance.subblock_container.hide()

    AddButtonScreen.addButton_container.disable()
    AddButtonScreen.addButton_container.hide()


def sendAndReceive(toSend):
    try:
        # Send the message to the server / user
        sync_socket.send(toSend.encode())
        return sync_socket.recv(1024).decode()
    except Exception as e:
        print(f'{str(e)}')

def skipSubblock():
    #TODO skip subblock instruction
    pass


def loadFromFile():
    # Load instructions from file
    global instructions

    blocks = []
    with open('instructions.pkl', 'rb') as f:
        blocks = pickle.load(f)

    instructions.set_blocks(blocks)


def saveToFile():
    # Dump instructions to file
    global instructions

    blocks = instructions.get_blocks()
    with open('instructions.pkl', 'wb') as f:
        pickle.dump(blocks, f)
    
    
   
def gptHeaderChange(conversation, content):
    conversation[0] = {"role": "system", "content": content}
    return conversation

   
def gptAddUserInput(conversation, content):
    conversation.append({"role": "user", "content": content})
    return conversation


def createLoopBlock(nameForBlock):
    loop_block = prototypingElements.Loop(nameForBlock,UI_MANAGER,WINDOW_CONTAINER, window_container_size)

    conversationText = prototypingElements.Subblock_Output((nameForBlock+"_ConversationText"),UI_MANAGER,WINDOW_CONTAINER, window_container_size)
    conversationText.set_input("")

    lastAISentence = prototypingElements.Subblock_Output((nameForBlock+"_LastAISentence"),UI_MANAGER,WINDOW_CONTAINER, window_container_size)
    lastAISentence.set_input("")

    prototyper_input = prototypingElements.Subblock_Prototyper_Input((nameForBlock+"_prompt1"),UI_MANAGER,WINDOW_CONTAINER, window_container_size)
    prototyper_input.set_prototyper_input("Converse with me in english.")

    header = prototypingElements.Subblock_Output((nameForBlock+"_Header"),UI_MANAGER,WINDOW_CONTAINER, window_container_size)
    header.set_input(nameForBlock+"_prompt1")


    loop_block.add_subblock(conversationText)
    loop_block.add_subblock(lastAISentence)
    loop_block.add_subblock(prototyper_input)
    loop_block.add_subblock(header)

    return loop_block 

def createAsyncBlock(nameForBlock):

    async_block = prototypingElements.Async(nameForBlock, UI_MANAGER,WINDOW_CONTAINER, window_container_size)

    eventText = prototypingElements.Subblock_Output((nameForBlock+"_EventText"),UI_MANAGER,WINDOW_CONTAINER, window_container_size)
    eventText.set_input("")

    sentToUser = prototypingElements.Subblock_Output((nameForBlock+"_SendToUser"),UI_MANAGER,WINDOW_CONTAINER, window_container_size)
    sentToUser.set_input(nameForBlock+"_EventText")


    async_block.add_subblock(eventText)
    async_block.add_subblock(sentToUser)

    return async_block



#----------------THREADS----------------

def sync():
        
    global sync_socket
    global labelCounter
    global conversationGPT
    global instructions
    global doRestart
    global conversationHTML
    global conversationRAW


    # Executing Instructions:
    #print(f"Initial instructions: {instructions}")

    #GUI render hierachy by printing(hierachyHTML)

    while True:
        index = 0

        try:
            while index < len(instructions):
                instructionList = instructions.get_blocks()
                block = instructionList[index]

                if type(block) is prototypingElements.Static:
                    print("This is a Static block.")

                    whileSubblocks(block)

                elif type(block) is prototypingElements.Loop:
                    print("This is a Loop block.")

                    while not doRestart:
                        whileSubblocks(block)

                        
                        # Send the message to the server / user
                        print("AI TEXTBLOX ERREICHT")
                        if(conversationGPT == []):
                            prompt = getSubblockOutput("Header")
                            conversationGPT.append({"role": "system", "content": prompt})
                            conversationGPT.append({"role": "user", "content": ""})
                        else:
                            conversationGPT = gptHeaderChange(conversationGPT, getSubblockOutput("Header"))
                        
                        print(conversationGPT)

                        response = openai.ChatCompletion.create(
                                model="gpt-4",
                                # max_tokens= 30,
                                messages=conversationGPT)
                        
                        output = response["choices"][0]["message"]["content"]
                        conversationGPT.append({"role": "assistant", "content": output})
                        conversationRAW += (output + "\n")


                        # Set conversationText Input                            
                        for subblock in block:
                            if(subblock.get_name() == block.get_name()+"_ConversationText"):
                                subblock.set_input(conversationRAW)
                                print(f"conversationText input: {conversationRAW}")

                        #Set lastAISentence Input
                        for subblock in block:
                            if(subblock.get_name() == block.get_name()+"_LastAISentence"):
                                subblock.set_input(output)
                                print(f"lastAISentence input: {output}")


                        outputLabel = f"ai{labelCounter}"
                        #outputHTML = "\n<font color=\"#209de0\">AI:</font>"+ " "+ "<font color=\"#76b8db\">" + "<a href= \""+outputLabel+"\">"+ output +"</a></font>"
                        outputHTML = f"\n<font color=\"#209de0\">AI:</font> <font color=\"#76b8db\"><a href= \"{outputLabel}+{output}\" label=\"findme\">{output}</a></font>"
                        labelCounter += 1

                        conversationHTML += outputHTML
                        sync_socket.send(conversationHTML.encode())
                        clientInput = sync_socket.recv(1024).decode()
                        conversationRAW += (clientInput + "\n")

                        #if(clientInput == "stop"):
                        #    doRestart = True
                        
                        # Set Label for client response
                        newLabel = f"user{labelCounter}"
                        #clientInputHTML = "\n<font color=\"#FF0000\">YOU:</font>" +" "+ "<font color=\"#ffeeee\">" + "<a href=\"pL\">"+ clientInput +"</a></font>"
                        clientInputHTML = f"\n<font color=\"#FF0000\">YOU:</font> <font color=\"#ffeeee\"><a href= \"{newLabel}+{clientInput}\">{clientInput}</a></font>"
                        labelCounter += 1

                        conversationHTML += clientInputHTML
                        conversationGPT = gptAddUserInput(conversationGPT, clientInput)         

                index += 1

            # Restart intructions
            if(doRestart):
                doRestart = False
                conversationHTML = ""
                conversationRAW = ""
                conversationGPT = []
                index = 0
        except Exception as e:
            print(f'Exception in sync thread {str(e)}')
            break
      
    sync_socket.close()


def pushAsync():
    global push_async_socket
    global conversationHTML

    testMessage = "ready"
    push_async_socket.send(testMessage.encode())

    while True:
        index = 0

        try:
            asyncEventFromUser = push_async_socket.recv(50000).decode()
            print(f"asyncEventFromUser: {asyncEventFromUser}")

            while index < len(instructions):
                instructionList = instructions.get_blocks()
                block = instructionList[index]

                if type(block) is prototypingElements.Async:

                    # Get sentence of asynEventFromUser = {outputLabel}:{output}
                    splitAsyncEventFromUser = asyncEventFromUser.split('+')

                    # Set asyncEventFromUser Input
                    for subblock in block:
                        if(subblock.get_name() == block.get_name()+"_EventText"):
                            subblock.set_input(splitAsyncEventFromUser[1])

                    # Execute subblocks
                    whileSubblocks(block)
                    asyncBlockOutput = getSubblockOutput(block.get_name()+"_SendToUser")

                    # TODO Stich asyncBlock Output in ConversationHTML
                    conversationHTML += f"\n<font color=\"#b670d6\">{asyncBlockOutput}</font>"

                index += 1

            #Send the HEADER element from Async block back to the prototyper  
            push_async_socket.send(conversationHTML.encode())

        except Exception as e:
            print(f'Exception in pushAsync thread {str(e)}')
            break

    push_async_socket.close()

def getAsync():
        global get_async_socket

        #stableIteration = 0
        #stablePicture(stableIteration, "beach, blue, sand, waves, ocean, jellyfish, purple, sunset")
        #stableIteration += 1


        while True:
            try:
                response = get_async_socket.recv(1024).decode()
                print(response)
            
                ## Send the message to the server / user
                #testdict = {
                #    "label": "test",
                #    "content": "Mustang"
                #}
                #testBytes = pickle.dumps(testdict)  
                #
                #testBytes_size = len(testBytes).to_bytes(4, byteorder='big')  # Convert image size to 4 bytes
                #get_async_socket.sendall(testBytes_size)  # Send the image size to the client
                #get_async_socket.sendall(testBytes)  # Send the image data to the client
#
                #response = get_async_socket.recv(1024).decode()
                #print(response)
#
                #
                #time.sleep(5) # TODO remove (just for testing)
    
            except:
                # code to handle the exception
                print("Connection to getAsync socket closed")
                break

        get_async_socket.close()

def stablePicture(stableIteration, imagePrompt):
    host = PICTURE_HOST
    port = PICTURE_PORT
    image_path = f'prototyper_output_{stableIteration}.png'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.connect((host, port))
        print(f'Connected to server: {host}:{port}')
        server_socket.sendall(imagePrompt.encode())  # Send the message to the server

        receive_image(server_socket, image_path)
    
    except Exception as e:
        print(f'Could not connect to stable server: {str(e)}') 
            

    server_socket.close()

def receive_image(server_socket, image_path):
    global get_async_socket

    image_size = int.from_bytes(server_socket.recv(4), byteorder='big')
    image_data = b''

    while len(image_data) < image_size:
        data = server_socket.recv(1024)
        if not data:
            break
        image_data += data

    # Send bytestream to client
    imagedict = {
                    "label": "image",
                    "content": image_data
                }           
    
    imageBytes = pickle.dumps(imagedict)

    imageBytes_size = len(imageBytes).to_bytes(4, byteorder='big')  # Convert image size to 4 bytes
    get_async_socket.sendall(imageBytes_size)  # Send the image size to the client
    get_async_socket.sendall(imageBytes)  # Send the image data to the client

    # Save picture to file
    with open(image_path, 'wb') as file:
        file.write(image_data)
        
    print(f'Image received and saved as {image_path}')

while(True):
    try:
        sync_socket.connect((userHost, syncPort))
        push_async_socket.connect((userHost, pushAsyncPort))
        get_async_socket.connect((userHost, getAsyncPort))
        print(f'Connected to server over all sockets: {userHost}:{syncPort}/{pushAsyncPort}/{getAsyncPort}')
          
    except:
        # code to handle the exception
        print("Could not connect to server over all sockets.")

        sync_socket.close()
        push_async_socket.close()
        get_async_socket.close()

        time.sleep(2)
        continue

    syncThread = threading.Thread(target=sync)
    syncThread.start()

    pushAsyncSocket = threading.Thread(target=pushAsync)
    pushAsyncSocket.start()

    getAsyncSocket = threading.Thread(target=getAsync)
    getAsyncSocket.start()

    break

#-------------------------------PYGAME-------------------------------

running = True

# Initialize Pygame
pygame.init()
pygame.mixer.init()

screen_width = 1152
screen_height = 768
window_size = (screen_width, screen_height)
image_size = (384,768)


SUBBLOCK_WINDOW_WIDTH = (screen_width / 3)*2
SUBBLOCK_WINDOW_X = (screen_width) / 3

window_container_size = (SUBBLOCK_WINDOW_WIDTH, screen_height)


# Initialize screen
screen = pygame.display.set_mode(window_size)

# Set the title of the window
pygame.display.set_caption("Prototyper_LivePrototyping")

# Setup Background 
background = pygame.Surface(window_size)

# Initialize the pygame_gui UIManager
UI_MANAGER = pygame_gui.UIManager(window_size)

#with themes
#UI_MANAGER = pygame_gui.UIManager(window_size, 'themes/themes.json')
#background.fill(UI_MANAGER.ui_theme.get_colour('dark_bg'))

# Set up the game clock
CLOCK = pygame.time.Clock()

#---------------UI ELEMENTS------------------------

WINDOW_CONTAINER = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((SUBBLOCK_WINDOW_X, 0), 
                                                window_container_size),
                                                manager=UI_MANAGER, 
                                                object_id='#window_container')

HIERACHY_CONTAINER = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                            (screen_width/3, screen_height)),
                                                manager=UI_MANAGER, 
                                                object_id='#hierachy_container')

TEXT_HIERACHY = pygame_gui.elements.UITextBox("",
                                    relative_rect=pygame.Rect((0, 0), 
                                    (screen_width/3, screen_height-40)),
                                    manager=UI_MANAGER,
                                    container=HIERACHY_CONTAINER, 
                                    object_id='#text_hierachy')

BUTTON_RESTART = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, screen_height-40), 
                                                            ((screen_width/3)/2, 40)),
                                                            text="RESTART",
                                                            object_id='#restart_button',
                                                            container=HIERACHY_CONTAINER,
                                                            manager=UI_MANAGER)

BUTTON_ADD = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_width/3)/2, screen_height-40), 
                                                            ((screen_width/3)/2, 40)),
                                                            text="ADD",
                                                            object_id='#add_button',
                                                            container=HIERACHY_CONTAINER,
                                                            manager=UI_MANAGER)




# Define the color of the line (in RGB format)
line_color = (255, 255, 255)  # White color

# Define the start and end points of the line
start_pos = (SUBBLOCK_WINDOW_X, 0)
end_pos = (SUBBLOCK_WINDOW_X, screen_height)

# Define the width of the line
line_width = 1

# Draw the line
pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)

pygame.display.flip()

AddButtonScreen = prototypingUIElements.AddButtonScreen(UI_MANAGER,WINDOW_CONTAINER, window_container_size)

#--------------LOAD EXAMPLE INSTRUCTIONS:---------------------

# Static Block Intro
static_block = prototypingElements.Static("UserInput",UI_MANAGER,WINDOW_CONTAINER, window_container_size)

input_example = prototypingElements.Subblock_User_Input("User Scenario",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
input_example.set_requestVarForUser("Hello! Please enter the scenario you want to Roleplay:")

sendToGPT_example = prototypingElements.Subblock_SendToGPT("Generate Image Prompt",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
sendToGPT_example.set_input("Based on this scenario:+User Scenario+. Create me 30 single words, delimited by comma, to create a suiting image.")

image_example = prototypingElements.Subblock_Image("Image",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
image_example.set_input("Generate Image Prompt")
#Good Image negative prompts: nsfw, blood, sad, 
image_example.set_negativeInput("nsfw, blood, sad")

static_block.add_subblock(input_example)
static_block.add_subblock(sendToGPT_example)
static_block.add_subblock(image_example)

instructions.append_block(static_block)


# Loop Block:
loop_block = prototypingElements.Loop("Loop",UI_MANAGER,WINDOW_CONTAINER, window_container_size)

conversationText_example = prototypingElements.Subblock_Output(loop_block.get_name()+"_ConversationText",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
conversationText_example.set_input("")

lastAISentence_example = prototypingElements.Subblock_Output(loop_block.get_name()+"_LastAISentence",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
lastAISentence_example.set_input("")

pinput_example = prototypingElements.Subblock_Prototyper_Input("Prompt1",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
pinput_example.set_prototyper_input("Converse with me to help me learn the english language. Never leave the roleplay.")

concat_example = prototypingElements.Subblock_Combine("Complete Prompt",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
concat_example.set_inputs("Prompt1+ The scenario for the roleplay is:+User Scenario")

header_example = prototypingElements.Subblock_Output("Header",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
header_example.set_input("Complete Prompt")

loop_block.add_subblock(conversationText_example)
loop_block.add_subblock(lastAISentence_example)
loop_block.add_subblock(pinput_example)
loop_block.add_subblock(concat_example)
loop_block.add_subblock(header_example)

instructions.append_block(loop_block)

# Async:
instructions.append_block(createAsyncBlock("Async"))


#------------------------------DISPLAY STARTING ELEMENTS------------------------
disableContainers()
TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))


#-------------------------------PYGAME WHILE------------------------------------

while running:
    UI_REFRESH_RATE = CLOCK.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            print(f"Button pressed with ID: {event.ui_object_id}")
            if(event.ui_object_id == '#window_container.#Subblock_Container.#save_button'):
                print("Save button triggered!")
                if(visibleSubblock != None):                  
                    visibleSubblock.save()

                else:
                    print("visibleSubblock empty!")
                
            elif(event.ui_object_id == '#hierachy_container.#add_button'):
                # Show Add button screen
                disableContainers()

                AddButtonScreen.addButton_container.enable()
                AddButtonScreen.addButton_container.show()
            
            # Move buttons
            elif(event.ui_object_id == '#window_container.#Block_Container.#move_up_button'):
                moveBlockUp(visibleBlock)
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))
                
            elif(event.ui_object_id == '#window_container.#Block_Container.#move_down_button'):
                moveBlockDown(visibleBlock)
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

            elif(event.ui_object_id == '#window_container.#Subblock_Container.#move_up_button'):
                moveSubblockUp(visibleSubblock)
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

            elif(event.ui_object_id == '#window_container.#Subblock_Container.#move_down_button'):
                moveSubblockDown(visibleSubblock)
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

            # Delete buttons
            elif(event.ui_object_id == '#window_container.#Subblock_Container.#del_button'):
                print(f"Deleting subblock: {visibleSubblock.get_name()}...")
                disableContainers()
                deleteSubblock(visibleSubblock)
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

            elif(event.ui_object_id == '#window_container.#Block_Container.#del_button'):
                print(f"Deleting block: {visibleBlock.get_name()}...")
                disableContainers()
                deleteBlock(visibleBlock)
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))


            #-----ADD BLOCK BUTTONS:

            elif(event.ui_object_id == '#window_container.#AddButton_Container.#pre_block_button'):
                nameForBlock = AddButtonScreen.name_entry_box.get_text()               
                newBlock = prototypingElements.Static(nameForBlock, UI_MANAGER,WINDOW_CONTAINER, window_container_size)
                instructions.append_block(newBlock) # TODO APPEND BEFORE LOOP
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))
                

                disableContainers()

            elif(event.ui_object_id == '#window_container.#AddButton_Container.#loop_block_button'):
                nameForBlock = AddButtonScreen.name_entry_box.get_text()    

                instructions.append_block(createLoopBlock(nameForBlock)) # TODO APPEND IN LOOP
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))
                disableContainers()

            elif(event.ui_object_id == '#window_container.#AddButton_Container.#post_block_button'):
                nameForBlock = AddButtonScreen.name_entry_box.get_text()               
                newBlock = prototypingElements.Static(nameForBlock, UI_MANAGER,WINDOW_CONTAINER, window_container_size)
                instructions.append_block(newBlock) # TODO APPEND AFTER LOOP
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))
                disableContainers()

            elif(event.ui_object_id == '#window_container.#AddButton_Container.#async_block_button'):
                nameForBlock = AddButtonScreen.name_entry_box.get_text()            
                instructions.append_block(createAsyncBlock(nameForBlock))   
                TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))
                disableContainers()


            #-------ADD SUBBLOCK BUTTONS:

            elif(event.ui_object_id == '#window_container.#Block_Container.#user_input_block_button'):
                if(visibleBlock != None):
                    nameForSubblock = visibleBlock.uiInstance.name_entry_box.get_text() 
                    newSubblock = prototypingElements.Subblock_User_Input(nameForSubblock, UI_MANAGER,WINDOW_CONTAINER, window_container_size) 
                    visibleBlock.add_subblock(newSubblock)
                    TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

                    disableContainers()

            elif(event.ui_object_id == '#window_container.#Block_Container.#prototyper_input_block_button'):
                if(visibleBlock != None):
                    nameForSubblock = visibleBlock.uiInstance.name_entry_box.get_text() 
                    newSubblock = prototypingElements.Subblock_Prototyper_Input(nameForSubblock, UI_MANAGER,WINDOW_CONTAINER, window_container_size) 
                    visibleBlock.add_subblock(newSubblock)
                    TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

                    disableContainers()

            elif(event.ui_object_id == '#window_container.#Block_Container.#combine_block_button'):
                if(visibleBlock != None):
                    nameForSubblock = visibleBlock.uiInstance.name_entry_box.get_text() 
                    newSubblock = prototypingElements.Subblock_Combine(nameForSubblock, UI_MANAGER,WINDOW_CONTAINER, window_container_size) 
                    visibleBlock.add_subblock(newSubblock)
                    TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

                    disableContainers()

            elif(event.ui_object_id == '#window_container.#Block_Container.#sendToGPT_block_button'):
                if(visibleBlock != None):
                    nameForSubblock = visibleBlock.uiInstance.name_entry_box.get_text() 
                    newSubblock = prototypingElements.Subblock_SendToGPT(nameForSubblock, UI_MANAGER,WINDOW_CONTAINER, window_container_size) 
                    visibleBlock.add_subblock(newSubblock)
                    TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

                    disableContainers()
            
            elif(event.ui_object_id == '#window_container.#Block_Container.#image_block_button'):
                if(visibleBlock != None):
                    nameForSubblock = visibleBlock.uiInstance.name_entry_box.get_text() 
                    newSubblock = prototypingElements.Subblock_Image(nameForSubblock, UI_MANAGER,WINDOW_CONTAINER, window_container_size) 
                    visibleBlock.add_subblock(newSubblock)
                    TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

                    disableContainers()

            elif(event.ui_object_id == '#window_container.#Block_Container.#output_block_button'):
                if(visibleBlock != None):
                    nameForSubblock = visibleBlock.uiInstance.name_entry_box.get_text() 
                    newSubblock = prototypingElements.Subblock_Output(nameForSubblock, UI_MANAGER,WINDOW_CONTAINER, window_container_size) 
                    visibleBlock.add_subblock(newSubblock)
                    TEXT_HIERACHY.set_text(prototypingElements.printOut(instructions, " "))

                    disableContainers()

            elif(event.ui_object_id == '#hierachy_container.#restart_button'):
                disableContainers() 
                doRestart = True

        if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            linkText = event.link_target
            print(f"Clicked HTML Link: {linkText}")

            block = getBlock(linkText)
            if(block != None):
                disableContainers()
                block.load()
                block.uiInstance.block_container.enable()
                block.uiInstance.block_container.show()
                visibleBlock = block
            else:
                subblock = getSubblock(linkText)
                if(subblock != None):
                    disableContainers()
                    subblock.load()
                    subblock.uiInstance.subblock_container.enable()
                    subblock.uiInstance.subblock_container.show()
                    visibleSubblock = subblock

        # print(f"Event type: {event.type}")
        UI_MANAGER.process_events(event)


    UI_MANAGER.update(UI_REFRESH_RATE)

        
    
    screen.blit(background, (0, 0))
    pygame.draw.line(screen, line_color, start_pos, end_pos, line_width)

    UI_MANAGER.draw_ui(screen) 

    pygame.display.update()

# Quit Pygame
pygame.mixer.quit()
pygame.quit()

syncThread.join()
pushAsyncSocket.join()
getAsyncSocket.join()