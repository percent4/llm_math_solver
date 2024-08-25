# -*- coding: utf-8 -*-
"""`eval/MATH/MATH_eval.py`: evaluation script for MATH dataset
"""
import os
import re
import math
import json
import subprocess
from rich.progress import track
from openai import OpenAI
import logging
from collections import defaultdict
from retry import retry
from random import choices

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

os.environ["OPENAI_BASE_URL"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "0"
client = OpenAI()

execution_desc = ["运行以上代码，输出会是： ",
                  "现在将上面的代码复制到Python环境中运行，运行结果为：",
                  "执行上述Python代码，运行结果将是：",
                  "上面的Python代码执行结果为：",
                  "运行上述代码，我们可以得到题目要求的答案。输出结果将是："]


question_answer_dict = defaultdict(list)

def last_boxed_only_string(string):
    idx = string.rfind("\\boxed")
    if idx < 0:
        idx = string.rfind("\\fbox")
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(string):
        if string[i] == "{":
            num_left_braces_open += 1
        if string[i] == "}":
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    if right_brace_idx == None:
        retval = None
    else:
        retval = string[idx:right_brace_idx + 1]

    return retval


def remove_boxed(s):
    left = "\\boxed{"
    try:
        assert s[:len(left)] == left
        assert s[-1] == "}"
        return s[len(left):-1]
    except:
        return None
    

def is_equal(first_answer: str, final_answer: str) -> bool:
    # 两个字符都不为空
    if first_answer and final_answer:
        # 如果两个数都是浮点数或整数，包括负数
        if re.match(r'^-?\d+(\.\d+)?$', first_answer) and re.match(r'^-?\d+(\.\d+)?$', final_answer):
            if math.fabs(float(first_answer) - float(final_answer)) > 1e-6:
                return False
    return True


@retry(exceptions=Exception, tries=3, delay=2)
def question_answer(query):
    messages = [{"role": "system", "content": "你是一个数学解题大师，请解决以下数学题，务必详细说明解题思路，并在必要时提供Python代码来支持你的推理。答案中的数值应使用\\boxed{}包围，最后的答案以“因此”开头并直接给出结论，不要添加任何多余的内容。"}]
    messages.append({"role": "user", "content": f"题目：{query}"})
    result = client.chat.completions.create(messages=messages, 
                                            model="gpt-3.5-turbo",
                                            temperature=0.2,
                                            stream=True)
    reply_message = ""
    for chunk in result:
        if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
            reply_message += chunk.choices[0].delta.content
    
    first_reply = reply_message
    
    # find python code and execute the code
    if '```python' in reply_message and '\n```' in reply_message:
        messages.append({"role": "assistant", "content": reply_message})
        python_code_string = re.findall(r'```python\n(.*?)\n```', reply_message, re.S)[0]
        python_file_path = 'temp.py'
        with open(python_file_path, 'w') as f:
            f.write(python_code_string)
        python_code_run = subprocess.run(['python3', python_file_path], stdout=subprocess.PIPE, timeout=10)
        if python_code_run.returncode:
            question_answer_dict[query].append(first_reply)
            raise RuntimeError("生成的Python代码无法运行！")
        python_code_execution = python_code_run.stdout.decode('utf-8')
        os.remove(python_file_path)
        if "``````" in python_code_execution:
            question_answer_dict[query].append(first_reply)
            raise ValueError("执行Python代码结果为空!")
        code_reply_str = choices(execution_desc, k=1)[0]
        code_reply = f"\n{code_reply_str}```{python_code_execution.strip()}```\n"
        reply_message += code_reply
        messages.append({"role": "user", "content": code_reply})
        result = client.chat.completions.create(messages=messages, 
                                            model="gpt-3.5-turbo",
                                            temperature=0.2,
                                            stream=True)
        
        final_reply = ""
        for chunk in result:
            if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
                reply_message += chunk.choices[0].delta.content
                final_reply += chunk.choices[0].delta.content
        # 判断第一个答案与最后的答案是否一致
        logger.info(first_reply)
        logger.info(final_reply)
        # 仅考虑\\boxed{在first_reply和final_reply中出现一次的情形
        if final_reply.count('\\boxed') == 1 and first_reply.count('\\boxed') == 1:
            first_answer = remove_boxed(last_boxed_only_string(first_reply))
            final_answer = remove_boxed(last_boxed_only_string(final_reply))
            if not is_equal(first_answer, final_answer):
                question_answer_dict[query].append(final_reply)
                raise ValueError("前后答案不一致！")
        return final_reply
    else:
        if '\\boxed' not in reply_message:
            question_answer_dict[query].append(reply_message)
            raise RuntimeError('生成答案中不含boxed!')
        return reply_message

with open('math_test.jsonl', 'r') as f:
    content = f.readlines()

samples = []
i = 1
for line in track(content):
    data = json.loads(line.strip())
    question, answer = data['problem'], data['solution']
    try:
        pred_answer = question_answer(question)
    except Exception:
        if question in question_answer_dict:
            # 如果question出现在question_answer_dict中，则以最后一次的预测答案作为最终答案
            pred_answer = question_answer_dict[question][-1]
        else:
            pred_answer = 'ERROR'
    data.update({"predict_answer": pred_answer})
    logger.info("*" * 50)
    logger.info('--- {} true: {}'.format(i, repr(answer)))
    logger.info('--- {} pred: {}'.format(i, repr(pred_answer)))
    i += 1
    with open('math_eval_result_qwen2_72b_math_v2.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False)+"\n")
