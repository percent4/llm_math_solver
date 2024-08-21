# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: add_boxed_in_first_reply.py
# @time: 2024/8/21 21:36
import re
import json

with open('train_data.json', 'r', encoding='utf-8') as f:
    train_data = json.loads(f.read())


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


new_train_data = []
for sample in train_data:
    conv = sample['conversations']
    if len(conv) != 5:
        new_train_data.append(sample)
    else:
        final_reply = conv[-1]['value']
        first_reply = conv[2]['value']
        final_answer = remove_boxed(last_boxed_only_string(final_reply))
        # print(final_answer)
        # 使用正则表达式实现: 检查final_answer是小数或整数，可以为负数
        if final_answer and re.match(r'^-?\d+(\.\d+)?$', final_answer):
            if ('```python' in first_reply and '验证' in first_reply and final_answer in first_reply and
                    '\\boxed' not in first_reply):
                # 使用正则表达式实现: 在first_reply中找到最后一个final_answer的位置
                last_final_answer_idx = first_reply.split('验证')[0].rfind(final_answer)
                # print(sample)
                # 如果final_answer在first_reply中只出现一次，或者last_final_answer_idx和验证在first_reply中的绝对值距离不超过100个字符
                if first_reply.count(final_answer) == 1 or 0 < first_reply.rfind('验证') - last_final_answer_idx <= 100:
                    # 则在first_reply中的最后一个final_answer的位置前面添加\\boxed{, 对final_answer的后面添加}
                    print(last_final_answer_idx, final_answer,
                          first_reply[last_final_answer_idx:last_final_answer_idx + len(final_answer)])
                    # print(conv[1]['value'])
                    first_reply = first_reply[:last_final_answer_idx] + '\\boxed{' + final_answer + '}' + first_reply[last_final_answer_idx+len(final_answer):]
        # 将原先conv中的first_reply替换为添加了boxed的first_reply
        conv[2]['value'] = first_reply
        new_train_data.append({"conversations": conv})


# 将新的train_data写入到新的文件中
with open('new_train_data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(new_train_data, ensure_ascii=False, indent=4))




