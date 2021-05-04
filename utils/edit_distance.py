import os
import sys
from typing import List
from itertools import product

from unicode_char_map import (
    consonant_kaars, halanta, amkaar,
    aNNkaar, Ri, akaars, basic_vowels,
)
from phonetic_groups import phonetic_groups, chars_grps_map

INSERT_COST = 1
DELETE_COST = 1
REPLACE_COST = 2

WORDS_PATH = os.path.join(os.path.dirname(__file__), 'words.txt')


def load_words():
    with open(WORDS_PATH, 'r') as f:
        return [x.strip() for x in f.readlines() if x]


def replace_with_phonetic_group(pos, word, group, size):
    return set([word[:pos] + x + word[pos+size:] for x in group])


def _generate_phonetic_edits(word: str) -> List[str]:
    positions = []
    grps = []
    for i, x in enumerate(word):
        for grp in phonetic_groups:
            if x in grp:
                positions.append(i)
                grps.append(grp)
                break
    prods = product(*grps)
    items = list()
    for p in prods:
        w = list(word)
        for i, rep in zip(positions, p):
            w[i] = rep
        items.append(''.join(w))
    return items


MAX_PROD_LEN = 0


def generate_phonetic_edits(word: str) -> List[str]:
    positions = []
    grps = []
    for i, x in enumerate(word):
        if x in chars_grps_map:
            positions.append(i)
            grps.append(chars_grps_map[x])

    # TRUNCATE MAX POSITIONS: do not generate products for too many possible positions
    positions = positions[:8]
    grps = grps[:8]

    prods = product(*grps)
    items = list()
    for i, p in enumerate(prods):
        w = list(word)
        for i, rep in zip(positions, p):
            w[i] = rep
        items.append(''.join(w))
    return items


def generate_1_edit_tokens(token: List[str], exclude: set = set()) -> List[List[str]]:
    tokens = set()
    size = len(token)
    akaars_uni = akaars.values()

    possible_suffs = [halanta, *consonant_kaars.values(), amkaar, aNNkaar, Ri, ':']
    basic_vowels_rev = {v: k for k, v in basic_vowels.items()}

    # First add the tokens containing aakaars for non aakar words
    for i in range(size):
        tok = token[i]
        generated = set()
        if len(tok) == 1:
            # If in basic_vowels
            if tok in basic_vowels.values():
                if basic_vowels_rev[tok] != 'a':  # Do nothing for a
                    rev_key = basic_vowels_rev[tok]
                    if not rev_key in consonant_kaars:
                        continue
                    new_tok = (*token[:i], consonant_kaars[rev_key], *token[i+1:])
                    if new_tok not in exclude:
                        generated.add(new_tok)
            else:
                # Just add halantas, aakars, amkars, Ri
                for suf in possible_suffs:
                    new_tok = (*token[:i], tok+suf, *token[i+1:])
                    if new_tok not in exclude:
                        generated.add(new_tok)
            tokens = tokens.union(generated)

    # Add the tokens by removing the akaars and replacing the aakars
    for i in range(size):
        tok = token[i]
        generated = set()
        if len(tok) == 2 and tok[0] in akaars_uni:
            # Remove the aakaar
            generated.add((*token[:i], tok[0], *token[i+1:]))
            for suf in possible_suffs:
                if suf == tok[-1]:
                    continue
                new_tok = (*token[:i], tok[0]+suf, *token[i+1:])
                if new_tok not in exclude:
                    generated.add(new_tok)
            tokens = tokens.union(generated)
    # Classic 1 edit distances, inserting and deleting
    # First create splits
    splits = [(token[:i], token[i:]) for i in range(len(token)+1)]

    removed = set()
    for a, b in splits:
        if a and len(a[-1]) == 1:
            new = tuple(a[:-1] + b)
            if new not in exclude:
                removed.add(new)
    tokens = tokens.union(removed)

    inserted = set()
    insertables = [*akaars.values(), *basic_vowels.values()]
    # print(len(insertables))
    for a, b in splits:
        for insertable in insertables:
            new = tuple(a + [insertable] + b)
            if new not in exclude:
                inserted.add(new)
    tokens = tokens.union(inserted)
    return tokens


def generate_2_edit_tokens(token: List[str]) -> List[List[str]]:
    edits1 = generate_1_edit_tokens(token)
    edits2 = set()
    # First get 1 edits of 1 edits
    # TODO: remove the original ones
    for x in edits1:
        new_gen = generate_1_edit_tokens(list(x), edits1)
        edits2 = edits2.union(new_gen)
    # Add replacements
    splits = [(token[:i], token[i:]) for i in range(len(token)+1)]
    replaceables = [*akaars.values(), *basic_vowels.values()]
    # replace single length token
    single_replaced = set()
    for a, b in splits:
        if not a or len(a[0]) != 1:
            continue
        for r in replaceables:
            if a[-1] != r:
                single_replaced.add(tuple(a[:-1] + [r] + b))
    edits2 = edits2.union(single_replaced)
            
    return edits2


def generate_3_edit_tokens(token: List[str]) -> List[List[str]]:
    edits2 = generate_2_edit_tokens(token)
    edits3 = set()
    for x in edits2:
        # print(cnt)
        edits3 = edits3.union(generate_1_edit_tokens(list(x), edits2))
    # Add replacements
    splits = [(token[:i], token[i:]) for i in range(len(token)+1)]
    replaceables = [*akaars.values(), *basic_vowels.values()]
    return edits3


