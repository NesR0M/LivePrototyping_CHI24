import pygame_gui
import pygame

size_button_rectangle = (100, 50)
size_button_square = (50,50)

class AddButtonScreen():
    def __init__(self, ui_manager, container, container_size):
        self.ui_manager = ui_manager
        self.container = container
        self.container_size = container_size
        self.addButton_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        self.container_size),
                                                        manager=ui_manager, 
                                                        object_id='#AddButton_Container',
                                                        container=container)
        self.name_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 50), (self.container_size[0],100)),
            initial_text="enter the name of your block here",
            container=self.addButton_container)
        self.pre_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((container_size[0]/2)-(size_button_rectangle[0]),200), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="Pre-Conversation",
                                            object_id='#pre_block_button',
                                            container= self.addButton_container,
                                            manager= self.ui_manager)
        self.loop_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((container_size[0]/2)-(size_button_rectangle[0]),260), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="Conversation",
                                            object_id='#loop_block_button',
                                            container= self.addButton_container,
                                            manager= self.ui_manager)
        self.post_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((container_size[0]/2)-(size_button_rectangle[0]),320), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="Post-Conversation",
                                            object_id='#post_block_button',
                                            container= self.addButton_container,
                                            manager= self.ui_manager)
        self.async_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((container_size[0]/2)-(size_button_rectangle[0]),380), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="While-Conversation",
                                            object_id='#async_block_button',
                                            container= self.addButton_container,
                                            manager= self.ui_manager)
        
class Block():
    def __init__(self, ui_manager, b_container, b_size):
        self.ui_manager = ui_manager
        self.b_container = b_container
        self.b_size = b_size
        self.block_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        self.b_size),
                                                        manager=ui_manager, 
                                                        object_id='#Block_Container',
                                                        container=b_container)
        self.name_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 30), (self.b_size[0],40)),
            html_text="name of block",
            container=self.block_container)
        self.name_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 70), (self.b_size[0],100)),
            initial_text="enter the name of your block here",
            container=self.block_container)
        self.user_input_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((b_size[0]/2)-(size_button_rectangle[0]),200), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="User Input",
                                            object_id='#user_input_block_button',
                                            container= self.block_container,
                                            manager= self.ui_manager)
        self.prototyper_input_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((b_size[0]/2)-(size_button_rectangle[0]),260), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="Prototyper Input",
                                            object_id='#prototyper_input_block_button',
                                            container= self.block_container,
                                            manager= self.ui_manager)
        self.combine_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((b_size[0]/2)-(size_button_rectangle[0]),320), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="Combine Variables",
                                            object_id='#combine_block_button',
                                            container= self.block_container,
                                            manager= self.ui_manager)
        self.sendToGPT_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((b_size[0]/2)-(size_button_rectangle[0]),380), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="Send to GPT",
                                            object_id='#sendToGPT_block_button',
                                            container= self.block_container,
                                            manager= self.ui_manager)
        self.image_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((b_size[0]/2)-(size_button_rectangle[0]),440), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="Create Image",
                                            object_id='#image_block_button',
                                            container= self.block_container,
                                            manager= self.ui_manager)
        self.output_block_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((b_size[0]/2)-(size_button_rectangle[0]),500), (size_button_rectangle[0] * 2, size_button_rectangle[1])),
                                            text="Output to Chat",
                                            object_id='#output_block_button',
                                            container= self.block_container,
                                            manager= self.ui_manager)
        self.hide_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.b_size[0]-10-(size_button_rectangle[0]*2), self.b_size[1]-10-size_button_rectangle[1]), size_button_rectangle),
                                                text="HIDE",
                                                object_id='#hide_button',
                                                container= self.block_container,
                                                manager=ui_manager)
        self.delete_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.b_size[0]-10-(size_button_rectangle[0]*3), self.b_size[1]-10-size_button_rectangle[1]), size_button_rectangle),
                                                text="DEL",
                                                object_id='#del_button',
                                                container= self.block_container,
                                                manager=ui_manager)
        self.move_up_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,self.b_size[1]-10-(size_button_rectangle[1]*2)), size_button_rectangle),
                                                text="MOVE UP",
                                                object_id='#move_up_button',
                                                container= self.block_container,
                                                manager=ui_manager)
        self.move_down_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,self.b_size[1]-10-size_button_rectangle[1]), size_button_rectangle),
                                                text="MOVE DOWN",
                                                object_id='#move_down_button',
                                                container= self.block_container,
                                                manager=ui_manager)
        
