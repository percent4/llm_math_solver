使用 `LLaMA-Factory` 框架进行模型SFT训练和模型推理。

基座模型：

- QWen-1.5-32B
- Yi-1.5-34B

### 数据合成

对大模型微调，使其具备数学解题能力，高质量的数据集是最重要的保障之一。

业界、数学界关于大模型数学解题能力方面的研究，已经有不少研究成果和数据集。在`LLaMa-Factory`中，内置了两类数学方面的数据集，它们为`BelleGroup/school_math_0.25M`和`TIGER-Lab/MathInstruct`，前者是包含约25万条由`BELLE`项目生成的中文数学题数据，包含解题过程，但题目偏简单，多为小学数学题；后者由13个具有中间原理的数学数据集编译而成，其中6个为新数据集，混合了思想链（CoT）和思想程序（PoT），确保覆盖了广泛的数学领域。

但是，这两个数据集并没有调用Python代码去解题，仅仅是利用了大模型本身的世界知识和推理能力（如COT）。

我们希望在用大模型解决数学题目时，能够按照我们读书时的解题过程，先给出思考过程，再调用合适的知识点（这里是Python）代码，最后给出结果。下面是一个数学题目的解答过程：

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

基于上述的这种格式，我们借助`GPT-4-turbo`模型进行数据合成，其中一个模板（即Prompt）如下：

```
现在，请你开始编写一个给初中生做的数学运算题目。
数学运算题目的出题方式要丰富多样，可以是加减乘除，也可以是分数、小数等，也可以出现复杂的运算，比如开方、对数、三角函数等。
在回答过程中，你可以调用Python代码，使用math或sympy模块，并给出Python代码的运行结果，要求输出格式与上述例子的输出相同，以```json开头，以```结尾，中间是JSON字符串，第一步一定要给出思考过程。

以下是一个示例的JSON格式的输出结果：

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

出题要求：
1. 题目要求随机生成，不能是固定的题目。
2. 题目要求有一定的难度，不能太简单。
3. 题目的描述要清晰明了，且表达形式要丰富多样，有时候可以用中文来描述。
4. 计算题中可以包含一些特殊的数学符号，比如分数、小数、开方、对数、三角函数等。
```

如何写好合适的Prompt，使得`GPT-4-turbo`能够遵循指令，给出高质量的数学解题过程，也是值得探索的，笔者这里只是给出了初步尝试的结果，这中间的过程还是有待提升的。

使用`GPT-4-turbo`模型生成数据，再经过大量时间的数据清洗与合成，最终我们得到547个样本（包含重复样本），它们都满足sharegpt格式，格式样例如下：

```
[
    {
        "conversations": [
            {
                "from": "human",
                "value": "题目：苹果的价格是每公斤3元，小明买了2.5公斤的苹果，他一共需要支付多少钱？"
            },
            {
                "from": "gpt",
                "value": "首先给出思考过程：这是一个简单的乘法问题，其中涉及到的是单价和数量的乘积计算。我们需要用苹果的单价乘以小明购买的苹果的重量来找出总金额。\n生成的Python代码如下：\n计算总金额的公式是： \\[ 总金额 = 单价 \\times 数量 \\] 在这个具体例子中，苹果的单价为3元每公斤，小明购买了2.5公斤。\n生成的Python代码如下：\n```python\ndef total_cost(price_per_kg, weight):\n    return price_per_kg * weight\n\n# 苹果的单价（每公斤）\nprice_per_kg = 3\n\n# 小明购买的苹果重量（公斤）\nweight = 2.5\n\n# 计算总金额\ncost = total_cost(price_per_kg, weight)\nprint('小明需要支付的总金额为:', cost)\n```\n"
            },
            {
                "from": "human",
                "value": "现在将上面的代码复制到Python环境中运行，我们应得到小明需要支付的总金额。运行结果将告诉我们具体的金额数值。 运行以上代码，输出会是： ```小明需要支付的总金额为: 7.5```"
            },
            {
                "from": "gpt",
                "value": "因此，小明购买2.5公斤苹果，总共需要支付7.5元。"
            }
        ]
    }
    ...
]
```

这就是我们最终送入`LLaMa-Factory`的数据格式了。

### 模型微调

使用`LLaMa-Factory`微调框架对大模型进行SFT，笔者之前在很多文章中已经介绍多次了，并没有太多新意，这里也不再给出详细的微调过程。

我们使用`Qwen/Qwen1.5-32B`模型，对上述合成的少量数据集进行SFT，训练完毕后导出模型为`Qwen1.5-32B-math`，再使用下面的脚本启动训练后模型的推理服务：

```
CUDA_VISIBLE_DEVICES=0 python -m llmtuner.api.app --model_name_or_path /models/Qwen1.5-32B-math --template qwen
```

### 模型预测

参考[`examples.pdf`](examples.pdf)文档。