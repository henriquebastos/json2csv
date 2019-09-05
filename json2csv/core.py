"""
Author: Henrique Bastos <henrique@bastos.net>
Based on the post from Amir Ziai
https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
"""
from json2csv.datastructures import MultiValueDict


def flatten(obj, path=(), sep='__'):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, dict):
                yield from flatten(v, path)
            else:
                yield from flatten(v, path + (str(i),))
    else:
        yield sep.join(path), obj


if __name__ == '__main__':
    # tests
    assert (dict(flatten({'a': 1, 'b': 2, 'c': 3}))
            == {'a': 1, 'b': 2, 'c': 3})

    assert (dict(flatten({'a': 1, 'b': [2, 3], 'c': 4}))
            == {'a': 1, 'b__0': 2, 'b__1': 3, 'c': 4})

    assert (dict(flatten({'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}))
            == {'a': 1, 'b__c': 2, 'b__d': 3, 'e': 4})

    assert (dict(flatten({'b': {'c': [2, 3], 'd': {'e': 4, 'f': 5}}}))
            == {'b__c__0': 2, 'b__c__1': 3, 'b__d__e': 4, 'b__d__f': 5})

    assert dict(flatten([1, 2, 3])) == {'0': 1, '1': 2, '2': 3}

    json = (
        [
            {"time": "Flamengo",
             "jogadores": [
                 {"nome": "Junior Baiano"},
                 {"nome": "Gilmar"},
                 {"nome": "Leão"},
             ],
             },
            {"time": "Sport",
             "jogadores":
                 [
                     {"nome": "Magrão"},
                     {"nome": "Juninho"},
                     {"nome": "Bala"},
                 ],
             },
            {"time": "Corinthians",
             "jogadores":
                 [
                     {"nome": "Socrates"},
                     {"nome": "Casa Grande"},
                     {"nome": "Cássio"},
                 ],
             },
        ]
    )

    csv = (
        [
            {"time": "Flamengo", "jogadores__nome": "Junior Baiano"},
            {"time": "Flamengo", "jogadores__nome": "Gilmar"},
            {"time": "Flamengo", "jogadores__nome": "Leão"},
            {"time": "Sport", "jogadores__nome": "Magrão"},
            {"time": "Sport", "jogadores__nome": "Juninho"},
            {"time": "Sport", "jogadores__nome": "Bala"},
            {"time": "Corinthians", "jogadores__nome": "Socrates"},
            {"time": "Corinthians", "jogadores__nome": "Casa Grande"},
            {"time": "Corinthians", "jogadores__nome": "Cássio"},
        ]
    )

    m = MultiValueDict()
    for k, v in flatten(json):
        #m.appendlist(k, v)
        print(k, v)

    #print(m)
    #assert defaultdict(list, flatten(json)) == csv
