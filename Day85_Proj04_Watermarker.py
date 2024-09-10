from tkinter import filedialog
import PIL
from watermarking import Watermarking
from tkinter import *
from tkinter import messagebox
import os
import pathlib

debug = True #enable to auto-populate image paths into UI

#UI contants
FONT_NAME = "Arial"
LABEL_FONT_SIZE = 14
LABEL_FONT_SIZE_SM = 10

#variables used to set parameters and paths
filename = ""
watermark_filename=""
export_filename=""
opacity= 0.7
size_value = .2
position = "br"
working_dir =  cwd = os.getcwd()

water_factory = Watermarking()

def get_processed_with_watermark():
    """gets a processed image object based on the parameters stored in the local variables:
        filename : background/main image path
        watermark_filename: watermark image path
        opacity: opacity of the watermark as a percentage of 1
        size_value: size of the watermark as a percentage of 1
        position : position to place the watermark 
        "tl" :top left
        "tc" :top center
        "tr" :top right
        "bl" :bottom left
        "bc" :bottom center
        "br" :bottom right
    """
    if bad_file_names(False):
        return
    im = PIL.Image.open(filename)
    wa = PIL.Image.open(watermark_filename)
    return water_factory.merge_by_percentage(im, wa, size_value / 100, position, opacity/100)


def preview():
    """ processes and opens a full-size image in order to view before exporting """
    get_processed_with_watermark().show()


def bad_file_names(isExport):
    """Checks if filename and watermark_file name are specified. If isExport is True, it will also check the export_filename"""
    if isExport:
        if not export_filename:
            messagebox.showerror(title="Export Path not specified", message="Please specify an export path.")
            return False
    
    if not filename:
        messagebox.showerror(title="File Path not specified", message="Please specify an file path.")
        return False
    
    if not watermark_filename:
       messagebox.showerror( title="Watermark Path not specified", message="Please specify an watermark path.")
       return False
    
    

def export():
    """ processes the images with the added watermark and exports it to a file"""
    if bad_file_names(True):
        return
    im = PIL.Image.open(filename)
    wa = PIL.Image.open(watermark_filename)

    if export_filename.lower().endswith(('.jpg', '.jpeg')):
            image = water_factory.merge_by_percentage(im, wa, size_value / 100, position, opacity/100).convert("RGB")
    elif export_filename.lower().endswith(('.png')):
        image = water_factory.merge_by_percentage(im, wa, size_value / 100, position, opacity/100).convert("RGBA")
    else:
        messagebox.showerror(title="Unrecognized file type", message=f"Unrecognized file type:{pathlib.Path(export_filename).suffix}")
        export_path.config(text="")
        return
    
    image.save(export_filename)
    if os.path.isfile(export_filename):
        showdirectory = messagebox.askyesno(title="File Exported", message=f"File Exported to : {export_filename}. Would you like to open the export folder?")
    
        if showdirectory :
            folder = os.path.dirname(export_filename)
            path = os.path.realpath(folder)
            os.startfile(path)
    else:
        messagebox.showerror(title="Exported File not Found", message=f"File not found after attempt to export:{export_filename}")

def update_position():
    """ Updates the position varaible based on the UI selection"""
    global position
    if position_var.get():
        position = str(position_var.get())
    print(f"Position {position}:")

def update_opacity(op):
    """ Updates the opacity varaible based on the UI selection"""
    global opacity 
    opacity = opacity_slider.get()
    print(f"opacity {opacity}:")
    
def update_size(si):
    """ Updates the size varaible based on the UI selection"""
    global size_value 
    size_value = size_slider.get()
    print(f"Position {size_value}:")


