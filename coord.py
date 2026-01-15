from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed: 
        print(f"Clicked at: ({x}, {y})")

def start_listener():
    with mouse.Listener(on_click=on_click) as listener:
        print("Listening for clicks... (Press Ctrl+C to stop)")
        listener.join()

if __name__ == "__main__":
    start_listener()

