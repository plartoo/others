def two_sum(nums, target):
    count = 0
    for i, n1 in enumerate(nums):
        for j, n2 in enumerate(nums[i:]):
            count += 1
            if n1+n2 == target:
                print(count)
                return [i, i+j]
    print(count)
    return "Sorry"


def two_sum2(nums, target):
    count = 0
    for i, n1 in enumerate(nums):
        diff = target - n1
        for j, n2 in enumerate(nums[i:]):
            count += 1
            if diff == n2:
                print(count)
                return [i, i+j]
    print(count)
    return "Sorry"


if __name__ == '__main__':
    nums1 = [2, 7, 11, 15]
    target = 9
    print(two_sum(nums1, target))

    nums1 = [2, 7, 11, 15]
    target = 15
    print(two_sum(nums1, target))

    nums1 = [2, 7, 11, 15]
    target = 22
    print(two_sum(nums1, target))

    nums1 = [2, 7, 11, 15]
    target = 26
    print(two_sum(nums1, target))

    nums1 = [7, 11, 15, 2]
    target = 9
    print(two_sum(nums1, target))

    print("\n====\n")

    nums1 = [2, 7, 11, 15]
    target = 9
    print(two_sum2(nums1, target))

    nums1 = [2, 7, 11, 15]
    target = 15
    print(two_sum2(nums1, target))

    nums1 = [2, 7, 11, 15]
    target = 22
    print(two_sum2(nums1, target))

    nums1 = [2, 7, 11, 15]
    target = 26
    print(two_sum2(nums1, target))

    nums1 = [7, 11, 15, 2]
    target = 9
    print(two_sum2(nums1, target))
