# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_post_process.py
# @time: 2024/5/9 22:02
import json

with open('math_train_data.json', 'r') as f:
    data = json.load(f)

# 对数据集进行去重处理，依据为题目描述完全一样
post_data = []
questions = set()
for sample in data:
    q = sample['conversations'][0]['value']
    if q not in questions:
        questions.add(q)
        post_data.append(sample)
    else:
        print("重复数据：", q)

# 依据题目的相似度进行去重处理
pass

with open('math_train_data_post.json', 'w') as f:
    json.dump(post_data, f, ensure_ascii=False, indent=4)

print(f"去重前数据集大小：{len(data)}\n"
      f"去重后数据集大小：{len(post_data)}\n"
      f"去重数据大小：{len(data) - len(post_data)}")
