from tkinter import *  # 导入tkinter库中的所有函数
import tkinter.font as tkFont  # 导入tkinter库中的字体设置函数并为其指定别名tkFont


def calculate():  # 此函数为数学运算函数，使此计算器可以正确地显示结果并在输入内容无法计算时报错
    sample = ['(j', '+j', '-j', '*j', '/j']
    for error_example in sample:
        if error_example in equ.get()[:]:
            j = 1j
            break
        else:
            continue
    if 'j' in equ.get()[:1]:
        j = 1j
    try:
        result = eval(equ.get())
        equ.set(equ.get() + "=\n" + str(result))
    except ZeroDivisionError:
        equ.set('error')
    except SyntaxError:
        equ.set('error')
    except NameError:
        equ.set('error')


def show(buttonString):  # 此函数为按钮显示函数，使此计算器能在按下按钮时正确地显示结果
    content = equ.get()
    if content == "0":
        content = ""
    equ.set(content + buttonString)


def backspace():  # 此函数定义了退格键的功能
    if 'error' in equ.get()[-5:]:
        equ.set("0")
    else:
        equ.set(str(equ.get()[:-1]))


def clear():  # 此函数定义了清除键的功能
    equ.set("0")


root = Tk()  # 建立根窗口
root.title('calculator')  # 根窗口的名字为calculator（计算器）

height = 440  # 显示框高度
width = 480  # 显示框宽度

x = (root.winfo_screenwidth() - width) / 2  # 根窗口横坐标
y = (root.winfo_screenheight() - height) / 2  # 根窗口纵坐标

root.resizable(False, False)  # 根窗口不可自由调整大小
root.geometry("%dx%d+%d+%d" % (width, height, x, y))  # 根窗口的位置和大小
root.configure(bg="white")  # 根窗口的颜色

w1 = 10  # 按钮宽度
h1 = 2  # 按钮高度

equ = StringVar()  # 保证值的变更随时可以显示在显示框上
equ.set("0")  # 初始化显示框，使其显示0

ft1 = tkFont.Font(size=25)  # 定义字体1
ft2 = tkFont.Font(size=15, weight=tkFont.BOLD)  # 定义字体2
ft3 = tkFont.Font(size=15, weight=tkFont.BOLD)  # 定义字体3

bg1 = "whitesmoke"  # 定义按钮背景颜色1
bg2 = "white"  # 定义按钮背景颜色2

fg1 = "blue"  # 定义按钮上文本的颜色

label = Label(root, width=27, height=3, anchor=SE, bg='white', font=ft1, textvariable=equ, wraplength=450)  # 调整显示框的各项属性
label.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

# 定义第一行按钮
clearButton = Button(root, text="C", bg=bg1, width=w1, height=h1, fg="blue", font=ft2, command=clear).grid(row=1,
                                                                                                           column=0)
Button(root, text="/", width=w1, height=h1, bg=bg1, fg=fg1, font=ft2, command=lambda: show("/")).grid(row=1, column=1)
Button(root, text="*", width=w1, height=h1, bg=bg1, fg=fg1, font=ft2, command=lambda: show("*")).grid(row=1, column=2)
Button(root, text="DEL", width=w1, height=h1, bg=bg1, fg=fg1, font=ft2, command=backspace).grid(row=1, column=3)

# 定义第二行按钮
Button(root, text="7", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("7")).grid(row=2, column=0)
Button(root, text="8", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("8")).grid(row=2, column=1)
Button(root, text="9", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("9")).grid(row=2, column=2)
Button(root, text="-", width=w1, height=h1, bg=bg1, fg=fg1, font=ft2, command=lambda: show("-")).grid(row=2, column=3)

# 定义第三行按钮
Button(root, text="4", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("4")).grid(row=3, column=0)
Button(root, text="5", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("5")).grid(row=3, column=1)
Button(root, text="6", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("6")).grid(row=3, column=2)
Button(root, text="+", width=w1, height=h1, bg=bg1, fg=fg1, font=ft2, command=lambda: show("+")).grid(row=3, column=3)

# 定义第四行按钮
Button(root, text="1", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("1")).grid(row=4, column=0)
Button(root, text="2", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("2")).grid(row=4, column=1)
Button(root, text="3", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("3")).grid(row=4, column=2)

# 定义第五行按钮
Button(root, text="j", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("j")).grid(row=5, column=0)
Button(root, text="0", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show("0")).grid(row=5, column=1)
Button(root, text=".", width=w1, height=h1, bg=bg2, font=ft2, command=lambda: show(".")).grid(row=5, column=2)

# 定义剩余按钮
Button(root, text="=", width=w1, height=5, bg="blue", fg="white", font=ft2, command=lambda: calculate()).grid(row=4,
                                                                                                              column=3,
                                                                                                              rowspan=2)
Button(root, text="(", width=21, height=h1, bg=bg1, font=ft2, command=lambda: show("(")).grid(row=6, column=0,
                                                                                              columnspan=2)
Button(root, text=")", width=21, height=h1, bg=bg1, font=ft2, command=lambda: show(")")).grid(row=6, column=2,
                                                                                              columnspan=2)
Button(root, text="^", width=21, height=h1, bg=bg1, font=ft2, command=lambda: show(")")).grid(row=7, column=2,
                                                                                              columnspan=2)


def main():
    # 令程序继续执行，同时进入等待和处理窗口事件
    root.mainloop()


if __name__ == '__main__':
    main()