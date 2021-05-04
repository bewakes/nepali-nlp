import os
from typing import Dict


Mappings = Dict[str, str]

numbers: Mappings = {
   '0': '०',
   '1': '१',
   '2': '२',
   '3': '३',
   '4': '४',
   '5': '५',
   '6': '६',
   '7': '७',
   '8': '८',
   '9': '९'
}

basic_vowels: Mappings = {
    'a': 'अ',
    'aa': 'आ',
    'ee': 'ई ',
    'i': 'इ',
    'u': 'उ',
    'oo': 'ऊ',
    'Ri': 'ॠ ',
    'Ree': 'ॠ',
    'e': 'ए',
    'ai': 'ऐ',
    'o': 'ओ',
}

consonant_kaars: Mappings = {
    'aa': 'ा',
    'e': 'े',
    'ee': 'ी',
    'i': 'ि',
    'u': 'ु',
    'oo': 'ू',
    'o': 'ो',
    'au': 'ौ',
    'ai': 'ै'
}

akaars: Mappings = {
    'ka': 'क',
    'kha': 'ख',
    'ga': 'ग',
    'gha': 'घ',
    'Nga': 'ङ',
    'NGa': 'ङ्ग',
    'cha': 'च',
    'chha': 'छ',
    'ja': 'ज',
    'jha': 'झ',
    'yNa': 'ञ',
    'Ta': 'ट',
    'Tha': 'ठ',
    'Da': 'ड',
    'Dha': 'ढ',
    'Na': 'ण',
    'ta': 'त',
    'tha': 'थ',
    'da': 'द',
    'dha': 'ध',
    'na': 'न',
    'nga': 'ङ',
    'pa': 'प',
    'pha': 'फ',
    'fa': 'फ',
    'ba': 'ब',
    'bha': 'भ',
    'va': 'भ',
    'ma': 'म',
    'ya': 'य',
    'ra': 'र',
    'la': 'ल',
    'wa': 'व',
    'sa': 'स',
    'sha': 'श',
    'Sha': 'ष',
    'ha': 'ह',
    'ksha': 'क्ष',
    'tra': 'त्र',
    'gya': 'ज्ञ',
    'gYa': 'ग्य',
}

halanta = '्'
amkaar = 'ं'
aNNkaar = 'ँ'
Ri = 'ृ'
