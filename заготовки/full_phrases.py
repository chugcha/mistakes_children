import os
import re

phrase_break =  r'(\n)([^*@%])'

original = 'Y_translitted_original'
originals = os.listdir(original)

translitted = 'Y_translitted'
if not os.path.isdir(translitted):  # папка с файлами .cha
    os.mkdir(translitted)  # папка с файлами .cha
for f in originals:
    r_path = os.path.join(original, f)
    with open(r_path, 'r', encoding='utf-8') as orig_file:
        content_orig = orig_file.read()
        # for r in re.findall(phrase_break, content_orig, re.MULTILINE):
        #     print(r)
        # print(content_orig)
        # print(f, len(re.findall(r'^\*[A-Z]', content_orig)))
    w_path = os.path.join(translitted, f)
    with open(w_path, 'w', encoding='utf-8') as new_file:
        new_file.write(re.sub(phrase_break, r' \2', content_orig, 0, re.MULTILINE))

#