def tokenize_word(word) -> List[str]:
    """
    Gets a nepali unicode string and tokenizes it with aakaars.
    For example kaam would normally be [ka, <aakaar>, ma].
    But this will return [kaa, ma]
    """
    tokenized = []
    curr_index = 0
    while True:
        if curr_index >= len(word):
            break
        curr = word[curr_index]

        if curr_index == len(word) - 1:
            tokenized.append(curr)
            break

        nxt = word[curr_index + 1]
        if nxt in [amkaar, aNNkaar, Ri, halanta] or nxt in consonant_kaars.values():
            curr += nxt
            curr_index += 2
        else:
            curr_index += 1

        tokenized.append(curr)
    return tokenized


def get_replace_cost(token1, token2):
    """
    Assumes max length of tokens is 2
    """
    if token1 == token2:
        return 0
    if len(token1) == 1 and len(token2) == 1:
        return 2
    s1 = set(token1)
    s2 = set(token2)
    diff = s1.symmetric_difference(s2)
    if len(diff) == 1 and (halanta in diff or consonant_kaars['aa'] in diff):
        return 1
    if len(diff) > 1:
        return 3
    return 2


# @print_inp_op
def get_insert_cost(token):
    if len(token) == 1:
        return 1
    if len(token) > 2:
        return 3
    if token[-1] in (halanta, amkaar, aNNkaar):
        return 1
    return 2


def get_delete_cost(token):
    return get_insert_cost(token)


def print_(mat, str1=None, str2=None):
    print('[')
    if str2 is not None:
        print(' '.rjust(3), end=' ')
        print('#'.rjust(3), end=' ')
        [print(x.rjust(3), end=' ') for x in str2]
        print()
    if str1 is not None:
        print('#'.rjust(3), end=' ')
    for i, row in enumerate(mat):
        if str1 is not None and i > 0:
            print(str1[i-1].rjust(3), end=' ')
        for x in row:
            print(str(x).rjust(3), end=' ')
        print()
    print(']')


def edit_distance(token1: List[str], token2: List[str]):
    # Initialize a matrix
    l1 = len(token1)
    l2 = len(token2)
    mat = [[-1] * (l2+1) for _ in range(l1+1)]
    # Cost for converting empty tokening to empty
    mat[0][0] = 0
    # Fill out the topmost and left most cells
    for x in range(l1):
        mat[x+1][0] = x+1
    for x in range(l2):
        mat[0][x+1] = x+1

    curr_col = 1
    curr_row = 1
    while True:
        # Fill out row
        for x in range(curr_col, l2+1):
            # replace_cost = mat[curr_row-1][x-1] + (0 if token1[curr_row-1] == token2[x-1] else REPLACE_COST)
            replace_cost = mat[curr_row-1][x-1] + get_replace_cost(token1[curr_row-1], token2[x-1])
            delete_cost = mat[curr_row][x-1] + get_delete_cost(token2[x-1])
            insert_cost = mat[curr_row-1][x] + get_insert_cost(token1[curr_row-1])
            min_cost = min([replace_cost, delete_cost, insert_cost])
            mat[curr_row][x] = min_cost

        # Fill out cols
        for x in range(curr_row+1, l1+1):  # curr_row+1 because the above loop already fills out mat[curr_row][curr_col]
            # replace_cost = mat[x-1][curr_col-1] + (0 if token1[x-1] == token2[curr_col-1] else REPLACE_COST)
            replace_cost = mat[x-1][curr_col-1] + get_replace_cost(token1[x-1], token2[curr_col-1])
            delete_cost = mat[x][curr_col-1] + get_delete_cost(token2[curr_col-1])
            insert_cost = mat[x-1][curr_col] + get_insert_cost(token1[x-1])
            min_cost = min([replace_cost, delete_cost, insert_cost])
            mat[x][curr_col] = min_cost
        curr_col += 1
        curr_row += 1

        if curr_col >= l2+1 or curr_row >= l1+1:
            break
    # print_(mat, token1, token2)
    return mat[l1][l2]


def get_vocab():
    with open(WORDS_PATH) as f:
        return f.read().split()


def get_suggestions(inp: str) -> List[str]:
    vocab = set(get_vocab())
    if inp in vocab:
        return [inp]

    tokenized = tokenize_word(inp)
    edits1 = [''.join(x) for x in generate_1_edit_tokens(tokenized)]
    in_vocab = [x for x in edits1 if x in vocab]
    if in_vocab:
        return in_vocab

    edits2 = [''.join(x) for x in generate_2_edit_tokens(tokenized)]
    in_vocab = [x for x in edits2 if x in vocab]
    if in_vocab:
        return in_vocab
    return [inp]
    # TODO: efficient 3 edits generation

    edits3 = [''.join(x) for x in generate_3_edit_tokens(tokenized)]
    in_vocab = [x for x in edits3 if x in vocab]
    if in_vocab:
        return in_vocab
    return [inp]


def average(N, f, *args):
    t = 0
    import time
    for x in range(N):
        a = time.time()
        f(*args)
        t += time.time() - a
    print(f(*args))
    print(t/N)


if __name__ == '__main__':
    words = load_words()
    processed_words = []
    for w in words:
        sp = w.split('/')
        processed_words.extend(sp)
    inp = 'अप्ठेरो'
    inp = 'अफ्ठेरो'
    inp = 'कमल'
    inp = 'अध्यारओ'
    inp = 'मिनै'
    comp = 'अप्ठ्यारो'
    comp = 'फेरो'

    sent = 'सिमा पहुच सम्राज्यबदी '
    tokenized_inp = tokenize_word(inp)
    # print([get_suggestions(x) for x in sent.split()])
    # edit_1s = generate_1_edit_tokens(tokenized_inp)
    # edit_2s = generate_2_edit_tokens(tokenized_inp)
    # edit_3s = generate_3_edit_tokens(tokenized_inp)
    # print('3 edits', len(edit_3s))
    average(100000, _generate_phonetic_edits, inp)
    average(100000, generate_phonetic_edits, inp)
