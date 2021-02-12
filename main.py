from tkinter import filedialog, Tk, StringVar, Label, Button, mainloop, Entry
import cv2
import numpy as np
from os import walk
import os
import sys
from pathlib import Path

def remove_black_borders():
    for (dirpath, dirnames, filenames) in walk(input_folder_path.get()):
        print(filenames)
        print(dirpath)
        for file in filenames:
            try:
                img = cv2.imread(os.path.join(dirpath, file))
            except:
                continue
            alg = ""
            threshold = int(threshold_var.get())
            if alg == "grayscale":
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnt = contours[0]
                x, y, w, h = cv2.boundingRect(cnt)
                crop = img[y:y + h, x:x + w]
            else:
                if len(img.shape) == 3:
                    flatImage = np.max(img, 2)
                else:
                    flatImage = img
                assert len(flatImage.shape) == 2

                rows = np.where(np.max(flatImage, 0) > threshold)[0]
                if rows.size:
                    cols = np.where(np.max(flatImage, 1) > threshold)[0]
                    crop = img[cols[0]: cols[-1] + 1, rows[0]: rows[-1] + 1]
                else:
                    crop = img[:1, :1]
            relpath = os.path.relpath(dirpath, input_folder_path.get())
            Path(os.path.join(output_folder_path.get(), relpath)).mkdir(parents=True, exist_ok=True)
            cv2.imwrite(os.path.join(output_folder_path.get(), relpath, file), crop)


root = Tk()

input_folder_path = StringVar()
output_folder_path = StringVar()
threshold_var = StringVar()
threshold_var.set("220")


if len(sys.argv) > 1:
    print(sys.argv[1])
    print(sys.argv[2])
    input_folder_path.set(sys.argv[1])
    output_folder_path.set(sys.argv[2])
    remove_black_borders()
    exit(0)


def browse_button_1():
    filename = filedialog.askdirectory()
    input_folder_path.set(filename)
    print(filename)

def browse_button_2():
    filename = filedialog.askdirectory()
    output_folder_path.set(filename)
    print(filename)


root.geometry("500x200")
root.title("remove black borders")

# input folder
lbl1 = Label(master=root, textvariable=input_folder_path)
lbl1.grid(row=0, column=1)
button2 = Button(text="Set input folder", command=browse_button_1)
button2.grid(row=0, column=3)

# output folder
lbl2 = Label(master=root, textvariable=output_folder_path)
lbl2.grid(row=1, column=1)
button1 = Button(text="Set output folder", command=browse_button_2)
button1.grid(row=1, column=3)

# text box
lbl2 = Label(master=root, text="threshold (set between 0 and 300")
lbl2.grid(row=2, column=1)
threshold_text = Entry(master=root, textvariable=threshold_var)
threshold_text.grid(row=2, column=3)

# click button
button1 = Button(text="Remove black borders", command=remove_black_borders)
button1.grid(row=3, column=3)


mainloop()