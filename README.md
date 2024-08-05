<div align="center">
  <h1>Welcome to LLM Math Solver</h1>

<h4 align="center">
  <a href="https://percent4.github.io/llm_math_solver/"><img src="https://img.shields.io/badge/📄-docs-000000?style=for-the-badge&colorA=09c&colorB=555" height='35px' alt="Docs"></a>
</h4>
  <p>LLM Math Solver: using LLM to solve MATH problems.
</p>
<h1></h1>
</div>

> 最新的微调模型`QWen-2-72B-Instruct-math`已在Huggingface上发布，可以下载使用，[点击这里](https://huggingface.co/jclian91/Qwen2-72B-Instruct-math)。

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

训练数据集分布如下（共`4688`条）：

- GPT-4生成: `451`条
- WEB服务（人工输入题目并检查）：`649`条
- APE210K: 大模型自动生成，`1103`条
- GSM8K: 大规模自动生成, `510`条
- TAL-SCQ5K: 大规模自动生成, `980`条
- NUMINA-MATH: 大规模自动生成, `995`条

### 改进点

后续将会改进的点如下：

- [x] 高质量数学题的数据集获取(进行中...)
- [x] 更大规模、更高质量、形式更丰富的数学题的数据合成(进行中...)
- [x] 数据集的清洗，包括公式整理、去重等(进行中...)
- [ ] 加入 高等数学题、与其它专业学科融合的题目等方面的数据集
- [ ] 多模态数据集的获取与合成，使得大模型能结合图片进行解题
- [ ] 多次思考过程，类似于COT，现在的方案只有一次思考，生成一次代码
- [x] 可靠性：生成的Python代码更可靠，现在生成的Python代码存在多种问题，如运行报错，无法执行，进入死循环等等, 解决方法：使用`subprocess`库运行代码
- [x] 准确性：Python代码运行后的数字精度问题，是否可以用分数或根式等其它形式表达，现在的执行结果有时候返回小数，与正确答案存在精度偏差，其实返回分数或根式更为合理, 解决方法：构建数据集时返回分数或根式
- [ ] 稳定性：大模型的生成文本或代码不稳定，变动较大，导致答案有时正确，有时不正确
- [ ] ...

### 数学能力测评

| 基座模型                | GSM8K  | MATH   | 样本数  |
|---------------------|--------|--------|------|
| QWen1.5-32B         | 79.68% | 43.58% | 2402 |
| Yi-1.5-34B          | 83.47% | 52.76% | 3480 |
| Yi-1.5-34B-Chat     | 85.67% | 57.22% | 3479 |
| QWen-2-72B-Instruct | 93.03% | 68.54% | 3469 |

### 文章与思考

本项目将会形成一系列的文章与思考，欢迎关注与讨论。

1. [NLP（九十七）大模型数学解题能力的初步探索](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486824&idx=1&sn=fd6b36cf78aead227359606a7270516d&chksm=fcb9b4f8cbce3dee332335092f576c703ccdc55598cf45cb7f483f822ba5c72590019384d12a&token=321761101&lang=zh_CN#rd)
2. [NLP（九十九）大模型的数学能力微调及测评](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486889&idx=1&sn=27c1a40d3af462f43a80a1ed401843f6&chksm=fcb9b439cbce3d2fd73e753618e0b32027314648eb13dc8b48bb9e713ad5313777c1ef27ce46&token=390124673&lang=zh_CN#rd)
3. [NLP（一百）大模型数学能力测评](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486909&idx=1&sn=31b01bd4155b2c9ca15e2a7ae9f4de15&chksm=fcb9b42dcbce3d3bb473cf138f0f0f9a71addeff934900d155b6b90fb2a5857c1926b8aa0e9d&token=584142844&lang=zh_CN#rd)
4. [Open WebUI的Pipelines学习之使用大模型解数学题](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247487013&idx=1&sn=6a6786ba8c8c7cfdbc02ef558adefe71&chksm=fcb9b7b5cbce3ea37f8fb61e743d0ea0a7d4f5d6b8e8b2c7a80171a5c8c217524d8f307c0146&token=120899150&lang=zh_CN#rd)