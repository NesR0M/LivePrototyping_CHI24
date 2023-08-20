import prototyperUIElements
#---------------------------SUBBLOCKS-------------------------------

class Subblock:
    def __init__(self, name):
        self.name = name
        self.output = ""
        self.comment = ""
        self.input = ""

    def set_output(self, output):
        self.output = output

    def get_output(self):
        return self.output
    
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def set_input(self, input):
        self.input = input

    def get_input(self):
        return self.input

    def save():
        return
    
    def load():
        return

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, output={self.output!r})"
    
class Subblock_User_Input(Subblock):
    def __init__(self, name, ui_manager, sb_container, sb_size):
        super().__init__(name) # variable name of output
        self.uiInstance = prototyperUIElements.Subblock_User_Input(ui_manager, sb_container, sb_size)
        self.uiInstance.name_box.set_text(name)

    def set_name(self, name):
        self.name = name
        self.uiInstance.name_box.set_text(name)
    
    def save(self):
        self.input = self.uiInstance.prompt_entry_box.get_text()
        self.comment = self.uiInstance.comment_entry_box.get_text()

    def load(self):
        self.uiInstance.prompt_entry_box.set_text(self.input)
        self.uiInstance.comment_entry_box.set_text(self.comment)

    def __repr__(self):
        return (f"{self.__class__.__name__}(name={self.name!r}, requestForUser={self.input!r}, "
                f"user_input={self.user_input!r}, output={self.output!r})")

class Subblock_Prototyper_Input(Subblock):
    def __init__(self, name, ui_manager, sb_container, sb_size):
        super().__init__(name)  # variable name of output
        self.uiInstance = prototyperUIElements.Subblock_Prototyper_Input(ui_manager, sb_container, sb_size)
        self.uiInstance.name_box.set_text(name)

    def set_name(self, name):
        self.name = name
        self.uiInstance.name_box.set_text(name)

    def save(self):
        self.input = self.uiInstance.prompt_entry_box.get_text()
        self.comment = self.uiInstance.comment_entry_box.get_text()

    def load(self):
        self.uiInstance.prompt_entry_box.set_text(self.input)
        self.uiInstance.comment_entry_box.set_text(self.comment)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, prototyper_input={self.input!r}, output={self.output!r})"

class Subblock_Combine(Subblock):
    def __init__(self, name, ui_manager, sb_container, sb_size):
        super().__init__(name)
        self.uiInstance = prototyperUIElements.Subblock_Combine(ui_manager, sb_container, sb_size)
        self.uiInstance.name_box.set_text(name)

    def set_name(self, name):
        self.name = name
        self.uiInstance.name_box.set_text(name)
    
    def save(self):
        self.input = self.uiInstance.prompt_entry_box.get_text()
        self.comment = self.uiInstance.comment_entry_box.get_text()

    def load(self):
        self.uiInstance.prompt_entry_box.set_text(self.input)
        self.uiInstance.comment_entry_box.set_text(self.comment)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, inputs={self.input!r}, output={self.output!r})"

class Subblock_SendToGPT(Subblock):
    def __init__(self, name, ui_manager, sb_container, sb_size):
        super().__init__(name)
        self.uiInstance = prototyperUIElements.Subblock_SendToGPT(ui_manager, sb_container, sb_size)
        self.uiInstance.name_box.set_text(name)

    def set_name(self, name):
        self.name = name
        self.uiInstance.name_box.set_text(name)
    
    def save(self):
        self.input = self.uiInstance.prompt_entry_box.get_text()
        self.comment = self.uiInstance.comment_entry_box.get_text()

    def load(self):
        self.uiInstance.prompt_entry_box.set_text(self.input)
        self.uiInstance.comment_entry_box.set_text(self.comment)


    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, input={self.input!r}, output={self.output!r})"
    
class Subblock_Image(Subblock):
    def __init__(self, name, ui_manager, sb_container, sb_size):
        super().__init__(name)
        self.uiInstance = prototyperUIElements.Subblock_Image(ui_manager, sb_container, sb_size)
        self.uiInstance.name_box.set_text(name)
        self.negativeInput = ""

    def set_name(self, name):
        self.name = name
        self.uiInstance.name_box.set_text(name)
    
    def set_negativeInput(self, negativeInput):
        self.negativeInput = negativeInput

    def get_negativeInput(self):
        return self.negativeInput
    
    def save(self):
        self.negativeInput = self.uiInstance.negativ_prompt_entry_box.get_text()
        self.input = self.uiInstance.positive_prompt_entry_box.get_text()
        self.comment = self.uiInstance.comment_entry_box.get_text()
    
    def load(self):
        self.uiInstance.negativ_prompt_entry_box.set_text(self.negativeInput)
        self.uiInstance.positive_prompt_entry_box.set_text(self.input)
        self.uiInstance.comment_entry_box.set_text(self.comment)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, input={self.input!r}, negativeInput={self.negativeInput!r}, output={self.output!r})"
    