class Subblock:
    def __init__(self, ui_manager, sb_container, sb_size, subblock_container):
        self.ui_manager = ui_manager
        self.sb_container = sb_container
        self.sb_size = sb_size
        self.save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.sb_size[0]-10-size_button_rectangle[0], self.sb_size[1]-10-size_button_rectangle[1]), size_button_rectangle),
                                                text="SAVE",
                                                object_id='#save_button',
                                                container= subblock_container,
                                                manager=ui_manager)
        self.hide_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.sb_size[0]-10-(size_button_rectangle[0]*2), self.sb_size[1]-10-size_button_rectangle[1]), size_button_rectangle),
                                                text="HIDE",
                                                object_id='#hide_button',
                                                container= subblock_container,
                                                manager=ui_manager)
        self.delete_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.sb_size[0]-10-(size_button_rectangle[0]*3), self.sb_size[1]-10-size_button_rectangle[1]), size_button_rectangle),
                                                text="DEL",
                                                object_id='#del_button',
                                                container= subblock_container,
                                                manager=ui_manager)
        self.move_up_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,self.sb_size[1]-10-(size_button_rectangle[1]*2)), size_button_rectangle),
                                                text="MOVE UP",
                                                object_id='#move_up_button',
                                                container= subblock_container,
                                                manager=ui_manager)
        self.move_down_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,self.sb_size[1]-10-size_button_rectangle[1]), size_button_rectangle),
                                                text="MOVE DOWN",
                                                object_id='#move_down_button',
                                                container= subblock_container,
                                                manager=ui_manager)

class Subblock_User_Input(Subblock):
    def __init__(self, ui_manager, sb_container, sb_size):
        self.subblock_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        sb_size),
                                                        manager=ui_manager, 
                                                        object_id='#Subblock_Container',
                                                        container=sb_container)
        super().__init__(ui_manager, sb_container, sb_size, self.subblock_container) 
        self.prompt_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 300), (self.sb_size[0],200)),
            initial_text="enter your text here",
            container=self.subblock_container)
        self.comment_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 150), (self.sb_size[0],100)),
            initial_text="enter your comment",
            container=self.subblock_container)
        self.name_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 50), (self.sb_size[0],100)),
            html_text="name of the subblock",
            container=self.subblock_container)
        
class Subblock_Prototyper_Input(Subblock):
    def __init__(self, ui_manager, sb_container, sb_size):
        self.subblock_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        sb_size),
                                                        manager=ui_manager, 
                                                        object_id='#Subblock_Container',
                                                        container=sb_container)
        super().__init__(ui_manager, sb_container, sb_size, self.subblock_container) 
        self.prompt_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 300), (self.sb_size[0],200)),
            initial_text="enter your text here",
            container=self.subblock_container)
        self.comment_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 150), (self.sb_size[0],100)),
            initial_text="enter your comment",
            container=self.subblock_container)
        self.name_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 50), (self.sb_size[0],100)),
            html_text="name of the subblock",
            container=self.subblock_container)

class Subblock_Combine(Subblock):
    def __init__(self, ui_manager, sb_container, sb_size):
        self.subblock_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        sb_size),
                                                        manager=ui_manager, 
                                                        object_id='#Subblock_Container',
                                                        container=sb_container)
        super().__init__(ui_manager, sb_container, sb_size, self.subblock_container) 
        self.prompt_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 300), (self.sb_size[0],200)),
            initial_text="enter your text here",
            container=self.subblock_container)
        self.comment_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 150), (self.sb_size[0],100)),
            initial_text="enter your comment",
            container=self.subblock_container)
        self.name_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 50), (self.sb_size[0],100)),
            html_text="name of the subblock",
            container=self.subblock_container)
        
