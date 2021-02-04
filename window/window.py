from window.layout import *

def enum(**enums):
    return type('Enum', (), enums)

WINDOW_TYPE = enum(Main=1, Multiline=2, Popup=3)

# main_window -> single_ton
# other -> no limit
class window_factory:
    __main_window_instance = None

    @staticmethod
    def make_main_window(name, layout):
        if window_factory.__main_window_instance is not None:
            return window_factory.__main_window_instance

        window_factory.__main_window_instance = sg.Window(
                                                            name, 
                                                            layout=layout, 
                                                            margins=(0, 0), 
                                                            resizable=True, 
                                                            return_keyboard_events=True, 
                                                            finalize=True
                                                        )

        window_factory.__main_window_instance['_BODY_'].expand(expand_x=True, expand_y=True)
        return window_factory.__main_window_instance

    @staticmethod
    def make_multiline_popup(name, buf):
        layout = gen_scollable_multiline_window_layout(buf)
        return sg.Window(name, layout, resizable=True, auto_size_buttons=True, grab_anywhere=True).read(timeout=10)

    @staticmethod
    def make_listbox(options, text, titile):
        layout = gen_listbox_layout(text, options)
        return sg.Window(titile, layout, resizable=True, auto_size_buttons=True, grab_anywhere=True)