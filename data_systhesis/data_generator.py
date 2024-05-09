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
你是一个出色的数学大师，你现在的任务是为某次数学测验编写题目，题目要包含几何、代数、分析、概率等。
编写过程中，请确保表述清晰，用词简洁，多用专业术语，题目背景可以考虑现实生活中的真实场景，不要出现与客观规律不符合的描述，可以考虑与其它学科进行结合。
以下是一个示例的JSON格式的输出结果：

```json
[
        {
            "from": "human",
            "value": "设函数 f(x) = x^3 - 3x + 1，请求出 f(x) = 0 时 x 的近似值，并论述解的存在性。"
        },
        {
            "from": "gpt",
            "value": "首先给出思考过程：为了求解方程 f(x) = 0，可以使用牛顿迭代法（Newton's method），一种有效的寻找函数零点的方法。我们首先确定解的存在性，可以使用介值定理。"
        },
        {
            "from": "gpt",
            "value": "观察函数 f(x)，其在合理定义域内连续且可微，我们首先选取一个近似值作为起点进行迭代。例如，选取 x=1 作为初始值。函数的导数是 f'(x) = 3x^2 - 3。我们应用牛顿迭代公式来更新 x 的值：\\\\[ x_{n+1} = x_n - \\\\frac{f(x_n)}{f'(x_n)} \\\\]。这个公式将被用于反复迭代直到收敛到零点。"
        },
        {
            "from": "function_call",
            "value": "```python\nimport math\n\ndef newton_method(f, df, x0, tol=1e-6, max_iter=100):\n    x = x0\n    for i in range(max_iter):\n        current_f = f(x)\n        current_df = df(x)\n        if abs(current_f) < tol:\n            return x, i\n        x -= current_f / current_df\n    return x, max_iter\n\n# 定义函数和其导数\nf = lambda x: x**3 - 3*x + 1\ndf = lambda x: 3*x**2 - 3\n\n# 进行牛顿迭代\ninitial_x = 1.1\nroot, iterations = newton_method(f, df, initial_x)\n\nprint('经过', iterations, '次迭代后，方程的解近似为：', root)\n```\n"
        },
        {
            "from": "observation",
            "value": "现在将上面的代码复制到Python环境中运行，这个程序将帮助我们找到方程 f(x) = 0 的一个根的近似值。运行结果为：```经过 6 次迭代后，方程的解近似为： 1.5320889844442256```"
        },
        {
            "from": "gpt",
            "value": "因此，使用牛顿迭代法，我们发现 f(x) = x^3 - 3x + 1 的一个解的近似值是 1.532。此外，通过介值定理，我们知道在 x = 0 和 x = 2 之间至少存在一个根，因为 f(0) = 1 和 f(2) = -1 故在 (0, 2) 区间内函数值经过了零点。"
        }
]
```

在回答过程中，你可以调用Python代码，并给出Python代码运行结果，要求输出格式与上述例子的输出相同，以```json开头，以```结尾，中间是JSON字符串，第一步一定要给出思考过程。
现在，请你开始编写一个给%s做的数学测验题目。

出题要求：
1. 题目要求随机生成，不能是固定的题目。
2. 题目要求有一定的难度，不能太简单。
3. 题目的描述要清晰明了，且表达形式要丰富多样，有时候可以用中文来描述。
4. 计算题中可以包含一些特殊的数学符号。
5. 题目的答案如果是无理数的话，则需要将其转化为分数或者根式，或者保留其原始的形式。
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
            time_sleep = random.randint(10, 300)
            time.sleep(time_sleep)
            print(f"time sleep: {time_sleep}")
        except Exception as e:
            print(e)
            pass
