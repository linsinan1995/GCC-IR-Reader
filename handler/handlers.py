'''
Author: Lin Sinan
Github: https://github.com/linsinan1995
Email: mynameisxiaou@gmail.com
LastEditors: Lin Sinan
Description: 
              
              
              
'''
import PySimpleGUI as sg
import pathlib

def about_me(event, info):
    if event in ('About',):
        sg.popup_no_wait('"All great things have small beginnings" - Peter Senge')
        return True
    else:
        return False

class Files:
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

    @staticmethod
    def open_file(info):
        '''Open _file and update the infobar'''
        filename = sg.popup_get_file('Open')
        if filename:
            _file = pathlib.Path(filename)
            info.update_window('_BODY_', _file.read_text())
            info.update_window('_INFO_', _file.absolute())
            info.update_file(_file)
            Files.clean_output_cache(info.get_filename())
            info.run_make("app")

    @staticmethod
    def save_file(info):
        '''Save _file instantly if already open; otherwise use `save-as` popup'''
        if info.get_file():
            info.write_to_file(info.query_window('_BODY_'))
        else:
            Files.save_file_as(info.get_filename())

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
        info.update_window(key = '_BODY_OUT_', val = assembly_file.read_text())
        info.update_window(key = '_INFO_OUT_', val = "Assembly")

    @staticmethod
    def handle_dump_gimple(event, info):
        # info.run_make("high-gimple")
        gimple_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".gimple")
        if not gimple_file.exists():
            print("Error in building from makefile")
            return
        info.update_window(key = '_BODY_OUT_', val = gimple_file.read_text())
        info.update_window(key = '_INFO_OUT_', val = "Gimple")
    
    @staticmethod
    def handle_dump_lower_gimple(event, info):
        # info.run_make("lower-gimple")
        gimple_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".gimple.lower")
        if not gimple_file.exists():
            print("Error in building from makefile")
            return
        info.update_window(key = '_BODY_OUT_', val = gimple_file.read_text())
        info.update_window(key = '_INFO_OUT_', val = "Lower Gimple")

    @staticmethod
    def handle_dump_cfg(event, info):
        # info.run_make("cfg")
        cfg_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".cfg")
        if not cfg_file.exists():
            print("Error in building from makefile")
            return
        info.update_window(key = '_BODY_OUT_', val = cfg_file.read_text())
        info.update_window(key = '_INFO_OUT_', val = "CFG")

    @staticmethod
    def handle_dump_ssa(event, info):
        ssa_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".ssa")
        if not ssa_file.exists():
            print("Error in building SSA from makefile")
            return
        info.update_window(key = '_BODY_OUT_', val = ssa_file.read_text())
        info.update_window(key = '_INFO_OUT_', val = "SSA")