class Subblock_SendToGPT(Subblock):
    def __init__(self, ui_manager, sb_container, sb_size):
        self.subblock_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        sb_size),
                                                        manager=ui_manager, 
                                                        object_id='#Subblock_Container',
                                                        container=sb_container)
        super().__init__(ui_manager, sb_container, sb_size, self.subblock_container) 
        self.prompt_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 300), (self.sb_size[0],200)),
            initial_text="enter your text here",
            container=self.subblock_container)
        self.comment_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 150), (self.sb_size[0],100)),
            initial_text="enter your comment",
            container=self.subblock_container)
        self.name_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 50), (self.sb_size[0],100)),
            html_text="name of the subblock",
            container=self.subblock_container)

class Subblock_Image(Subblock):
    def __init__(self, ui_manager, sb_container, sb_size):
        self.subblock_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        sb_size),
                                                        manager=ui_manager, 
                                                        object_id='#Subblock_Container',
                                                        container=sb_container)
        super().__init__(ui_manager, sb_container, sb_size, self.subblock_container) 
        self.negativ_prompt_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 500), (self.sb_size[0],100)),
            initial_text="enter your negative prompt here",
            container=self.subblock_container)
        self.negative_title_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 460), (self.sb_size[0],40)),
            html_text="Negative Prompt:",
            container=self.subblock_container)
        
        self.positive_prompt_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 340), (self.sb_size[0],100)),
            initial_text="enter your positive prompt here",
            container=self.subblock_container)
        self.positive_title_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 300), (self.sb_size[0],40)),
            html_text="Positive Prompt: ",
            container=self.subblock_container)
        
        self.comment_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 150), (self.sb_size[0],100)),
            initial_text="enter your comment",
            container=self.subblock_container)
        self.name_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 50), (self.sb_size[0],100)),
            html_text="name of the subblock",
            container=self.subblock_container)

class Subblock_Special():
    def __init__(self, ui_manager, sb_container, sb_size):
        self.ui_manager = ui_manager
        self.sb_container = sb_container
        self.sb_size = sb_size

        self.subblock_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        sb_size),
                                                        manager=ui_manager, 
                                                        object_id='#Subblock_Container',
                                                        container=sb_container)
        self.prompt_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 300), (self.sb_size[0],200)),
            initial_text="enter your text here",
            container=self.subblock_container)
        self.comment_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 150), (self.sb_size[0],100)),
            initial_text="enter your comment",
            container=self.subblock_container)
        self.name_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 50), (self.sb_size[0],100)),
            html_text="name of the subblock",
            container=self.subblock_container)
        self.save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.sb_size[0]-10-size_button_rectangle[0], self.sb_size[1]-10-size_button_rectangle[1]), size_button_rectangle),
                                                text="SAVE",
                                                object_id='#save_button',
                                                container= self.subblock_container,
                                                manager=ui_manager)
        

class Subblock_Output(Subblock):
    def __init__(self, ui_manager, sb_container, sb_size):
        self.subblock_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), 
                                                        sb_size),
                                                        manager=ui_manager, 
                                                        object_id='#Subblock_Container',
                                                        container=sb_container)
        super().__init__(ui_manager, sb_container, sb_size, self.subblock_container) 
        self.prompt_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 300), (self.sb_size[0],200)),
            initial_text="enter your text here",
            container=self.subblock_container)
        self.comment_entry_box = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((0, 150), (self.sb_size[0],100)),
            initial_text="enter your comment",
            container=self.subblock_container)
        self.name_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 50), (self.sb_size[0],100)),
            html_text="name of the subblock",
            container=self.subblock_container)