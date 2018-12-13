from flask import Flask
from flask import send_file
from flask import request

app = Flask(__name__)

@app.route('/')
def sat_image():
    sat = request.args.get('sat', default = '*', type = str)
    if sat == "ls8":
        return send_file("LS8.png", mimetype='image/png')
    elif sat == "him8":
        return send_file("Him8.png", mimetype='image/png')
    elif sat == "modis":
        return send_file("Modis.png", mimetype='image/png')
    else:
        return "unkown satellite [ls8, him8, modis]"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
