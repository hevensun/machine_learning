from model.Deduplication import Deduplication

if __name__ == '__main__':
    '''
    docs:初始docs库，可为空
    '''
    docs = "这个对news.txt文本的编码有什么要求吗?为什么我的运行完是0.0一直到结尾\t这个对news.txt文本的编码有什么要求吗?我的运行完是0.0一直到结尾\t今天天气不错"
    deduplication = Deduplication(docs, type="longest", partion=3, cutoff=3)
    print(deduplication.start("这个对news.txt文本的编码有要求吗?我的运行完是0.0一直到结尾"))
    print(deduplication.start("如果有机会赢，一定参加"))
    print(deduplication.start("刘备收养寇封为子时，汉怀帝还未出生。"))
    print(deduplication.start("Only the owner of this repository can see this message."))
    print(deduplication.docs_dict)