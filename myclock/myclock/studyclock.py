from tkinter import *
from time import sleep
from datetime import datetime, timedelta
from threading import current_thread, Thread
# 我需要新建一个闹钟，它的功能是选择安排的时间，在给定的时间范围内，给与休息
# 与继续的提示画面。要求是可以同时添加任意个项目。
# 我还需要一个界面使我能够弹窗
# 有个问题先标记一下，就是每天必须重新打开
# 排序问题，多个时间，时间线排序
# 不支持自定义项目提示内容


#Frame 是一个父级的widget
class application(Frame):
    # self是对象本身,这里master，在Tkinter中，一个控件可能属于另一个控件，这时另一个控件就是这个控件的master。
    # 默认一个窗口没有master，因此master有None的默认值。
    def __init__(self, master=None):
        # 使用参数master=None,将类的Frame类部分初始化,bg表示background 背景色
        Frame.__init__(self, master, bg="white")
        # pack()打包，也可以用grid() 布局
        self.pack()
        self.window_init()
        self.creatWidget()

    def window_init(self):
        self.master.title('Tomato Clock')
        # 设置窗口颜色为red 不过暂时看起来没有什么用
        self.master.bg = "red"
        # 设置窗口大小，'宽x高+偏移X+偏移Y'
        self.master.geometry("300x100+700+300")

    def command(self):
        self.master.withdraw()
        self.master.quit()

    def creatWidget(self):
        # 设置一个Label控件用于显示文字
        self.hellolable = Label(self, text="")
        # 把它放入到Frame中去
        self.hellolable.pack()
        # 设置一个Button
        self.quitbutton = Button(self, text="好的", command=self.command)
        # 把它放到frame去
        self.quitbutton.pack(side=TOP)

# 本版本不支持跨日，仅限当天
class StudyTime(object):
    """
    整体的思路就是根据给出的时间，通过计算->得到一个任务的时间线->根据时间线的每个元素，到点进行播报
    class_hours 上课时间
    break_time 休息时间
    start_time 开始时间
    end_time 结束时间
    """
    def __init__(self, class_hours, break_time):
        self.class_hours = class_hours
        self.break_time = break_time
        self.time = []
        self.timeline = []
        self.now_day = datetime.strftime(datetime.now(), "%Y-%m-%d ")

    # add new time
    # 这里添加时间线还有一个是为了消除bug，每次添加时间都会查看时间段是否有重叠，如果有，那么就不对这个时间段进行安排
    def add_time(self, start_time, end_time):
        self.start_clock = datetime.strptime(self.now_day + start_time, "%Y-%m-%d %H:%M")
        self.end_clock = datetime.strptime(self.now_day + end_time, "%Y-%m-%d %H:%M")
        if self.time == []:
            self.time.append((self.start_clock, self.end_clock))
            self.timeline = self.timeline + self.caltime(self.class_hours, self.break_time, start_time, end_time)
        else:
            bol = True
            for k in self.time:
                if k[0] < self.start_clock < k[1] or k[0] < self.end_clock < k[1]:
                    bol = FALSE
                else:
                    pass
            if bol:
                self.time.append((self.start_clock, self.end_clock))
                self.timeline = self.timeline + self.caltime(self.class_hours, self.break_time, start_time, end_time)
            else:
                pass

    @staticmethod
    def caltime(class_hours, break_time, start_time, end_time):
        time_line = []
        now_day = datetime.strftime(datetime.now(), "%Y-%m-%d ")
        start_clock = datetime.strptime(now_day + start_time, "%Y-%m-%d %H:%M")
        end_clock = datetime.strptime(now_day + end_time, "%Y-%m-%d %H:%M")
        rest_clock = datetime.strptime(now_day + start_time, "%Y-%m-%d %H:%M") + timedelta(minutes=int(class_hours))
        back_clock = rest_clock + timedelta(minutes=int(break_time))
        time_line.append(("study time", start_clock))
        while True:
            if rest_clock >= end_clock:
                time_line.append(("end to study", end_clock))
                break
            elif back_clock >= end_clock:
                time_line.append(("time to rest", rest_clock))
                time_line.append(("end to study", end_clock))
                break
            else:
                time_line.append(("time to rest", rest_clock))
                time_line.append(("time to back study", back_clock))
            rest_clock = back_clock + timedelta(minutes=int(class_hours))
            back_clock = rest_clock + timedelta(minutes=int(break_time))
        return time_line


def down():
    while True:
        temp = input("输入Q关闭时钟")
        if temp == "q":
            print("ok")
            exit()


def action():
    # 创建一个弹窗的实例
    app = application()

    # 添加时间
    first_clock = StudyTime("55", "5")
    first_clock.add_time("10:00", "12:00")
    first_clock.add_time("14:00", "17:30")
    first_clock.add_time("19:05", "21:00")
    first_clock.add_time("22:17", "22:32")
    # 遍历时间线timeline中所有需要播报的时间点
    app.hellolable["text"] = f"欢迎使用番茄钟0.1,您的配置如下:\nclass hours: {first_clock.class_hours} minutes" \
                             f"\nbreak time: {first_clock.break_time} minutes\nTIP：在终端输入q关闭闹钟"
    app.mainloop()
    for temp in first_clock.timeline:
        # if first_clock.timeline not empty
        if temp:
            # 去掉过时的时间点
            if temp[1] > datetime.now():
                # 使用sleep函数让程序暂停若干秒直到下个时间
                lag = (temp[1] - datetime.now()).seconds - 1
                # 循环lag秒，每次sleep一秒，并且检测线程是否还在，如果不在则退出
                for var1 in range(1, lag):
                    if thread1.is_alive():
                        sleep(1)
                    else:
                        exit()
                # 修改播报内容
                app.hellolable["text"] = temp[0]
                # 更新啥，这个不同理解
                app.master.update()
                # 让app显示出来
                app.master.deiconify()
                # 运行app
                app.mainloop()
    # 完成所有任务，退出程序
    exit()

if __name__ == "__main__":
    thread1 = Thread(target=down, name="down")
    thread2 = Thread(target=action, name="loop")
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

# 多线程两个线程，一个运行时钟，一个在终端等待用户输入Q来退出程序



