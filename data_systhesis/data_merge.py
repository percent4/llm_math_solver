# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_merge.py
# @time: 2024/5/10 14:20
import json

with open("hand-make-train-data.json", "r", encoding="utf-8") as f:
    hand_make_train_data = json.load(f)

with open("math_train_data.json", "r", encoding="utf-8") as f:
    math_train_data = json.load(f)

content = hand_make_train_data + math_train_data
with open("train_data.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(content, ensure_ascii=False, indent=4))

print("共有{}条数据".format(len(content)))
