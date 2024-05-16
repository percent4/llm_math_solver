# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_merge.py
# @time: 2024/5/10 14:20
import json

with open("hand-make-train-data.json", "r", encoding="utf-8") as f:
    hand_make_train_data = json.load(f)

with open("llm_train_data.json", "r", encoding="utf-8") as f:
    math_train_data = json.load(f)

with open("ape210k_sample_data.json", "r", encoding="utf-8") as f:
    ape210k_train_data = json.load(f)

with open("gsm8k_train_data.json", "r", encoding="utf-8") as f:
    gsm8k_train_data = json.load(f)

content = hand_make_train_data + math_train_data + ape210k_train_data + gsm8k_train_data
new_content = []
for item in content:
    conversations = item["conversations"]
    conversations.insert(0, {"from": "system", "value": "你是一个数学解题大师，请解决下面的数学题，给出思考过程，必要时需要给出解题过程中的Python代码。正确答案的数值用\\boxed{}包围起来，最终的答案以因此开头，不要讲多余的废话。"})
    new_content.append({"conversations": conversations})

with open("train_data.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(new_content, ensure_ascii=False, indent=4))

print("共有{}条数据".format(len(new_content)))
