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
    return_messasge = await process_message(await request.form, await request.files, False)
    
    if "error" in return_messasge:
        return jsonify({"error": "ERROR"}), 500
    return jsonify(return_messasge)

@app.route('/return', methods=['POST'])
async def return_value():
    print("# [server.py] [return_value] Request received")
    if "image" in (await request.files):
        return_message = await process_message(await request.form, (await request.files)["image"] , True)
    else:
        return_message = await process_message(await request.form, None, True)

    if "error" in return_message:
        return jsonify({"error": "ERROR"}), 500
    return jsonify(return_message)

if __name__ == '__main__':
    app.run(host="0.0.0.0")