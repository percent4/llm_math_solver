# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_collector.py
# @time: 2024/5/14 17:31
import os
import json


content = []
for file in os.listdir('./save'):
    if file.endswith('.json'):
        with open(f'./save/{file}', 'r') as f:
            content.append(json.loads(f.read()))

with open('../data/ape210k_sample_data.json', 'w') as f:
    f.write(json.dumps(content, ensure_ascii=False, indent=4))

print(f"共有{len(content)}条数据已保存到ape210k_sample_data.json文件中！")
