# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: eval_visualization.py
# @time: 2024/5/22 14:54
import json
import plotly.graph_objects as go
from collections import defaultdict
from random import shuffle
from operator import itemgetter

# 读取数据
with open("math_eval_result_final.json", "r", encoding="utf-8") as f:
    data = f.readlines()

type_dict = defaultdict(int)
level_dict = defaultdict(int)
for line in data:
    sample = json.loads(line.strip())
    if sample['is_correct']:
        type_dict[sample['type']] += 1
        level_dict[sample['level']] += 1

# 绘制类型的饼图
fig1 = go.Figure(data=go.Pie(labels=list(type_dict.keys()), values=list(type_dict.values())))
fig1.update_layout(
    title="Type Distribution of Correct Answers in MATH",
    font=dict(size=20)
)
# fig1.show()
# 绘制Level的饼图
fig2 = go.Figure(data=go.Pie(labels=list(level_dict.keys()), values=list(level_dict.values())))
fig2.update_layout(
    title="Level Distribution of Correct Answers in MATH",
    font=dict(size=20)
)
# fig2.show()

# 获取每个类型的正确率
type_cnt_dict = defaultdict(int)
level_cnt_dict = defaultdict(int)
for line in data:
    sample = json.loads(line.strip())
    type_cnt_dict[sample['type'] + '_total'] += 1
    level_cnt_dict[sample['level'] + '_total'] += 1
    if sample['is_correct']:
        type_cnt_dict[sample['type'] + '_correct'] += 1
        level_cnt_dict[sample['level'] + '_correct'] += 1

type_correct_ratio = {key: type_cnt_dict[f'{key}_correct']/type_cnt_dict[f'{key}_total'] for key in type_dict.keys()}
level_correct_ratio = {key: level_cnt_dict[f'{key}_correct']/level_cnt_dict[f'{key}_total'] for key in level_dict.keys()}
sorted_type_correct_ratio = {k: round(v, 4) for k, v in sorted(type_correct_ratio.items(), key=itemgetter(1), reverse=True)}
sorted_level_correct_ratio = {k: round(v, 4) for k, v in sorted(level_correct_ratio.items(), key=itemgetter(1), reverse=True)}

# 绘制类型的柱状图
colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink', 'brown']
shuffle(colors)
fig3 = go.Figure(data=[go.Bar(x=list(sorted_type_correct_ratio.keys()),
                              y=list(sorted_type_correct_ratio.values()),
                              text=list(sorted_type_correct_ratio.values()),
                              textposition='auto',
                              marker=dict(color=colors[:len(type_dict.keys())]),
                              textfont=dict(size=20)
                              )])
fig3.update_layout(
    title="Type Correct Ratio of MATH",
    xaxis_title="Type",
    yaxis_title="Correct Ratio",
    legend_title="Type",
    font=dict(size=20)
)
# fig3.show()
# 绘制Level的柱状图
fig4 = go.Figure(data=[go.Bar(x=list(sorted_level_correct_ratio.keys()),
                              y=list(sorted_level_correct_ratio.values()),
                              text=list(sorted_level_correct_ratio.values()),
                              textposition='auto',
                              marker=dict(color=colors[:len(type_dict.keys())]),
                              textfont=dict(size=20)
                              )])
fig4.update_layout(
    title="Level Correct Ratio of MATH",
    xaxis_title="Level",
    yaxis_title="Correct Ratio",
    legend_title="Level",
    font=dict(size=20)
)
fig4.show()
