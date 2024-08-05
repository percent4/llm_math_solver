# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: math_eval_update.py
# @time: 2024/5/21 14:00
# 对模型评估后的结果加入是否正确的标记
"""`eval/MATH/math_eval_update.py`: update the evaluation result with correctness for MATH dataset.
"""
import json

from math_equivalence import is_equiv


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


if __name__ == '__main__':
    with open("math_eval_result_qwen2_72b_math_v2.json", "r", encoding="utf-8") as f:
        data = f.readlines()

    correct_cnt = 0
    content = []
    for i, line in enumerate(data):
        is_correct = False
        sample = json.loads(line.strip())
        true_answer, pred_answer = sample["solution"], sample["predict_answer"]
        try:
            true_answer_str = remove_boxed(last_boxed_only_string(true_answer))
            pred_answer_str = remove_boxed(last_boxed_only_string(pred_answer))
            if pred_answer_str is not None and is_equiv(true_answer_str, pred_answer_str):
                correct_cnt += 1
                is_correct = True
            print(i, true_answer_str, pred_answer_str, correct_cnt, i + 1, correct_cnt/(i+1))
        except Exception as e:
            print(e)
        sample.update({"is_correct": is_correct})
        content.append(sample)

    with open("math_eval_result_update.json", "w", encoding="utf-8") as f:
        for _ in content:
            f.write(json.dumps(_, ensure_ascii=False) + "\n")