class Subblock_Special(Subblock):
    def __init__(self, name, ui_manager, sb_container, sb_size):
        super().__init__(name)
        self.uiInstance = prototyperUIElements.Subblock_Special(ui_manager, sb_container, sb_size)
        self.uiInstance.name_box.set_text(name)

    def set_name(self, name):
        self.name = name
        self.uiInstance.name_box.set_text(name)
    
    def save(self):
        self.input = self.uiInstance.prompt_entry_box.get_text()
        self.comment = self.uiInstance.comment_entry_box.get_text()

    def load(self):
        self.uiInstance.prompt_entry_box.set_text(self.input)
        self.uiInstance.comment_entry_box.set_text(self.comment)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, input={self.input!r}, output={self.output!r})"
    
class Subblock_Output(Subblock):
    def __init__(self, name, ui_manager, sb_container, sb_size):
        super().__init__(name)
        self.uiInstance = prototyperUIElements.Subblock_Output(ui_manager, sb_container, sb_size)
        self.uiInstance.name_box.set_text(name)

    def set_name(self, name):
        self.name = name
        self.uiInstance.name_box.set_text(name)
    
    def save(self):
        self.input = self.uiInstance.prompt_entry_box.get_text()
        self.comment = self.uiInstance.comment_entry_box.get_text()

    def load(self):
        self.uiInstance.prompt_entry_box.set_text(self.input)
        self.uiInstance.comment_entry_box.set_text(self.comment)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, input={self.input!r}, output={self.output!r})"


#---------------------------BLOCKS-------------------------------


class Block:
    def __init__(self, name, ui_manager, sb_container, sb_size):
        self.name = name
        self.output = None
        self.subblocks = []
        self.uiInstance = prototyperUIElements.Block(ui_manager, sb_container, sb_size)
        self.uiInstance.name_box.set_text(name)

    def __iter__(self):
        return iter(self.subblocks)

    def add_subblock(self, subblock):
        if isinstance(subblock, Subblock):
            self.subblocks.append(subblock)
        else:
            raise ValueError("Only objects of type Subblock or its derivatives can be added!")
        
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
        
    def set_output(self, output):
        self.output = output

    def get_output(self):
        return self.output
    
    def set_subblocks(self, subblocks):
        self.subblocks = subblocks

    def get_subblocks(self):
        return self.subblocks

    def endfunction(self):
        pass

    def load(self):
        self.uiInstance.name_entry_box.set_text("EnterSubblockName")

    # def move()    

    # def suicide()

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, output={self.output!r}, subblocks={self.subblocks!r})"
    
    def __len__(self):
        return len(self.subblocks)

class Static(Block):
    def __init__(self, name,  ui_manager, sb_container, sb_size):
        super().__init__(name,  ui_manager, sb_container, sb_size)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, output={self.output!r}, subblocks={self.subblocks!r})"

class Loop(Block):
    def __init__(self, name,  ui_manager, sb_container, sb_size):
        super().__init__(name,  ui_manager, sb_container, sb_size)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, output={self.output!r}, subblocks={self.subblocks!r})"

class Async(Block):
    def __init__(self, name, ui_manager, sb_container, sb_size):
        super().__init__(name, ui_manager, sb_container, sb_size)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, output={self.output!r}, subblocks={self.subblocks!r})"

class Instructions:
    def __init__(self, blocks):
        self.blocks = blocks

    def __iter__(self):
        return iter(self.blocks)

    def append_block(self, block):
        if isinstance(block, Block):
            self.blocks.append(block)
        else:
            raise ValueError("Only objects of type Subblock or its derivatives can be added!")
        
    def add_block_at(self, position, block):
        """Adds the block at the specified position."""
        if not isinstance(block, Block):
            raise ValueError("Only objects of type Block or its derivatives can be added!")
        if position < 0 or position > len(self.blocks):  # Allowing position to be equal to len(self.blocks) so we can append at the end.
            raise ValueError("Position out of range!")
        self.blocks.insert(position, block)
        
    def remove_block_at(self, position):
        """Removes the block at the specified position."""
        if position < 0 or position >= len(self.blocks):
            raise ValueError("Position out of range!")
        self.blocks.pop(position)

    def set_blocks(self, blocks):
        self.blocks = blocks

    def get_blocks(self):
        return self.blocks
        
    def __repr__(self):
        return f"{self.__class__.__name__}(blocks={self.blocks!r})"
    
    def __len__(self):
        return len(self.blocks)
    
    def getAsyncBlocks(self):
        asyncBlocks = []
        for block in self.blocks:
            if(type(block) is Async):
                asyncBlocks.append(block)
        return asyncBlocks


#-------------------------FUNCTIONS--------------------------------


