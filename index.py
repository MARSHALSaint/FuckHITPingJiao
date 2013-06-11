# coding=utf8

import re
import requests
from random import randint, shuffle
from flask import Flask, request

app = Flask("FuckPingJiao")


# build a regex pattern to fetch the hidden inputs out of form
pattern = r'<input\s+name="(?P<name>[^"]+)"[^>]+value="(?P<value>[^"]+)"\s*>'


def step1(cookies):
    """The first step: http://xscj.hit.edu.cn/hitjwgl/xs/pj/PJJS4.asp"""
    # get the html of form
    uri_get = "http://xscj.hit.edu.cn/hitjwgl/xs/pj/PJJS4.asp"
    res = requests.get(uri_get, cookies=cookies)
    html = res.text  # repsonse html

    data = {}  # build our post data
    lst = re.findall(pattern, html)  # find out the inputs
    data.update(dict((x[0], x[1]) for x in lst))
    # how many his courses are
    number = int(data["ALLRS"])
    for i in range(1, number+1):
        for j in range(1, 8):
            data["PJ"+str(i)+"_"+str(j)] = randint(3, 5)
        data["PJ"+str(i)+"_8"]  = ""
        data["PJ"+str(i)+"_9"]  = ""
    # url to post to
    uri_post = "http://xscj.hit.edu.cn/hitjwgl/xs/pj/PJJS4_Save.asp"
    res = requests.post(uri_post, data=data, cookies=cookies)
    return res


def step2(cookies):
    """The 2nd step: http://xscj.hit.edu.cn/hitjwgl/xs/pj/PJKC4.asp"""
    # get the html of form
    uri_get = "http://xscj.hit.edu.cn/hitjwgl/xs/pj/PJKC4.asp"
    res = requests.get(uri_get, cookies=cookies)
    html = res.text  # repsonse html

    data = {}  # build our post data
    lst = re.findall(pattern, html)  # find out the inputs
    data.update(dict((x[0], x[1]) for x in lst))
    # how many his courses are
    number = int(data["ALLRS"])
    for i in range(1, number+1):
        for j in range(10, 15):
            data["PJ"+str(i)+"_"+str(j)] = randint(3, 5)
        data["PJ"+str(i)+"_15"] = str(randint(80, 95))
    # url to post to
    uri_post = "http://xscj.hit.edu.cn/hitjwgl/xs/pj/PJKC4_Save.asp"
    res = requests.post(uri_post, data=data, cookies=cookies)
    return res


def step3(cookies):
    """The 3rd step: http://xscj.hit.edu.cn/hitjwgl/xs/pj/ZHPJ4.asp"""

    uri_get = "http://xscj.hit.edu.cn/hitjwgl/xs/pj/ZHPJ4.asp"
    res = requests.get(uri_get, cookies=cookies)
    html = res.text  # repsonse html

    data = {}  # build our post data
    lst = re.findall(pattern, html)  # find out the inputs
    data.update(dict((x[0], x[1]) for x in lst))
    # how many his courses are
    number = int(data["ALLRS"])

    # best: 0-1 teacher
    # good: 2-4 teachers

    # make a list of number size
    l = [0] * number
    l[0] = 6
    l[1] = l[2] = l[3] = l[4] =  5
    for i in range(5, number):
        l[i] = 4
    # shuffle it
    shuffle(l)

    for i in range(0, number):
        data["PJ"+str(i+1)] = l[i]
    # url to post to
    uri_post = "http://xscj.hit.edu.cn/hitjwgl/xs/pj/ZHPJ4_Save.asp"
    res = requests.post(uri_post, data=data, cookies=cookies)
    return res


@app.route("/")
def main():
    # --------------- Create Cookies  -------------------
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

    # ----------  End cookies creation -----------------
    re_1 = step1(cdct)
    re_2 = step2(cdct)
    re_3 = step3(cdct)

    relst = [re_1.status_code, re_2.status_code, re_3.status_code]

    re_codes = []

    for i in relst:
        if i == 200:
            re_codes.append(0)
        else:
            re_codes.append(1)

    return str(sum(re_codes))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
