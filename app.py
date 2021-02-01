'''
  A minimalist Notepad built with the PySimpleGUI TKinter framework
  Author:     Israel Dryer
  Email:      israel.dryer@gmail.com
  Modified:   2020-06-20
'''
import PySimpleGUI as sg
import os
import pathlib
from handler.handlers import *

# global variables => for easier configuration
sg.ChangeLookAndFeel('BrownBlue')

default_compiler = "riscv64-unknown-elf-gcc"
default_demangler = "riscv64-unknown-elf-c++filt"

WIN_W = 90
WIN_H = 25

class Config:
    def __init__(self):
        self.CC = default_compiler
        self.CXXFILT = default_demangler
    def update_compiler(self, cc):
        self.CC = cc
    def update_demangler(self, dmgler):
        self.CXXFILT = dmgler

# class for managing resources, such as editing file, window, config
class Info:
    def __init__(self, config, _file, window):
        self.config = config
        self.file   = _file
        self.window = window
        self.file_not_modified = False

    def get_output_dir(self):
        return "data/{}/".format(self.get_filename())

    def file_is_modified(self):
        self.file_not_modified = False

    def update_compiler(self, cc):
        self.config.update_compiler(cc)
        self.file_not_modified = False

    def update_demangler(self, dmgler):
        self.config.update_demangler(dmgler)
        self.file_not_modified = False

    def write_to_file(self, content):
        self.file.write_text(content)
        self.file_not_modified = False

    def window_track_event(self):
        event, _ = self.window.read()
        return event

    def update_window(self, key, val):
        self.window[key].update(value = val)
    
    def query_window(self, key):
        return self.window.read()[1][key]

    def get_compiler(self):
        return self.config.CC

    def get_demangler(self):
        return self.config.CXXFILT

    def get_file(self):
        return self.file

    def get_filename(self):
        return self.file.name

    def update_file(self, other_file):
        self.file = other_file

    def run_make(self, target):
        out_path = 'data/' + self.get_filename()
        os.system("make %s CC=%s CXXFILT=%s FILE=%s SDIR=%s" % (
                target, 
                self.get_compiler(), 
                self.get_demangler(), 
                self.get_filename(),
                out_path
            )
        )

# a pluggable event handler based on chain of responsibility design pattern
class Handlers:
    def __init__(self, info):
        self.info = info
        self.handlers = []

    def register_handler(self, handler):
        self.handlers.append(handler)

    def handle(self, event):
        for handler in self.handlers:
            if hasattr(handler, "handle"):
                if handler.handle(event, self.info):
                    return 
            else:
                if handler(event, self.info):
                    return

if "__main__" == __name__:
    # Layout of gui menu
    menu_layout = [
        [
            'File', 
            [
                'New (Ctrl+N)', 
                'Open (Ctrl+O)', 
                'Save (Ctrl+S)', 
                'Save As', 
                '---', 
                'Exit'
            ]
        ],
        [
            'Configuration', 
            [
                'Edit Configure'
            ]
        ],
        [
            'Tools', 
            [
                'Dump high level GIMPLE',
                'Dump low level GIMPLE', 
                'Dump CFG',
                'Dump SSA',
                'Dump assembly',
            ]
        ],
        [
            'Help', 
            [
                'About'
            ]
        ]
    ]

    # Layout of gui body
    body_layout = [
        [
            sg.Menu(menu_layout)
        ],
        [
            sg.Text('> Temp File <', 
                    font=('Consolas', 8), 
                    size=(int(WIN_W/2), 1), 
                    key='_INFO_'
            ), 
            sg.Text('', 
                    font=('Consolas', 10), 
                    size=(int(WIN_W/2), 1), 
                    key='_INFO_OUT_'
            )
        ],
        [
            sg.Multiline(font=('Consolas', 12), 
                         size=(int(WIN_W/2), WIN_H), 
                         key='_BODY_'
                        ), 
            sg.Multiline(font=('Consolas', 12), 
                         size=(int(WIN_W/2), WIN_H),
                         disabled=True, 
                         key='_BODY_OUT_'
                        )
        ]
    ]

    # initialize main window
    window = sg.Window('Notepad', layout=body_layout, margins=(0, 0), resizable=True, return_keyboard_events=True, finalize=True)
    window['_BODY_'].expand(expand_x=True, expand_y=True)

    # initialize configure
    config = Config()

    # initialize resource manager
    info = Info(config, None, window)

    # initialzie handler
    handler = Handlers(info)
    
    # register all handlers
    for unregister_handler in [about_me, Files, Configuration, Tools]:
        handler.register_handler(unregister_handler)

    # looping
    while True:
        event = info.window_track_event()
        if event is None:
            break
        handler.handle(event)