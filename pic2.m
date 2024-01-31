clc;%清理命令行窗口
clear all;%清理工作区

% storybook仓库
% 创建横坐标向量,读取Excel文件中B列第32行到第43行的数据
x3 = xlsread('平均提交速度.xlsx', 'Sheet1', 'B32:B43'); 
% 创建纵坐标向量,读取Excel文件中C列第32行到第43行的数据
y3 = xlsread('平均提交速度.xlsx', 'Sheet1', 'C32:C43'); 

% 在同一个图中绘制多幅折线图
plot(x3,y3);
xlabel('平均提交速度');
ylabel('问题解决速度');
title('平均提交速度对问题解决速度的影响');
legend('storybook'); % 添加图例
grid on;