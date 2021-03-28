import re
from typing import Dict, Set, List, NewType, Tuple
from typing_extensions import TypedDict


SUFFIXES_FILE = 'suffixes.txt'


class SuffixesMap(TypedDict):
    remove: Set[str]
    split: Set[str]
    exception: Set[str]
    replace: Set[Tuple[str, str]]


def get_suffixes() -> SuffixesMap:
    """
    Reads SUFFIXES_FILE and gets suffixes that either need to be removed or
    splitted with the word.
    The file has items in the format: "[r|s] <space> <suffix>" in each line
    where r stands for remove the suffix and s for split the suffix
    """
    suffixes: SuffixesMap = {
        'remove': set(),
        'split': set(),
        'replace': set(),
        'exception': set()
    }
    actions = suffixes.keys()

    with open(SUFFIXES_FILE, 'r') as suff_file:
        for line in suff_file.readlines():
            if not line.strip():
                continue
            [action, suffix, *other] = line.split()

            if action not in actions:
                print(f"Invalid action {action}. Ignoring...")
                continue

            if action == 'replace':
                suffixes[action].add((suffix, other[0]))
            else:
                suffixes[action].add(suffix)
    return suffixes


def process_word_suffix(suffixes: SuffixesMap, word: str) -> List[str]:
    if word in suffixes['exception']:
        return [word]
    for src, tgt in suffixes['replace']:
        if word.endswith(src):
            word = re.sub(rf'{src}', tgt, word)
            break

    changes = True
    while changes:
        # Loop until no changes are done
        changes = False
        for suff in suffixes['remove']:
            if word.endswith(suff):
                changes = True
                word = word.rstrip(suff)
                break

        for suff in suffixes['split']:
            if word.endswith(suff):
                splitted = word.split(suff)
                subject = suff.join(splitted[:-1])
                # We again need to process the subject because we can have something like:
                #   dal-haru-bata in which case we split bata, but need to process dal-haru
                #   to remove haru
                return [*process_word_suffix(suffixes, subject), suff]
    return [word]


def process_suffixes(suffixes: SuffixesMap, words: List[str]) -> List[str]:
    processed = []
    for word in words:
        processed.extend(process_word_suffix(suffixes, word))
    return processed


if __name__ == '__main__':
    string1 = ' नेपाली कांग्रेसका दिवगंत नेता नवीन्द्रराज जोशीलाई शीर्ष नेताहरुले श्रद्धाञ्जली दिएका छन् । '
    string2 = 'प्रतिनिधिसभा विघटनलाई असंवैधानिक भनेर सडकमा गएका दलहरुबाटै हतारमा समर्थन फिर्ता नलिन आफूमाथि जबर्जस्त दबाब रहेको उनले बताए'
    string3 = 'डिजाइन अर्कोतिर गयो । सर्वोच्च अदालतको संवैधानिक इजलासले यो सरकारलाई धारा ७६ (१) भनेको छ । त्यही सर्वोच्चको दुईजना न्यायाधीशको बेञ्चले ७६(२) को भन्यो ।’'
    strs = [string1, string2, string3]
    suffixes = get_suffixes()
    for s in strs:
        print(process_suffixes(suffixes, s.split()))
