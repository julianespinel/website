

def to_dict(elements):
    all_true = [True] * len(elements)
    return dict(zip(elements, all_true))


def query_set_to_dict(key_label, value_label, query_set):
    some_dict = {}
    for row in query_set:
        some_dict[row[key_label]] = row[value_label]
    return some_dict
