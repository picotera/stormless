import random
import sys
import re

# functions = {
#     "filter": (lambda x: int(x) if x.match(r"\d",x) else None),
#     "splitter": (lambda x: "mul" if x%2==0 else "sum"),
#     # "dehydrate": ()
#     "mul": (lambda x: x[0]*x[1]),
#     "sum": (lambda x: x[0]+x[1]),
# }


# functions = {
#     "spout": ("split", random.choice(["a a a a a", 
#         "how much wood would the woodchuck chuck if the wouldchuck could chuck wood" ,
#         "the cow jumped over the moon", "an apple a day keeps the doctor away",
#         "four score and seven years ago", 
#         "snow white and the seven dwarfs", 
#         "i am at two with nature"])),
#     "split": (lambda sentence: [("count",x) for x in sentence[0].split(' ')] ),
#     "count": (lambda inputs: (counts.update({inputs[0]:counts.get(inputs[0], 0)+1}))),
# }


# functions = {
#     "spout": ("split", "how much wood would the woodchuck chuck if the wouldchuck could chuck wood"),
#     "split": (lambda sentence: [("count",x) for x in sentence[0].split(' ')] ),
#     "count": (lambda inputs: (counts.update({inputs[0]:counts.get(inputs[0], 0)+1}))),
# }



counts = {}

def run(functions, inputs):
    if isinstance(inputs, basestring):
        run(functions,functions.get(inputs))
    elif isinstance(inputs, tuple):
        run(functions,functions.get(inputs[0])(inputs[1:]))
    elif isinstance(inputs, list):
        for tup in inputs:
            run(functions,tup)


if __name__ == "__main__":
    # args = sys.argv[1:]

    request = (None,"","""{
"spout": ("split", "how much wood would the woodchuck chuck if the wouldchuck could chuck wood"),
"split": (lambda sentence: [("count",x) for x in sentence[0].split(' ')] ),
"count": (lambda inputs: (counts.update({inputs[0]:counts.get(inputs[0], 0)+1}))),
}
""")
#     request = """{
# "spout": ("split", random.choice(["a a a a a", 
#     "how much wood would the woodchuck chuck if the wouldchuck could chuck wood" ,
#     "the cow jumped over the moon", "an apple a day keeps the doctor away",
#     "four score and seven years ago", 
#     "snow white and the seven dwarfs", 
#     "i am at two with nature"])),
# "split": (lambda sentence: [("count",x) for x in sentence[0].split(' ')] ),
# "count": (lambda inputs: (counts.update({inputs[0]:counts.get(inputs[0], 0)+1}))),
# }
# """
    functions = eval(request[2])
    if request[0] is None:
    	run(functions,"spout")
    else:
    	run(functions,request[0])(eval(request[1]))
    print(counts)
