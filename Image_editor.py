import cv2
import os
import tkinter as tk
import numpy as np
import random
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image 
global count,emig
global bright,con
global frp,tname#list of paths
frp=[]
tname=[]
con=1
bright=0

def getpath(path):
    a=path.split(r'/')
    print(a)
    fname=a[-1]
    l=len(fname)
    location=path[:-l]
    return location

def getfoldername(path):
    a=path.split(r'/')
    print(a)
    name=a[-1]
    return name

def getfilename(path):
    a=path.split(r'/')
    fname=a[-1]
    a=fname.split('.')
    a=a[0]
    return a

def openfilename():
    filename = filedialog.askopenfilename(title ='"pen') 
    return filename 


def open_img():
    global x, panelA, panelB
    global count,eimg,location,filename
    count=0
    x = openfilename() 
    img = Image.open(x) 
    eimg=img
    img = ImageTk.PhotoImage(img)
    temp=x
    location=getpath(temp)
    filename=getfilename(temp)
    if panelA is None or panelB is None:
        panelA = Label(image=img)
        panelA.image = img
        panelA.pack(side="left", padx=10, pady=10)
        panelB = Label(image=img)
        panelB.image = img
        panelB.pack(side="right", padx=10, pady=10)
    else:
        panelA.configure(image=img)
        panelB.configure(image=img)
        panelA.image = img
        panelB.image = img

def sketch():
    image = cv2.imread(x)
    global count,eimg
    count=1
    if image is None:
        print("can not find image")
        sys.exit()
    # gray scale
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #invert gray image
    grayImageInv = 255 - grayImage
    # gaussian blur
    grayImageInv = cv2.GaussianBlur(grayImageInv, (21, 21), 0)
    #blend using color dodge
    output = cv2.divide(grayImage, 255-grayImageInv, scale=256.0)
    #edge 
    gray = cv2.medianBlur(grayImage, 1)
    edges = cv2.adaptiveThreshold(gray, 10, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(output, 6, 60, 200)
    global o1
    o1 = cv2.bitwise_and(color, color, mask=edges)
    image = Image.fromarray(o1)
    eimg=image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image
   
    
def sharp():
    image = cv2.imread(x)[:, :, ::-1]
    global count,eimg
    count=2
    if image is None:
        print("can not find image")
        sys.exit()
    k2 = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])
    global o2
    o2 = cv2.filter2D(image, -1, k2)
    image = Image.fromarray(o2)
    eimg=image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def cartoon():
    image = cv2.imread(x)[:, :, ::-1]
    global count,eimg
    count=4
    if image is None:
        print("can not find image")
        exit()
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.GaussianBlur(image_gray, (3, 3), 0)
    image_edge = cv2.Laplacian(image_gray, -1, ksize=5)
    image_edge = 255 - image_edge
    ret, image_edge = cv2.threshold(image_edge, 150, 255, cv2.THRESH_BINARY)
    edgePreservingImage = cv2.edgePreservingFilter(image, flags=2, sigma_s=50, sigma_r=0.4)
    global o4
    output =np.zeros(image_gray.shape)
    output = cv2.bitwise_and(edgePreservingImage, edgePreservingImage, mask=image_edge)
    o4 = cv2.convertScaleAbs(output,alpha=1, beta=60)
    image = Image.fromarray(o4)
    eimg=image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def conto():
    img = cv2.imread(x)[:, :, ::-1]
    global count,eimg
    count=3
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #check if image exists
    if image is None:
        print("can not find image")
        sys.exit()     
    #apply canny to the input image
    canny = cv2.Canny(image, 50, 150, apertureSize=3)
    #find contours
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    #output image to draw contours on
    output = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    #draw contours
    for i in range(0, len(contours)):
        cv2.drawContours(output, contours, i, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)
    global o3
    o3=output
    image = Image.fromarray(o3)
    eimg=image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def jeetesh():
    image = cv2.imread(x)[:, :, ::-1] 
    global count,eimg
    count=5
    result = np.copy(image)

    original_Val = np.array([0, 50, 100, 150, 200, 255])
    red_Val = np.array([0, 20, 40, 75, 150, 255])
    blue_Val = np.array([0, 80, 150, 190, 220, 255])
    all_Val = np.arange(0, 256)
    redLookupTable = np.interp(all_Val, original_Val, red_Val)

    blueLookupTable = np.interp(all_Val, original_Val, blue_Val)

    B, G, R = cv2.split(result)
    R = cv2.LUT(R, redLookupTable)
    R = np.uint8(R)
    B = cv2.LUT(B, blueLookupTable)
    B = np.uint8(B)

    result = cv2.merge([B, G, R])
    global o5
    o5=result
    image = Image.fromarray(o5)
    eimg=image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image

