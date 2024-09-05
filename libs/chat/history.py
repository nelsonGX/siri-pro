from libs.chat.llm import generate_response
import re
import time
import aiofiles

history = []

def process_text(input_text):
    print("# [history.py] [process_text] Processing Text...")
    lines = input_text.split('\n')
    result = []
    for line in lines:
        if '```call_function' in line:
            break
        result.append(line)
    return '\n'.join(result)

async def read_prompt(location):
    print("# [history.py] [read_prompt] Creating System Prompt...")
    async with aiofiles.open("prompt.md", "r", encoding="utf-8") as f:
        system_prompt = await f.read()
    system_prompt = re.sub("{%variable.time_now%}", time.ctime(), system_prompt)
    system_prompt = re.sub("{%variable.location%}", location, system_prompt)
    print("# [history.py] [read_prompt] System Prompt: " + system_prompt[:50] + "...")
    return system_prompt

async def call_ai(prompt, is_first, has_image, media_type, encoded_image, location):
    print("# [history.py] [call_ai] Calling AI...")

    global history

    system_prompt = await read_prompt(location)

    print("# [history.py] [call_ai] User Prompt: " + prompt)
    if is_first:
        history = []

    if has_image and len(prompt) > 0:
        history.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": encoded_image,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        )
    elif has_image:
        history.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": encoded_image,
                        },
                    }
                ],
            }
        )
    else:
        history.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        )

    response = await generate_response(history, system_prompt)
    response_processed = process_text(response)

    history.append(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": response_processed
                }
            ],
        }
    )

    return response, response_processed