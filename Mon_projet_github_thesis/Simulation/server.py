from flask import Flask, send_file

app = Flask(__name__)

@app.route('/firmware')
def serve():
    return send_file('firmware.bin', mimetype='application/octet-stream')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)