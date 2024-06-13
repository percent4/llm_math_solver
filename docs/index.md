# Welcome to LLM Math Solver Project

欢迎来到`LLM Math Solver`项目，本项目旨在使用大模型来解决数学习题.

# Content

- [demo](demo.pdf)
- [examples](examples.pdf)
- [sft model](llm_sft.md)
- [GSM8K Evaluation](gsm8k_eval.md)
- [MATH](MATH_eval.md)

# Evaluation

不同模型经过微调的数学能力测评表如下：

| 数据集             | GSM8K  | MATH   | 样本数  |
|-----------------|--------|--------|------|
| QWen1.5-32B     | 79.68% | 43.58% | 2402 |
| Yi-1.5-34B      | 83.47% | 52.76% | 3480 |
| Yi-1.5-34B-Chat | 85.67% | 57.22% | 3479 |

其它模型的数学能力测评：[LLM Leaderboard](https://www.vellum.ai/llm-leaderboard)

# More

1. [NLP（九十七）大模型数学解题能力的初步探索](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486824&idx=1&sn=fd6b36cf78aead227359606a7270516d&chksm=fcb9b4f8cbce3dee332335092f576c703ccdc55598cf45cb7f483f822ba5c72590019384d12a&token=321761101&lang=zh_CN#rd)
2. [NLP（九十九）大模型的数学能力微调及测评](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486889&idx=1&sn=27c1a40d3af462f43a80a1ed401843f6&chksm=fcb9b439cbce3d2fd73e753618e0b32027314648eb13dc8b48bb9e713ad5313777c1ef27ce46&token=390124673&lang=zh_CN#rd)
3. [NLP（一百）大模型数学能力测评](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486909&idx=1&sn=31b01bd4155b2c9ca15e2a7ae9f4de15&chksm=fcb9b42dcbce3d3bb473cf138f0f0f9a71addeff934900d155b6b90fb2a5857c1926b8aa0e9d&token=584142844&lang=zh_CN#rd)

