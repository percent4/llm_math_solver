# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_collector.py
# @time: 2024/4/30 23:09
import json
import os
from tqdm import tqdm

train_data = []
dataset_dir = '../align_data'
for os_file_path in tqdm(os.listdir(dataset_dir)):
    json_file_path = os.path.join(dataset_dir, os_file_path)
    print(json_file_path)
    with open(json_file_path, 'r', encoding='utf-8') as f:
        transformed_messages = []
        messages = json.loads(f.read())['quiz']
        i = 0
        while i < len(messages):
            role = messages[i]['from']
            if role == 'human':
                if '题目：' not in messages[i]['value']:
                    messages[i]['value'] = '题目：' + messages[i]['value']
                transformed_messages.append(messages[i])
                i += 1
            elif role == 'gpt':
                gpt_message = messages[i]['value']
                i += 1
                while i < len(messages) and messages[i]['from'] in ['gpt', 'function_call']:
                    add_message = '\n' if messages[i]['value'] == 'gpt' else '\n生成的Python代码如下：\n'
                    gpt_message += (add_message + messages[i]['value'])
                    i += 1
                transformed_messages.append({"from": "gpt", "value": gpt_message})
            elif role == 'observation':
                transformed_messages.append({"from": "human", "value": messages[i]['value']})
                i += 1

        # check role
        for _index, role_message in enumerate(transformed_messages):
            role = role_message['from']
            if _index % 2 == 0:
                assert role == 'human'
            else:
                assert role == 'gpt'

        train_data.append({"conversations": transformed_messages})

with open('math_train_data_2.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(train_data, ensure_ascii=False, indent=4))
