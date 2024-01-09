# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 22:51:36 2023
This program creates a simple text editor using tkinter. 
@author: aslama2
"""

from pathlib import WindowsPath
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from pathlib import Path


#command to exit
def exit_sys():
    root.quit()

#command for new file
def new_file():
    root.title("Untitled")
    file = None
    text.delete("1.0", tk.END)
    global current_file
    current_file= "None"

#command for open button
def open_file():
    filepath = filedialog.askopenfilename(
        filetypes = [("Text Files", "*.txt"), ("All Files", "*.*")])
    
    if not filepath:
        return
    
    f = open(filepath, "r")
    text.delete("1.0", tk.END)
    txt = f.read()
    text.insert(tk.END, txt)
    f.close()
    root.title("Text Editor - " + Path(filepath).stem)

    global current_file
    current_file = filepath

#command for save button
def save_file():
        if(current_file == "None"):
            saveas_file()
        else:
            print(current_file)
            f = open(current_file, "w")
            txt = text.get("1.0", tk.END)
            f.write(txt)
            f.close()

#command for save as button
def saveas_file():
    filepath = asksaveasfilename( defaultextension = ".txt",
        filetypes = [("Text Files", "*.txt"), ("All Files", "*.*")])
    
    if not filepath:
        return
    
    f = open(filepath ,"w")
    txt = text.get("1.0", tk.END)
    f.write(txt)
    f.close()
    root.title("Text Editor - " + Path(filepath).stem)

    global current_file
    current_file = filepath

#command for cut
def cut_txt():
     content = text.get(SEL_FIRST, SEL_LAST)
     text.delete(SEL_FIRST, SEL_LAST)
     root.clipboard_clear()
     root.clipboard_append(content)

#command for copy
def copy_txt():
    content = text.get(SEL_FIRST, SEL_LAST)
    root.clipboard_clear()
    root.clipboard_append(content)

#command for paste
def paste_txt():
    content = root.clipboard_get()
    text.insert(tk.INSERT, content)

#command for delete
def delete_txt():
    text.delete(SEL_FIRST, SEL_LAST)
    
#command for select all
def select_all():
    text.tag_add("sel", "1.0", tk.END)
    return "break"  

#command for highlight
def highlight():
    text.tag_add("start", SEL_FIRST, SEL_LAST)
    text.tag_config("start", background= "yellow", foreground= "black")

#command to un-highlight
def unhighlight():
    text.tag_add("start", SEL_FIRST, SEL_LAST)
    text.tag_config("start", background= "white", foreground= "black")

#show live updated info
def update(event):
   chars = str(len(text.get("1.0", "end-1c")))
   line= text.index(INSERT).split(".")[0]
   wordc = str(len(text.get("1.0", "end-1c").split()))
   info.config(text= f"Line Number: {line} Word Count: {wordc} Total Characters: {chars}")

#create window and label text editor
root = tk.Tk()
root.title("Text Editor")
root.geometry("800x400")
current_file = "None"

#menu bar
menu = tk.Menu(root)
root.config(menu=menu)
#menu = tk.Menu(root, background = "gray" , relief= tk.GROOVE, bd=2)

#create text box
text = tk.Text(root, foreground= "black", background = "white", 
               cursor="xterm", font = ("arial", 12), wrap= tk.WORD, undo= TRUE)
text.grid(row = 0, column= 0, sticky = "nsew", padx= 5, pady =5)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#create info bar
info = tk.Label(root, text= "", bg= "gray", height= 1)
info.grid(row = 1, column= 0, sticky = "we")
text.bind('<KeyPress>', update)
text.bind('<KeyRelease>', update)


#scrollbar
scrollbar = Scrollbar(root)
scrollbar.grid(row =0, column =1, sticky= "ns")
scrollbar.config(command = text.yview)
text.config(yscrollcommand = scrollbar.set)

#create drop down menu: file
file_menu = tk.Menu(menu)
menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "New", command= new_file)
file_menu.add_command(label = "Open", command = open_file)
file_menu.add_command(label = "Save", command = save_file)
file_menu.add_command(label = "Save as...", command = saveas_file)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command = exit_sys)

#create a dropdown menu: edit
edit_menu = tk.Menu(menu)
menu.add_cascade(label = "Edit", menu = edit_menu)
edit_menu.add_command(label = "Undo", command = text.edit_undo)
edit_menu.add_command(label = "Redo", command = text.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label = "Cut", command = cut_txt)
edit_menu.add_command(label = "Copy", command = copy_txt)
edit_menu.add_command(label = "Paste", command= paste_txt)
edit_menu.add_command(label = "Delete", command= delete_txt)

#ceate a dropdown menu: tools
slct_menu = tk.Menu(menu)
menu.add_cascade(label="Tools", menu= slct_menu)
slct_menu.add_command(label ="Select All", command= select_all)
slct_menu.add_command(label = "Highlight", command= highlight )
slct_menu.add_command(label = "Un-Highlight", command= unhighlight )


root.mainloop()
