# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_generator.py
# @time: 2024/5/24 15:46
import os
import re
import json
import subprocess
from random import choices
from openai import OpenAI
from dotenv import load_dotenv
from retry import retry
from datasets import load_dataset

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

execution_desc = ["运行以上代码，输出会是： ",
                  "现在将上面的代码复制到Python环境中运行，运行结果为：",
                  "执行上述Python代码，运行结果将是：",
                  "上面的Python代码执行结果为：",
                  "运行上述代码，我们可以得到题目要求的答案。输出结果将是："]


def get_system_prompt(true_answer) -> str:
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
                  "正确答案的数值用\\boxed{}包围起来，\\boxed{}中的答案格式" + f"按 '{true_answer}' 格式给出，不要改变最终答案，最终的答案以因此开头，不要讲多余的废话。")
    return ''.join(prompt)


def write_to_json(query, thought, code, code_result, output, filename):
    file_path = f'./save/{filename}.json'
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


@retry(exceptions=Exception, tries=2, delay=2)
def generate_data(query, true_answer, queId):
    print('->', queId, repr(query), repr(true_answer))
    messages = [{'role': 'system', 'content': get_system_prompt(true_answer)},
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
        python_code_execution = subprocess.run(['python3', python_file_path],
                                               stdout=subprocess.PIPE,
                                               timeout=10).stdout.decode('utf-8')
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
        # find the answer
        predict_answer = remove_boxed(last_boxed_only_string(second_reply))
    else:
        # find the answer
        predict_answer = remove_boxed(last_boxed_only_string(first_reply))
    print('--->', repr(second_reply), repr(code_reply), repr(python_code_string))
    print('---->', repr(predict_answer), repr(true_answer))
    # check if the answer is correct
    if true_answer.strip() == predict_answer.strip():
        write_to_json(query,
                      first_reply.split('\n```')[0],
                      '```python\n' + python_code_string + '\n```',
                      code_reply,
                      second_reply,
                      filename=queId)
        return True
    else:
        raise ValueError('The answer is not correct.')


if __name__ == '__main__':
    exist_file_list = [_.split('.')[0] for _ in os.listdir('./save')]
    # get tal_scq5k train dataset
    train_data = load_dataset('math-eval/TAL-SCQ5K', split='train')
    new_data = train_data.shuffle(seed=4202)
    # generate data using GPT-4o
    cnt = 0
    for i in range(len(new_data)):
        if new_data[i]['qtype'] == 'single_choice':
            queId = new_data[i]['queId']
            if queId not in exist_file_list:
                problem = new_data[i]['problem'].replace('$$', '')
                answer_option_list = {_[0]['aoVal']: _[0]['content'].replace('$$', '') for _ in new_data[i]['answer_option_list']}
                correct_answer = answer_option_list[new_data[i]['answer_value']]
                try:
                    flag = generate_data(problem, true_answer=correct_answer, queId=queId)
                except Exception as e:
                    flag = False
                    print('----->', repr(e))
                if flag:
                    cnt += 1
        if cnt >= 1:
            break

