"""
Author: Henrique Bastos <henrique@bastos.net>
Based on the post from Amir Ziai
https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
"""
from itertools import count, chain

from json2csv.datastructures import MultiValueDict


def flatten(obj, path=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, path + (k,))
    elif isinstance(obj, list):
        if all(isinstance(item, dict) for item in obj):
            for item in obj:
                yield from flatten(item, path)
        else:
            for i, v in enumerate(obj):
                yield from flatten(v, path + (str(i),))
    else:
        yield path, obj


def tabulate(iterable, sep='__'):
    row = {}
    last_level = level = 0

    for path, value in iterable:
        level = len(path)
        header = sep.join(path)

        if level == last_level and header in row:
            yield row.copy()
        elif level < last_level:
            yield row.copy()
            for n in range(last_level - level):
                row.popitem()

        row[header] = value

        last_level = level
    yield row

def trim(d, level):
    return {k: v for k, v in d.items() if len(k) < level}


if __name__ == '__main__':
    # tests
    assert (dict(flatten({'a': 1, 'b': 2, 'c': 3}))
            == {('a',): 1, ('b',): 2, ('c',): 3})

    assert (dict(flatten({'a': 1, 'b': [2, 3], 'c': 4}))
            == {('a',): 1, ('b', '0'): 2, ('b', '1'): 3, ('c',): 4})

    assert (dict(flatten({'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}))
            == {('a',): 1, ('b', 'c'): 2, ('b', 'd'): 3, ('e',): 4})

    assert (dict(flatten({'b': {'c': [2, 3], 'd': {'e': 4, 'f': 5}}}))
            == {('b', 'c', '0'): 2, ('b', 'c', '1'): 3, ('b', 'd', 'e'): 4, ('b', 'd', 'f'): 5})

    assert dict(flatten([1, 2, 3])) == {('0',): 1, ('1',): 2, ('2',): 3}

    json = (
        [
            {"time": "Flamengo",
             "jogadores": [
                 {"nome": "Junior Baiano", "idade": 40},
                 {"nome": "Gilmar", "idade": 50},
                 {"nome": "Leão", "idade": 60},
             ],
             },
            {"time": "Sport",
             "jogadores":
                 [
                     {"nome": "Magrão", "idade": 45},
                     {"nome": "Juninho", "idade": 55},
                     {"nome": "Bala", "idade": 65},
                 ],
             },
            {"time": "Corinthians",
             "jogadores":
                 [
                     {"nome": "Socrates"},
                     {"nome": "Casa Grande"},
                     {"nome": "Cássio", "idade": 40},
                 ],
             },
        ]
    )

    csv = [
        dict(time="Flamengo", jogadores__nome="Junior Baiano", jogadores_idade=40),
        dict(time="Flamengo", jogadores__nome="Gilmar", jogadores_idade=50),
        dict(time="Flamengo", jogadores__nome="Leão", jogadores_idade=60),
        dict(time="Sport", jogadores__nome="Magrão", jogadores_idade=45),
        dict(time="Sport", jogadores__nome="Juninho", jogadores_idade=55),
        dict(time="Sport", jogadores__nome="Bala", jogadores_idade=65),
        dict(time="Corinthians", jogadores__nome="Socrates"),
        dict(time="Corinthians", jogadores__nome="Casa Grande"),
        dict(time="Corinthians", jogadores__nome="Cássio", jogadores_idade=40),
    ]
    print(list(tabulate(flatten(json))))
    assert list(tabulate(flatten(json))) == csv

    g = tabulate(flatten(json))
    row = next(g)
    print(list(row.keys()))
    print(list(row.values()))
    for row in g:
        print(list(row.values()))





    #print(m)
    #assert defaultdict(list, flatten(json)) == csv
