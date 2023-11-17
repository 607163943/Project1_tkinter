"""
这是扫雷项目相关类的定义部分
"""
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font
from tkinter import ttk
import random as ra


class Board_base:
    """
    这是扫雷窗口的基类的定义部分
    """
    board_self = None  # 存放扫雷主要类的对象

    def __init__(self, self1):  # 定义扫雷窗口和菜单及其功能
        self.board_self = self1
        self.tk1 = tk.Tk()
        self.menu1 = tk.Menu(self.tk1)
        self.menu1.add_command(label="设置", command=self.menu_set)
        self.menu1.add_command(label="帮助", command=lambda: self.menu_help_or_logging(True))
        self.menu1.add_command(label="日志", command=lambda: self.menu_help_or_logging(False))
        self.tk1.configure(menu=self.menu1)

    def menu_set(self):  # 在扫雷主要类实现设置功能
        self.board_self.board_set()

    def menu_help_or_logging(self, is_help: bool):  # 实现菜单项帮助和日志的功能
        self.top1 = tk.Toplevel(self.tk1)
        self.t1scr1 = scrolledtext.ScrolledText(self.top1, width=100)
        self.t1scr1.pack_configure()
        if is_help:  # 判断是否打开帮助手册,负责打开日志文件
            temp = "project1_2_tkinter_help.txt"
        else:
            temp = "project1_2_tkinter_logging.txt"
        with open(temp, "r+", encoding="utf-8") as f:
            f.seek(0)
            self.t1scr1.insert("1.0", f.read())  # 在新窗口展示文件内容

    def display(self):  # 显示扫雷窗口
        self.tk1.mainloop()


