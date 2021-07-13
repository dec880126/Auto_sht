import tkinter as tk
from PIL import Image, ImageTk
import io
from urllib.request import urlopen 
from tkinter import messagebox
import os

def get_img(url):
    global tk_image
    
    image_bytes = urlopen(url).read()
    # internal data file
    data_stream = io.BytesIO(image_bytes)
    # open as a PIL image object
    pil_image = Image.open(data_stream)

    # set the size of the image
    img_weight = 900
    img_height =  515
    pil_image = pil_image.resize((img_weight, img_height))

    # convert PIL image object to Tkinter PhotoImage object
    tk_image = ImageTk.PhotoImage(pil_image)

def change_img(flag):
    global current_pic

    current_pic += flag
    print(current_pic)
        
    if current_pic < 0:
        messagebox.showerror('', '這已經是第一張圖片了')
    elif current_pic >= len(imgURL_list):   
        messagebox.showerror('', '這已經是最後一張圖片了')
        return
    else:            
        get_img(imgURL_list[current_pic])
        label.configure(image = tk_image)

def del_movie():
    print("delete!")
    

if __name__ == '__main__':
    window = tk.Tk()
    window.title('My Window')
    width = 1024
    height = 768
    window.geometry(f'{width}x{height}')

    # Parameters
    current_pic = 0
    imgURL_list = ["https://www.tucahuand.com/tupian/forum/202107/13/130307dkykghkxgzghuoph.jpg", "https://www.tucahuand.com/tupian/forum/202107/13/130307oz98suu1v1cdruc9.jpg"]

    # Initialize the picture frame
    get_img(imgURL_list[0])

    label = tk.Label(window, image=tk_image, bg='white')
    label.pack(padx=5, pady=5)

    delete = tk.Button(window, text='DELETE', font=('Arial', 12), width=30, height=1, command=lambda: del_movie()).pack()
    next = tk.Button(window, text='NEXT', font=('Arial', 12), width=10, height=1, command=lambda: change_img(1)).pack(side = 'right', padx = 200)
    pre = tk.Button(window, text='PRE', font=('Arial', 12), width=10, height=1, command=lambda: change_img(-1)).pack(side = 'left', padx = 200)

    window.mainloop()
