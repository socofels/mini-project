from nose.tools import *
from app import app

app.config["TESTING"] = True
# flask 中的app.test_client() 会返回一个客户端，可以模拟web客户端进行测试
web = app.test_client()

def test_index():
    #follow_redirects=True 这个参数表示支持重新定向，因为我们页面会由hello_form转跳至index，所以要重新定向
    rv = web.get("/", follow_redirects=True)
    #网络请求状态码 200表示成功 404 失败
    assert_equal(rv.status_code, 200)

    #follow_redirects=True 这个参数表示支持重新定向，因为我们页面会由hello_form转跳至index，所以要重新定向
    rv = web.get("/game", follow_redirects=True)
    #网络请求状态码 200表示成功 404 失败
    assert_equal(rv.status_code, 200)