# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: openai_eval.py
# @time: 2024/8/29 11:05
import os
import json
from openai import OpenAI
from dotenv import load_dotenv


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


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

with open("gaokao_2024_ii.json", "r", encoding="utf-8") as file:
    data = json.load(file)

system_prompt = ("你是一个数学解题大师，请解决以下数学题，务必详细说明解题思路，并在必要时提供Python代码来支持你的推理。"
                 "答案中的数值应使用\\boxed{}包围，最后的答案以“因此”开头并直接给出结论，不要添加任何多余的内容。")

predict_answers = []
for i, item in enumerate(data):
    print(f"第{i+1}题：{item['question']}")
    question = item["question"]

    # using openai chat api to get the response, model: gpt-4o
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"题目：{question}"}
    ]
    result = client.chat.completions.create(messages=messages,
                                            model="gpt-4o",
                                            temperature=0.2)
    answer = result.choices[0].message.content
    print(answer)
    predict_answers.append({
        "question_no": i+1,
        "answer": answer,
        "predict": remove_boxed(last_boxed_only_string(answer))
    })


# save the predict answers to json file
with open("openai_predict_3.json", "w", encoding="utf-8") as file:
    json.dump(predict_answers, file, ensure_ascii=False, indent=4)
