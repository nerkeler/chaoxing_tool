import requests,json,random
from tkinter import *
from tkinter import Scrollbar,messagebox
import tkinter.font as tf

"""
作者：nerkeler
时间：2020-06-30
联系邮箱：2739038007@qq.com
"""


class AnswerGUI(Frame):
    def __init__(self,master=None):

        super().__init__(master)
        self.master = master
        self.master.bind("<Button-3>",lambda event:self.buttonTest(event))
        self.ft = tf.Font(family='微软雅黑', size=12)       #设置输出文本框字体
        self.grid()
        self.history = []           #搜索历史保存列表
        self.createWiget()          #运行主程序
        #self.message()

    def message(self):

        messagebox.showinfo(title="重要提示",message= "仅供测试使用，")

    def createWiget(self):#创建布局

        """整体控件框"""
        frame_all = LabelFrame(self.master,text="作者:nerkeler",labelanchor="se")
        frame_all.grid(row=0,column=1,rowspan=2,columnspan=4,padx=8, pady=5,sticky=NSEW)

        """输入控件"""
        frame_input = LabelFrame(frame_all, text="搜索框", labelanchor="nw")
        frame_input.grid(row=0,column=1,rowspan=2,columnspan=4,padx=8, pady=5,sticky=NSEW)

        """输出控件"""
        frame_output = LabelFrame(frame_all, text="搜索结果", labelanchor="nw")
        frame_output.grid(row=2, column=1, rowspan=6, columnspan=4, padx=8, pady=5,sticky=NSEW)

        """提示文字"""
        self.lay = Label(frame_input,text="请输入需要搜索的题目：(整体查询（首选）或关键字查询（次选））",anchor='w')
        self.lay.grid(row=1,column=0,columnspan=4,sticky=NSEW,padx=5,)

        """输入文本框"""
        v1 = StringVar()
        self.eny1 = Entry(frame_input, textvariable=v1,width=32,font=self.ft )
        self.eny1.grid(row=2,column=0,columnspan=3,sticky=NSEW,padx=8,pady=5)
        self.eny1.bind("<Return>",lambda event:self.get_answer())           #绑定回车按键,隐式函数

        """天键按键"""
        btn1 = Button(frame_input, text='天键', width=10,command=self.sky_button)
        btn1.grid(row=2, column=3, sticky=NSEW, pady=5,padx=8 )

        """确定按键"""
        btn1 = Button(frame_input,text='确定',command=self.get_answer)
        btn1.grid(row=3,column=3,sticky=NSEW,pady=5,padx=8)

        """清空按键"""
        btn2 = Button(frame_input, text='清空', command=lambda :self.eny1.delete(0,END))
        btn2.grid(row=3, column=1, sticky=NSEW, pady=5, padx=8)

        """粘贴按键"""
        btn2 = Button(frame_input, text='粘贴', command=self.buttonTest)
        btn2.grid(row=3, column=2, sticky=NSEW, pady=5, padx=8)

        """历史按键"""
        btn2 = Button(frame_input, text='历史', command=self.get_history)
        btn2.grid(row=3, column=0, sticky=NSEW, pady=5, padx=8)

        """text 输出框"""
        self.tet = Text(frame_output, width=40, height=17,font=self.ft)
        self.tet.grid(row=4,column=0,columnspan=3,pady=5,padx=8)

        """初始使用说明"""
        self.tet.insert(INSERT,"""                            _ooOoo_                    
                           o8888888o                 
                            88"  .  "88                
                             (| ^_^ |)             
                            O\\  =  /O              
                         ____/`---'\____
                       .'  \\\|          |//  `. 
                      /  \\\|||    :    |||//  \\
                     /  _|||||   -:-   |||||-  \\       
                     |   | \\\\     -   /// |   |         
                     | \_|  ''\---/''  |   |
                     \  .-\__  `-`  ___/-. /
                   ___`. .'  /--.--\  `. . ___ 
                ."" '<  `.___\_<|>_/___.'  >'"".
               | | :  `- \`.;`\ _ /`;.`/ - ` : | |
                \  \ `-.   \_ __\ /__ _/   .-` /  /
            =`-.____`-.___\_____/___.-`____.-'= 
                              `=---='                          
     
 """)
        #self.tet.insert(INSERT,"功能演示地址：https://www.15156626517.top/48/\n")
        self.tet.insert(INSERT,"**v1.9新增佛祖个性界面**\n")
        self.tet.insert(INSERT,"**v1.7:更改整体布局，加入GitHub地址**\n")
        self.tet.insert(INSERT,"**v1.5:增‘天键’，即一键顺序完成清空，粘贴，确定等功能。手动输入题目请勿使用**\n\n")
        self.tet.insert(INSERT,"1、本应用为超星尔雅查题工具，支持超星尔雅平台和智慧树知道平台。\n")
        self.tet.insert(INSERT,"2、第一行为题目输入框。\n")
        self.tet.insert(INSERT,"3、右键粘贴或 ctrl+v，ctrl+a全选，enter 回车确定，添加了纵向滚动条。\n")
        self.tet.insert(INSERT,"4、输出文本框禁用编辑,历史默认保存最近10条查询记录\n")
        self.tet.insert(INSERT,"5、联系反馈邮箱：2739038007@qq.com\n作者：nerkeler\nGithub源码地址:https://github.com/nerkeler/chaoxing_tool\n")
        self.tet.insert(INSERT,"6、基于python tkinter 编写，技术不足之处还望谅解。\n\n")
        self.tet.insert(INSERT,"友情提示：\n   查题时优先复制题目所有内容，整体搜索失败可尝试关键字查询， 由于查题api是调用外部接口，所以应用需要不定期更改查题接口。")
        self.tet.insert(INSERT,"如发现查题失败，请尽快联系本人，并附上你的联系方式,我会尽快修复！\n感谢支持！")
        self.tet.config(state=DISABLED)         #禁用编辑

        """添加纵向滚动条"""
        scroll = Scrollbar(frame_output)
        scroll.grid(row=4,column=3,sticky='ns',)
        self.tet.configure(yscrollcommand = scroll.set)
        scroll.configure(command=self.tet.yview)




    """调用api搜索题目"""
    def get_answer(self):

        self.tet.config(state=NORMAL)               #设置可写
        self.tet.delete(1.0,END)                    #清空文本框
        self.question = self.eny1.get()
        self.answer = f"http://47.112.247.80/wkapi.php?q={self.question}"  # 合成搜索链接
        user_list = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"]
        headers = { 'User-Agent': random.choice(user_list)}
        res = requests.get(self.answer,headers = headers)
        res.encoding = res.apparent_encoding
        if res.status_code == 200:
            a = json.loads(res.text)
            band={'code': 1, 'tm': '查询速度过快', 'answer': '喝一杯咖啡再来吧，交流群893833995'}
            if a == band:
                return self.get_answer()
            else:
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
    root.geometry("447x564+500+220")
    root.title('超星尔雅查题工具v1.9')
    app = AnswerGUI(master=root)
    root.mainloop()
