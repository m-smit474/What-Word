import PySimpleGUI as sg

EXIT_BUTTON = sg.WIN_CLOSED

# default settings
bw = {'size':(7,2), 'font':('Franklin Gothic Book', 24), 'button_color':("black","#F8F8F8")}
bt = {'size':(7,2), 'font':('Franklin Gothic Book', 24), 'button_color':("black","#F1EABC")}
bo = {'size':(24,2), 'font':('Terminal', 22), 'button_color':("black","green"), 'focus':True}
bn = {'size':(10,1), 'font':('Terminal', 22), 'button_color':("black","red")}
td = {'font':('Terminal', 22), 'background_color':("#272533")}
cl = {'expand_x':'True', 'background_color':'#272533'}

frame_layout = [
    [sg.T('', key="-GUESSED-", background_color='#272533', size=(24,2))]
]

guess_layout = [
    # Row 3 
    [sg.In('Guess Here', size=(60, 1), enable_events=True, key="-GUESS-")], 
    # Row 4  
    [sg.Button('Guess!',**bo, bind_return_key=True)]
]

info_layout = [
    [sg.Text("Lives:", **td), sg.Text("10", key="-LIVES-", **td),
    sg.Text("Score:", **td), sg.Text("0", key="-SCORE-", **td)]
]

control_layout = [
    # Row 3 
    [sg.Button('NEW GAME',**bn)], 
    # Row 4  
    [sg.Button('Restart', **bn)]
]

layout = [
     # Row 1
    [sg.Col(control_layout, element_justification='left', **cl),
    sg.Col(info_layout, element_justification='center', **cl), 
    sg.Frame('Letters Guessed', frame_layout, title_color=None, element_justification='right', background_color='#272533')],
    # Row 2
    [sg.Text("Welcome!", size=(48,1), justification='center', background_color='black', text_color='red', 
        font=('Digital-7',24), relief='sunken', key="_DISPLAY_")],
    [sg.Button('Procedural', **bn),
    sg.Col(guess_layout, element_justification='center', **cl),
    sg.Button('Info', **bn)]
]


window = sg.Window('What Word?!', layout=layout, background_color="#272533",  return_keyboard_events=True)