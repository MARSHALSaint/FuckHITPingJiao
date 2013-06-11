# coding=utf8

import re
import requests
from flask import Flask, request

app = Flask("FuckPingJiao")


@app.route("/")
def main():
    # get student id from url's parameters
    sid = request.args.get("SID")
    # read cookies string and create a new one
    cstr = open("data/cookie").read()
    clst = cstr.split(";")  # split into list
    cdct = {}

    for item in clst:
        k, v = item.split("=")
        k, v = k.strip(), v.strip()
        cdct[k]=v

    cdct["UserName"] = ""
    cdct["UserID"] = sid
    cdct["UserClass"] = "111111"

    # get the html of form
    uri_get = "http://xscj.hit.edu.cn/hitjwgl/xs/pj/PJJS4.asp"
    resp = requests.get(uri_get, cookies=cdct)
    html = resp.text  # repsonse html

    # how many his courses are
    number = html.count("</tr>") - 6

    data = {}  # build our post data

    for i in range(1, number+1):
        for j in range(1, 8):
            data["PJ"+str(i)+"_"+str(j)] = j % 2 + 4
        data["PJ"+str(i)+"_8"]  = ""
        data["PJ"+str(i)+"_9"]  = ""

    # build a regex pattern to fetch the hidden inputs out of form
    pattern = r'<input\s+name="(?P<name>[^"]+)"[^>]+value="(?P<value>[^"]+)"\s*>'

    lst = re.findall(pattern, html)  # find out the inputs

    data.update(dict((x[0], x[1]) for x in lst))
    # this is what, the number
    data["ALLRS"] = str(number)
    # url to post to
    uri_post = "http://xscj.hit.edu.cn/hitjwgl/xs/pj/PJJS4_Save.asp"
    res = requests.post(uri_post, data=data, cookies=cdct)
    return res.text


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
