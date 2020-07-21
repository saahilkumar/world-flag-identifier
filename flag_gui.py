import tkinter as tk
import flagpy as fp
from PIL import Image, ImageTk

HEIGHT = 600
WIDTH = 600

root = tk.Tk()
root.title("Flag Visualizer")
flag_df = fp.get_flag_df()

def closest_flag(flag_left):
    '''
    Sets the right flag to the flag that is most similar to the given flag.

    Parameters
    ----------
    flag_left : str
        The name of the country whose flag is being displayed on the left
    '''
    chosen_flag_right.set(fp.closest_flag(flag_left))

def farthest_flag(flag_left):
    '''
    Sets the right flag to the flag that is least similar to the given flag.

    Parameters
    ----------
    flag_left : str
        The name of the country whose flag is being displayed on the left
    '''
    chosen_flag_right.set(fp.farthest_flag(flag_left))

def swap():
    '''
    Swaps the left and right flags.
    '''
    temp = chosen_flag_left.get()
    chosen_flag_left.set(chosen_flag_right.get())
    chosen_flag_right.set(temp)

def update_flags():
    '''
    Updates the size and value of the two flags. This function is called every
    10 milliseconds to ensure that the flags are always updated.
    '''
    # setting the width/height of the flags based on the dimensions of the canvas itself
    flag_width = int(min(frame.winfo_width(), frame.winfo_height()) / 2.5)
    flag_height = int(flag_width / 2)

    # updating size/image of the left flag
    img_left = Image.fromarray(flag_df["flag"].loc[chosen_flag_left.get()])
    img_left = img_left.resize((flag_width, flag_height), Image.ANTIALIAS)
    flag_img_left = ImageTk.PhotoImage(image = img_left)
    flag_left.configure(image=flag_img_left)
    flag_left.image = flag_img_left

    # updating size/image of the right flag
    img_right = Image.fromarray(flag_df["flag"].loc[chosen_flag_right.get()])
    img_right = img_right.resize((flag_width, flag_height), Image.ANTIALIAS)
    flag_img_right = ImageTk.PhotoImage(image = img_right)
    flag_right.configure(image=flag_img_right)
    flag_right.image = flag_img_right

    # updating the "distance" label
    dist = int(fp.flag_dist(chosen_flag_left.get(), chosen_flag_right.get()))
    dist_label.configure(text = "mse: " + str(dist))
    dist_label.text = "mse: " + str(dist)

    # rerunning this method every 10 milliseconds
    root.after(10, update_flags)

# the canvas
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

# the frame
frame = tk.Frame(root, bg="#80c1ff", bd = 10)
frame.place(relx = 0.05, rely = 0.05, relw = 0.9, relh = 0.9)

# the chosen flag variables
chosen_flag_left = tk.StringVar(root)
chosen_flag_left.set("Canada")

chosen_flag_right = tk.StringVar(root)
chosen_flag_right.set("The United States")

# the dropdown menu to choose the left flag
dropdown_left = tk.OptionMenu(frame, chosen_flag_left, *fp.get_country_list())
dropdown_left.place(relx = 0.05, rely = 0.8, relwidth = 0.4, anchor = "nw")

# the dropdown menu to choose the left flag
dropdown_right = tk.OptionMenu(frame, chosen_flag_right, *fp.get_country_list())
dropdown_right.place(relx = 0.95, rely = 0.8, relwidth = 0.4, anchor = "ne")

# the flags
root.update()
flag_width = int(min(frame.winfo_width(), frame.winfo_height()) / 6)
flag_height = int(flag_width / 2)

img_left = Image.fromarray(flag_df["flag"].loc[chosen_flag_left.get()])
img_left = img_left.resize((flag_width, flag_height), Image.ANTIALIAS)
flag_img_left = ImageTk.PhotoImage(image = img_left)
flag_left = tk.Label(frame, image = flag_img_left)
flag_left.place(relx = 0.25, rely = 0.2, anchor = "center")

img_right = Image.fromarray(flag_df["flag"].loc[chosen_flag_right.get()])
img_right = img_right.resize((flag_width, flag_height), Image.ANTIALIAS)
flag_img_right = ImageTk.PhotoImage(image = img_right)
flag_right = tk.Label(frame, image = flag_img_right)
flag_right.place(relx = 0.75, rely = 0.2, anchor = "center")

# the dist between the two flags
dist = int(fp.flag_dist(chosen_flag_left.get(), chosen_flag_right.get()))
dist_label = tk.Label(frame, text = "mse: " + str(dist))
dist_label.place(relx = 0.5, rely = 0.5, relwidth = 0.4, relheight = 0.1, anchor = "center")

# closest flag button
button = tk.Button(frame, text = "Closest Flag", command = lambda: closest_flag(chosen_flag_left.get()))
button.place(relx = 0.6, rely = 0.9, relwidth = 0.2, relheight = 0.1)

# farthest flag button
button2= tk.Button(frame, text = "Farthest Flag", command = lambda: farthest_flag(chosen_flag_left.get()))
button2.place(relx = 0.2, rely = 0.9, relwidth = 0.2, relheight = 0.1)

# swap flags button
swap_button = tk.Button(frame, text = "<-->", command = lambda: swap())
swap_button.place(relx = 0.5, rely = 0.6, relwidth = 0.2, anchor = "center")

# calling method to update the flags
update_flags()

root.mainloop()