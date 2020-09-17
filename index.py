# -*- encoding: utf-8 -*-
 
import os
import time
import pyautogui as auto
import PyHook3 as pyhook
import pythoncom
from PIL import Image
from pytesseract import image_to_string
from googletrans import Translator
import asyncio
import tkinter as tk
# 引入字体模块
import tkinter.font as tkFont
from concurrent.futures import ThreadPoolExecutor

translator = Translator(service_urls=['translate.google.cn'])

px=-1000
py=-1000
x=-1000
y=-1000
last=0


root = tk.Tk("Advise")
root.overrideredirect(True)
sw=root.winfo_screenwidth()
sh=root.winfo_screenheight()
root_x=sw-200
root_y=sh-120
root.geometry("200x50+%d+%d"%(root_x,root_y))
root.wm_attributes('-topmost',1)
root.wm_attributes('-alpha',0.15)
font =  tkFont.Font(family="Microsoft YaHei",size=9);
english = tk.Label(root,text="English",font=font)
english.pack()
chinese = tk.Label(root,text="Chinese",font=font)
chinese.pack()

async def translateZh(text):
    global translator,english
    text=text.replace("\n"," ")
    english['text']=translator.translate(text,src="zh-cn",dest="en").text
    await asyncio.sleep(0.5)

async def translateEn(text):
    global translator
    text=text.replace("\n"," ")
    chinese['text']=translator.translate(text,src="en",dest="zh-cn").text
    await asyncio.sleep(0.5)

async def translate(text):
    global root
    task1 = asyncio.create_task(translateEn(text))
    task2 = asyncio.create_task(translateZh(text))
    await task1
    await task2
    root.wm_attributes('-alpha',0.4)
    root.update()
    await hide(5)

async def hide(delay):
    global root
    await asyncio.sleep(delay)
    root.wm_attributes('-alpha',0)
    root.update()

def getClickPosition(_x,_y):
    global x,y,px,py
    px=x;py=y;
    x=_x;y=_y;
    l=min(x,px)
    t=min(y,py)
    w=abs(px-x)
    h=abs(py-y)
    if w<1000 and h<1000:
        auto.screenshot("temp.png",region=(l,t,w,h))
        img=Image.open("temp.png")
        img=img.convert("L")
        text = image_to_string(img,"chi_sim+eng")
        if text:
            asyncio.run(translate(text))
        x=-1000
        y=-1000


def onMouseEvent(event):
    try:
        global last,loop
        if event.Message==514:
            # Judge Double Click
            if event.Time-last<300:
                getClickPosition(event.Position[0],event.Position[1])
            last=event.Time
        return True  
    except KeyboardInterrupt:
        exit(0)

def main():
    hm = pyhook.HookManager()
    hm.MouseAll = onMouseEvent
    hm.HookMouse()
    pythoncom.PumpMessages()

if __name__ == "__main__":
    main()
