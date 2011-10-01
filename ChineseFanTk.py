# File: gui_ch_convert.py

from Tkinter import *
from UnihanDictDesktop import UnihanDictDesktop as UnihanDict

def convert():
    check_checkboxes()
    output.delete(1.0, END)
    my_input = t.get(1.0, END)
    lines = my_input.split("\n")
    my_output = ""
    for l in lines:
        my_output = my_output + unihan.convert(l) + "\n"
    print(my_output)
    output.insert(END, my_output + "\n")
    #output.insert(END, l + "\n")

def check_checkboxes():
    boxenTF = [pinyin_var.get(),
             zhuyin_var.get(),
             wg_var.get(),
             tongyu_var.get(),
             gwoyu_var.get()]
    unihan.set_pinyin_type(pinyin = boxenTF[0],
                           zhuyin = boxenTF[1],
                           wg     = boxenTF[2],
                           tongyu = boxenTF[3],
                           gwoyu  = boxenTF[4])

root = Tk()

w = Label(root, text="Chinese names go below!")
t = Text(root)
b = Button(root, text="Convert", command=convert)
pinyin_var = IntVar()
zhuyin_var = IntVar()
wg_var = IntVar()
tongyu_var = IntVar()
gwoyu_var = IntVar()
pinyin_checkb = Checkbutton(root, text="Pinyin", variable = pinyin_var)
zhuyin_checkb = Checkbutton(root, text="Zhuyin", variable = zhuyin_var)
wg_checkb     = Checkbutton(root, text="Wade-Giles", variable = wg_var)
tongyu_checkb = Checkbutton(root, text="Tongyu", variable = tongyu_var)
gwoyu_checkb  = Checkbutton(root, text="GwuoyuRomazi", variable = gwoyu_var)
output = Text(root)
w.pack()
t.pack()
b.pack()
pinyin_checkb.pack()
zhuyin_checkb.pack()
wg_checkb.pack()
tongyu_checkb.pack()
gwoyu_checkb.pack()
output.pack()

unihan = UnihanDict()
unihan.load()
unihan.set_pinyin_type(pinyin=1)


root.mainloop()
