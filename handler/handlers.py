'''
Author: Lin Sinan
Github: https://github.com/linsinan1995
Email: mynameisxiaou@gmail.com
LastEditors: Lin Sinan
Description: 
              
              
              
'''
import PySimpleGUI as sg
import pathlib
from config import * 
from window.window import * 

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
            pass
        else:
            return False
        
        if event in ('Edit Configure', ):
            Configuration.handle_edit(info)
            return True

        return False

    @staticmethod
    def handle_edit(info):
        config_window = window_factory.make_multiline_popup_layout(name = 'Configuration', layout = gen_configure_layout(info))  
        config_event, config_values = config_window.read()
        if config_event == 'Ok':   
            info.update_compiler(config_values[0])
            info.update_demangler(config_values[1])
            info.update_flags(config_values[2])
            info.update_abi(config_values[3])
            info.update_arch(config_values[4])
        
        config_window.close()
        
class Tools:
    rtl_files = None
    @staticmethod
    def handle(event, info):

        if Tools.rtl_files is not None and event in Tools.rtl_files:
            Tools.handle_rtl_listbox(event, info)

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
        elif event in ('Dump RTL', ):
            Tools.handle_dump_rtl(event, info)
        else:
            return False

        return True

    @staticmethod
    def handle_dump_assembly(event, info):
        assembly_file = pathlib.Path(info.get_output_dir() + "assembly.s")
        if not assembly_file.exists():
            print("Error in building from makefile")
            return

        window_factory.make_multiline_popup('Assembly', assembly_file)

    @staticmethod
    def handle_dump_gimple(event, info):
        gimple_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".gimple")
        if not gimple_file.exists():
            print("Error in building from makefile")
            return

        window_factory.make_multiline_popup('Gimple', gimple_file)

    @staticmethod
    def handle_dump_lower_gimple(event, info):
        gimple_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".gimple.lower")
        if not gimple_file.exists():
            print("Error in building from makefile")
            return
        
        window_factory.make_multiline_popup('Lower Gimple', gimple_file)

    @staticmethod
    def handle_dump_cfg(event, info):
        cfg_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".cfg")
        if not cfg_file.exists():
            print("Error in building from makefile")
            return

        window_factory.make_multiline_popup('CFG', cfg_file)

    @staticmethod
    def handle_dump_ssa(event, info):
        ssa_file = pathlib.Path(info.get_output_dir() + info.get_filename() + ".ssa")
        if not ssa_file.exists():
            print("Error in building SSA from makefile")
            return

        window_factory.make_multiline_popup('SSA', ssa_file)

    @staticmethod
    def handle_dump_rtl(event, info):
        files = pathlib.Path(info.get_output_dir() + "rtl").glob(info.get_filename()+".*")
        # get { pass_index : path }
        Tools.rtl_files = {f : f.name.split('.')[-2] for f in files if f.is_file()}
        # get { passname : path }
        Tools.rtl_files = {f.name[f.name.rfind('.') + 1 : len(f.name)] : f for f, _ in sorted(Tools.rtl_files.items(), key=lambda item: item[1])}
        info.load_rtl_window(window_factory.make_listbox(list(Tools.rtl_files.keys()), "Select RTL pass", "RTL"))

    @staticmethod 
    def handle_rtl_listbox(event, info):
        rtl_file = Tools.rtl_files[event]

        if not rtl_file.exists():
            print("Error in reading rtl file")
            return
        
        window_factory.make_multiline_popup("RTL - " + event, rtl_file)