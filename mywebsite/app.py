from flask import Flask
from flask import render_template
from flask import request
import os
thisdir = os.getcwd()

app = Flask(__name__)

#@app.route 将页面"/hello" 与 自定义的函数 index 绑定，当进入页面时运行函数index
@app.route("/hello", methods=["POST", "GET"])
def index():
    greeting = "hello world"
    print(request.method)
    try:
        print(request.form['name'])
    except:
        pass
    if request.method == "POST":
        name = request.form['name']
        greet = request.form['greet']
        greeting = f"{greet}{name}"

        return render_template("index.html", greeting=greeting)
    else:
        return render_template("hello_form.html")

@app.route("/upload", methods=["POST", 'GET'])
def upload():
    print(request.method)
    if request.method == "GET":
        return render_template("upload_image.html")
    else:
        #上传图片
        image = request.files['file']
        dir(request.files)
        imagedir = thisdir + "\\disk\\images\\"
        file_path = imagedir + image.filename
        print(image.filename)
        image.save(file_path)
        # return "ok"
        upimage = {"file": file_path}
        return render_template("show_image.html", image_path=upimage)

@app.route('/up', methods=['GET', 'POST'])
def up():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        # f.save(os.path.join('app/static',filename))
        f.save('app/static/' + str(filename))
        return 'ok'
    else:
        return render_template('upload.html')

if __name__ == "__main__":
    app.run
