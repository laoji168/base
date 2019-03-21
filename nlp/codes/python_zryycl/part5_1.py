# coding=utf-8
import nltk
"""
分类和标注
"""
def fun1():
    """
    使用词性标注器
    :return:
    """
    text = nltk.word_tokenize("And now for something completely different")
    print nltk.pos_tag(text)
    # NLTK中提供了每个标记的文档,可以使用标记来查询,如:nltk.help.upenn_tagset('RB'),或正则
    # 表达式,如:nltk.help.upenn_brown_
    # tagset('NN.*')。一些语料库有标记集文档的README文件;见
    # nltk.name.readme(),用语料库的名称替换name

    # 考虑下面的分析,涉及woman(名词),bought(动词),over(介词)和the(限定词)。
    # text.similar()方法为词w找出所有上下文w1ww2,然后找出所有出现在相同上下文中的词w',即w1w'w2
    text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
    print text.similar('woman')
    print text.similar('bought')
    print text.similar('over')
    print text.similar('the')

# nltk.download('averaged_perceptron_tagger')
fun1()