# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: math_solver_pipeline.py
# @time: 2024/7/1 15:35
import os
import re
import subprocess
from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
from openai import OpenAI
from random import choices

os.environ["OPENAI_BASE_URL"] = "http://117.50.185.39:50080/v1"
os.environ["OPENAI_API_KEY"] = "token-abc123"
client = OpenAI()

execution_desc = ["运行以上代码，输出会是： ",
                  "现在将上面的代码复制到Python环境中运行，运行结果为：",
                  "执行上述Python代码，运行结果将是：",
                  "上面的Python代码执行结果为：",
                  "运行上述代码，我们可以得到题目要求的答案。输出结果将是："]


class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.name = "Math Solver Pipeline"
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")
        print(f"user_message: {user_message}")
        query = user_message
        messages = [{"role": "system","content": "你是一个数学解题大师，请解决下面的数学题，给出思考过程，必要时需要给出解题过程中的Python代码。正确答案的数值用\\boxed{}包围起来，最终的答案以因此开头，不要讲多余的废话。"}]
        messages.append({"role": "user", "content": f"题目：{query}"})
        result = client.chat.completions.create(messages=messages,
                                                model="Qwen2-72B-Instruct-math",
                                                temperature=0.2,
                                                stream=True)
        reply_message = ""
        for chunk in result:
            if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
                reply_message += chunk.choices[0].delta.content

        # find python code and execute the code
        if '```python' in reply_message and '\n```' in reply_message:
            messages.append({"role": "assistant", "content": '```'.join(reply_message.split('```')[:-1]) + '```'})
            python_code_string = re.findall(r'```python\n(.*?)\n```', reply_message, re.S)[0]
            python_file_path = 'temp.py'
            with open(python_file_path, 'w') as f:
                f.write(python_code_string)
            python_code_run = subprocess.run(['python3', python_file_path], stdout=subprocess.PIPE, timeout=10)
            if python_code_run.returncode:
                raise RuntimeError("生成的Python代码无法运行！")
            python_code_execution = python_code_run.stdout.decode('utf-8')
            os.remove(python_file_path)
            code_reply_str = choices(execution_desc, k=1)[0]
            code_reply = f"\n{code_reply_str}```{python_code_execution.strip()}```\n"
            reply_message += code_reply
            messages.append({"role": "user", "content": code_reply})
            result = client.chat.completions.create(messages=messages,
                                                    model="Qwen2-72B-Instruct-math",
                                                    temperature=0.2,
                                                    stream=True)

            final_reply = ""
            for chunk in result:
                if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
                    reply_message += chunk.choices[0].delta.content
                    final_reply += chunk.choices[0].delta.content
            return reply_message.replace('```python', '\n```python')
        else:
            return reply_message
