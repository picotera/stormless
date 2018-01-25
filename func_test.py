import random
import sys
# functions = {
#     "sum": "a+b",
#     "mul": "a*b",
# }




# print(eval(cmd,{"a":1,"b":3})


def random_sentence_spout():
    yield random.choice(["the cow jumped over the moon", "an apple a day keeps the doctor away",
        "four score and seven years ago", "snow white and the seven dwarfs", "i am at two with nature"])

def sentence_splitter(inputs):
    words_str = inputs
    # print "word str", words_str
    words = words_str.split(' ')
    for word in words:
        # print "word s", word
        yield word


def word_counter(inputs):
    word = inputs[0]
    counts = inputs[1]
    # print "word c", word
    count = counts.get(word)
    if count is None:
        count = 0
    count += 1
    counts[word] = count
    return counts

# print(exec(cmd_def,{"a":1,"b":3}))
# print(exec(cmd,{"a":5,"b":8}))
# print(exec(cmd_return,{"a":1,"b":3}))
if __name__ == "__main__":
    counts = {}
    args = sys.argv[1:]
    for a in random_sentence_spout():
        for b in sentence_splitter(a):
            c = (b,counts)
            for d in word_counter(c):
            	pass
    print counts