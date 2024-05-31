# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: human_eval_server.py
# @time: 2024/5/21 11:16
# 对模型评估后的结果进行人工评估，使用gradio实现
"""`eval/MATH/human_eval_server.py`: human check script for MATH dataset using Gradio.
"""
import json
import gradio as gr

from math_eval_update import last_boxed_only_string, remove_boxed


def read_samples():
    with open("math_eval_result_update.json", "r") as f:
        data = f.readlines()

    content = []
    for i, sample in enumerate(data):
        sample_dict = json.loads(sample.strip())
        question, true_answer, pred_answer = sample_dict["problem"], sample_dict["solution"], sample_dict["predict_answer"]
        try:
            true_answer_str = remove_boxed(last_boxed_only_string(true_answer))
            pred_answer_str = remove_boxed(last_boxed_only_string(pred_answer))
            if not sample_dict["is_correct"] and pred_answer_str:
                content.append([i, true_answer_str, pred_answer_str, 0])
        except Exception as e:
            # content.append([i, '', '', 0])
            continue
    return content


def get_human_eval(df):
    # get model evaluation
    with open("math_eval_result_update.json", "r") as f:
        data = f.readlines()

    model_true_cnt = 0
    for sample in data:
        sample_dict = json.loads(sample.strip())
        if sample_dict["is_correct"]:
            model_true_cnt += 1
    # get human evaluation
    human_true_cnt = 0
    for i, row in df.iterrows():
        if row['Human Evaluation']:
            human_true_cnt += 1
    # save human evaluation to json file
    final_result = [json.loads(line.strip()) for line in data]
    for i, row in df.iterrows():
        if row['Human Evaluation']:
            final_result[row['No.']]["is_correct"] = True
    with open("math_eval_result_final.json", "w") as g:
        for _ in final_result:
            g.write(json.dumps(_, ensure_ascii=False) + '\n')

    return (f"Update {human_true_cnt} samples with human evaluation, \n"
            f"Total Accuracy: {model_true_cnt + human_true_cnt}/{len(data)} = {(model_true_cnt + human_true_cnt)/len(data)}")


with gr.Blocks() as demo:
    with gr.Column():
        with gr.Row():
            table = gr.DataFrame(label='Table',
                                 value=read_samples(),
                                 headers=['No.', 'True_Answer_Number', 'Pred_Answer_Number', 'Human Evaluation'],
                                 interactive=True,
                                 wrap=True
                                 )
        with gr.Row():
            output = gr.Textbox(label='Human Evaluation')
            submit = gr.Button("Search")

        submit.click(fn=get_human_eval,
                     inputs=table,
                     outputs=output)

demo.launch()
