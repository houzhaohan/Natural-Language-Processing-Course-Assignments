# 文本自动分类

## 一、实验目的

​	本次实验旨在利用KNN、SVM 、决策树、随机森林四种算法完成文本任务并分析不同算法性能，原始数据文件一共给出了6种类别的新闻文本，通过自行分割数据集并构建模型进行训练。

​	在任务开始之前先对数据进行预处理，首先按照9:1的比例划分了训练和测试集，同时为每个新闻文本给定相应的类别。

## 二、指标公式

### 1. **TF-IDF（词频-逆文档频率）**

#### 词频（TF）

$$
\text{TF}(t,d) = \frac{\text{词 } t \text{ 在文档 } d \text{ 中出现的次数}}{\text{文档 } d \text{ 的总词数}}
$$



#### 逆文档频率（IDF）

$$
\text{IDF}(t,D) = \log\left(\frac{N}{\text{包含词 } t \text{ 的文档数} + 1}\right)
$$



#### TF-IDF权重

$$
\text{TF-IDF}(t,d,D) = \text{TF}(t,d) \times \text{IDF}(t,D)
$$

### 2. **分类评估指标**

#### 精确率（Precision）

$$
P = \frac{\text{TP}}{\text{TP} + \text{FP}}
$$



#### 召回率（Recall）

$$
R = \frac{\text{TP}}{\text{TP} + \text{FN}}
$$



#### F1分数

$$
\text{F1} = 2 \times \frac{P \times R}{P + R}
$$



#### 宏平均（Macro-average）

$$
\text{Macro-P} = \frac{1}{C}\sum_{i=1}^C P_i
$$



#### 微平均（Micro-average）

$$
\text{Micro-P} = \frac{\sum_{i=1}^C \text{TP}_i}{\sum_{i=1}^C (\text{TP}_i + \text{FP}_i)}
$$

#### 符号说明

- **TP（True Positive）**：预测为某类且实际正确的样本数  
- **FP（False Positive）**：预测为某类但实际错误的样本数  
- **FN（False Negative）**：未预测为某类但实际正确的样本数  
- **C**：类别总数  

## 三、算法模型

### 1.KNN

​	KNN算法通过计算输入文本与训练集中所有文本的距离，选取距离最近的K个实例。然后，对这K个实例的类别进行统计，得出每个类别的得分。最终，选择得分最高的类别作为输入文本的预测类别。

​	首先我利用jieba分词库对于文本进行分词，完成了分词之后我基于TF-IDF对于文本进行了向量化公式如下：
$$
TFC = TF \times \log\left(\frac{N}{n}\right)
$$
​	完成了向量化之后可以输入测试文本，对于测试文本也进行向量化然后和我们的训练集中所有其他文本计算相似度，选择前K个最为相似的文本，在本次的实验中我选择K为5，同时针对每个类别相似分数进行计算最后取得分最高的哪个类作为测试文本的类别。

*运行结果*：

![image](https://github.com/user-attachments/assets/7bb1dfb5-b147-42e0-b052-fc399a548481)

### 2.SVM

​	SVM（支持向量机）算法是一种常用的监督学习模型，尤其适用于分类任务。SVM通过在高维空间中找到一个最佳的超平面，将不同类别的样本分开，以实现分类目的。在本次实验中，使用SVM算法进行文本分类。

​	在本部分的实现中我使用sklearn机器学习库完成，首先针对文本基于TF-IDF完成向量化，然后训练SVM进行预测。

​	支持向量机线性核的决策函数：
$$
f(x) = \mathbf{w} \cdot \mathbf{x} + b
$$
*运行结果*：

![image](https://github.com/user-attachments/assets/117a7f65-2936-4af6-a1c6-6bda753af1b9)

### 3.决策树

​	决策树算法是一种简单但非常有效的监督学习算法，常用于分类和回归任务。决策树通过一系列的分裂规则将数据分割成不同的类别，每个内部节点表示一个特征，每个分支代表一个特征值，每个叶节点表示一个类别。在本次实验中，我们使用决策树算法进行文本分类。决策树分类器：
$$
\text{Gini}(D) = 1 - \sum_{k=1}^{K} p_k^2
$$
​	在本部分的实现中我使用sklearn机器学习库完成，首先针对文本基于TF-IDF完成向量化，然后训练决策树模型进行预测。
*运行结果*：

![image](https://github.com/user-attachments/assets/f7a31bdc-8af5-4e15-8ec7-edd187e49889)

### 4.随机森林

​	随机森林算法是一种集成学习方法，通过构建多个决策树并结合其输出结果来提高模型的分类性能和稳定性。随机森林的每棵决策树都是在训练集的一个随机子集上构建的，并且在每个节点分裂时，只考虑随机选择的一部分特征。这样可以有效地减少过拟合，提升模型的泛化能力。
​	信息增益（分类问题）：
$$
InformationGain = Entropy(parent) - Σ [ (样本比例) × Entropy(child) ]
$$
​	基尼不纯度（默认指标）：
$$
Gini = 1 - Σ (p_i)^2
$$
​	在本部分的实现中我使用sklearn机器学习库完成，首先针对文本基于TF-IDF完成向量化，然后训练随机森林模型进行预测。

*运行结果*：

![image](https://github.com/user-attachments/assets/3cade237-5f75-4b00-9215-78943eaadbe0)

## 四、结果分析

​	微观平均，宏观平均指标对比：

|          | 微观平均准确率 | 宏观平均准确率 |
| -------- | -------------- | -------------- |
| KNN      | 0.63           | 0.58           |
| SVM      | 0.68           | 0.6            |
| 决策树   | 0.67           | 0.63           |
| 随机森林 | 0.79           | 0.79           |

​	在实验中，通过不同机器学习算法进行了文本分类任务的性能评估，包括KNN、SVM、决策树和随机森林。性能指标主要关注各个类别的准确率（Precision）、召回率（Recall）和 F1分数（F1 score），以及宏观平均准确率和微观平均准确率。

​	KNN算法在国际类别与体育类别中表现出色，F1分数分别为0.80和0.73。其余类别F1分数均不到0.5，效果较差。在社会类别表现最差，F1分数只有0.36。

​	SVM算法在国际类别与体育类别中表现出色，F1分数分别为0.79和0.88。其余类别效果较差。

​	决策树在国际类别与体育类别中表现出色，F1分数分别为0.80和0.85。其余类别效果较差。

​	随机森林在各个类别的预测中均表现较好。尤其是在体育类别，F1分数达到了0.97。在其他类别中，性能指标有所下降，但整体而言，随机森林在所有类别中的平均表现相对较好。

​	结果表明不同的算法在不同的类别上有着各自的优势和局限。对于实际应用，选择合适的算法需要考虑到目标类别的具体需求以及算法的性能特点。同时可以尝试应用深度学习的方法进行类别预测，例如使用BERT等预训练模型进行文本分类。
