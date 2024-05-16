# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_generator.py
# @time: 2024/5/15 11:18
# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_generator.py
# @time: 2024/5/13 22:07
import os
import re
import json
from uuid import uuid4
import subprocess
from random import choices
from openai import OpenAI
from dotenv import load_dotenv
from retry import retry
import math


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

execution_desc = ["运行以上代码，输出会是： ",
                  "现在将上面的代码复制到Python环境中运行，运行结果为：",
                  "执行上述Python代码，运行结果将是：",
                  "上面的Python代码执行结果为：",
                  "运行上述代码，我们可以得到题目要求的答案。输出结果将是："]


def get_system_prompt() -> str:
    prompt = ["观察下面的数学解题示例：\n"]
    i = 0
    files = choices(os.listdir('../hand_make/save'), k=3)
    for file in files:
        if file.endswith('.json'):
            with open(f'../hand_make/save/{file}', 'r') as f:
                data = json.load(f)
                i += 1
                prompt.append(f"\n\n- 示例{i}: \n\n")
                for sample in data['conversations']:
                    role = sample['from'].replace('human', 'user').replace('gpt', 'assistant')
                    content = sample['value']
                    if '```python' in content and '\n```' in content:
                        content = '```'.join(content.split('```')[:-1]) + '```'
                    prompt.append("{}: {}\n".format(role, content))
    prompt.append("\n\n现在，请解决下面的数学题，首先要给出思考过程，注意解题过程要严格按照示例中的来，必要时需要给出解题过程中的Python代码。"
                  "正确答案的数值用\\boxed{}包围起来，最终的答案以因此开头，不要讲多余的废话。")
    return ''.join(prompt)


def write_to_json(query, thought, code, code_result, output):
    file_path = f'./save/{str(uuid4())}.json'
    if code_result:
        data = {
            "conversations": [
                {
                    "from": "human",
                    "value": f"题目：{query}"
                },
                {
                    "from": "gpt",
                    "value": thought + code
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
    else:
        data = {
            "conversations": [
                {
                    "from": "human",
                    "value": f"题目：{query}"
                },
                {
                    "from": "gpt",
                    "value": thought + code
                }
            ]
        }
    with open(file_path, 'w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
    print(f"write to {file_path} successfully!")


def read_sample(shift: int) -> list[tuple]:
    with open('train.jsonl', 'r') as f:
        data = f.readlines()

    samples = []
    for line in data[shift:10000000]:
        sample = json.loads(line.strip())
        q, a = sample['question'], sample['answer'].split('####')[-1].strip().replace(',', '')
        samples.append((q, a))
    return samples


@retry(exceptions=Exception, tries=3, delay=2)
def generate_data(no, query, answer):
    answer = answer.replace('(', '').replace(')', '')
    true_answer = float(answer) if '/' not in answer else float(answer.split('/')[0]) / float(answer.split('/')[1])
    print('*' * 50)
    print('->', no, repr(query), repr(answer))
    messages = [{'role': 'system', 'content': get_system_prompt()},
                {"role": "user", "content": f"题目：{query}"}]
    result = client.chat.completions.create(messages=messages,
                                            model="gpt-4o",
                                            temperature=0.2,
                                            stream=True)
    first_reply = ""
    for chunk in result:
        if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
            first_reply += chunk.choices[0].delta.content
    print('-->', repr(first_reply))

    # find python code and execute the code
    python_code_string, code_reply, second_reply = "", "", ""
    if '```python' in first_reply:
        messages.append({"role": "assistant", "content": '```'.join(first_reply.split('```')[:-1]) + '```'})
        python_code_string = re.findall(r'```python\n(.*?)\n```', first_reply, re.S)[0]
        python_file_path = 'temp.py'
        with open(python_file_path, 'w') as f:
            f.write(python_code_string)
        python_code_execution = subprocess.run(['python3', python_file_path], stdout=subprocess.PIPE).stdout.decode(
            'utf-8')
        os.remove(python_file_path)
        code_reply_str = choices(execution_desc, k=1)[0]
        code_reply = f"\n{code_reply_str}```{python_code_execution.strip()}```\n"
        messages.append({"role": "user", "content": code_reply})
        result = client.chat.completions.create(messages=messages,
                                                model="gpt-3.5-turbo",
                                                temperature=0.2,
                                                stream=True)
        second_reply = ""
        for chunk in result:
            if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
                second_reply += chunk.choices[0].delta.content
        print('--->', repr(second_reply), repr(code_reply), repr(python_code_string))
        # find the answer
        if re.findall(r'\\boxed\{.+?}', second_reply):
            if '\\frac' in second_reply and len(re.findall(r'\\frac{(\d+)}{(\d+)}', second_reply)) == 1 and len(
                    re.findall(r'\\frac{(\d+)}{(\d+)}', second_reply)[0]) == 2:
                numerator, denominator = re.findall(r'\\frac{(\d+)}{(\d+)}', second_reply)[0]
                pred_answer_number = float(numerator) / float(denominator)
            else:
                pred_answer_number = \
                re.findall(r'(?<!\d|\.)\d+(?:\.\d+)?\s*?', re.findall(r'\\boxed\{.+?}', second_reply)[0])[0]
        else:
            pred_answer_number = math.inf
    else:
        # find the answer
        if re.findall(r'\\boxed\{.+?}', first_reply):
            if '\\frac' in first_reply and len(re.findall(r'\\frac{(\d+)}{(\d+)}', first_reply)) == 1 and len(re.findall(r'\\frac{(\d+)}{(\d+)}', first_reply)[0]) == 2:
                numerator, denominator = re.findall(r'\\frac{(\d+)}{(\d+)}', first_reply)[0]
                pred_answer_number = float(numerator) / float(denominator)
            else:
                pred_answer_number = re.findall(r'(?<!\d|\.)\d+(?:\.\d+)?\s*?', re.findall(r'\\boxed\{.+?}', first_reply)[0])[0]
        else:
            pred_answer_number = math.inf
    # check if the answer is correct
    if math.fabs(true_answer - float(pred_answer_number)) < 1e-2:
        print(no, true_answer, float(pred_answer_number))
        write_to_json(query,
                      first_reply.split('\n```')[0],
                      '```python\n' + python_code_string + '\n```',
                      code_reply,
                      second_reply)
        return True
    else:
        raise ValueError('The answer is not correct.')


if __name__ == '__main__':
    shift = 1000
    samples = read_sample(shift=shift)
    i = 1
    for j, item in enumerate(samples):
        try:
            q, a = item
            is_correct = generate_data(j + shift, q, a)
            if is_correct:
                i += 1
            if i > 300:
                break
        except Exception as e:
            print(e)
            pass
