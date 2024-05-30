# -*- coding: utf-8 -*-
import gradio as gr
import os
import re
import json
from uuid import uuid4
import subprocess
from random import choices
from openai import OpenAI
from retry import retry

os.environ["OPENAI_BASE_URL"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "0"
client = OpenAI()

execution_desc = ["运行以上代码，输出会是： ",
                  "现在将上面的代码复制到Python环境中运行，运行结果为：",
                  "执行上述Python代码，运行结果将是：",
                  "上面的Python代码执行结果为：",
                  "运行上述代码，我们可以得到题目要求的答案。输出结果将是："]


@retry(exceptions=Exception, tries=3, delay=2)
def first_turn_answer(query):
    messages = [{"role": "system", "content": "你是一个数学解题大师，请解决下面的数学题，给出思考过程，必要时需要给出解题过程中的Python代码。正确答案的数值用\\boxed{}包围起来，最终的答案以因此开头，不要讲多余的废话。"}]
    messages.append({"role": "user", "content": f"题目：{query}"})
    result = client.chat.completions.create(messages=messages, 
                                            model="Qwen1.5-32B-math",
                                            temperature=0.0,
                                            stream=True)
    first_reply = ""
    for chunk in result:
        if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
            first_reply += chunk.choices[0].delta.content

    print('---->', first_reply)
    # find python code and execute the code
    if '```python' in first_reply and '\n```' in first_reply:
        messages.append({"role": "assistant", "content": first_reply})
        python_code_string = re.findall(r'```python\n(.*?)\n```', first_reply, re.S)[0]
        python_file_path = 'temp.py'
        with open(python_file_path, 'w') as f:
            f.write(python_code_string)
        python_code_run = subprocess.run(['python3', python_file_path], stdout=subprocess.PIPE)
        if python_code_run.returncode:
            print("生成的Python代码无法运行！")
            raise RuntimeError("生成的Python代码无法运行！")
        python_code_execution = python_code_run.stdout.decode('utf-8')
        os.remove(python_file_path)
        code_reply_str = choices(execution_desc, k=1)[0]
        code_reply = f"\n{code_reply_str}```{python_code_execution.strip()}```\n"
        messages.append({"role": "user", "content": code_reply})
        result = client.chat.completions.create(messages=messages,
                                                model="Qwen1.5-32B-math",
                                                temperature=0.0,
                                                stream=True)
        
        second_reply = ""
        for chunk in result:
            if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
                second_reply += chunk.choices[0].delta.content
                
        return first_reply.replace('```python\n' + python_code_string + '\n```', ''), '```python\n' + python_code_string + '\n```', code_reply, second_reply
    else:
        return first_reply, '', '', ''
    

def write_to_json(query, tought, code, code_result, output):
    file_path = f'./save/{str(uuid4())}.json'
    data = {
        "conversations": [
            {
                "from": "human",
                "value": f"题目：{query}"
            },
            {
                "from": "gpt",
                "value": tought + code
            },
            {
                "from": "human",
                "value": code_result
            },
            {
                "from": "gpt",
                "value": output
            }
        ]
    }
    with open(file_path, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
    print(f"write to {file_path} successfully!")
    return '', '', '', '', ''
                

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(lines=3, placeholder="题目", label="数学题目")
        with gr.Column():
            tought = gr.Textbox(lines=3, label="思考过程")
            code = gr.Markdown(label="代码Python结果")
            code_result = gr.Markdown(label="执行结果")
            output = gr.Textbox(lines=3, label="最终回答")
            submit = gr.Button("Submit")
            save = gr.Button("Save")
            
    submit.click(fn=first_turn_answer,
                 inputs=user_input,
                 outputs=[tought, code, code_result, output])
    save.click(fn=write_to_json,
               inputs=[user_input, tought, code, code_result, output],
               outputs=[user_input, tought, code, code_result, output])

demo.launch(server_name="0.0.0.0", server_port=8001, share=True)
