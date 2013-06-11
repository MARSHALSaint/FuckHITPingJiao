# coding=utf8

from flask import Flask, request
from fuckpj import main
app = Flask("FuckPingJiao")


@app.route("/")
def api():
    sid = request.args.get("SID")
    return str(main(sid))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
