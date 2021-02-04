import PySimpleGUI as sg
import os
import pathlib
from config import * 
from handler.handlers import *
from window.window import *

# global variables => for easier configuration
sg.ChangeLookAndFeel(theme_color)

class Config:
    def __init__(self):
        self.CC = default_compiler
        self.CXXFILT = default_demangler
        self.CFLAGS = default_flags
        self.ABI = default_abi
        self.ARCH = default_arch
    def update_compiler(self, cc):
        self.CC = cc
    def update_demangler(self, dmgler):
        self.CXXFILT = dmgler
    def update_flags(self, flags):
        self.CFLAGS = flags
    def update_arch(self, arch):
        self.ARCH = arch
    def update_flags(self, abi):
        self.ABI = abi

# class for managing resources, such as editing file, window, config
class Info:
    def __init__(self, config, _file, window):
        self.config = config
        self.file   = _file
        self.window = window
        self.rtl_window = None
        self.file_not_modified = False

    def load_rtl_window(self, window):
        self.rtl_window = window

    def get_output_dir(self):
        return "data/{}/".format(self.get_filename())

    def set_not_modified(self):
        self.file_not_modified = True

    def file_is_modified(self):
        self.file_not_modified = False
    
    def update_abi(self, abi):
        self.config.update_flags(abi)
        self.file_not_modified = False
    
    def update_arch(self, arch):
        self.config.update_arch(arch)
        self.file_not_modified = False

    def update_flags(self, flags):
        self.config.update_flags(flags)
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
        if self.rtl_window is not None:
            event, value = self.rtl_window.read()
            if event == 'RTL-Exit':
                self.rtl_window.close()
                self.rtl_window = None
                return event
            else:
                if value is not None and value['RTL'] is not None:
                    return value['RTL'][0]
                else:
                    self.rtl_window.close()
                    self.rtl_window = None
        
        
        event, _ = self.window.read()

        return event

    def update_window(self, key, val):
        self.window[key].update(value = val)
    
    def query_window(self, key):
        if self.window is not None:
            return self.window.read()[1][key] 
        else:
            return None
    
    def get_abi(self):
        return self.config.ABI
    
    def get_arch(self):
        return self.config.ARCH
    
    def get_compiler(self):
        return self.config.CC

    def get_demangler(self):
        return self.config.CXXFILT

    def get_flags(self):
        return self.config.CFLAGS

    def get_file(self):
        return self.file

    def get_filename(self):
        return self.file.name

    def update_file(self, other_file):
        self.file = other_file

    def run_make(self, target):
        out_path = 'data/' + self.get_filename()

        os.system("make %s CC=%s CXXFILT=%s CFLAGS=%s ABI=%s ARCH=%s FILE=%s SDIR=%s" % (
                target, 
                self.get_compiler(), 
                self.get_demangler(), 
                self.get_flags(), 
                self.get_abi(), 
                self.get_arch(), 
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
        # we assume that if the there is an unrecognize event, 
        # the source file is edited, except mousewheel
        if "MouseWheel" not in event:
            info.file_not_modified = False

if "__main__" == __name__:
    

    # initialize main window
    main_window = window_factory.make_main_window("GCC Analyzer", main_window_layout)

    # initialize configure
    config = Config()

    # initialize resource manager
    info = Info(config, None, main_window)

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
        