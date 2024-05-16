本项目用于大模型数学解题能力方面的数据集合成，主要包括以下几个部分：

### 数据集

- 数据合成: data_synthesis/data_generation.py
- 数据校验: data_synthesis/data_validator.py
- 数据格式转换: data_synthesis/make_train_data.py
- Web服务人工数据录入: data_synthesis/math_gen_server.py
- 人工数据整理：data_synthesis/hand-make-train-data.py
- 数据合并：data_synthesis/data_merge.py

生成的样例数据如下：

```json
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
    },
    ...
]
```

训练数据集分布如下（共``条）：

- GPT-4生成: `451`条
- WEB服务（GPT-4 few-shot生成，人工输入题目并检查）：`330`条
- gsm8k 训练集数据: 人工输入题目并检查， ~`30`条
- Chinese-AAAI-Math: 预计`10`条
- APE210K: 大模型自动生成，`1109`条
- GSM8K: 大规模自动生成, ~`500`条

### 改进点

后续将会改进的点如下：

- [ ] 高质量数学题的数据集获取(进行中...)
- [ ] 更大规模、更高质量、形式更丰富的数学题的数据合成(进行中...)
- [ ] 数据集的清洗，包括公式整理、去重等(进行中...)
- [ ] 加入 高等数学题、与其它专业学科融合的题目等方面的数据集
- [ ] 多模态数据集的获取与合成，使得大模型能结合图片进行解题
- [ ] 多次思考过程，类似于COT，现在的方案只有一次思考，生成一次代码
- [ ] 可靠性：生成的Python代码更可靠，现在生成的Python代码存在多种问题，如运行报错，无法执行，进入死循环等等
- [ ] 准确性：Python代码运行后的数字精度问题，是否可以用分数或根式等其它形式表达，现在的执行结果有时候返回小数，与正确答案存在精度偏差，其实返回分数或根式更为合理
- [ ] 稳定性：大模型的生成文本或代码不稳定，变动较大，导致答案有时正确，有时不正确
- [ ] 更优雅地数学解题过程与代码生成，有时候一道题目有更好的解法
- [ ] 其它...

### 数学能力测评

- GSM8K
- MATH
- ...

### 文章与思考

本项目将会形成一系列的文章与思考，欢迎关注与讨论。

1. [NLP（九十七）大模型数学解题能力的初步探索](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486824&idx=1&sn=fd6b36cf78aead227359606a7270516d&chksm=fcb9b4f8cbce3dee332335092f576c703ccdc55598cf45cb7f483f822ba5c72590019384d12a&token=321761101&lang=zh_CN#rd)