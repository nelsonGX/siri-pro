from libs.process_image import process_image
from libs.chat.history import call_ai
from libs.functions.execute_python_function import execute_python_code
from libs.functions.search_google import search_google
import base64
import re

async def extract_function_call(text):
    print("# [process_message.py] [extract_function_call] Extracting Function Call...")
    pattern = r'```call_function\n(\w+)\((.*?)\)\n```'
    
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        action = match.group(1)
        params_str = match.group(2)
        
        params = {}
        triple_quote_pattern = r'(\w+)="""(.*?)"""'
        triple_quote_params = re.findall(triple_quote_pattern, params_str, re.DOTALL)
        for key, value in triple_quote_params:
            params[key] = value.strip()
            params_str = params_str.replace(f'{key}="""{value}"""', '')
        
        single_param_pattern = r'(\w+)=([^,]+)'
        single_params = re.findall(single_param_pattern, params_str)
        for key, value in single_params:
            value = value.strip('"\'')
            params[key] = value
        
        print("# [process_message.py] [extract_function_call] Function Call Extracted: " + action + " " + str(params))
        return action, params
    
    print("# [process_message.py] [extract_function_call] No Function Call Found")
    return None, None

async def process_server_functions(action, params):
    print("# [process_message.py] [process_server_functions] Processing Server Functions...")
    if action == "exec_py_code":
        code = params["code"]
        return await execute_python_code(code)
    elif action == "search_google":
        query = params["query"]
        return await search_google(query)
    return None

async def process_message(request_form, image, is_return):
    print("# [process_message.py] [process_message] Processing Message...")

    global is_first
    global location
    
    if 'count' in request_form:
        is_first = str(request_form['count']) == "1"
    else:
        is_first = False

    if not is_return:
        location = request_form['location']

    if 'prompt' not in request_form:
        prompt = ""
    else:
        prompt = request_form['prompt']
    
    if not image:
        return_message, return_message_processed = await call_ai(prompt, is_first, False, None, None, location)

    else:
        image_data, media_type = process_image(image)
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        return_message, return_message_processed = await call_ai(prompt, is_first, True, media_type, encoded_image, location)

    if return_message.startswith("[ERROR]"):
        return {"error": True}

    action, params = await extract_function_call(return_message)

    if action != None:
        check_server = await process_server_functions(action, params)
        if check_server:
            if action == "exec_py_code":
                action_name = "\n(執行了一些程式碼)\n\n"
            elif action == "search_google":
                action_name = "\n(搜尋了一些東西)\n\n"
            return_message1, return_message_processed1 = await call_ai("[SYSTEM] " + check_server, False, False, None, None, location)
            return {"response": return_message_processed + action_name + return_message_processed1}
        
        return {"response": return_message_processed, "action": {"name": action, "variables": params}}
    
    return {"response": return_message}