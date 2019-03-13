# coding=utf-8
"""
分割
"""
def fun1():
    # 从分词表示字符串seg1和seg2中重建文本分词。seg1和seg2表示假设的
    # 一些儿童讲话的初始和最终分词。函数segment()可以使用它们重现分词的文本
    text = "doyouseethekittyseethedoggydoyoulikethekittylikethedoggy"
    seg1 = "0000000000000001000000000010000000000000000100000000000"
    seg2 = "0100100100100001001001000010100100010010000100010010000"
    seg3 = "0000100100000011001000000110000100010000001100010000001"

    def segment(text, segs):
        words = []
        last = 0
        for i in range(len(segs)):
            if segs[i] == '1':
                words.append(text[last:i+1])
                last = i + 1
        words.append(text[last:])
        return words

    print segment(text, seg1)
    print segment(text, seg2)

    # 计算目标函数:给定一个假设的源文本的分词(左),推导出一个词典和推导表,它能让源文本重构,然后合计每个词项(包括边界标
    # 志)与推导表的字符数,作为分词质量的得分;得分值越小表明分词越好
    # 例3-3 计算存储词典和重构源文本的成本
    def evaluate(text, segs):
        words = segment(text, segs)
        text_size = len(words)
        lexicon_size = len(" ".join(list(set(words))))
        return text_size + lexicon_size
    print segment(text, seg1)
    print evaluate(text, seg1)
    print segment(text, seg2)
    print evaluate(text, seg2)
    print segment(text, seg3)
    print evaluate(text, seg3)
    # 最后一步是寻找最大化目标函数值0和1的模式,如例3-4所示。请注意,最好的分词包括像“thekitty”这
    # 样的“词”,因为数据中没有足够的证据进一步分割这个词。

    # 使用模拟退火算法的非确定性搜索:一开始仅搜索短语分词;随机扰
    # 动0和1,它们与“温度”成比例;每次迭代温度都会降低,扰动边界会减少
    from random import randint
    def flip(segs, pos):
        return segs[:pos] + str(1 - int(segs[pos])) + segs[pos+1:]

    def flip_n(segs, n):
        for i in range(n):
            segs = flip(segs, randint(0, len(segs)-1))
        return segs

    def anneal(text, segs, iterations, cooling_rate):
        temperature = float(len(segs))
        while temperature > 0.5:
            best_segs, best = segs, evaluate(text, segs)
            for i in range(iterations):
                guess = flip_n(segs, int(round(temperature)))
                score = evaluate(text, guess)
                if score < best:
                    best, best_segs = score, guess
            score, segs = best, best_segs
            temperature = temperature / cooling_rate
            print evaluate(text, segs), segment(text, segs)
        print
        return segs

    print anneal(text, seg1, 5000, 1.2)

fun1()