<div align="center">
  <h1>Welcome to LLM Math Solver</h1>

<h4 align="center">
  <a href="https://percent4.github.io/llm_math_solver/"><img src="https://img.shields.io/badge/📄-docs-000000?style=for-the-badge&colorA=09c&colorB=555" height='35px' alt="Docs"></a>
</h4>
  <p>LLM Math Solver: using LLM to solve MATH problems.
</p>
<h1></h1>
</div>

> 最新的微调模型`QWen-2-72B-Instruct-math-v2`的[Demo体验网址](https://0131bbfe66de0ae822.gradio.live)，有效期三天，截止2024年9月8日早10点45分，如有需要，后续会提供稳定的web服务！

> 最新的微调模型`QWen-2-72B-Instruct-math`已在Huggingface上发布，可以下载使用，[点击这里](https://huggingface.co/jclian91/Qwen2-72B-Instruct-math)。

本项目用于大模型数学解题能力方面的数据集合成，主要包括以下几个部分：

### 数据集

- 数据大规模自动合成: data_systhesis/ape210k/data_generator.py, data_systhesis/gsm8k_train/data_generator.py, data_systhesis/numina-math-tir/data_generator.py, data_systhesis/tal_scq5k/data_generator.py
- 大模型合成数据: data_systhesis/llm/data_generator.py
- Web服务人工数据录入: data_systhesis/hand_make/data_generator.py
- 数据合并：data_synthesis/data_merge.py

生成的样例数据（一个样本数据）如下：

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
    }
]
```

训练数据集分布如下（共`4799`条）：

- GPT-4生成: `451`条
- WEB服务（人工输入题目并检查）：`760`条
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
- [x] 稳定性：大模型的生成文本或代码不稳定，变动较大，导致答案有时正确，有时不正确

### 数学能力测评

| 基座模型                | GSM8K  | MATH   | 样本数  |
|---------------------|--------|--------|------|
| QWen1.5-32B         | 79.68% | 43.58% | 2402 |
| Yi-1.5-34B          | 83.47% | 52.76% | 3480 |
| Yi-1.5-34B-Chat     | 85.67% | 57.22% | 3479 |
| QWen-2-72B-Instruct | 93.03% | 68.54% | 3469 |
| QWen-2-72B-Instruct | 93.56% | 69.66% | 4799 |

#### 2024新高考II卷高考真题数学能力测评

- 去除试卷中的证明题，总分共130分，计分方式同高考阅卷（这里只考虑最终答案是否正确，不考虑中间过程得分）。
- 使用`MathPix`将高考真题PDF文档转化为带LaTeX格式的Markdown文档，然后分别使用OpenAI(模型为GPT-4o), Claude(模型为claude-3-5-sonnet-20240620), 自研微调模型（基座模型为QWen-2-72B-Instruct）进行解题，得到每道题的解答过程和最终答案，然后与标准答案进行比对，计算总体得分。
- 评测的具体细节可参考 `eval/gaokao` 文件夹。

模型的总体得分评测结果如下：

|模型| 得分1 | 得分2 | 得分3 | 平均得分  |
|---|-----|-----|-----|-------|
|OpenAI| 68  | 82  | 66  | 72.0  |
|Claude| 68  | 65  | 63  | 65.33 |
|自研微调模型| 58  | 67  | 56  | 60.33 |

![score_1.jpg](https://s2.loli.net/2024/08/29/lu5CJ1ZxeoOprF2.png)

按题型(单项选择题, 多项选择题, 填空题, 解答题)进行统计，测评结果如下：

|题型|模型| 得分1 | 得分2 | 得分3 | 平均得分  |
|---|---|-----|-----|-----|-------|
|单项选择题|OpenAI| 35  | 30  | 25  | 30.0  |
|单项选择题|Claude| 35  | 30  | 30  | 31.67 |
|单项选择题|自研微调模型| 20  | 20  | 10  | 16.67 |
|多项选择题|OpenAI| 14  | 8   | 11  | 11.0  |
|多项选择题|Claude| 10  | 10  | 10  | 10    |
|多项选择题|自研微调模型| 0   | 6   | 0   | 2     |
|填空题|OpenAI| 7   | 7   | 7   | 7.0   |
|填空题|Claude| 7   | 2   | 7   | 5.33  |
|填空题|自研微调模型| 7   | 10  | 15  | 10.67 |
|解答题|OpenAI| 12  | 37  | 23  | 24.0  |
|解答题|Claude| 16  | 23  | 16  | 18.33 |
|解答题|自研微调模型| 31  | 31  | 31  | 31    |

![score_2.jpg](https://s2.loli.net/2024/08/29/Cg4OhHGFMTArLpI.png)

### 评测数据集存在问题

1. GSMK8K的测试数据集部分问题出错，笔者发现4条样本，参见后续的`文章与思考`中的文章6.
2. MATH的测试集中，部分样本存在两个或多个答案，行号为79, 4976, 4696, 4686, 4459, 4229, 4015, 3962, 3928, 3098。

### 文章与思考

本项目将会形成一系列的文章与思考，欢迎关注与讨论。

1. [NLP（九十七）大模型数学解题能力的初步探索](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486824&idx=1&sn=fd6b36cf78aead227359606a7270516d&chksm=fcb9b4f8cbce3dee332335092f576c703ccdc55598cf45cb7f483f822ba5c72590019384d12a&token=321761101&lang=zh_CN#rd)
2. [NLP（九十九）大模型的数学能力微调及测评](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486889&idx=1&sn=27c1a40d3af462f43a80a1ed401843f6&chksm=fcb9b439cbce3d2fd73e753618e0b32027314648eb13dc8b48bb9e713ad5313777c1ef27ce46&token=390124673&lang=zh_CN#rd)
3. [NLP（一百）大模型数学能力测评](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486909&idx=1&sn=31b01bd4155b2c9ca15e2a7ae9f4de15&chksm=fcb9b42dcbce3d3bb473cf138f0f0f9a71addeff934900d155b6b90fb2a5857c1926b8aa0e9d&token=584142844&lang=zh_CN#rd)
4. [Open WebUI的Pipelines学习之使用大模型解数学题](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247487013&idx=1&sn=6a6786ba8c8c7cfdbc02ef558adefe71&chksm=fcb9b7b5cbce3ea37f8fb61e743d0ea0a7d4f5d6b8e8b2c7a80171a5c8c217524d8f307c0146&token=120899150&lang=zh_CN#rd)
5. [笔记：大模型数学解题能力](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247487038&idx=1&sn=ae458cbb6d9f23fb04229bd18961449d&chksm=fcb9b7aecbce3eb800f9b80de1c2931660b7ce1ea103f44759ed179638bad5711d357757f568&token=1938218370&lang=zh_CN#rd)
6. [NLP（一百零六）GSM8K测试集中答案错误的4道题目](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247487146&idx=1&sn=6a6fc931b76b2db3414c3208e26fe5a8&chksm=fcb9b73acbce3e2cb48fd2348d8e2225b620b93e229ecf17ac26e0982b03b7097bee529a51d4&token=552536245&lang=zh_CN#rd)