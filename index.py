# coding=utf8

from flask import Flask, request
from fuckpj import main
app = Flask("FuckPingJiao")


@app.route("/")
def api():
    sid = request.args.get("SID", None)
    if not sid:
        return "Add student id: ?SID=your-student-id"
    return str(main(sid))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
