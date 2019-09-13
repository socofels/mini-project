from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from gothonweb import planisphere
# 实例当前这个程序


app = Flask(__name__)


@app.route("/")
def index():
    # this is used to "setup" the session with starting values
    # session，就是会话，其作用是保证在页面转跳时，这个session['room_name']变量能得到保存
    session['room_name'] = planisphere.START

    # 返回的意思是转跳至 def game这个函数。
    return redirect(url_for("game"))


@app.route("/game", methods=['GET', 'POST'])
def game():
    # room_name是字符串 room 是变量
    room_name = session.get('room_name')
    if request.method == "GET":
        room = planisphere.load_room(room_name)
        return render_template("show_room.html", room=room)


    # 当输入提交的时候，任务转跳到这里
    else:
        action = request.form.get('action')

        if room_name and action:
            # room 就是 room_name 的变量
            room = planisphere.load_room(room_name)
            # 下一个房间就是room.go(对应的操作)
            next_room = room.go(action)
            if not next_room:
                # 如果你的动作没有下个房间，那么就保持原地不动
                #session['room_name']是字符串
                pass
            else:
                session['room_name'] = next_room

        return redirect(url_for("game"))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run
