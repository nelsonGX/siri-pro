from anthropic import Anthropic
from load_config import ANTHROPIC_API_KEY

anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

async def generate_response(history, system_prompt):
    print("# [llm.py] [generate_response] Generating Response...")
    try:
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=system_prompt,
            messages=history
        )
        
        response = message.content[0].text
        print("# [llm.py] [generate_response] Response Generated: " + response)
        return response
    except Exception as e:
        print("# [llm.py] [generate_response] Error: " + str(e))
        return "[ERROR] " + str(e)