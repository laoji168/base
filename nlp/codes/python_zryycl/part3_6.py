# coding=utf-8
from __future__ import division
import nltk, re, pprint
"""
处理原始文本
"""
def fun1():
    from urllib import urlopen
    url = "http://www.gutenberg.org/files/2554/2554.txt"
    # proxies = {'http': 'http://www.someproxy.com:3128'}
    raw = urlopen(url).read()
    print type(raw)
    print len(raw)
    print raw[:75]
    tokens = nltk.word_tokenize(raw)
    print type(tokens)
    print len(tokens)
    print tokens[:10]
    text = nltk.Text(tokens)
    print type(text)
    print text[0:10]
    print text.collocations()
    # 从HTML中提取文本是极其常见的任务,NLTK提供了辅助函数nltk.clean_html()将HTML字符串作为参
    # 数,返回原始文本。然后可以对原始文本进行分词,获得我们熟悉的文本结构
    url = "http://www.qidian.com"
    html = urlopen(url).read()
    print html[:60]
    import bs4
    # raw = nltk.clean_html(html)
    raw = bs4.BeautifulSoup().get_text(html)
    print raw[:100]
    tokens = nltk.word_tokenize(raw)
    print tokens[:100]


"""
规范化文本
"""
def fun2():
    # NLTK中包括了一些现成的词干提取器,如果需要使用词干提取器,应该优先使用它们中的一个,而不
    # 是使用正则表达式制作自己的词干提取器,因为NLTK中的词干提取器能处理的不规则情况很广泛。Porter
    # 和Lancaster词干提取器按照它们自己的规则剥离词缀。
    raw = """DENNIS: Listen, strange women lying in ponds distributing swords
            is no basis for a system of government. Supreme executive power derives from
            a mandate from the masses, not from some farcical aquatic ceremony."""
    tokens = nltk.word_tokenize(raw)
    porter = nltk.PorterStemmer()
    lancaster = nltk.LancasterStemmer()
    print [porter.stem(t) for t in tokens]
    print [lancaster.stem(t) for t in tokens]


fun2()