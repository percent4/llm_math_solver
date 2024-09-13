# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: make_glm_4_ft_data.py
# @time: 2024/9/5 17:42
import json

with open('new_train_data.json', 'r', encoding='utf-8') as f:
    train_data = json.loads(f.read())


with open('glm_4_ft_data.jsonl', 'w', encoding='utf-8') as f:
    for sample in train_data:
        conv = sample['conversations']
        print(conv)
        new_conv = []
        for dialog in conv:
            new_dialog = {"role": dialog['from'].replace("human", "user").replace("gpt", "assistant"),
                          "content": dialog['value']}
            new_conv.append(new_dialog)
        f.write(json.dumps({"messages": new_conv}, ensure_ascii=False) + '\n')
