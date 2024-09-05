import os
import sys
import venv
import asyncio
import tempfile
import re

import os
import sys
import venv
import asyncio
import tempfile
import re

async def execute_python_code(code: str):
    print("# [execute_python_function.py] [execute_python_code] Executing Python Code...")
    with tempfile.TemporaryDirectory() as temp_dir:
        venv.create(temp_dir, with_pip=True)

        python_path = os.path.join(temp_dir, "Scripts" if sys.platform == "win32" else "bin", "python" + (".exe" if sys.platform == "win32" else ""))

        requirements = extract_requirements(code)

        if requirements:
            await asyncio.create_subprocess_exec(python_path, "-m", "pip", "install", *requirements, check=True)

        code_file = os.path.join(temp_dir, "code.py")
        with open(code_file, "w", encoding="utf-8") as f:
            f.write(code)

        process = await asyncio.create_subprocess_exec(
            python_path,
            code_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        result = decode_output(stdout) + decode_output(stderr)
        print("# [execute_python_function.py] [execute_python_code] Python Code Executed: " + result)
        return result

def extract_requirements(code: str):
    print("# [execute_python_function.py] [extract_requirements] Extracting Requirements...")
    import_pattern = re.compile(r'^import\s+(\w+)|^from\s+(\w+)', re.MULTILINE)
    matches = import_pattern.findall(code)
    
    requirements = [m[0] or m[1] for m in matches if (m[0] or m[1]) not in sys.stdlib_module_names]
    
    return list(set(requirements))

def decode_output(output):
    encodings = ['utf-8', 'ascii', 'latin1', 'cp1252']
    for encoding in encodings:
        try:
            return output.decode(encoding)
        except UnicodeDecodeError:
            continue
    return output.decode('utf-8', errors='replace')