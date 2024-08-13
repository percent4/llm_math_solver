# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data-merge.py
# @time: 2024/5/20 14:18
import json

with open("hand-make-train-data.json", "r", encoding="utf-8") as f:
    hand_make_train_data = json.load(f)

with open("llm_train_data.json", "r", encoding="utf-8") as f:
    math_train_data = json.load(f)

with open("ape210k_sample_data.json", "r", encoding="utf-8") as f:
    ape210k_train_data = json.load(f)

with open("gsm8k_train_data.json", "r", encoding="utf-8") as f:
    gsm8k_train_data = json.load(f)

with open("tal_scq5k_train_data.json", "r", encoding="utf-8") as f:
    tal_scq5k_train_data = json.load(f)

with open("numina_train_data.json", "r", encoding="utf-8") as f:
    numina_train_data = json.load(f)

content = []
content.extend(hand_make_train_data)
content.extend(math_train_data)
content.extend(ape210k_train_data)
content.extend(gsm8k_train_data)
content.extend(tal_scq5k_train_data)
content.extend(numina_train_data)
new_content = []
for item in content:
    conversations = item["conversations"]
    conversations.insert(0, {"from": "system", "value": "你是一个数学解题大师，请解决以下数学题，务必详细说明解题思路，并在必要时提供Python代码来支持你的推理。答案中的数值应使用\\boxed{}包围，最后的答案以“因此”开头并直接给出结论，不要添加任何多余的内容。"})
    new_content.append({"conversations": conversations})

with open("train_data.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(new_content, ensure_ascii=False, indent=4))

print("共有{}条人工检查数据".format(len(hand_make_train_data)))
print("共有{}条GPT-4生成数据".format(len(math_train_data)))
print("共有{}条APE210K数据".format(len(ape210k_train_data)))
print("共有{}条GSM8K数据".format(len(gsm8k_train_data)))
print("共有{}条TAL-SCQ5K数据".format(len(tal_scq5k_train_data)))
print("共有{}条NUMINA数据".format(len(numina_train_data)))
print("共有{}条数据".format(len(new_content)))
