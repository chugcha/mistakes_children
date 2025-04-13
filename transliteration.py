import os
import re
from transliterate import translit
from string import punctuation

import json
# end_phrase = r'\d[^\d]{1}\r\n'
# end_phrase = r'\d'
def transliterate(latin_text):
    latin_text = latin_text.replace('tsja','тся')
    latin_text = latin_text.replace('s(hch)','щ')
    latin_text = latin_text.replace('shch','щ')
    latin_text = latin_text.replace('jo','ё')
    latin_text = latin_text.replace('zh','ж')
    latin_text = latin_text.replace('ts','ц')
    latin_text = latin_text.replace('s(h)','ш')
    latin_text = latin_text.replace('ch','ч')
    latin_text = latin_text.replace('sh','ш')
    latin_text = latin_text.replace('^','ъ')
    latin_text = latin_text.replace("'",'ь')
    latin_text = latin_text.replace('ju','ю')
    latin_text = latin_text.replace('ja','я')
    latin_text = latin_text.replace('æ','э')
    latin_text = latin_text.replace('x','x')
    cyrillik_text = translit(latin_text, 'ru')
    return cyrillik_text

# print(os.path.dirname('T_test'))
files_li = os.listdir('Yasha_transcripts')
print(files_li)

# from google.colab import drive
# drive.mount('/content/drive')

if not os.path.isdir('Y_translitted'):
    os.mkdir('Y_translitted')
for f in files_li:
    if '.cha' in f:
        new_f_name = 'Y_translitted\\' + f
        nf = 'Yasha_transcripts\\' + f
        f_el = open(nf, 'r', encoding = 'utf-8')
        new_f = open(new_f_name, 'w', encoding = 'utf-8')
        for line in f_el:
            if line.startswith('*'):
                speaker = line[:5]
                part_to_trans = str(line[5:])
                traslitted = transliterate(part_to_trans)
                new_line = speaker + traslitted
                print(new_line.strip(), file=new_f)
            elif line.startswith('\t'):
                part_to_trans = str(line)
                traslitted = transliterate(part_to_trans)
                new_line = traslitted
                print(new_line.strip(), file=new_f)
                # if re.findall(end_phrase, line):
                #     end_translit = str(re.findall(end_phrase, line)[0])
                #     # print(end_translit)
                #     end_line = line.find(end_translit)
                #     part_to_trans = str(line[5:end_line]) # транслитерируется все, что до первой цифры включительно
                #     # print(part_to_trans)
                #     traslitted = transliterate(part_to_trans)
                #     new_line = speaker + traslitted
                #     print(new_line.strip(), file = new_f)
            else:
                print(line.strip(), file = new_f)
        f_el.close()
        new_f.close()