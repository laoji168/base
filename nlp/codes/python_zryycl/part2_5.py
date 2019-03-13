# coding=utf-8
import nltk
"""
WordNet
WordNet是面向语义的英语词典,与传统辞典类似,但结构更丰富。NLTK中包括英语WordNet,共有
155287个单词和117659个同义词。我们将从寻找同义词和如何在WordNet中访问它们开始
"""
def fun1():
    # motorcar和automobile有相同的含义即它们是同义
    # 词。在WordNet的帮助下,我们可以探索这些词
    from nltk.corpus import wordnet as wn
    print wn.synsets('motorcar')
    # 因此,motorcar只有一个可能的含义,它被定义为car.n.01,car的第一个名词意义。car.n.01被称
    # 为synset或“同义词集”,即意义相同的词(或“词条”)的集合
    print wn.synset('car.n.01').lemma_names()
    # 同义词集中的每个词可以有多种含义,例如:car可能是火车车厢、货车或电梯厢。但对于这个同义词
    # 集中的所有单词来说,最感兴趣的是其最常用的意义。同义词集也有一些一般的定义和例句
    print wn.synset('car.n.01').definition()
    print wn.synset('car.n.01').examples()
    # 虽然定义可以帮助人们了解一个同义词集的本意,但往往是同义词集中的词对程序是更有用的。为了
    # 消除歧义,将这些词标注为car.n.01.automobile、car.n.01.motorcar等。这种同义词集和词的配对叫做词条。
    # 可以得到指定同义词集的所有词条 1 ,查找特定的词条 2 ,得到一个词条所对应的同义词集 3 ,也可以得到
    # 一个词条的“名字” 4 。
    print wn.synset('car.n.01').lemmas()
    print wn.lemma('car.n.01.automobile')
    print wn.lemma('car.n.01.automobile').synset()
    print wn.lemma('car.n.01.automobile').name()
    # 与词automobile和motorcar这些意义明确且只有一个同义词集的词不同,词car是含糊的,共有5个同义
    # 词集
    print wn.synsets('car')
    for synset in wn.synsets('car'):
        print synset.lemma_names()
    print wn.lemmas('car')
    # WordNet使我们能容易驾驭各种概念。例如:摩托车,可以看到更加具体(直接)的概念——下位词
    motorcar = wn.synset('car.n.01')
    type_of_motorcar = motorcar.hyponyms()
    print type_of_motorcar[26]
    print sorted([lemma.name() for synset in type_of_motorcar for lemma in synset.lemmas()])
    # 通过访问上位词来操纵层次结构。有些词有多条路径,因为它们可以归类在多种分类中。car.n.01与
    # entity.n.01之间有两条路径,因为wheeled_vehicle.n.01可以同时被归类为车辆和容器
    print motorcar.hyponyms()
    paths = motorcar.hypernym_paths()
    print len(paths)
    print [synset.name() for synset in paths[0]]
    print [synset.name() for synset in paths[1]]
    # 我们可以用如下方式得到一个最笼统的上位(或根上位)同义词集
    print motorcar.root_hypernyms
    # 上位词和下位词被称为词汇关系,因为它们是同义集之间的关系。这两者的关系为上下定位“is-a”层
    # 次。WordNet网络另一个重要的定位方式是从条目到它们的部件(部分)或到包含它们的东西(整体)。例
    # 如:一棵树可以分成树干、树冠等部分,这些都是part_meronyms()。一棵树的实质是由心材和边材组成
    # 的,即substance_meronyms()。树木的集合形成了一个森林,即member_holonyms()
    print wn.synset('tree.n.01').part_meronyms()
    print wn.synset('tree.n.01').substance_meronyms()
    print wn.synset('tree.n.01').member_holonyms()
    # 看看有多么复杂吧,比如单词mint,有好几个密切相关的意思。mint.n.04是mint.n.02的一部分,同时也
    # 是组成mint.n.05的材料
    for synset in wn.synsets('mint', wn.NOUN):
        print synset.name() + ":", synset.definition
    print wn.synset('mint.n.04').part_holonyms()
    print wn.synset('mint.n.04').substance_holonyms()
    # 动词之间也存在关系。例如:走路的动作包括抬脚的动作,所以走路蕴涵着抬脚。一些动词有多个含
    # 义。
    print wn.synset('walk.v.01').entailments()
    print wn.synset('eat.v.01').entailments()
    print wn.synset('tease.v.03').entailments()
    # 词条之间还存在一些词汇关系,如:反义词
    print wn.lemma('supply.n.02.supply').antonyms()
    print wn.lemma('rush.v.01.rush').antonyms()
    print wn.lemma('horizontal.a.01.horizontal').antonyms()
    print wn.lemma('staccato.r.01.staccato').antonyms()
    # 同义词集是由复杂的词汇关系网络所连接起来的。给定一个同义词集,可以遍历WordNet网络来查找相
    # 关含义的同义词集。知道哪些词是语义相关的,是对索引文本集合有用的,当搜索一个一般性的用语时
    # ——例如车辆——就可以匹配包含特定术语——例如豪华轿车——的文档。
    # 每个同义词集都有一个或多个上位词路径连接到一个根上位词,如entity.n.01。连接到同一个根的两个
    # 同义词集可能有一些共同的上位词(见图2-8)。如果两个同义词集共用一个特定的上位词——在上位词层
    # 次结构中处于较低层——它们一定有密切的联系
    right = wn.synset('right_whale.n.01')
    orca = wn.synset('orca.n.01')
    minke = wn.synset('minke_whale.n.01')
    tortoise = wn.synset('tortoise.n.01')
    novel = wn.synset('novel.n.01')
    print right.lowest_common_hypernyms(minke)
    print right.lowest_common_hypernyms(orca)
    print right.lowest_common_hypernyms(tortoise)
    print right.lowest_common_hypernyms(novel)
    # 当然,鲸鱼是非常具体的(须鲸更是如此),脊椎动物是更具一般化,而实体完全是抽象的。我们可
    # 以通过查找每个同义词集的深度来量化这个普遍性的概念
    print wn.synset('baleen_whale.n.01').min_depth()
    print wn.synset('whale.n.02').min_depth()
    print wn.synset('vertebrate.n.01').min_depth()
    print wn.synset('entity.n.01').min_depth()
    # WordNet同义词集定义了类似的方法来进行深入的观察。例如:path_similarity基于上位词层次结构概念
    # 中相互关联的最短路径下,在0~1范围内的相似度(两者之间没有路径就返回−1)。同义词集与自身比较
    # 将返回1。考虑以下的相似度:露脊鲸与小须鲸、逆戟鲸、乌龟以及小说。虽然这些数字本身的意义并不
    # 大,但是从海洋生物的语义空间转移到非生物时,数字是减少的
    print right.path_similarity(minke)
    print right.path_similarity(orca)
    print right.path_similarity(tortoise)
    print right.path_similarity(novel)




# nltk.download('wordnet')
fun1()