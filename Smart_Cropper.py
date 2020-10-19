# Import Required Libraries
import pygame
import tkinter
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog 
import os
import time
import cv2
import sys
import numpy as np
from pygame.locals import *

#Set Up tkinter 
root = tkinter.Tk()
root.attributes("-topmost", True)
root.withdraw()

# Dimensions
W = 1366
H = 768
img_width = 1024
img_height = 576
img_path = ''

# Load Images 
pygame.display.set_caption("Image_Cropper")
cross = pygame.transform.scale(pygame.image.load(os.path.join('images','cross.png')), (40,40))
MAIN = pygame.image.load(os.path.join('images', 'main3.png'))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join('images','bg.png')), (W, H))

# Create Rect Object for buttons
crop = pygame.Rect(1126, 223, 208, 72)
enhance = pygame.Rect(1126, 348, 208, 72)
bw = pygame.Rect(1127, 471, 208, 72)
save = pygame.Rect(1127, 598, 208, 72)
select = pygame.Rect(455, 689, 334, 68)
points = []

# Points class for points to be shown on images
class Points:
    
    
    img = cross
    rect = img.get_rect()
    
    moving = False

    def __init__(self,x,y):

        self.x=x
        self.y=y
        self.pos = (x,y)
        self.rect = pygame.Rect(self.x,self.y,40,40)

    def draw(self,win):     
        if self.moving:
            self.rect.center = pygame.mouse.get_pos()
            a, b= self.rect.center
            self.x, self.y = a-20 , b-20
        win.blit(self.img, (self.x, self.y))

# Funtion to check click on image        
def Button_click(event,button):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position
            if button.collidepoint(mouse_pos):
                return True
                                                                              
# Open window to search and get path of image
def Open_file():
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilename(title ='"pen')
    root.lift()
    if len(tempdir) > 0:
        return tempdir
# To take resolution of image
class Resolution(simpledialog.Dialog):
    x = 0
    y = 0

    def body(self, master):

        Label(master, text="Enter Resolution ").grid(row=0)
        Label(master, text="Width (x):").grid(row=1)
        Label(master, text="Height (y):").grid(row=2)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        return self.e1 # initial focus

    def apply(self):
        self.x = self.e1.get()
        self.y = self.e2.get()
        #print (first, second )

# Draw main background image
def Draw_Main(win,flag):
    win.blit(MAIN,(0,0))
    if flag:
        pygame.display.update()

# Draw 4 cross images(points) and connect them by lines
def Draw_Window(win,tl,tr,bl,br,img , cropped, dx, dy):
    global points
    r = (1024-dx)//2 + 59
    t = 96
    win.blit(img,(r,t))
    if not cropped:
        tl.draw(win)
        tr.draw(win)
        bl.draw(win)
        br.draw(win)
    points = [tl.rect.center, tr.rect.center, bl.rect.center, br.rect.center ]
    p2 = [tr.rect.center, tl.rect.center, bl.rect.center, br.rect.center]
    if not cropped:
        pygame.draw.polygon(win,(255,0,0), p2,  2)   
    pygame.display.update()

# Make 4 point images draggable    
def point_event(event, tl, tr, bl, br):
    # Top Left
    if event.type == pygame.MOUSEBUTTONDOWN:
        if tl.rect.collidepoint(event.pos):
            tl.moving = True
    elif event.type == pygame.MOUSEBUTTONUP:
        tl.moving = False
    elif event.type == pygame.QUIT:
        pygame.quit(); sys.exit()
    elif event.type == MOUSEMOTION and tl.moving:
            tl.rect.move_ip(event.rel)
    ''' Top Right
    '''
    if event.type == pygame.MOUSEBUTTONDOWN:
        if tr.rect.collidepoint(event.pos):
            tr.moving = True
    elif event.type == pygame.MOUSEBUTTONUP:
        tr.moving = False
    elif event.type == pygame.QUIT:
        pygame.quit(); sys.exit()
    elif event.type == MOUSEMOTION and tr.moving:
            tr.rect.move_ip(event.rel)
    '''Bottom Left 
    '''        
    if event.type == pygame.MOUSEBUTTONDOWN:
        if bl.rect.collidepoint(event.pos):
            bl.moving = True
    elif event.type == pygame.MOUSEBUTTONUP:
        bl.moving = False
    elif event.type == pygame.QUIT:
        pygame.quit(); sys.exit()
    elif event.type == MOUSEMOTION and bl.moving:
            bl.rect.move_ip(event.rel)
    '''Bottom Right
    '''
    if event.type == pygame.MOUSEBUTTONDOWN:
        if br.rect.collidepoint(event.pos):
            br.moving = True
    elif event.type == pygame.MOUSEBUTTONUP:
        br.moving = False
    elif event.type == pygame.QUIT:

        pygame.quit()
    elif event.type == MOUSEMOTION and br.moving:
            br.rect.move_ip(event.rel)


