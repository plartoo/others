# https://stackoverflow.com/q/62124898/1330974

# import json
#
# counting_table = dict(zip([str(i) for i in range(10)],[0 for i in range(10)]))
#
# compute_counter = 0
# n = 123456 # 1,000,000 == 5,888,896
# print(f"n: {n}")
# for num in range(1, n+1):
#     for digit in str(num):
#         compute_counter += 1
#         counting_table[digit] += 1
#
# print(json.dumps(counting_table, sort_keys=True, indent=4))
# print(compute_counter)


def main():
    n = int(input('n : '))
    num_arr = [0] * 10
    w = 1

    for step in range(len(str(n))):
        remaining = 9 - int(str(n)[-1:])

        for i in range(len(num_arr)):
            num_arr[i] += (n // 10 + 1) * w

        for i in range(10 - remaining, 10):
            num_arr[i] -= w
        num_arr[0] -= w

        for number in str(n)[:-1]:
            num_arr[int(number)] -= remaining * w

        n //= 10
        w *= 10

    print(num_arr)


if __name__ == '__main__':
    main()