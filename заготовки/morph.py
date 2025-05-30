import csv
import re
out = []
morpho_list = []
verbs_list = []
out_v = []
with open('T_mistakes.tsv', 'r', encoding='utf-8') as f:
    mistakes = csv.reader(f, delimiter='\t')
    with open('RusLan-M_Tosya_nouns.tsv', 'r', encoding='utf-8') as m:
        morpho = csv.reader(m, delimiter='\t')
        for j in morpho: # создание списка строк по которому проходить несколько раз(по каждой строке)
            morpho_list.append(j)
        for mistake in mistakes:
            error = re.sub(r'@[а-я]+|\(|\)', '', mistake[4])
            phrase = mistake[3]
            # print(phrase)
            for i in range(len(morpho_list)):
                error_morph = morpho_list[i][2]
                phrase_morph = morpho_list[i][4]
                if mistake[0] == morpho_list[i][0] and error == error_morph and phrase == phrase_morph:
                    lemma = morpho_list[i][3]
                    grammar = morpho_list[i][-1]
                    line_out = mistake

                    if line_out not in out:
                        line_out.append(lemma) # в строку из файла mistakes.tsv добавляются столбцы с морф.разбором
                        line_out.append(grammar)
                        out.append(line_out)
                        # print(line_out)

with open('T_mistakes.tsv', 'r', encoding='utf-8') as f:
    mistakes = csv.reader(f, delimiter='\t')
    with open('RusLan-M_Tosya_verbs.tsv', 'r', encoding='utf-8') as v:
        verbs = csv.reader(v, delimiter='\t')
        for j in verbs:  # создание списка строк по которому проходить несколько раз(по каждой строке)
            verbs_list.append(j)
        for mistake in mistakes:
            error = re.sub(r'@[а-я]+|\(|\)', '', mistake[4])
            phrase = mistake[3]
            # print(phrase)
            for i in range(len(verbs_list)):
                error_verb = verbs_list[i][2]
                phrase_verb = verbs_list[i][4]
                if mistake[0] == verbs_list[i][0] and error == error_verb and phrase == phrase_verb:
                    lemma = verbs_list[i][3]
                    grammar = verbs_list[i][-1]
                    line_out = mistake
                    if line_out not in out_v:
                        line_out.append(lemma)  # в строку из файла mistakes.tsv добавляются столбцы с морф.разбором
                        line_out.append(grammar)
                        out_v.append(line_out)
                        # print(line_out)

with open('T_morph.tsv', 'w', encoding='utf-8', newline='') as f_tsv:
    writer = csv.writer(f_tsv, delimiter='\t')
    writer.writerow(['Название файла-источника', 'Возраст ребенка', 'ID говорящего', 'Реплика', 'Слово-ошибка', 'Правильная форма', 'Лемма', 'Морфологический разбор'])
    for line_out in out:
        writer.writerow(line_out)
    for line_out in out_v:
        writer.writerow(line_out)
