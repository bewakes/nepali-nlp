_whole_phonetic_groups = [
    'स श ष',
    'ब व',
    'न ण ञ',
    'उ ऊ ौ',
    'इ ई ै',
    'य ये ए',
    'ु ू',
    ' ि ी',
    'ं ँ न्',
#    'इ ई यि यी',
]

phonetic_groups = [set(x.split()) for x in _whole_phonetic_groups]

chars_grps_map = {k: grp for grp in phonetic_groups for k in grp}