# Crop and Straighten part of image according to points selected
def Crop_img(img, points, x, y):
    
    p = points
    a = []
    for i in range(4):

        a.append([p[i][0]-59 , p[i][1] - 96])

    orignal_height = img.shape[0]
    orignal_width = img.shape[1]
    Resized_height = 576
    Resized_width = 1024
    Rx = Resized_width/orignal_width
    Ry = Resized_height/orignal_height
    pts_src = np.array([[a[0][0]//Rx, a[0][1]//Ry], [a[1][0]//Rx, a[1][1]//Ry], [a[2][0]//Rx, a[2][1]//Ry], [a[3][0]//Rx, a[3][1]//Ry]])
    pts_dst = np.array([[0,0], [x, 0], [ 0,y], [x, y]])
    im_dst = np.zeros((y, x, 3), np.uint8)
    h, status = cv2.findHomography(pts_src, pts_dst)
    cropped = cv2.warpPerspective(img, h, (im_dst.shape[1],im_dst.shape[0]))
    return cropped

# Convert opencv image to Pygame Surface image
def cv2ImageToSurface(cv2Image):
    if cv2Image.dtype.name == 'uint16':
        cv2Image = (cv2Image / 256).astype('uint8')
    size = cv2Image.shape[1::-1]
    if len(cv2Image.shape) > 2:
        size = cv2Image.shape[1::-1]
        format = 'RGBA' if cv2Image.shape[2] == 4 else 'RGB'
        cv2Image[:, :, [0, 2]] = cv2Image[:, :, [2, 0]]
        
    else:
        size = cv2Image.shape[::-1]
        cv2Image = np.repeat(cv2Image.reshape(size[1], size[0], 1), 3, axis = 2)
        format = 'RGB'

    
    surface = pygame.image.frombuffer(cv2Image.tostring(), size, format)
    return surface.convert_alpha() if format == 'RGBA' else surface.convert()

# Convert image to Black and White / Gray Image
def Black_white(img):
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grayImage


# Enhance image by Otsu's Binarization Process
def Enhance_img(img):
    img = Black_white(img)
    ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th2

# Save edited image
def Save_img(img,path, tool):
    abc = path.split('/')
    name = abc[-1].split('.')[0]+"-" + tool +"."+abc[-1].split('.')[1]
    path = path.replace(abc[-1], "")
    #print(path,name)
    cv2.imwrite(os.path.join(path, name), img)

# MAIN FUNCTION / DRIVER FUNCTION
def main():
    tl = Points(163, 174)
    tr = Points(963, 166)
    bl = Points(162, 604)
    br = Points(965, 604) 
    
    flag = True
    imag_load = False
    cp = False
    win = pygame.display.set_mode((W,H))
    clock = pygame.time.Clock()
    global points
    global IMAGE
    global img_path
    run = True
    direction = 1
    cropped = False
    dx=1024 
    dy= 384
    state = 0
    # Main loop
    while run:
        clock.tick(30)
        
        for event in pygame.event.get():

            point_event(event,tl,tr,bl,br)

            # Crop Image Button
            if Button_click(event, crop):
                cropped = False
                i = cv2.imread(img_path)
                d = Resolution(root)
                x = int(d.x)
                y = int(d.y)
                rx = 1024/x
                ry = 576/y
                dy = round(ry * y)
                dx = round(ry * x)
                cropped_img = Crop_img(i, points, x, y)
                IMAGE = pygame.transform.scale(cv2ImageToSurface(cropped_img), (dx, dy))
                cropped = True
                cp = True

            # Enhance Image Button    
            if Button_click(event, enhance):
                if not cp:
                    k = cv2.imread(img_path)
                    enhanced = Enhance_img(k)
                    IMAGE = pygame.transform.scale(cv2ImageToSurface(enhanced), (1024, 576))
                    cropped = True
                    state = 1
                else:
                    enhanced = Enhance_img(cropped_img)
                    IMAGE = pygame.transform.scale(cv2ImageToSurface(enhanced), (dx, dy))
                    cropped = True
                    state = 1

            # B/W Filter Button        
            if Button_click(event, bw):
                if not cp:
                    j = cv2.imread(img_path)
                    bw_img = Black_white(j)
                    IMAGE = pygame.transform.scale(cv2ImageToSurface(bw_img), (1024, 576))
                    cropped = True
                    state = 2
                else:
                    bw_img = Black_white(cropped_img)
                    IMAGE = pygame.transform.scale(cv2ImageToSurface(bw_img), (dx, dy))
                    cropped = True
                    state = 2

            # Save Image Button            
            if Button_click(event, save):
                abc = img_path.split('/')
                path1 = img_path.replace(abc[-1], "")
                if state == 0:
                    Save_img(cropped_img, img_path, "Cropped")
                    messagebox.showinfo("Image Cropper", f"Image Saved Sucessfully at {path1}")
                elif state == 1:
                    Save_img(enhanced, img_path, "Enhanced")
                    messagebox.showinfo("Image Cropper", f"Image Saved Sucessfully at {path1}")
                elif state == 2:
                    Save_img(bw_img, img_path, "Black_white")
                    messagebox.showinfo("Image Cropper", f"Image Saved Sucessfully at {path1}")

            # Select/Open Image Button        
            if Button_click(event, select):
                
                img_path = Open_file()

                IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(img_path)), (1024, 576))
                img = cv2.imread(img_path)
                imag_load = True

        Draw_Main(win, flag)
        if imag_load:
            Draw_Window(win,tl,tr,bl,br,IMAGE,cropped,dx,dy)
            flag = False   
main()


