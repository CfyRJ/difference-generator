import json


def generate_diff(file1_path: str, file2_path: str) -> str:
    values_up_to = json.load(open(file1_path))
    values_after = json.load(open(file2_path))

    values = []

    for k, v in values_up_to.items():
        if k in values_after.keys() and values_after[k] == v:
            values += [['   ', k, v]]
            continue
        if k in values_after.keys() and values_after[k] != v:
            values += [['  -', k, v], ['  +', k, values_after[k]]]
            continue
        values += [['  -', k, v]]
    
    for k, v in values_after.items():
        if k not in values_up_to.keys():
            values += [['  +', k, v]]
    
    values.sort(key=lambda x: x[1])
    values = ['{'] + list(map(lambda x: f'{x[0]} {x[1]}: {x[2]}', values)) + ['}']
    values = '\n'.join(values)

    return values



# p1 = 'second-project/python-project-50/data/file1.json'
# p2 = 'second-project/python-project-50/data/file2.json'

# generate_diff(p1, p2)

# if __name__ == '__main__':
#     main()
