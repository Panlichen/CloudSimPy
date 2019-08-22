import simpy


def yield_test():
    j = 0
    for i in range(5):
        recv = yield j
        if recv is None:
            recv = 0
            print("i = {}".format(i), "recv nothing")
        else:
            print("i = {}".format(i), recv, type(recv))
        j = j + int(recv) + i


yt = yield_test()

print(next(yt))
print("==============")
print(yt.send(199))
print("==============")
print(next(yt))

# for i in range(3):
#     print(next(yt))
#     print("=============")
#
#
# for i in range(3):
#     print(next(yt))
