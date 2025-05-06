import FreeSimpleGUI as sg

layout = [[sg.Text("You can resize this window!")],
          [sg.Multiline(size=(40, 10))]]

window = sg.Window("Resizable Example", layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

window.close()
