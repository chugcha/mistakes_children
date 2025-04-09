import os
import re
from string import punctuation
import json

counter = 0
dict_id = {}
speaker_id = str()
pattern = r'([A-ЯЁа-яё@\(\)-]+?)\s\[\:\s([A-ЯЁа-яё@\(\)-]+?)\]\s\[\*\]'
pat_age = r'\d+?;\d{2}\.\d{2}'
pat_part = r'.+?\|ruslan-m\|(.+?)\|'
pat_speech = r'(.+?)\s(\.|\!|\?)'
files_li = os.listdir(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y_translitted')  # папка с файлами .cha
if not os.path.isdir(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y_translitted'):  # папка с файлами .cha
    os.mkdir(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y_translitted')  # папка с файлами .cha
with open(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\mistakes.tsv', 'w',
          encoding='utf-8') as f_mis:  # док записи
    f_mis.write(f'{'Название файла-источника'}\t {'Возраст ребенка'}\t {'ID говорящего'}\t "{'Реплика'}"\t {'Слово-ошибка'}\t {'Правильная форма'}\n')
    for f in files_li:
        file_name = f  # имя файла
        if '.cha' in f:
            read_f_path = os.path.join(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y_translitted', f)
            with open(read_f_path, 'r', encoding='utf-8') as curr_f:
                for line in curr_f:
                    if line.startswith('@ID:'):
                        act_id = line.replace('@ID:\t', '')
                        dict_id[re.findall(pat_part, act_id)[0]] = act_id
                        list_age = re.findall(pat_age, line)
                        if list_age:
                            ch_age = list_age[0]  # предположительно, возраст ребёнка
                    if line.startswith('*'):
                        speaker = line[1:5].replace(':', '').replace(' ', '')
                        speaker_id = dict_id[speaker].strip()  # ID говорящего
                        speech = str(line[5:])
                        if '.' in speech:
                            speech_cleaned = speech[1:speech.find('.') + 1]
                        elif '?' in speech:
                            speech_cleaned = speech[1:speech.find('?') + 1]
                        elif '!' in speech:
                            speech_cleaned = speech[1:speech.find('!') + 1]  # остаток строки без цифр
                            speech_cleaned = speech_cleaned.strip()
                        if re.search(pattern, speech_cleaned):
                            for one_word in re.findall(pattern, speech_cleaned):
                                counter += 1  # подсчёт ошибок, вдруг пригодится
                                mis_w = one_word[0]  # слово с ошибкой
                                corr_w = one_word[1]  # исправленное слово
                                # print(f'{file_name}: {ch_age}, {speaker_id}, "{speech_cleaned}", {mis_w} -> {corr_w}')
                                f_mis.write(
                                    f'{file_name}\t {ch_age}\t {speaker_id}\t "{speech_cleaned}"\t {mis_w}\t {corr_w}\n')
# print(counter)
