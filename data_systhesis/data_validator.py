# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_validator.py
# @time: 2024/4/29 21:28
import os
import re
import json
import subprocess


def check_file(file_path: str) -> bool:
    code_pass_flag = False
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.loads(f.read())['quiz']

    python_code_execution = ""
    result = ""
    try:
        # find Python code
        for item in content:
            if item['from'] == 'function_call':
                code = item['value']
                if '```python' in code:
                    python_code_string = re.findall(r'```python\n(.*?)\n```', code, re.S)[0]
                    python_file_path = 'temp.py'
                    with open(python_file_path, 'w') as f:
                        f.write(python_code_string)
                    python_code_execution = subprocess.run(['python3', python_file_path], stdout=subprocess.PIPE).stdout.decode('utf-8')
                    os.remove(python_file_path)

        # get code execution result
        for item in content:
            if item['from'] == 'observation':
                code = item['value']
                if '代码' in code and ('运行' in code or '执行' in code or '输出' in code) and '```' in code:
                    result = re.findall(r'```(.*?)```', code, re.S)[0]

    except Exception as err:
        print(err)

    # check code execution result
    if result and python_code_execution and result in python_code_execution:
        code_pass_flag = True
    if not code_pass_flag:
        print('*' * 50)
        print(f"file: {file_path}\npython code execution: {repr(python_code_execution)}result: {repr(result)}\n"
              f"code pass: {code_pass_flag}")

    return code_pass_flag


if __name__ == '__main__':
    file_white_list = ["4c40358d-3821-4090-8cff-842fd2229615.json",
                       "356e876e-d0b6-453d-b1bd-fe4a94f207d2.json",
                       "ee2bc137-6d7e-4543-9267-3c50afe0af8a.json",
                       "0962e1ef-33c3-4baa-ada4-f134e8776840.json",
                       "f19a2a70-56a9-4db4-b61a-400352907db7.json",
                       "640e0db7-aff5-41ee-860d-d3a97cac1874.json"
                       ]

    dataset_dir = '../data'
    file_not_pass_list = []
    for os_file_path in os.listdir(dataset_dir):
        if os_file_path in file_white_list:
            continue
        json_file_path = os.path.join(dataset_dir, os_file_path)
        code_pass = check_file(json_file_path)
        if not code_pass:
            file_not_pass_list.append(os_file_path)

    print("\nfile not pass list:\n")
    for _ in file_not_pass_list:
        print(_)
    print("length of file not pass list: ", len(file_not_pass_list))
