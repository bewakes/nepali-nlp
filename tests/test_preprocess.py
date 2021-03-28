from preprocess import process_suffixes, get_suffixes


def test_suffix_processing():
    suffixes = get_suffixes()
    str1 = ' नेपाली कांग्रेसका दिवगंत नेता नवीन्द्रराज जोशीलाई शीर्ष नेताहरुले श्रद्धाञ्जली दिएका छन् । '
    str1_expected = ' नेपाली कांग्रेस दिवगंत नेता नवीन्द्रराज जोशी लाई शीर्ष नेता श्रद्धाञ्जली दिए छन् । '.split()
    assert process_suffixes(suffixes, str1.split()) == str1_expected

    str2 = 'प्रतिनिधिसभा विघटनलाई असंवैधानिक भनेर सडकमा गएका दलहरुबाटै हतारमा समर्थन फिर्ता नलिन आफूमाथि जबर्जस्त दबाब रहेको उनले बताए'
    str2_expected = 'प्रतिनिधिसभा विघटन लाई असंवैधानिक भनेर सडक गए दल बाट हतार समर्थन फिर्ता नलिन आफू माथि जबर्जस्त दबाब रहे उन बताए'.split()
    assert process_suffixes(suffixes, str2.split()) == str2_expected

    str3 = 'डिजाइन अर्कोतिर गयो । सर्वोच्च अदालतको संवैधानिक इजलासले यो सरकारलाई धारा ७६ (१) भनेको छ । त्यही सर्वोच्चको दुईजना न्यायाधीशको बेञ्चले ७६(२)को भन्यो ।’'
    str3_expected = 'डिजाइन अर्को तिर गयो । सर्वोच्च अदालत संवैधानिक इजलास यो सरकार लाई धारा ७६ (१) भने छ । त्यही सर्वोच्च दुईजना न्यायाधीश बेञ्च ७६(२) भन्यो ।’ '.split()
    assert process_suffixes(suffixes, str3.split()) == str3_expected
