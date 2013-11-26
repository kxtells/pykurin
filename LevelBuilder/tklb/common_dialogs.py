#
#
# Generic Dialog functions. Common dialogs to be used almost everywhere.
#
#

import tkFileDialog, tkSimpleDialog, tkMessageBox

def open_file_chooser(naming, ftype="*", basepath = None):
    if not basepath:
        basepath = '.'

    somefile = tkFileDialog.askopenfilename(filetypes=[(naming, ftype)],
            initialdir=basepath,
            multiple=False)
    return somefile or u''

def open_image_chooser(naming, basepath = None):
    """Ask to open an image file"""
    if not basepath:
        basepath = '.'

    somefile = tkFileDialog.askopenfilename(
            filetypes=[("ANY IMAGE", "*.png *.jpeg *.gif *.jpg"),
                ("GIF", "*.gif"), ("PNG", "*.png"), ("JPG", "*.jpg"),
                ("JPEG", "*.jpeg"),  ],
            initialdir=basepath,
            multiple=False)
    return somefile or u''

def open_dir_chooser(naming,ftype="*"):
	try:
		somedir = tkFileDialog.askdirectory(title=naming,mustexist=True)
		return somedir
	except:
		return None

def save_file_chooser(naming, ftype=".prop"):
	try:
		somefile = tkFileDialog.asksaveasfilename(filetypes=[(naming, ftype)])
		return somefile
	except:
		return None

def popup_message(title,text):
    return tkMessageBox.showinfo(title,text)

def error_message(title, text):
    tkMessageBox.showerror(title, text)

def show_disclaimer():
    """
        Show a disclaimer saying that this software is shit
    """
    popup_message("BorinotGames Note","This program is provided AS IS :-P\n\
It is just a helper utility, don't expect to be beautiful or bug free in Exotic cases")

def ask_dialog(title, question):
    """A simple ask dialog will return True or False"""
    return tkMessageBox.askyesno(title, question)