def open_image():
    """ Browses the local file system to select an image"""
    global filename
    filename = filedialog.askopenfile(mode='r', initialdir=working_dir, title="Select An Image", filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    image_path.config(text=filename.name, highlightbackground="gray", highlightthickness=1)
    
def open_watermark():
    """ Browses the local file system to select an watermark image"""
    global watermark_filename
    watermark_filename = filedialog.askopenfile(mode='r', initialdir=working_dir, title="Select An Image", filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png")))
    watermark_path.config(text=watermark_filename.name, highlightbackground="gray", highlightthickness=1)
    
def set_export_path():
    """ Browses the local file system to set an export path"""
    global export_filename
    export_filename = filedialog.asksaveasfilename( initialdir=working_dir, title="Specify An Image",  filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))
    export_path.config(text=export_filename, highlightbackground="gray", highlightthickness=1)
    
    if not export_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        messagebox.showerror( title="Invalid Export File Path", message="Please specify a file of type '.png', '.jpg', '.jpeg'")
        return
    
    export_path.config(text=export_filename.name, highlightbackground="gray", highlightthickness=1)
    

#setup the UI 
window = Tk()
window.title("Watermarker")
window.config(padx=50, pady=50)

canvas = Canvas (width=600, height=600, highlightthickness=0)

#add the labels
image_label = Label(text="Image:", font=(FONT_NAME, LABEL_FONT_SIZE))
image_label.grid(row=1, column = 0, sticky=E, padx = 20, pady=20)

watermark_label = Label(text="Watermark Image:", font=(FONT_NAME, LABEL_FONT_SIZE))
watermark_label.grid(row=2, column = 0, sticky=E, padx = 20, pady=20)

position_label = Label(text="Watermark Position:", font=(FONT_NAME, LABEL_FONT_SIZE))
position_label.grid(row=3, column = 0,  columnspan =1, sticky=E, padx = 20)

size_label = Label(text="Watermark Size:", font=(FONT_NAME, LABEL_FONT_SIZE))
size_label.grid(row=6, column = 0,  columnspan =1, sticky=E, padx = 20, pady=20)

opacity_label = Label(text="Watermark Opacity:", font=(FONT_NAME, LABEL_FONT_SIZE))
opacity_label.grid(row=6, column = 3,  columnspan =1, sticky=E, padx = 20, pady=20)

export_label = Label(text="Export:", font=(FONT_NAME, LABEL_FONT_SIZE))
export_label .grid(row=20, column = 0,  columnspan =1, sticky=E, padx = 20, pady=20)

#Add the interactive input objects
image_path = Label( width = 96, font=(FONT_NAME, LABEL_FONT_SIZE_SM))
image_path.config(highlightbackground="red", highlightthickness=2)
image_path.grid(row=1, column = 1, columnspan = 3,sticky = W)

watermark_path = Label(width = 96, font=(FONT_NAME, LABEL_FONT_SIZE_SM))
watermark_path.config(highlightbackground="red", highlightthickness=2)
watermark_path.grid(row=2, column = 1, columnspan = 3,sticky = W)

#   Position radio buttons
position_var = StringVar()
update_position()

position1 = Radiobutton(window, text="top left", variable=position_var, value="tl",  command=update_position)
position1.grid(row=3, column = 1,sticky = W)

position2 = Radiobutton(window, text="top center", variable=position_var, value="tc",  command=update_position)
position2.grid(row=4, column = 1,sticky = W)

position3 = Radiobutton(window, text="top right", variable=position_var, value="tr",  command=update_position)
position3.grid(row=5, column = 1,sticky = W)

position4 = Radiobutton(window, text="bottom left", variable=position_var, value="bl",  command=update_position)
position4.grid(row=3, column = 2,sticky = W)

position5 = Radiobutton(window, text="bottom center", variable=position_var, value="bc",  command=update_position)
position5.grid(row=4, column = 2,sticky = W)

position6 = Radiobutton(window, text="bottom right", variable=position_var, value="br", command=update_position)
position6.grid(row=5, column = 2,sticky = W)
position6.select()

#sliders
size_slider = Scale(window, from_=1, to=100, orient=HORIZONTAL, command=update_size)
size_slider.set(20)
size_slider.grid(row=6, column = 1,  columnspan = 1)

opacity_slider =Scale(window, from_=1, to=100, orient=HORIZONTAL,command=update_opacity)
opacity_slider.set(70)
opacity_slider.grid(row=6, column = 4,  columnspan = 1)

export_path = Label(width = 96, font=(FONT_NAME, LABEL_FONT_SIZE_SM))
export_path.config(highlightbackground="red", highlightthickness=2)
export_path.grid(row=20, column = 1, columnspan = 3, sticky = W)


#Add the buttons
open_image_button = Button(text="Browse", command=open_image)
open_image_button .grid(row=1, column=4, sticky=E, ipadx=20, padx=20)

open_watermark_button = Button(text="Browse", command=open_watermark)
open_watermark_button .grid(row=2, column=4, sticky=E, ipadx=20, padx=20)

preview_button = Button(text="Preview",  command=preview, width=50)
preview_button.grid(row=19, column=2, columnspan=2, ipady=10, pady=10)

export_path_button = Button(text="Set Path", command=set_export_path )
export_path_button.grid(row=20, column = 4, columnspan = 1,ipadx=20, padx=10, sticky=W)

export_button = Button(text="Export", command=export , width = 50)
export_button.grid(row=21, column = 2, columnspan = 2, ipady=10, pady=10)


#if debug is set to true, auto-populate default image and export values.
if debug:
    filename=f"{working_dir}//beach.png"
    watermark_filename = f"{working_dir}//socalreggae.gif"
    export_filename = f"{working_dir}//export.jpg"
    
    image_path.config(text=filename, highlightbackground="blue", highlightthickness=1)
    watermark_path.config(text=watermark_filename, highlightbackground="blue", highlightthickness=1)
    export_path.config(text=export_filename, highlightbackground="blue", highlightthickness=1)


window.mainloop()