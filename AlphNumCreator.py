from ast import Continue
from cProfile import label
from multiprocessing.sharedctypes import Value
from PIL import ImageFont, ImageDraw, Image
import os
import os.path
from os import path, sep
from fontTools.ttLib import TTFont
import random
import numpy as np
import cv2 as cv
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def textLoader(path):

    drawn_text = ""

    directory = path + '/Text_files/'

    for filename in os.listdir(directory):

        with open(directory+filename) as write_text_file:
            for line in write_text_file:
                drawn_text += line
    return drawn_text


def imageRenderText(string):

    try:
        random_beggin = random.randint(0, len(string)-20)
        random_string_size = random_beggin + random.randint(5, 24)

        current_string = string[random_beggin:random_string_size]
        return current_string
    except:
        print("Cant get image text!")


# Checks .ttf file for given char, if char is not defined in cmap, returns false
def char_in_font(unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(unicode_char) in cmap.cmap:
                return True
    return False


def rowZeroArray():

    rowZero = ['label']

    for collumn in range(0, 6272):
        rowZero.append('pixel'+str(collumn))

    return rowZero


def imageRenderFont(my_path):

    font_label_dict = {}

    with open('dataset_table.csv', 'w+', newline='') as dataset_file:

        writer = csv.writer(dataset_file)
        writer.writerows([rowZeroArray()])

        # Checking important dirs, and adding relativ path for directory
        if path.exists(my_path + "/Fonts") == False:
            messagebox.showerror("Error", 'There is no "Fonts" directory in AlpNumsEnv.\nCreate "Fonts" directory add ".ttf" files and try again.')
            exit()

        directory = my_path + '/Fonts'

        if path.exists(my_path + "/Renders") == False:
            os.mkdir(my_path + "/Renders")

        # Delete this var, this is only for labeling fonts
        numerical_label = -1
        # Iterate over files in that directory
        for filename in os.listdir(directory):

            
            numerical_label += 1
            font_label_dict[filename[:-4]] = numerical_label

            fileNameJoin = os.path.join(directory, filename)

            # Checking if it is a file
            if os.path.isfile(fileNameJoin):
                print(filename)

                # Adds TTF font file as current font, FONT FILES MUST CORESPOND TO ASCII
                num_of_image = 0
                color = 'black'
                try:

                    # Adding diffrent size of the fonts, for diverse sizes
                    for fontSizeIterations in range(0, 5):
                        
                        randomFontSize = random.randrange(20, 24)
                        randomXDraw = random.randrange(0, 120)

                        font = ImageFont.truetype(
                            fileNameJoin, size=randomFontSize)
                        checkFont = TTFont(fileNameJoin)

                        # Iterates trough ASCII printable chars, and draws a picture for every sign

                        for c in range(33, 50, 1):  # range is 33 to 127 for all chars
                            
                            # Char we want to draw on image,
                            drawnChar = chr(c)
                            # Saving on conversions
                            stringOfChar = str(c)

                            # Checks for the char in .ttf file, skips iteration if there is no current char. This is used as we can
                            # create some chars from font files even tho not all of them are defined in .ttf
                            if char_in_font(drawnChar, checkFont) == False:
                                print('There is no char('+drawnChar +') defined in '+fileNameJoin)
                                continue

                            image = Image.new("RGB", (224, 28), (255, 255, 255))
                            draw = ImageDraw.Draw(image)

                            # Adds the text over image, with indexed font. And saves the image under the name of font + ASCII value of char
                            draw.text((randomXDraw, 0), drawnChar,
                                      font=font, fill=color)

                            # NameOfImageNeeds to have '.png' to work
                            # Needs to have '.png' to work
                            NameOfImage = str(
                                str(filename) + str(num_of_image) + '.png')
                            num_of_image += 1

                            print(NameOfImage)

                            # All of given variables from above have the same name as variables in imageCropp() function

                            cv_image = cv.cvtColor(
                                np.array(image), cv.COLOR_RGB2BGR)
                            cv_image_gs = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
                            cv_image_gs = ~cv_image_gs

                            #To write images enable this part
                            #cv.imwrite(my_path + "/Renders/" + NameOfImage, cv_image_gs)

                            image_array = np.asarray(cv_image_gs)

                            oneDimensionArray = image_array.flatten()

                            row_info = [numerical_label]
                            for value in oneDimensionArray:
                                row_info.append(value)

                            writer.writerow(row_info)
                except:
                    print('\nError, cannot render character\n')

                try:

                    for fontSizeIterations in range(0, 5):
                        randomFontSize = random.randrange(20, 24)
                        randomXDraw = random.randrange(0, 30)

                        font = ImageFont.truetype(
                            fileNameJoin, size=randomFontSize)
                        checkFont = TTFont(fileNameJoin)

                        image = Image.new("RGB", (224, 28), (255, 255, 255))

                        draw = ImageDraw.Draw(image)
                        
                        #ERROR: Ovdje baca da ne može kreirat sliku.
                        imageText = imageRenderText(textLoader(my_path))

                        draw.text((randomXDraw, 0), imageText,
                                  font=font, fill=color)
                        NameOfImage = str(
                            str(filename) + str(num_of_image) + '.png')
                        num_of_image += 1
                        print(NameOfImage)

                        cv_image = cv.cvtColor(
                            np.array(image), cv.COLOR_RGB2BGR)
                        cv_image_gs = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
                        cv_image_gs = ~cv_image_gs

                        #To write images enable this part
                        #cv.imwrite(my_path + "/Renders/" + NameOfImage, cv_image_gs)

                        image_array = np.asarray(cv_image_gs)

                        oneDimensionArray = image_array.flatten()

                        row_info = [numerical_label]
                        for value in oneDimensionArray:
                            row_info.append(value)

                        writer.writerow(row_info)
                except:
                    print('\nError, cannot render a sentence\n')

    dataset_file.close()

    with open(my_path + '/font_labels.csv', 'w+', newline='') as font_csv:
        
        writer = csv.writer(font_csv)

        for key, value in font_label_dict.items():
            label_row = [key, value]
            writer.writerow(label_row)

def select_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(tk.END, directory)

def start_process():
    directory = directory_entry.get()
    if directory:
        imageRenderFont(directory)
    else:
        messagebox.showerror("Error", 'No directory selected!')


root = tk.Tk()

directory_entry = tk.Entry(root, width=50)
directory_entry.pack(padx=5, pady=5)

select_button = tk.Button(root, text="Select Directory", command=select_directory)
select_button.pack(padx=5, pady=5)

start_button = tk.Button(root, text="Start Process", command=start_process)
start_button.pack(padx=5, pady=5)

root.mainloop()