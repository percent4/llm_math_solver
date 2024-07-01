# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_collector.py
# @time: 2024/5/25 09:46
import os
import json


content = []
for file in os.listdir('./save'):
    if file.endswith('.json'):
        with open(f'./save/{file}', 'r') as f:
            content.append(json.loads(f.read()))

with open('../data/tal_scq5k_train_data.json', 'w') as f:
    f.write(json.dumps(content, ensure_ascii=False, indent=4))

print(f"共有{len(content)}条数据已保存到tal_scq5k_train_data.json文件中！")