def reset():
    image = cv2.imread(x)[:, :, ::-1] 
    global count,eimg
    count=6
    global o6
    o6=image
    image = Image.fromarray(o6)
    eimg=image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image
    
def adjust_brightness(value):  
    
    value=int(float(value))
    txtbrit_per= Label(sliderframe,text=str(value)+"%").grid(row=0,column=5)
    global bright,eimg
    bright=value
    if count == 0:
        img = cv2.imread(x)[:, :, ::-1]
    elif count == 1:
        img = o1
    elif count == 2:
        img = o2
    elif count == 3:
        img = o3
    elif count == 4:
        img = o4
    elif count == 5:
        img = o5
    elif count == 6:
        img = o6
    if img is None:
        print("can not find image")
        sys.exit()
    final_output = cv2.convertScaleAbs(img,alpha=con, beta=value)
    image = Image.fromarray(final_output)
    eimg=image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image
    
def adjust_contrast(value):  
    value=int(float(value))
    global con,eimg
    con=value
    txtcon_per= Label(sliderframe,text=str(int((float((value-1)/4)*100)))+"%").grid(row=1,column=5)
    if count == 0:
        img = cv2.imread(x)[:, :, ::-1]
    elif count ==1:
        img = o1
    elif count == 2:
        img = o2
    elif count == 3:
        img = o3
    elif count == 4:
        img = o4
    elif count == 5:
        img = o5
    elif count == 6:
        img = o6
    if img is None:
        print("can not find image")
        sys.exit()
    final_output = cv2.convertScaleAbs(img,alpha=value, beta=bright)
    image = Image.fromarray(final_output)
    eimg=image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image 

def save():
    global location,filename,eimg
    eimg.save(location+filename+r"_edit.png")

###########################

    
win = tk.Tk()
win.title("Aviato")
win.resizable(width = True, height = True) 
menubar = Menu(win)


           
# Adding File Menu and commands
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='New File', command=open_img)
file.add_command(label='Save', command=save)
file.add_command(label='Exit', command=win.destroy)

#frame for buttons and slider
bframe=Frame(win)
bframe.pack(side=BOTTOM,fill=Y,pady=10)

#frame for the image
imgframe=Frame(win)
panelB=None
panelA=None
imgframe.pack(side=TOP,fill=Y)

#frame for slider
sliderframe=Frame(bframe)
sliderframe.pack(side=TOP)

#frame for Buttons
butframe=Frame(bframe)
butframe.pack(side=BOTTOM)

    
#buttons in the button frame
ttk.Button(butframe, text="sketch", command=sketch).grid(column=0, row=0)
ttk.Button(butframe, text="sharpen", command=sharp).grid(column=1, row=0)
ttk.Button(butframe, text="contour",command=conto).grid(column=2, row=0)
ttk.Button(butframe, text="cartoon", command=cartoon).grid(column=3, row=0)
ttk.Button(butframe, text="kelvin", command=jeetesh).grid(column=4, row=0)
ttk.Button(butframe, text="reset", command=reset).grid(column=5, row=0)

#slider
txtbrit= Label(sliderframe,text="Brightness:").grid(row=0,column=3)
txtcon=Label(sliderframe,text="Contrast:").grid(row=1,column=3)
slider=ttk.Scale(sliderframe,from_=0,to=100,command=adjust_brightness).grid(row=0,column=4)
slider=ttk.Scale(sliderframe,from_=1,to=5,command=adjust_contrast).grid(row=1,column=4)
txtbrit_per= Label(sliderframe,text="0%").grid(row=0,column=5)
txtcon_per= Label(sliderframe,text="0%").grid(row=1,column=5)
#======================
# Start GUI
#======================

win.config(menu = menubar)
win.mainloop()