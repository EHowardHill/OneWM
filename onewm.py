from Xlib.display import Display
from Xlib import X, XK

# Set up variables
dpy = Display()
root = dpy.screen().root
super_keycode = dpy.keysym_to_keycode(XK.string_to_keysym("Super_L"))
window_ids = []
current_index = 0
root.grab_key(super_keycode, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)
first = True

def fullscreen_window(id):
    global window_ids
    print("#" + str(id))
    print(window_ids)
    window_id = window_ids[id]
    for other_id in window_ids:
        if other_id != window_id:
            other_window = dpy.create_resource_object('window', other_id)
            other_window.unmap()
    window = dpy.create_resource_object('window', window_id)
    window.configure(width=root.get_geometry().width, height=root.get_geometry().height)
    window.map()

def update_windows():
    global window_ids
    window_ids = []
    for window in root.query_tree().children:
        window_ids.append(window.id)
    print(window_ids)

update_windows()
while True:
    ev = dpy.next_event()

    # Swap between windows
    if ev.type == X.KeyPress and ev.detail == super_keycode:
        if window_ids:
            current_window = dpy.create_resource_object('window', window_ids[current_index])
            current_index = (current_index + 1) % len(window_ids)
            fullscreen_window(current_index)

    # Bring window to front if just opened
    elif ev.type == X.CreateNotify or first:
        first = False
        update_windows()
        fullscreen_window(-1)