class Board(Board_base):
    """
    这是扫雷窗口的主要类定义部分
    """
    board_all = {"row": 9, "col": 9, "booms": 10, "flags": 10, "time": 0}  # 存放扫雷各素材的数据
    ph_list = []  # 用于存放扫雷相关图片对象

    def __init__(self):
        super().__init__(self)
        self.font = font.Font(name="微软雅黑", size=20)  # 统一定义文本字体格式
        temp = ["face1.png", "face2.png", "face3.png", "flag1.png", "mine1.png", "mine2.png", "normal.png", "safe0.png",
                "safe1.png", "safe2.png", "safe3.png", "safe4.png", "safe5.png", "safe6.png", "safe7.png", "safe8.png"]
        temp = [r"project1_2_tkinter_png\\"
                + i for i in temp]  # 创建含扫雷相关图片文件的绝对路径的列表
        for i in temp:
            self.ph_list += [tk.PhotoImage(file=i, format="png")]  # 存放扫雷相关图片的对象
        self.var_temp = tk.Variable(value="简单")  # 用于记录当前棋盘的难度
        self.var_temp.trace_add("write", lambda x, y, z: self.board_set_replace)  # 跟踪棋盘当前难度
        self.board_start()

    def board_start(self):  # 初始化生成棋盘按钮,和雷区中雷的分布,以及雷区中各区域周围雷数的统计
        self.flag_board = []  # 记录当前插旗的区域
        self.button_list = []  # 存放棋盘的按钮对象
        self.time_continue = True  # 初始化计时标签状态
        self.row = self.board_all.get("row")  # 记录行数
        self.col = self.board_all.get("col")  # 记录列数
        self.booms = self.board_all.get("booms")  # 记录雷数
        self.flags = self.board_all.get("flags")  # 记录红旗数
        self.time = self.board_all.get("time")  # 记录初始用时
        self.frame1 = tk.Frame(self.tk1)
        self.frame1_1 = tk.Frame(self.frame1)
        self.label1_1_1 = tk.Label(self.frame1_1, text=f"红旗数:{self.flags}", width=10, font=self.font)
        self.label1_1_1.grid_configure(row=0, column=0)
        self.button1_1_1 = tk.Button(self.frame1_1, image=self.ph_list[0], command=self.board_once_again)
        self.button1_1_1.grid_configure(row=0, column=1)
        self.label1_1_2 = tk.Label(self.frame1_1, text=f"用时:{self.time}", width=10, font=self.font)
        self.label1_1_2.grid_configure(row=0, column=2)
        self.frame1_1.pack_configure()
        self.frame1_2 = tk.Frame(self.frame1)
        for i in range(self.row):  # 生成指定数量的按钮并绑定插旗的相关函数
            temp = []
            for j in range(self.col):
                temp1 = tk.Button(self.frame1_2, image=self.ph_list[6], command=lambda x=i, y=j: self.board_move(x, y))
                temp1.grid_configure(row=i, column=j)
                temp1.bind("<Button-3>", lambda event, x=i, y=j: self.board_flag(x, y))
                temp += [temp1]
            self.button_list += [temp]
        self.board1 = [[0 for j in range(self.col + 2)] for i in range(self.row + 2)]  # 记录雷所在区域的棋盘
        self.board2 = []  # 记录每格的周围雷数的棋盘
        self.board3 = [["*" for j in range(self.col + 2)] for i in range(self.row + 2)]  # 记录区域排查情况的棋盘
        k = self.booms
        while k > 0:  # 放置指定数量的雷
            x = ra.randint(1, self.row)
            y = ra.randint(1, self.col)
            if self.board1[x][y] == 0:
                self.board1[x][y] = 1
                k -= 1
        for i in range(self.row + 2):  # 将每格周围雷数统计并存放在对应棋盘中
            temp = []
            for j in range(self.col + 2):
                if 0 < i and i < self.row + 1 and 0 < j and j < self.col + 1:
                    temp += [(self.board1[i + 1][j] + self.board1[i][j + 1] + self.board1[i + 1][j + 1]
                              + self.board1[i - 1][j] + self.board1[i][j - 1] + self.board1[i - 1][j - 1]
                              + self.board1[i - 1][j + 1] + self.board1[i + 1][j - 1])]
                else:
                    temp += [0]
            self.board2 += [temp]
        self.frame1_2.pack_configure()
        self.frame1.pack_configure()
        self.label1_1_2.after(1000, self.board_time)  # 开始计时

    def board_time(self):  # 计时相关函数
        if self.time_continue:  # 判断是否继续计时
            self.time += 1
            self.label1_1_2.configure(text=f"用时:{self.time}")
            self.label1_1_2.after(1000, self.board_time)

    def board_move(self, x, y):  # 玩家排查区域相关函数
        if self.board1[x + 1][y + 1] == 1:  # 判断玩家是否触雷
            self.board_move_over(x, y)
        else:
            self.button_list[x][y].grid_forget()
            self.board3[x + 1][y + 1] = ' '
            temp = tk.Label(self.frame1_2, image=self.ph_list[self.board2[x + 1][y + 1] + 7])
            temp.grid_configure(row=x, column=y)
            if (x, y) in self.flag_board:  # 判断排查区域是否插旗,是则回收旗帜
                self.flags += 1
                self.flag_board.pop(self.flag_board.index(x, y))
            if self.board2[x + 1][y + 1] == 0:  # 判断是否展开棋盘
                self.board_move_continue(x, y)
            if self.board_is_win():  # 判断是否排查完雷区
                self.board_win()  # 执行游戏胜利相关函数

    def board_flag(self, x, y):  # 插旗相关函数
        if (x, y) not in self.flag_board:  # 判断是插旗还是撤回旗
            self.button_list[x][y].configure(image=self.ph_list[3])
            self.flag_board += [(x, y)]
            self.flags -= 1
        else:
            self.button_list[x][y].configure(image=self.ph_list[6])
            self.flag_board.pop(self.flag_board.index((x, y)))
            self.flags += 1
        self.label1_1_1.configure(text=f"红旗数:{self.flags}")  # 更新红旗标签的文本

    def board_move_over(self, x, y):  # 执行游戏失败相关函数
        for i in range(self.row):
            for j in range(self.col):
                self.button_list[i][j].configure(command=lambda: None)  # 将排查功能撤去
                if self.board1[i + 1][j + 1] == 1:
                    self.button_list[i][j].configure(image=self.ph_list[4])  # 将有雷区域的雷显示在按钮上
        self.button_list[x][y].configure(image=self.ph_list[5])  # 将当前触雷的雷显示在按钮上
        self.button1_1_1.configure(image=self.ph_list[1])  # 标签按钮替换表情为死亡
        self.time_continue = False  # 停止计时

    def board_move_continue(self, x, y):  # 执行棋盘展开相关函数
        i = x
        j = y
        while i < self.row:  # 进行右下角展开
            if self.board1[i + 1][j + 1] == 0 and self.board3[i + 1][j + 1] == "*" and self.board2[i + 1][j + 1] == 0:
                temp1 = False
                if self.board2[i + 2][j + 1] == 0 and self.board3[i + 2][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j + 2] == 0 and self.board3[i + 1][j + 2] == ' ':
                    temp1 = True
                elif self.board2[i][j + 1] == 0 and self.board3[i][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j] == 0 and self.board3[i + 1][j] == ' ':
                    temp1 = True
                if temp1:
                    self.button_list[i][j].grid_forget()
                    temp = tk.Label(self.frame1_2, image=self.ph_list[7])
                    temp.grid_configure(row=i, column=j)
                    self.board3[i + 1][j + 1] = ' '
                    j = y - 1
                    if (i, j) in self.flag_board:  # 判断排查区域是否插旗,是则回收旗帜
                        self.flags += 1
                        self.flag_board.pop(self.flag_board.index(i, j))
            if j == self.col - 1:
                i += 1
                j = y
            else:
                j += 1
        else:
            i = x
            j = y
        while i >= 0:  # 进行右上角展开
            if self.board1[i + 1][j + 1] == 0 and self.board3[i + 1][j + 1] == "*" and self.board2[i + 1][j + 1] == 0:
                temp1 = False
                if self.board2[i + 2][j + 1] == 0 and self.board3[i + 2][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j + 2] == 0 and self.board3[i + 1][j + 2] == ' ':
                    temp1 = True
                elif self.board2[i][j + 1] == 0 and self.board3[i][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j] == 0 and self.board3[i + 1][j] == ' ':
                    temp1 = True
                if temp1:
                    self.button_list[i][j].grid_forget()
                    temp = tk.Label(self.frame1_2, image=self.ph_list[7])
                    temp.grid_configure(row=i, column=j)
                    self.board3[i + 1][j + 1] = ' '
                    j = y - 1
                    if (i, j) in self.flag_board:  # 判断排查区域是否插旗,是则回收旗帜
                        self.flags += 1
                        self.flag_board.pop(self.flag_board.index(i, j))
            if j == self.col - 1:
                i -= 1
                j = y
            else:
                j += 1
        else:
            i = x
            j = y
        while i < self.row:  # 进行左下角展开
            if self.board1[i + 1][j + 1] == 0 and self.board3[i + 1][j + 1] == "*" and self.board2[i + 1][j + 1] == 0:
                temp1 = False
                if self.board2[i + 2][j + 1] == 0 and self.board3[i + 2][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j + 2] == 0 and self.board3[i + 1][j + 2] == ' ':
                    temp1 = True
                elif self.board2[i][j + 1] == 0 and self.board3[i][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j] == 0 and self.board3[i + 1][j] == ' ':
                    temp1 = True
                if temp1:
                    self.button_list[i][j].grid_forget()
                    temp = tk.Label(self.frame1_2, image=self.ph_list[7])
                    temp.grid_configure(row=i, column=j)
                    self.board3[i + 1][j + 1] = ' '
                    j = y - 1
                    if (i, j) in self.flag_board:  # 判断排查区域是否插旗,是则回收旗帜
                        self.flags += 1
                        self.flag_board.pop(self.flag_board.index(i, j))
            if j == 0:
                i += 1
                j = y
            else:
                j -= 1
        else:
            i = x
            j = y
        while i >= 0:  # 进行左上角展开
            if self.board1[i + 1][j + 1] == 0 and self.board3[i + 1][j + 1] == "*" and self.board2[i + 1][j + 1] == 0:
                temp1 = False
                if self.board2[i + 2][j + 1] == 0 and self.board3[i + 2][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j + 2] == 0 and self.board3[i + 1][j + 2] == ' ':
                    temp1 = True
                elif self.board2[i][j + 1] == 0 and self.board3[i][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j] == 0 and self.board3[i + 1][j] == ' ':
                    temp1 = True
                if temp1:
                    self.button_list[i][j].grid_forget()
                    temp = tk.Label(self.frame1_2, image=self.ph_list[7])
                    temp.grid_configure(row=i, column=j)
                    self.board3[i + 1][j + 1] = ' '
                    j = y - 1
                    if (i, j) in self.flag_board:  # 判断排查区域是否插旗,是则回收旗帜
                        self.flags += 1
                        self.flag_board.pop(self.flag_board.index(i, j))
            if j == 0:
                i -= 1
                j = y
            else:
                j -= 1
        else:
            i = 0
            j = 0
        while i < self.row:  # 进行全盘统一展开
            if self.board1[i + 1][j + 1] == 0 and self.board3[i + 1][j + 1] == "*" and self.board2[i + 1][j + 1] == 0:
                temp1 = False
                if self.board2[i + 2][j + 1] == 0 and self.board3[i + 2][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j + 2] == 0 and self.board3[i + 1][j + 2] == ' ':
                    temp1 = True
                elif self.board2[i][j + 1] == 0 and self.board3[i][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j] == 0 and self.board3[i + 1][j] == ' ':
                    temp1 = True
                if temp1:
                    self.button_list[i][j].grid_forget()
                    temp = tk.Label(self.frame1_2, image=self.ph_list[7])
                    temp.grid_configure(row=i, column=j)
                    self.board3[i + 1][j + 1] = ' '
                    j = -1
                    if (i, j) in self.flag_board:  # 判断排查区域是否插旗,是则回收旗帜
                        self.flags += 1
                        self.flag_board.pop(self.flag_board.index(i, j))
            if j == self.col - 1:
                i += 1
                j = 0
            else:
                j += 1
        else:
            i = 0
            j = 0
        while i < self.row:  # 将空白标签周围的无雷但有数的标签展开
            if self.board2[i + 1][j + 1] != 0 and self.board3[i + 1][j + 1] == "*" and self.board1[i + 1][j + 1] == 0:
                temp1 = False
                if self.board2[i + 1][j + 2] == 0 and self.board3[i + 1][j + 2] == ' ':
                    temp1 = True
                elif self.board2[i + 2][j + 1] == 0 and self.board3[i + 2][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 2][j + 2] == 0 and self.board3[i + 2][j + 2] == ' ':
                    temp1 = True
                elif self.board2[i][j + 1] == 0 and self.board3[i][j + 1] == ' ':
                    temp1 = True
                elif self.board2[i + 1][j] == 0 and self.board3[i + 1][j] == ' ':
                    temp1 = True
                elif self.board2[i][j] == 0 and self.board3[i][j] == ' ':
                    temp1 = True
                elif self.board2[i][j + 2] == 0 and self.board3[i][j + 2] == ' ':
                    temp1 = True
                elif self.board2[i + 2][j] == 0 and self.board3[i + 2][j] == ' ':
                    temp1 = True
                if temp1:
                    self.button_list[i][j].grid_forget()
                    temp = tk.Label(self.frame1_2, image=self.ph_list[self.board2[i + 1][j + 1] + 7])
                    temp.grid_configure(row=i, column=j)
                    self.board3[i + 1][j + 1] = ' '
                    if (i, j) in self.flag_board:  # 判断排查区域是否插旗,是则回收旗帜
                        self.flags += 1
                        self.flag_board.pop(self.flag_board.index(i, j))
            if j == self.col - 1:
                i += 1
                j = 0
            else:
                j += 1

    def board_is_win(self):  # 判断扫雷是否成功的函数
        for i in range(self.row):
            for j in range(self.col):
                if self.board1[i + 1][j + 1] == 0 and self.board3[i + 1][j + 1] == "*":  # 若找到未排查的无雷区域则返回假
                    return False
        else:
            return True  # 整个棋盘都未找到未排查的无雷区域,则游戏完成返回真

    def board_win(self):  # 游戏胜利相关函数
        for i in range(self.row):
            for j in range(self.col):
                self.button_list[i][j].configure(command=lambda: None)  # 取消按钮的排查功能
                if self.board1[i + 1][j + 1] == 1:
                    self.button_list[i][j].configure(image=self.ph_list[4])  # 将雷显示在对应区域的按钮上
        self.button1_1_1.configure(image=self.ph_list[2])  # 替换表情按钮为墨镜
        self.time_continue = False  # 停止计时

    def board_once_again(self):  # 重新开始的函数
        self.frame1.destroy()
        self.board_start()

    def board_set(self):  # 定义设置界面控件及其功能
        self.menu_temp = tk.Menu(self.tk1)
        self.tk1.configure(menu=self.menu_temp)  # 生成临时的空菜单替换已有菜单来实现使菜单栏目消失的效果
        self.time_continue = False  # 停止计时
        self.frame1.destroy()  # 销毁此棋盘
        self.frame2 = tk.Frame(self.tk1)
        self.frame2_1 = tk.Frame(self.frame2)
        self.label2_1_1 = tk.Label(self.frame2_1, text="选择的难度:", width=10, font=self.font)
        self.label2_1_1.grid_configure(row=0, column=0)

        temp = ttk.Style()
        temp.configure("a.TMenubutton", font=self.font)
        self.opmenu2_1_1 = ttk.OptionMenu(self.frame2_1, self.var_temp, self.var_temp.get(), "简单", "普通", "困难",
                                          "自定义", style="a.TMenubutton",
                                          command=lambda x: self.board_set_replace())  # 定义菜单供玩家选择扫雷难度
        self.opmenu2_1_1.grid_configure(row=0, column=1)
        self.frame2_1.pack_configure()
        self.frame2_2 = tk.Frame(self.frame2)
        self.label2_2_1 = tk.Label(self.frame2_2, text="行数:", width=20, font=self.font, anchor="w")
        self.label2_2_1.pack_configure()
        self.entry2_2_1 = ttk.Entry(self.frame2_2, justify="right", font=self.font, validate="focus",
                                    validatecommand=self.board_set_is_replace1)
        self.entry2_2_1.pack_configure()
        self.label2_2_2 = tk.Label(self.frame2_2, text="列数:", width=20, font=self.font, anchor="w")
        self.label2_2_2.pack_configure()
        self.entry2_2_2 = ttk.Entry(self.frame2_2, justify="right", font=self.font, validate="focus",
                                    validatecommand=self.board_set_is_replace2)
        self.entry2_2_2.pack_configure()
        self.label2_2_3 = tk.Label(self.frame2_2, text="雷数:", width=20, font=self.font, anchor="w")
        self.label2_2_3.pack_configure()
        self.entry2_2_3 = ttk.Entry(self.frame2_2, justify="right", font=self.font, validate="focus",
                                    validatecommand=self.board_set_is_replace3)
        self.entry2_2_3.pack_configure()
        self.frame2_2.pack_configure()
        self.frame2_3 = tk.Frame(self.frame2)
        temp.configure("a.TButton", font=self.font)
        self.button2_3_1 = ttk.Button(self.frame2_3, text="确定", command=self.board_set_true, style="a.TButton")
        self.button2_3_1.grid_configure(row=0, column=0)
        self.label2_3_1 = tk.Label(self.frame2_3, width=15)
        self.label2_3_1.grid_configure(row=0, column=1)
        self.button2_3_2 = ttk.Button(self.frame2_3, text="返回", command=self.board_set_return, style="a.TButton")
        self.button2_3_2.grid_configure(row=0, column=2)
        self.frame2_3.pack_configure(pady=40)
        self.frame2.pack_configure()
        self.entry2_2_1.insert(0, str(self.board_all["row"]))  # 给行数文本框传入当前行数
        self.entry2_2_2.insert(0, str(self.board_all["col"]))  # 给列数文本框传入当前列数
        self.entry2_2_3.insert(0, str(self.board_all["booms"]))  # 给雷数文本框传入当前雷数
        if self.var_temp.get() != "自定义":  # 判断是否未自定义难度(自定义模式下三个文本框自由输入,其余模式下三个文本框均锁定)
            self.entry2_2_1.configure(state="disabled")
            self.entry2_2_2.configure(state="disabled")
            self.entry2_2_3.configure(state="disabled")

    def board_set_is_replace1(self):  # 判断行数文本框输入是否合理,不合理则将文本替换为当前使用的行数
        if not self.entry2_2_1.get().isdigit():
            self.entry2_2_1.delete(0, len(self.entry2_2_1.get()))
            self.entry2_2_1.insert(0, str(self.board_all.get("row")))
        return self.entry2_2_1.get().isdigit()  # 不返回布尔值会导致判断输入只会触发一次

    def board_set_is_replace2(self):  # 判断列数文本框输入是否合理,不合理则将文本替换为当前使用的列数
        if not self.entry2_2_2.get().isdigit():
            self.entry2_2_2.delete(0, len(self.entry2_2_2.get()))
            self.entry2_2_2.insert(0, str(self.board_all.get("col")))
        return self.entry2_2_2.get().isdigit()  # 不返回布尔值会导致判断输入只会触发一次

    def board_set_is_replace3(self):  # 判断雷数文本框输入是否合理,不合理则将文本替换为当前使用的雷数
        if not self.entry2_2_3.get().isdigit():
            self.entry2_2_3.delete(0, len(self.entry2_2_3.get()))
            self.entry2_2_3.insert(0, str(self.board_all.get("booms")))
        return self.entry2_2_3.get().isdigit()  # 不返回布尔值会导致判断输入只会触发一次

    def board_set_replace(self):  # 执行文本框值替换的函数
        # 解锁文本输入框
        self.entry2_2_1.configure(state="normal")
        self.entry2_2_2.configure(state="normal")
        self.entry2_2_3.configure(state="normal")
        if self.var_temp.get() != "自定义":  # 判断是否为自定义模式,自定义模式下只需解锁文本输入框
            # 清空各文本框内容
            self.entry2_2_1.delete(0, len(self.entry2_2_1.get()))
            self.entry2_2_2.delete(0, len(self.entry2_2_2.get()))
            self.entry2_2_3.delete(0, len(self.entry2_2_3.get()))
            temp = ["9", "9", "10"]
            if self.var_temp.get() == "简单":
                temp = ["9", "9", "10"]
            elif self.var_temp.get() == "普通":
                temp = ["16", "16", "40"]
            elif self.var_temp.get() == "困难":
                temp = ["16", "40", "99"]
            # 替换对应文本并再次锁住文本框
            self.entry2_2_1.insert(0, temp[0])
            self.entry2_2_2.insert(0, temp[1])
            self.entry2_2_3.insert(0, temp[2])
            self.entry2_2_1.configure(state="disabled")
            self.entry2_2_2.configure(state="disabled")
            self.entry2_2_3.configure(state="disabled")

    def board_set_true(self):  # 执行设置完成的函数
        self.tk1.configure(menu=self.menu1)  # 替换为原菜单
        # 将棋盘的数据进行更新
        self.board_all["row"] = int(self.entry2_2_1.get())
        self.board_all["col"] = int(self.entry2_2_2.get())
        self.board_all["booms"] = int(self.entry2_2_3.get())
        self.board_all["flags"] = int(self.entry2_2_3.get())
        self.frame2.destroy()  # 销毁设置界面
        self.board_start()  # 初始化棋盘

    def board_set_return(self):  # 执行设置界面的返回函数
        self.tk1.configure(menu=self.menu1)  # 替换为原菜单
        self.frame2.destroy()  # 销毁设置界面
        self.board_start()  # 初始化棋盘
