import os
import re



# правильная форма из двух слов: отдельная строка на слово или два слова через пробел

# тятя@ц [: кота] [: кот] [*]  --> тятя@ц \t кота, кот
# : и :: без *
# тятя@ц [: кота] [:: кот] и тятя@ц [: кота] [:: кот] без *
# ры(б)ка [: рыбку] [*]

# оши(бка) --> оши ошибка

counter = 0
dict_id = {}
speaker_id = str()
mis = r'[A-ЯЁа-яё@\(\)-]+\s\[:+\s[A-ЯЁа-яё@\(\)-]+\s*[A-ЯЁа-яё\-]+\](\s[:+\s[A-ЯЁа-яё@\(\)-]+\s*[A-ЯЁа-яё\-]+\])*\s*(\[\*\])*' # шаблон для поиска 4 случаев  # рабочая
# mis = r'[A-ЯЁа-яё@\(\)-]+\s\[:|::\s[A-ЯЁа-яё@\(\)-]+(\s[A-ЯЁа-яё@\(\)-]+\])*(\s\[\*\])*'
not_mis = r'[A-ЯЁа-яё\-]+\([A-ЯЁа-яё\-]+\)[A-ЯЁа-яё\-]+\s[^\[]' # оши(бка) --> оши ошибка без правильной формы в скобках, ее нужно вытаскивать вручную, убирая скобки. после пробела в конце не должно быть квадратной скобки

pat_corr_w = r'\[:|::\s[A-ЯЁа-яё@\(\)-]+\s*[A-ЯЁа-яё@\(\)-]*\]' # нерабочая # правильная форма в скобках


# two_mis = r'[A-ЯЁа-яё@\(\)-]+\s\[:|::\s[A-ЯЁа-яё@\(\)-]+\s*[A-ЯЁа-яё@\(\)-]*\]\s\[:|::\s[A-ЯЁа-яё@\(\)-]+\s*[A-ЯЁа-яё@\(\)-]*\](\[\*\])*' # ошибки из двух слов # нерабочая
pat_age = r'\d+?;\d{2}\.\d{2}' # возраст
pat_speaker = r'|[A-Z]{3}|'
# pat_id = r'.+?\|ruslan-m\|(.+?)\|' # ID # после ID \t всегда будет верный ID?
# pat_speech = r'(.+?)\s(\.|\!|\?)' нигде не используется  # для чего?
pat_end_speech = r'\s.{1}\d+_\d+.{1}' # пробел, NAK, цифры, NAK, перенос строки
add = ''
files_li = os.listdir(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y_translitted')  # папка с файлами .cha
if not os.path.isdir(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y-translitted'):  # папка с файлами .cha
    os.mkdir(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y_translitted')  # папка с файлами .cha
with open(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y_mistakes-add.tsv', 'w',
          encoding='utf-8') as f_mis:  # док записи
    f_mis.write(f'{'Название файла-источника'}\t{'Возраст ребенка'}\t{'ID говорящего'}\t{'Реплика'}\t{'Слово-ошибка'}\t{'Правильная форма'}\n')
    for f in files_li:
        file_name = f  # имя файла
        if '.cha' in f:
            read_f_path = os.path.join(r'C:\Users\biksh\OneDrive\Documents\PyCharm\Errors\pythonProject\Y_translitted', f)
            with open(read_f_path, 'r', encoding='utf-8') as current_file:
                for line in current_file:
                    if line.startswith('@ID:'):
                        id_ = line.replace('@ID:\t', '') # оставляем только ID
                        dict_id[re.findall(pat_speaker, id_)[0]] = id_   # ключ -- найденные три буквы говорящего, значение - ID
                        list_age = re.findall(pat_age, line)
                        if list_age: # если в строке есть возраст ребенка
                            ch_age = list_age[0]  # возраст ребёнка
                    elif line.startswith('*'):
                        speaker = line[1:5].replace(':', '').replace(' ', '')  # три буквы-название говорящего
                        speaker_id = dict_id[speaker]  # ID говорящего
                        speech = str(line[5:])
                        if re.search(pat_end_speech, speech):
                            end_ = re.findall(pat_end_speech, speech)[0]
                            speech_cleaned = speech.replace(end_, '')
                            add = ''
                        else:
                            speech_cleaned = speech
                            add = speech.replace('\r\n', '')
                    else:
                        speech = add + str(line)
                        if re.search(pat_end_speech, speech):
                            end_ = re.findall(pat_end_speech, speech)[0]
                            # print('end', end_)
                            speech_cleaned = speech.replace(end_, '')
                            add = ''
                        else:
                            speech_cleaned = speech
                            add = speech.replace('\r\n', '')

                    if re.search(mis, speech_cleaned):  # если после ошибочной дана правильная форма в квадратных скобках
                        speech_cleaned = speech_cleaned.strip()
                        for one_word in re.findall(mis, speech_cleaned):  # для каждого найденного фрагмента с ошибками:
                            mis_w = one_word[0] # слово с ошибкой
                            corr_w = re.findall(pat_corr_w, one_word)[0] # правильная форма в скобках
                            corr_w = re.sub(r'[\[\s\]:]', '', corr_w) # очищение от скобок и пробела
                            if len(re.findall(pat_corr_w, one_word)) == 2:  # если два варианта правильной формы : тятя@ц [: кота] [: кот] [*]
                                corr_ww = re.findall(pat_corr_w, one_word)[1] # второй элемент из списка совпадений по шаблону: адём [: отдай дом] [*]
                                corr_ww = re.sub(r'[\[\s\]:]', '', corr_ww) # очищение его от скобок
                                corr_w = corr_w + ', ' + corr_ww  # две возможные верные формы в одной ячейке через запятую

                            mis_w = re.sub(r'\([А-ЯЁа-яё]+\)', '', mis_w) # ошибочная или оборванная форма, если есть скобки


                            f_mis.write(
                                f'{file_name}\t{ch_age}\t{speaker_id}\t{re.sub(r'@[а-я]+|\(|\)', '', speech_cleaned)}\t{mis_w}\t{corr_w}\n')

                    if re.search(not_mis, speech_cleaned): # если не дано правильной формы, в ошибочной пропущена часть слова в круглых скобках
                        speech_cleaned = speech_cleaned.strip()
                        for one_word in re.findall(not_mis, speech_cleaned):
                            mis_w = one_word[0]
                            corr_w = re.sub(r'\([A-ЯЁа-яё\-]+\)', '', mis_w) # убираем все, что в скобках
                            f_mis.write(
                                f'{file_name}\t{ch_age}\t{speaker_id}\t{re.sub(r'@[а-я]+|\(|\)', '', speech_cleaned)}\t{mis_w}\t{corr_w}\n')





                            # реплика в формате, как в таблицах с морфологической разметкой(Ruslan..):
                            # удалены скобки, @...
                    # if re.search(two_mis, speech_cleaned):  # правильная форма из двух слов
                    #     # print(speech_cleaned)
                    #     for one_word in re.findall(two_mis, speech_cleaned):
                    #         one_word = list(one_word.split())
                    #         mis_w = one_word[0]
                    #         f_mis.write(
                    #             f'{file_name}\t{ch_age}\t{speaker_id}\t{re.sub(r'@[а-я]+|\(|\)', '', speech_cleaned)}\t{mis_w}\t{one_word[2]}\n')
                    #         f_mis.write(
                    #             f'{file_name}\t{ch_age}\t{speaker_id}\t{re.sub(r'@[а-я]+|\(|\)', '', speech_cleaned)}\t{mis_w}\t{one_word[3].rstrip(']')}\n')

# print(counter)
