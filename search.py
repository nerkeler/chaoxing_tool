import requests,json
from tkinter import *
from tkinter import Scrollbar
import tkinter.font as tf


class AnswerGUI(Frame):
    def __init__(self,master=None):

        super().__init__(master)
        self.master = master
        self.master.bind("<Button-3>",lambda event:self.buttonTest(event))
        self.ft = tf.Font(family='微软雅黑', size=12)       #设置输出文本框字体
        self.grid()
        self.history = []           #搜索历史保存列表
        self.createWiget()          #运行主程序

    def createWiget(self):#创建布局

        """提示文字"""
        self.lay = Label(self.master,text="请输入需要搜索的题目：(整体查询（首选）或关键字查询（次选））")
        self.lay.grid(row=0,column=0,columnspan=4,sticky=NSEW,padx=5,)

        """输入文本框"""
        v1 = StringVar()
        self.eny1 = Entry(self.master, textvariable=v1,width=30,font=self.ft )
        self.eny1.grid(row=2,column=0,columnspan=3,sticky=NSEW,pady=5,padx=8)
        self.eny1.bind("<Return>",lambda event:self.get_answer())           #绑定回车按键,隐式函数

        """天键按键"""
        btn1 = Button(self.master, text='天键', command=self.sky_button)
        btn1.grid(row=2, column=3, sticky=NSEW, pady=5, padx=8)

        """确定按键"""
        btn1 = Button(self.master,text='确定',command=self.get_answer)
        btn1.grid(row=3,column=3,sticky=NSEW,pady=5,padx=8)

        """清空按键"""
        btn2 = Button(self.master, text='清空', command=lambda :self.eny1.delete(0,END))
        btn2.grid(row=3, column=1, sticky=NSEW, pady=5, padx=8)

        """粘贴按键"""
        btn2 = Button(self.master, text='粘贴', command=self.buttonTest)
        btn2.grid(row=3, column=2, sticky=NSEW, pady=5, padx=8)

        """历史按键"""
        btn2 = Button(self.master, text='历史', command=self.get_history)
        btn2.grid(row=3, column=0, sticky=NSEW, pady=5, padx=8)

        """text 输出框"""
        self.tet = Text(self.master, width=40, height=15,font=self.ft)
        self.tet.grid(row=4,column=0,columnspan=4,pady=5,padx=8)

        """初始使用说明"""
        self.tet.insert(INSERT,"**新增‘天键’，即一键顺序完成清空，粘贴，确定功能。手动输入题目请勿使用**\n\n")
        self.tet.insert(INSERT,"1、本应用为超星尔雅查题工具，支持超星尔雅平台和智慧树知道平台。\n")
        self.tet.insert(INSERT,"2、第一行为题目输入框。\n")
        self.tet.insert(INSERT,"3、右键粘贴或 ctrl+v，ctrl+a全选，enter 回车确定，添加了纵向滚动条。\n")
        self.tet.insert(INSERT,"4、输出文本框禁用编辑,历史默认保存最近10条查询记录\n")
        self.tet.insert(INSERT,"5、联系反馈邮箱：2739038007@qq.com\n")
        self.tet.insert(INSERT,"6、基于python tkinter 编写，技术不足之处还望谅解。\n\n")
        self.tet.insert(INSERT,"友情提示：\n   查题时优先复制题目所有内容，整体搜索失败可尝试关键字查询， 由于查题api是调用外部接口，所以应用需要不定期更改查题接口。")
        self.tet.insert(INSERT,"如发现查题失败，请尽快联系本人，并附上你的联系方式,我会尽快修复！\n感谢支持！")
        self.tet.config(state=DISABLED)         #禁用编辑

        """添加纵向滚动条"""
        scroll = Scrollbar(root)
        scroll.grid(row=4,column=4,sticky='ns')
        self.tet.configure(yscrollcommand = scroll.set)
        scroll.configure(command=self.tet.yview)

    """调用api搜索题目"""
    def get_answer(self):

        self.tet.config(state=NORMAL)               #设置可写
        self.tet.delete(1.0,END)                    #清空文本框
        self.question = self.eny1.get()
        self.answer = f"http://47.112.247.80/wkapi.php?q={self.question}"  # 合成搜索链接
        res = requests.get(self.answer)
        res.encoding = res.apparent_encoding
        if res.status_code == 200:
            a = json.loads(res.text)
            if a['answer'] != "":
                self.tet.insert(1.0, f"题目：\n  {a['tm']}\n\n")
                self.tet.insert(INSERT, f"答案：\n  {a['answer']}")
                self.tet.config(state=DISABLED)  # 禁止编辑
                self.history.append(f"题目：\n   {a['tm']}\n答案：\n   {a['answer']}")
        else:
            return None

    def sky_button(self):       #天键选项函数

        self.eny1.delete(0,END)
        self.buttonTest()
        self.get_answer()

    def buttonTest(self,*args):         #粘贴函数。*args满足bind 和 button 传参绑定

        s = root.clipboard_get()
        self.eny1.insert(1,s)

    def get_history(self):          #搜索历史存储函数；判断列表长度，反转列表输出

        while(len(self.history)>10):
            self.history.remove(self.history[0])
        self.tet.config(state=NORMAL)
        self.tet.delete(1.0,END)
        num = len(self.history)
        for i in range(0,num):
            self.tet.insert(INSERT,self.history[num-(1+i)])
            self.tet.insert(INSERT,"\n\n")
        self.tet.config(state=DISABLED)

"""主函数"""
if __name__ == '__main__':
    root = Tk()
    root.iconbitmap("xuexitong.ico")
    root.geometry("400x435+500+300")
    root.title('超星尔雅查题工具v1.5')
    app = AnswerGUI(master=root)
    root.mainloop()
