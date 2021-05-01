from preprocess import process_suffixes, get_suffixes, remove_punctuation


def test_suffix_processing():
    suffixes = get_suffixes()

    strs_expected = [
        # ('ढोकाको', ['ढोका']),
        (
            ' नेपाली कांग्रेसका दिवगंत नेता नवीन्द्रराज जोशीलाई शीर्ष नेताहरुले श्रद्धाञ्जली दिएका छन् । ',
            ' नेपाली कांग्रेस दिवगंत नेता नवीन्द्रराज जोशी लाई शीर्ष नेता श्रद्धाञ्जली दिए छन् । '.split()
        ),
        (
            'प्रतिनिधिसभा विघटनलाई असंवैधानिक भनेर सडकमा गएका दलहरुबाटै हतारमा समर्थन फिर्ता नलिन आफूमाथि जबर्जस्त दबाब रहेको उनले बताए',
            'प्रतिनिधिसभा विघटन लाई असंवैधानिक भनेर सडक गए दल बाट हतार समर्थन फिर्ता नलिन आफू माथि जबर्जस्त दबाब रहे उन बताए'.split()
        ),
        ('नगरपालिकामा' , ['नगरपालिका']),
        (
            'डिजाइन अर्कोतिर गयो । सर्वोच्च अदालतको संवैधानिक इजलासले यो सरकारलाई धारा ७६ (१) भनेको छ । त्यही सर्वोच्चको दुईजना न्यायाधीशको बेञ्चले ७६(२)को भन्यो ।’',
            'डिजाइन अर्को तिर गयो । सर्वोच्च अदालत संवैधानिक इजलास यो सरकार लाई धारा N (N) भने छ । त्यही सर्वोच्च दुईजना न्यायाधीश बेञ्च N(N) भन्यो ।’ '.split()
        ),
        (
            'एक सातासम्म चल्ने तालिममा प्रदेशका आठै जिल्लाका अभियन्ताको सहभागिता रहेको छ ।',
            'एक साता सम्म चल्ने तालिम प्रदेश आठै जिल्ला अभियन्ता सहभागिता रहे छ ।'.split()
        ),
        ('मुखियाहरू', ['मुखिया']),
        ('सफाइकर्मीहरू', ['सफाइकर्मी']),
        ('कोरियाबीच', ['कोरिया', 'बीच']),
        ('विद्यालयसहित', ['विद्यालय', 'सहित']),
        ('निषेधाज्ञाभर', ['निषेधाज्ञा', 'भर']),
        ('लेखनीबारे', ['लेखनी', 'बारे']),
        ('लेखनीबारेमा', ['लेखनी', 'बारे']),
        ('जेलखानाअघि', ['जेलखाना', 'अघि']),
        ('तथ्याकंहरू', ['तथ्याकं']),
        ('ढोकाबाहिरै', ['ढोका', 'बाहिर']),
        ('चितवनकाे', ['चितवन']),
        ('सहायताअन्तर्गत', ['सहायता', 'अन्तर्गत']),
        ('समयअघिमात्र', ['समय', 'अघि', 'मात्र']),
        ('घरप्रति', ['घर', 'प्रति']),
        ('उपाध्यायकहाँ', ['उपाध्याय', 'कहाँ']),
        ('भरियामात्रै', ['भरिया', 'मात्र']),
        ('दूतावासवीच', ['दूतावास', 'बीच']),
        ('अवधिसंगै', ['अवधि', 'सँग']),
        ('प्रधानमन्त्रीमात्र', ['प्रधानमन्त्री', 'मात्र']),
        ('सफाइप्रति', ['सफाइ', 'प्रति']),
        ('सन १९९० देखि', ['सन', 'N', 'देखि']),
    ]
    for s, exp in strs_expected:
        assert process_suffixes(suffixes, s.split()) == exp


def test_remove_punctuation():
    strs_expected = [
        ('…प्रमुख', 'प्रमुख'),
    ]
    for s, exp in strs_expected:
        assert remove_punctuation(s) == exp