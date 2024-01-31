clc;%清理命令行窗口
clear all;%清理工作区

% dubbo仓库
% 创建横坐标向量,读取Excel文件中B列第2行到第13行的数据
x1 = xlsread('平均每日评论.xls', 'Sheet1', 'B2:B13'); 
% 创建纵坐标向量,读取Excel文件中C列第2行到第13行的数据
y1 = xlsread('平均每日评论.xls', 'Sheet1', 'C2:C13'); 

% meteor仓库
% 创建横坐标向量,读取Excel文件中B列第17行到第28行的数据
x2 = xlsread('平均每日评论.xls', 'Sheet1', 'B17:B28'); 
% 创建纵坐标向量,读取Excel文件中C列第17行到第28行的数据
y2 = xlsread('平均每日评论.xls', 'Sheet1', 'C17:C28'); 

% storybook仓库
% 创建横坐标向量,读取Excel文件中B列第32行到第43行的数据
x3 = xlsread('平均每日评论.xls', 'Sheet1', 'B32:B43'); 
% 创建纵坐标向量,读取Excel文件中C列第32行到第43行的数据
y3 = xlsread('平均每日评论.xls', 'Sheet1', 'C32:C43'); 

% kong仓库
% 创建横坐标向量,读取Excel文件中B列第47行到第58行的数据
x4 = xlsread('平均每日评论.xls', 'Sheet1', 'B47:B58'); 
% 创建纵坐标向量,读取Excel文件中C列第47行到第58行的数据
y4 = xlsread('平均每日评论.xls', 'Sheet1', 'C47:C58'); 

% left仓库
% 创建横坐标向量,读取Excel文件中B列第62行到第73行的数据
x5 = xlsread('平均每日评论.xls', 'Sheet1', 'B62:B73'); 
% 创建纵坐标向量,读取Excel文件中C列第62行到第73行的数据
y5 = xlsread('平均每日评论.xls', 'Sheet1', 'C62:C73'); 

% 在同一个图中绘制多幅折线图
plot(x1, y1, x2, y2, x4, y4,x5, y5);
xlabel('平均每日评论');
ylabel('问题解决速度');
title('平均每日评论对问题解决速度的影响');
legend('dubbo', 'meteor', 'kong','left'); % 添加图例
grid on;

