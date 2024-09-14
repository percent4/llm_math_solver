# Welcome to LLM Math Solver Project

欢迎来到`LLM Math Solver`项目，本项目旨在使用大模型来解决数学习题.

> 最新的微调模型`QWen-2-72B-Instruct-math`已在Huggingface上发布，可以下载使用，[点击这里](https://huggingface.co/jclian91/Qwen2-72B-Instruct-math)。


# Content

- [demo](demo.pdf)
- [examples](examples.pdf)
- [sft model](llm_sft.md)
- [GSM8K Evaluation](gsm8k_eval.md)
- [MATH Evaluation](MATH_eval.md)
- [高考数学题评测](gaokao_eval.md)

# Evaluation

不同模型经过微调的数学能力测评表如下：

| 基座模型                | GSM8K  | MATH   | 样本数  |
|---------------------|--------|--------|------|
| QWen1.5-32B         | 79.68% | 43.58% | 2402 |
| Yi-1.5-34B          | 83.47% | 52.76% | 3480 |
| Yi-1.5-34B-Chat     | 85.67% | 57.22% | 3479 |
| QWen-2-72B-Instruct | 93.03% | 68.54% | 3469 |
| QWen-2-72B-Instruct | 93.56% | 69.66% | 4799 |

其它模型的数学能力测评：[LLM Leaderboard](https://www.vellum.ai/llm-leaderboard)

# More

1. [NLP（九十七）大模型数学解题能力的初步探索](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486824&idx=1&sn=fd6b36cf78aead227359606a7270516d&chksm=fcb9b4f8cbce3dee332335092f576c703ccdc55598cf45cb7f483f822ba5c72590019384d12a&token=321761101&lang=zh_CN#rd)
2. [NLP（九十九）大模型的数学能力微调及测评](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486889&idx=1&sn=27c1a40d3af462f43a80a1ed401843f6&chksm=fcb9b439cbce3d2fd73e753618e0b32027314648eb13dc8b48bb9e713ad5313777c1ef27ce46&token=390124673&lang=zh_CN#rd)
3. [NLP（一百）大模型数学能力测评](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247486909&idx=1&sn=31b01bd4155b2c9ca15e2a7ae9f4de15&chksm=fcb9b42dcbce3d3bb473cf138f0f0f9a71addeff934900d155b6b90fb2a5857c1926b8aa0e9d&token=584142844&lang=zh_CN#rd)
4. [Open WebUI的Pipelines学习之使用大模型解数学题](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247487013&idx=1&sn=6a6786ba8c8c7cfdbc02ef558adefe71&chksm=fcb9b7b5cbce3ea37f8fb61e743d0ea0a7d4f5d6b8e8b2c7a80171a5c8c217524d8f307c0146&token=120899150&lang=zh_CN#rd)
5. [笔记：大模型数学解题能力](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247487038&idx=1&sn=ae458cbb6d9f23fb04229bd18961449d&chksm=fcb9b7aecbce3eb800f9b80de1c2931660b7ce1ea103f44759ed179638bad5711d357757f568&token=1938218370&lang=zh_CN#rd)
6. [NLP（一百零六）GSM8K测试集中答案错误的4道题目](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247487146&idx=1&sn=6a6fc931b76b2db3414c3208e26fe5a8&chksm=fcb9b73acbce3e2cb48fd2348d8e2225b620b93e229ecf17ac26e0982b03b7097bee529a51d4&token=552536245&lang=zh_CN#rd)
7. [NLP（一百零七）大模型解答高考数学题评测实验](https://mp.weixin.qq.com/s?__biz=MzU2NTYyMDk5MQ==&mid=2247487202&idx=1&sn=da3ad2b629b6033cacb0724349c8f7e4&chksm=fcb9b772cbce3e64c432b09d25bbcf1253b6ba78af91565eba91de189cce1af89dc72e443968&token=410216179&lang=zh_CN#rd)