def printOut(instructionList, subblockNameForPointer):
        printOut = ""

        for block in instructionList:
            printOut += f"<a href=\"{block.get_name()}\">{block.get_name()}</a></font>\n"

            for subblock in block:
                pointerStr = "  "
                if(subblockNameForPointer != None and subblock.get_name() == subblockNameForPointer):
                    pointerStr = "<font color=\"#FF0000\">-></font>"
                    
                if type(subblock) is Subblock_Image:
                    printOut += f"{pointerStr} AI <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"
                elif type(subblock) is Subblock_Combine:
                    printOut += f"{pointerStr} + <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"
                elif type(subblock) is Subblock_SendToGPT:
                    printOut += f"{pointerStr} AI <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"
                elif type(subblock) is Subblock_User_Input:
                    printOut += f"{pointerStr} < <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"
                elif type(subblock) is Subblock_Special and "Header" in subblock.get_name():
                    printOut += f"{pointerStr} AI <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"
                elif type(subblock) is Subblock_Special and "Async_SendToUser" in subblock.get_name():
                    printOut += f"{pointerStr} < <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"
                elif type(subblock) is Subblock_Special:
                    printOut += f"{pointerStr} > <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"
                elif type(subblock) is Subblock_Output:
                    printOut += f"{pointerStr} << <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"
                else:
                    printOut += f"{pointerStr} - <a href=\"{subblock.get_name()}\">{subblock.get_name()}</a>\n"

            #if type(block) is Loop or type(block) is Async:
            #    printOut += f" -> <a href=\"END_{block.get_name()}\">SEND {block.get_name()} TO USER</a></font>\n"

            printOut += f"----------------------------------\n"

        return printOut

#--------------------------CREATE INSTRUCTION LIST----------------

instructions = Instructions([])
print(printOut(instructions, " "))

#---------------------------EXAMPLES FOR PROTOTYPERMAIN-------------------------------

#input1 = prototypingElements.Subblock_User_Input("UserName",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#input1.set_requestVarForUser("Please enter your name:")
#
#pinput_1 = prototypingElements.Subblock_Prototyper_Input("PUserName",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#pinput_1.set_prototyper_input("This is my name: ")
#
#input2 = prototypingElements.Subblock_User_Input("UserAge",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#input2.set_requestVarForUser("Please enter your age:")
#
#pinput_2 = prototypingElements.Subblock_Prototyper_Input("PUserAge",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#pinput_2.set_prototyper_input("This is my age: ")
#
#input3 = prototypingElements.Subblock_User_Input("UserLocation",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#input3.set_requestVarForUser("Where do you want to be:")
#
#pinput_3 = prototypingElements.Subblock_Prototyper_Input("PUserLocation",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#pinput_3.set_prototyper_input("We are in: ")
#
#input4 = prototypingElements.Subblock_User_Input("UserScenario",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#input4.set_requestVarForUser("Please enter the scenario:")
#
#pinput_4 = prototypingElements.Subblock_Prototyper_Input("PUserScenario",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#pinput_4.set_prototyper_input("The scenario is: ")
#
#
#concat_1 = prototypingElements.Subblock_Combine("CombineUserInput",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#concat_1.set_inputs("PUserName+UserName+PUserAge+UserAge+PUserLocation+UserLocation+PUserScenario+UserScenario")
#
##Image negative prompts: nsfw, blood, sad, 
#
#
#static_block = prototypingElements.Static("UserInput",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#static_block.add_subblock(input1)
#static_block.add_subblock(pinput_1)
#static_block.add_subblock(input2)
#static_block.add_subblock(pinput_2)
#static_block.add_subblock(input3)
#static_block.add_subblock(pinput_3)
#static_block.add_subblock(input4)
#static_block.add_subblock(pinput_4)
#static_block.add_subblock(concat_1)
#
#
#instructions.append_block(static_block)
#
## Loop Block:
#loop_block = prototypingElements.Loop("Loop",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#
#conversationText = prototypingElements.Subblock_Output(loop_block.get_name()+"_ConversationText",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#conversationText.set_input("")
#
#lastAISentence = prototypingElements.Subblock_Output(loop_block.get_name()+"_LastAISentence",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#lastAISentence.set_input("")
#
#prototyper_input_2 = prototypingElements.Subblock_Prototyper_Input("prompt1",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#prototyper_input_2.set_prototyper_input("We are roleplaying in this conversation. You are a policeofficer asking me if I have seen a bank robbery")
#
#prototyper_input_3 = prototypingElements.Subblock_Prototyper_Input("prompt2",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#prototyper_input_3.set_prototyper_input("The topic of this roleplay will be:")
#
#concat_1 = prototypingElements.Subblock_Combine("CombineToScenario",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#concat_1.set_inputs("prompt1+prompt2+CombineUserInput")
#
#header = prototypingElements.Subblock_Output("Header",UI_MANAGER,WINDOW_CONTAINER, window_container_size)
#header.set_input("CombineToScenario")
#
#loop_block.add_subblock(conversationText)
#loop_block.add_subblock(lastAISentence)
#loop_block.add_subblock(prototyper_input_2)
#loop_block.add_subblock(prototyper_input_3)
#loop_block.add_subblock(concat_1)
#loop_block.add_subblock(header)
#
#instructions.append_block(loop_block)
#
#instructions.append_block(createAsyncBlock("Async"))