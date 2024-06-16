from Xlib.display import Display
from Xlib import X, XK

# Set up variables
dpy = Display()
root = dpy.screen().root
super_keycode = dpy.keysym_to_keycode(XK.string_to_keysym("Super_L"))
window_ids = []
current_index = 0
root.grab_key(super_keycode, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeAsync)

def is_toplevel_window(window):
    attrs = window.get_attributes()
    return attrs.map_state == X.IsViewable

def fullscreen_window(id):
    global window_ids
    window_id = window_ids[id]
    window = dpy.create_resource_object('window', window_id)
    window.configure(stack_mode=X.Above, width=root.get_geometry().width, height=root.get_geometry().height) 
    window.set_input_focus(X.RevertToParent, X.CurrentTime)
    window.map()
    return None

def update_windows():
    global window_ids
    window_ids = []
    for window in root.query_tree().children:
        if is_toplevel_window(window):
            window_ids.append(window.id)

update_windows()
while True:
    ev = dpy.next_event()

    # Swap between windows
    if ev.type == X.KeyPress and ev.detail == super_keycode:
        current_index = (current_index + 1) % len(window_ids)
        title = fullscreen_window(current_index)

    # Bring window to front if just opened
    elif ev.type == X.CreateNotify:
        update_windows()
        fullscreen_window(-1)