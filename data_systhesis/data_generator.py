# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: data_generator.py
# @time: 2024/4/25 10:45
import json
import os
import re
import time
import random
from uuid import uuid4
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_math_data():
    _type = random.choices(["高中生", "初中生", "小学生"], k=1)[0]
    print(_type)
    query = """
现在，请你开始编写一个给%s做的数学运算题目。
数学运算题目的出题方式要丰富多样，可以是加减乘除，也可以是分数、小数等，也可以出现复杂的运算，比如开方、对数、三角函数等。
在回答过程中，你可以调用Python代码，使用math或sympy模块，并给出Python代码的运行结果，要求输出格式与上述例子的输出相同，以```json开头，以```结尾，中间是JSON字符串，第一步一定要给出思考过程。

以下是一个示例的JSON格式的输出结果：

```json
[
    {
        "from": "human",
        "value": "计算 345 * 321 = ？"
    },
    {
        "from": "gpt",
        "value": "首先给出思考过程：这是一道简单的数学运算题目，考察的是两个整数的乘法。直接调用Python代码计算即可。"
    },
    {
        "from": "function_call",
        "value": "```python\ndef multiply(num1, num2):\n    return num1 * num2\n\nnum1 = 345\nnum2 = 123\n\nprint(f'{num1} * {num2} = {multiply(num1, num2)}')\n```\n"
    },
    {
        "from": "observation",
        "value": "现在将上面的代码复制到Python环境中运行，运行以上代码，输出会是： ```345 * 123 = 42435```"
    },
    {
        "from": "gpt",
        "value": "因此，345 * 123 = 42435"
    }
]
```

出题要求：
1. 题目要求随机生成，不能是固定的题目。
2. 题目要求有一定的难度，不能太简单。
3. 题目的描述要清晰明了，且表达形式要丰富多样，有时候可以用中文来描述。
4. 计算题中可以包含一些特殊的数学符号，比如分数、小数、开方、对数、三角函数等。
""" % _type

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
        model="gpt-4-turbo",
        temperature=1.0
    )

    return _type, response.choices[0].model_dump()['message']['content']


if __name__ == '__main__':
    while True:
        _type, output = get_math_data()
        try:
            print(repr(output))
            post_output = json.loads(re.findall(r'```json\n(.*)\n```', output.strip(), re.DOTALL)[0], strict=False)
            print(repr(post_output))
            with open(f'../data/{str(uuid4())}.json', 'w') as f:
                f.write(json.dumps({"type": _type, "quiz": post_output}, ensure_ascii=False, indent=4))
            time_sleep = random.randint(1, 3)
            time.sleep(time_sleep)
            print(f"time sleep: {time_sleep}")
        except Exception as e:
            print(e)
            pass
