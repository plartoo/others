def two_sum(nums, target):
    count = 0
    for i, n1 in enumerate(nums):
        for j, n2 in enumerate(nums[i:]):
            count += 1
            if n1+n2 == target:
                print(count)
                return [i, i+j]
    print(count)
    return "Sorry. No desired pairing found."


def two_sum2(nums, target):
    count = 0
    print("\n", nums, "=>", target)
    for i, n1 in enumerate(nums):
        diff = target - n1
        for j, n2 in enumerate(nums[i:]):
            count += 1
            if diff == n2:
                # print(count)
                return ''.join(["Found:", str([i, i+j])])
    # print(count)
    return "Sorry. No desired pairing found."


def two_sum3(nums, target):
    d = {}
    count = 0
    print("\n", nums, "=>", target)
    for i, n1 in enumerate(nums):
        count += 1
        diff = target - n1
        if diff > 0:
            d[diff] = i
        if n1 in d:
            if i != d[n1]: # for cases where the target = current_num * 2
                return ''.join(["Found:", str([i,d[n1]])])
    # print(count)
    return "Sorry. No desired pairing found."


if __name__ == '__main__':
    # print(two_sum([2, 7, 11, 15], 9))
    # print(two_sum([2, 7, 11, 15], 15))
    # print(two_sum([2, 7, 11, 15], 22))
    # print(two_sum([2, 7, 11, 15], 26))
    # print(two_sum([7, 11, 15, 2], 9))
    # print("\n====\n")
    print(two_sum2([2, 7, 11, 15], 9))
    print(two_sum2([22, 7, 11, 15], 15))
    print(two_sum2([2, 7, 11, 15], 22))
    print(two_sum2([2, 7, 11, 15], 26))
    print(two_sum2([7, 11, 15, 2], 9))
    print(two_sum2([7, 11, 15, 2], 0)) # no
    print("\n====\n")
    print(two_sum3([2, 7, 11, 15], 9)) # [0,1]
    print(two_sum3([22, 7, 11, 15], 15)) # no
    print(two_sum3([2, 7, 11, 15], 22)) # [1,3]
    print(two_sum3([2, 7, 11, 15], 26)) # [2,3]
    print(two_sum3([7, 11, 15, 2], 9)) # [0,3]
    print(two_sum3([7, 11, 15, 2], 0)) # no
