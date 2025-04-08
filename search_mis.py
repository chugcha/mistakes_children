import os
import re
from string import punctuation
import json

counter = 0
pattern = r'([А-ЯЁа-яё-]+?)\s\[\:\s([А-ЯЁа-яё-]+?)\]\s\[\*\]'
files_li = os.listdir(r'ПУТЬ К ПАПКЕ С ФАЙЛАМИ (всеми)')
if not os.path.isdir(r'ПУТЬ К ПАПКЕ С ФАЙЛАМИ (всеми)'):
    os.mkdir(r'ПУТЬ К ПАПКЕ С ФАЙЛАМИ (всеми)')
with open(r'ПУТЬ К ФАЙЛУ, В КОТОРЫЙ БУДЕМ ЗАПИСЫВАТЬ', 'w', encoding='utf-8') as f_mis:
    for f in files_li:
        if '.cha' in f:
            read_f_path = os.path.join(r'ПУТЬ К ПАПКЕ С ФАЙЛАМИ (всеми)', f)
            with open(read_f_path, 'r', encoding='utf-8') as curr_f:
                for line in curr_f:
                    if line.startswith('*'):
                        speaker = line[1:4]
                        speech = str(line[5:])
                        if re.search(pattern, speech):
                            for one_word in re.findall(pattern, speech):
                                counter+=1
                                print(f'{speaker},{one_word[0]},{one_word[1]}\n')
                                f_mis.write(f'{speaker},{one_word[0]},{one_word[1]}\n')
print(counter)
