import argparse


parser = argparse.ArgumentParser(description="sorting")
parser.add_argument('-i','--input',metavar='', required=True, help="Path to input")
args = parser.parse_args()

def remove_correct_places(org,trg,orgw):
    indexes_to_delete = []

    for index, tpl in enumerate(zip(org, trg)):
        if tpl[0] == tpl[1]:
            indexes_to_delete.append(index)

    for index in reversed(indexes_to_delete):
        org.pop(index)
        trg.pop(index)
        orgw.pop(index)

data = [line.strip() for line in open(args.input, 'r')]
weight = [int(x) for x in data[1].split()]
origin = [int(x) for x in data[2].split()]
target = [int(x) for x in data[3].split()]


weights = {nr+1:item for nr, item in enumerate(weight)}
origin_weights= [weights[x] for x in origin]
result = 0
remove_correct_places(origin,target,origin_weights)


while origin_weights:

    min_weight = min(origin_weights)
    min_weight_index = origin_weights.index(min_weight)
    min_weight_element = origin[min_weight_index]
    other_element = target[min_weight_index]
    other_index = origin.index(other_element)
    other_weight = weights[other_element]
    origin[min_weight_index] = other_element
    origin_weights[min_weight_index] = other_weight
    origin[other_index] = min_weight_element
    origin_weights[other_index] = min_weight
    result += other_weight + min_weight
    remove_correct_places(origin, target, origin_weights)

print(result)