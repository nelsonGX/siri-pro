from quart import Quart, request, jsonify
from libs.process_message import process_message

app = Quart(__name__)

@app.route('/', methods=['GET'])
async def index():
    print("# [server.py] [index] Request received")
    return "Siri Pro API Endpoint. Please visit https://github.com/nelsonGX/siri-pro for more information."

@app.route('/check' , methods=['GET'])
async def check():
    print("# [server.py] [check] Request received")
    return "System Operational"

@app.route('/ask', methods=['POST'])
async def ask():
    print("# [server.py] [ask] Request received")
    try:
        ip = request.remote_addr
        if ip == "127.0.0.1":
            ip = request.headers["CF-Connecting-IP"]
        print("# [server.py] [ask] User IP: " + str(ip))
        return_messasge = await process_message(await request.form, await request.files, False, str(ip))
        
        if "error" in return_messasge:
            return jsonify({"error": "ERROR"}), 500
        return jsonify(return_messasge)
    except Exception as e:
        print("# [server.py] [ask] Error: " + str(e))
        return jsonify({"error": "ERROR"}), 500

@app.route('/return', methods=['POST'])
async def return_value():
    print("# [server.py] [return_value] Request received")
    try:
        print("# [server.py] [test] Request received")
        ip = request.remote_addr
        if ip == "127.0.0.1":
            ip = request.headers["CF-Connecting-IP"]
        print("# [server.py] [return_value] User IP: " + str(ip))
        if "image" in (await request.files):
            return_message = await process_message(await request.form, (await request.files)["image"] , True, str(ip))
        else:
            return_message = await process_message(await request.form, None, True, str(ip))

        if "error" in return_message:
            return jsonify({"error": "ERROR"}), 500
        return jsonify(return_message)
    except Exception as e:
        print("# [server.py] [return_value] Error: " + str(e))
        return jsonify({"error": "ERROR"}), 500

if __name__ == '__main__':

    app.run(host="0.0.0.0")