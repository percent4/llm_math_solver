# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: human_eval_server.py
# @time: 2024/5/15 14:35
"""`eval/gsm8k/human_eval_server.py`: human check script for GSM8K dataset using Gradio.
"""
import json
import gradio as gr


def read_samples():
    with open("eval_result_qwen2_72b_instruct.json", "r") as f:
        data = f.readlines()

    content = []
    cnt = 0
    for sample in data:
        sample_dict = json.loads(sample.strip())
        if not sample_dict['is_correct']:
            cnt += 1
            content.append([cnt, sample_dict['question'],
                            sample_dict['answer'].split('####')[-1].strip(),
                            sample_dict['pred_answer'],
                            0])
    return content


def get_human_eval(df):
    # get model evaluation
    with open("eval_result_qwen2_72b_instruct.json", "r") as f:
        data = f.readlines()

    model_true_cnt = 0
    for sample in data:
        sample_dict = json.loads(sample.strip())
        if sample_dict['is_correct']:
            model_true_cnt += 1

    # get human evaluation
    human_true_cnt = 0
    for i, row in df.iterrows():
        if row['Human Evaluation']:
            human_true_cnt += 1
    return (f"Update {human_true_cnt} samples with human evaluation, \n"
            f"Total Accuracy: {model_true_cnt + human_true_cnt}/{len(data)} = {(model_true_cnt + human_true_cnt)/len(data)}")


with gr.Blocks() as demo:
    with gr.Column():
        with gr.Row():
            table = gr.DataFrame(label='Table',
                                 value=read_samples(),
                                 headers=['No.', 'Question', 'Answer', 'Prediction', 'Human Evaluation'],
                                 interactive=True,
                                 wrap=True)
        with gr.Row():
            output = gr.Textbox(label='Human Evaluation')
            submit = gr.Button("Search")

        submit.click(fn=get_human_eval,
                     inputs=table,
                     outputs=output)

demo.launch()
