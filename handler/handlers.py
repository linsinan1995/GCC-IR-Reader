'''
Author: Lin Sinan
Github: https://github.com/linsinan1995
Email: mynameisxiaou@gmail.com
LastEditors: Lin Sinan
Description: 
              
              
              
'''
import PySimpleGUI as sg
import pathlib
from handler.config import * 

def sg_show_scrollable_text(buf, name):
    layout = [ 
                [
                    sg.Multiline(
                        buf.read_text(),
                        font=('Consolas', 12),
                        size=(WIN_W * 3 // 4, WIN_H * 3 // 4), 
                        disabled=True,
                        background_color=sg.LOOK_AND_FEEL_TABLE[theme_color]['BACKGROUND'],
                        text_color=sg.LOOK_AND_FEEL_TABLE[theme_color]['TEXT'],
                    )
                ]
             ]
    sg.Window(name, layout, auto_size_buttons=True, grab_anywhere=True).read(timeout=10)

def about_me(event, info):
    if event in ('About',):
        sg.popup("Nothing here", '"All great things have small beginnings" - Peter Senge')
        return True
    else:
        return False

class Files:
    # static member variable: store all extended types
    file_types = (("C/C++ Source Code", src_type) for src_type in default_source_type)
    
    @staticmethod
    def handle(event, info):
        '''Interface for handling events related to Files'''
        
        if event in ('New (Ctrl+N)', 'n:78'):
            Files.new_file(info)
        elif event in ('Open (Ctrl+O)', 'o:79'):
            Files.open_file(info)
        elif event in ('Save (Ctrl+S)', 's:83'):
            Files.save_file(info)
        elif event in ('Save as',):
            Files.save_file_as(info)
        else:
            return False
        
        return True

    @staticmethod
    def new_file(info):
        '''Reset body and info bar, and clear filename variable'''
        info.update_window('_BODY_', '')
        info.update_window('_INFO_', '> Temp File <')
        info.update_file(None)
        info.file_is_modified()
# , "*.c", "*.cc", "*.cxx"

    @staticmethod
    def open_file(info):
        '''Open _file and update the infobar'''
        filename = sg.popup_get_file('', no_window=True, file_types = Files.file_types)
        if filename:
            _file = pathlib.Path(filename)
            info.update_window('_BODY_', _file.read_text())
            info.update_window('_INFO_', _file.absolute())
            info.update_file(_file)
            Files.clean_output_cache(info.get_filename())
            info.set_not_modified()

    @staticmethod
    def save_file(info):
        '''Save _file instantly if already open; otherwise use `save-as` popup'''
        if info.get_file():
            info.write_to_file(info.query_window('_BODY_'))
            info.set_not_modified()
        else:
            my_file = info.get_file()
            if my_file is None:
                return
                
            Files.save_file_as(info.get_filename())
            info.set_not_modified()

    @staticmethod
    def save_file_as(info):
        '''Save new _file or save existing _file with another name'''
        filename = sg.popup_get_file('Save As', save_as=True)
        if filename:
            _file = pathlib.Path(filename)
            _file.write_text(info.query_window('_BODY_'))
            info.update_window('_INFO_', _file.absolute())
            info.update_file(_file)
            Files.clean_output_cache(info.get_filename())
            info.file_is_modified()
            info.set_not_modified()

    @staticmethod
    def clean_output_cache(filename):
        # clean cache
        out_path = 'data/' + filename
        dir_path = pathlib.Path(out_path)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        for x in dir_path.iterdir():
            if x.is_file():
                pathlib.Path.unlink(x)

class Configuration:
    @staticmethod
    def handle(event, info):
        if event is not None and 'Configure' in event:
            # window for editing configure
            print(info.get_compiler())
            configure_layout = [
                [
                    sg.Text('Compiler', size=(15, 1)), 
                    sg.InputText(default_text = info.get_compiler())
                ],
                [
                    sg.Text('C++Filter', size = (15, 1)), 
                    sg.InputText(default_text = info.get_demangler())
                ],
                [
                    sg.Button('Ok'), 
                    sg.Cancel()
                ]
            ]
        else:
            return False
        
        if event in ('Edit Configure', ):
            Configuration.handle_edit(info, configure_layout)
            return True

        return False

    @staticmethod
    def handle_edit(info, configure_layout):
        config_window = sg.Window('Configuration', configure_layout)
        config_event, config_values = config_window.read()
        if config_event == 'Ok':   
            info.update_compiler(config_values[0])
            info.update_demangler(config_values[1])
        
        config_window.close()
        
class Tools:
    @staticmethod
    def handle(event, info):
        if event is not None and 'Dump' in event:
            my_file = info.get_file()
            if my_file is None:
                my_file = Files.save_file_as(info)

            if my_file is None:
                print("Can't handle temporary file!")
                return True

            if info.file_is_modified:
                info.run_make("app")

        if event in ('Dump assembly', ):
            Tools.handle_dump_assembly(event, info)
        elif event in ('Dump SSA', ):
            Tools.handle_dump_ssa(event, info)
        elif event in ('Dump CFG', ):
            Tools.handle_dump_cfg(event, info)
        elif event in ('Dump high level GIMPLE', ):
            Tools.handle_dump_gimple(event, info)
        elif event in ('Dump low level GIMPLE', ):
            Tools.handle_dump_lower_gimple(event, info)
        else:
            return False

        return True

    @staticmethod
    def handle_dump_assembly(event, info):
        # info.run_make("assembly")
        assembly_file = pathlib.Path(info.get_output_dir() + "assembly.s")
        if not assembly_file.exists():
            print("Error in building from makefile")
            return
        # sg.popup_non_blocking('Assembly', assembly_file.read_text())
        sg_show_scrollable_text(assembly_file, 'Assembly')
        

    @staticmethod
    def handle_dump_gimple(event, info):
        # info.run_make("high-gimple")
        gimple_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".gimple")
        if not gimple_file.exists():
            print("Error in building from makefile")
            return
        
        sg_show_scrollable_text(gimple_file, 'Gimple')
        # sg.popup_non_blocking('Gimple', gimple_file.read_text())
    
    @staticmethod
    def handle_dump_lower_gimple(event, info):
        # info.run_make("lower-gimple")
        gimple_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".gimple.lower")
        if not gimple_file.exists():
            print("Error in building from makefile")
            return
        
        sg_show_scrollable_text(gimple_file, 'Lower Gimple')
        # sg.popup_non_blocking('Lower Gimple', gimple_file.read_text())

    @staticmethod
    def handle_dump_cfg(event, info):
        # info.run_make("cfg")
        cfg_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".cfg")
        if not cfg_file.exists():
            print("Error in building from makefile")
            return

        sg_show_scrollable_text(cfg_file, 'CFG')
        # sg.popup_non_blocking('CFG', cfg_file.read_text())

    @staticmethod
    def handle_dump_ssa(event, info):
        ssa_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".ssa")
        if not ssa_file.exists():
            print("Error in building SSA from makefile")
            return

        sg_show_scrollable_text(ssa_file, 'SSA')
        # sg.popup_non_blocking('SSA', ssa_file.read_text())