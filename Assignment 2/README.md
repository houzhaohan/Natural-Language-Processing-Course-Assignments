# 现代汉语分词规范学习与精标实验

## 1 实验目的
中文分词作为自然语言处理的基础任务，其性能直接影响下游任务的效果。本实验评估机器分词系统在中文文本处理中的性能表现，通过对比机器分词结果与人工校对标准答案，计算精确率（Precision）、召回率（Recall）和F测度值（F-measure）三项核心指标，量化分析分词系统的准确性和可靠性。本实验还采用序列标注方法，构建基于B-I-E-S四标记的分词模型。通过精确率（P）、召回率（R）和F1值三个核心指标，系统评估模型在不同词位标记上的表现。

## 2 实验数据
机器分词文件：hzh.txt  
人工校对文件：hzh（校对后）.txt  （作为标准答案）  

数据处理：采用四分类标记集。  
B（Begin）：多字词的首字符  
I（Inner）：多字词的中间字符（含长度≥3词的中间部分）  
E（End）：多字词的尾字符  
S（Single）：单字词  

## 3 测评指标
精准率P=重合部分/分词结果  
召回率R=重合部分/标准答案  
F测度值=2PR/(P+R)  

采用精准率P、召回率R和调和平均值F等指标计算，分别测试语料中的B、I、E、S四个标记是否标记正确。  
精准率P=正确识别的标记/(正确识别的标记+错误识别的标记)*100%  
召回率R=正确识别的标记/(正确识别的标记+未被识别的标记)*100%  

## 4 实验结果
分词性能：    
![image](https://github.com/user-attachments/assets/aab0010b-ca75-415c-8869-e756cb7989b7)

基于B-I-E-S四标记的分词性能：  
![image](https://github.com/user-attachments/assets/608137c2-29f7-4584-8fb8-10b6158fd66f)

## 5 结果分析
机器分词性能在保持高召回率（98.40%）的同时，实现了优异的精确率（96.99%），同时F测度值达97.69%，表明系统整体性能接近人工校对标水平。召回率略高于精确率，说明系统更倾向减少漏分错误。
整体来看，在通用领域文本处理中表现优异，各项指标均超过90%的基准线要求。  

在基于B-I-E-S四标记的分词模型中，B标记达到98.64%的F1值，E标记达到98.77%的F1值。首尾字符识别稳健，反映模型能有效捕捉词边界特征。0.14%的P-R差异源于训练数据中的嵌套词处理。I标记中精确率高达99.79%，但召回率仅93.14%。表现出高精确率：中间字符误标为其他标记的概率极低；低召回率：长词中间部分存在漏标现象。S标记中召回率99.57%为最优，但精确率相对最低单字词易被正确识别（高R），但存在将短词首尾误判为单字词的情况。
