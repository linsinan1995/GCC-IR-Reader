import PySimpleGUI as sg
from config import *

# gen a layout of a scollable multiline popup window
def gen_scollable_multiline_window_layout(buf):
    return [ 
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

# generate layout for listbox
def gen_listbox_layout(text, options, key = 'RTL'):
    return [  
                [
                    sg.Text(text)
                ],
                [
                    sg.Listbox(options, size=(15, len(options)), key=key, enable_events=True)
                ], 
                [
                    sg.Button('Exit', key = key + '-Exit')
                ]
            ]

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
            'Dump RTL',
        ]
    ],
    [
        'Help', 
        [
            'About'
        ]
    ]
]


# Layout of gui 
main_window_layout = [
    [
        sg.Menu(menu_layout)
    ],
    [
        sg.Text(
            '> Temp File <', 
            font=('Consolas', 8), 
            size=(WIN_W, 1), 
            key='_INFO_'
        )
    ],
    [
        sg.Multiline(
            font=('Consolas', 12), 
            size=(WIN_W, WIN_H), 
            key='_BODY_'
        )
    ]
]

# Layout of configure window 
def gen_configure_layout(info):
    return  [
                [
                    sg.Text('Compiler', size=(15, 1)), 
                    sg.InputText(default_text = info.get_compiler())
                ],
                [
                    sg.Text('C++Filter', size = (15, 1)), 
                    sg.InputText(default_text = info.get_demangler())
                ],
                [
                    sg.Text('CFLAG', size = (15, 1)), 
                    sg.InputText(default_text = info.get_flags())
                ],
                [
                    sg.Text('ABI', size = (15, 1)), 
                    sg.InputText(default_text = info.get_abi())
                ],
                [
                    sg.Text('ARCH', size = (15, 1)), 
                    sg.InputText(default_text = info.get_arch())
                ],
                [
                    sg.Button('Ok'), 
                    sg.Cancel()
                ]
            ]