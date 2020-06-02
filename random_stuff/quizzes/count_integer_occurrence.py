# https://stackoverflow.com/q/62124898/1330974

import json

counting_table = dict(zip([str(i) for i in range(10)],[0 for i in range(10)]))

compute_counter = 0
n = 1000 # 1,000,000 == 5,888,896
for num in range(1, n+1):
    for digit in str(num):
        compute_counter += 1
        counting_table[digit] += 1

print(json.dumps(counting_table, sort_keys=True, indent=4))
print(compute_counter)