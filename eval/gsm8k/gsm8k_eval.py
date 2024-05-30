import os
import re
import json
import subprocess
from rich.progress import track
from openai import OpenAI
import logging
from retry import retry
from random import choices

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

os.environ["OPENAI_BASE_URL"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "0"
client = OpenAI()

execution_desc = ["运行以上代码，输出会是： ",
                  "现在将上面的代码复制到Python环境中运行，运行结果为：",
                  "执行上述Python代码，运行结果将是：",
                  "上面的Python代码执行结果为：",
                  "运行上述代码，我们可以得到题目要求的答案。输出结果将是："]

@retry(exceptions=Exception, tries=3, delay=2)
def question_answer(query):
    messages = [{"role": "system", "content": "你是一个数学解题大师，请解决下面的数学题，给出思考过程，必要时需要给出解题过程中的Python代码。正确答案的数值用\\boxed{}包围起来，最终的答案以因此开头，不要讲多余的废话。"}]
    messages.append({"role": "user", "content": f"题目：{query}"})
    result = client.chat.completions.create(messages=messages,
                                            model="Yi-1.5-34B-Chat-math",
                                            temperature=0.0,
                                            stream=True)
    reply_message = ""
    for chunk in result:
        if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
            reply_message += chunk.choices[0].delta.content

    # find python code and execute the code
    if '```python' in reply_message and '\n```' in reply_message:
        messages.append({"role": "assistant", "content": '```'.join(reply_message.split('```')[:-1]) + '```'})
        python_code_string = re.findall(r'```python\n(.*?)\n```', reply_message, re.S)[0]
        python_file_path = 'temp.py'
        with open(python_file_path, 'w') as f:
            f.write(python_code_string)
        python_code_run = subprocess.run(['python3', python_file_path], stdout=subprocess.PIPE)
        if python_code_run.returncode:
            raise RuntimeError("生成的Python代码无法运行！")
        python_code_execution = python_code_run.stdout.decode('utf-8')
        os.remove(python_file_path)
        code_reply_str = choices(execution_desc, k=1)[0]
        code_reply = f"\n{code_reply_str}```{python_code_execution.strip()}```\n"
        reply_message += code_reply
        messages.append({"role": "user", "content": code_reply})
        result = client.chat.completions.create(messages=messages,
                                                model="Yi-1.5-34B-Chat-math",
                                                temperature=0.0,
                                                stream=True)
        
        final_reply = ""
        for chunk in result:
            if hasattr(chunk, "choices") and chunk.choices[0].delta.content:
                reply_message += chunk.choices[0].delta.content
                final_reply += chunk.choices[0].delta.content
        return final_reply
    else:
        return reply_message

with open('gsm8k_test.jsonl', 'r') as f:
    content = f.readlines()

total_cnt = 0
correct_cnt = 0
for line in track(content):
    question, answer = json.loads(line.strip())['question'], json.loads(line.strip())['answer']
    true_answer_number = answer.split('####')[-1].strip().replace(',', '')
    try:
        pred_answer = question_answer(question)
    except Exception:
        pred_answer = 'ERROR'
    if re.findall(r'\\boxed\{.+?}', pred_answer) and re.findall('\d+', re.findall(r'\\boxed\{.+?}', pred_answer)[-1].replace(',', '')):
        pred_answer_number = re.findall('\d+', re.findall(r'\\boxed\{.+?}', pred_answer)[-1].replace(',', ''))[0]
    else:
        pred_answer_number = ''
    total_cnt += 1
    logger.info("*" * 50)
    logger.info('--- {} {} {}'.format(true_answer_number, pred_answer_number, repr(pred_answer)))
    if true_answer_number == pred_answer_number:
        correct_cnt += 1
        
    with open('eval_result_yi_15_34b.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps({"is_correct": true_answer_number == pred_answer_number, "question": question, "answer": answer, "pred_answer": pred_answer}, ensure_ascii=False)+"\n")

    logger.info('--- {} {} {}'.format(total_cnt, correct_cnt, correct_cnt/total_cnt))
    