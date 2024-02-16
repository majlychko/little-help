import json

def recursive_change(obj, is_name_found=False, is_TSN_found=False):
    if isinstance(obj, dict):
        for key, value in obj.items():
            #находим отступ 20 снизу (есть вопросы)
            if key == "bottom" and value == 20:
                obj[key] = 0
            #выключаем комментарии и возможность найти в поиске
            elif key in ["searchable", "is_commentable"]:
                obj[key] = False
            #добавляем тег fullscreen
            elif key == "tags" and isinstance(value, list):
                value.append("fullscreen")
            elif isinstance(value, (dict, list)):
                recursive_change(value, is_name_found, is_TSN_found)
                #ищем в ключе name задачку МБ, джунов или инвеста, добавляем слово фуллскрин
            elif key == "name" and isinstance(value, str):
                if not is_name_found:
                    index_TSN = value.find("(TSN")
                    index_INVMC = value.find("INVMC")
                    if index_TSN != -1:
                        obj[key] = value[:index_TSN] + "(фуллскрин) " + value[index_TSN:]
                        is_name_found = True #я запуталась, но вроде работает
                        is_TSN_found = True
                    elif index_INVMC != -1 and not is_TSN_found:
                        obj[key] = value[:index_INVMC] + "(фуллскрин) " + value[index_INVMC:]
                        is_name_found = True
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                recursive_change(item, is_name_found, is_TSN_found)

with open('updated_story.json', 'r') as json_file:
    data = json.load(json_file)

recursive_change(data)

with open('updated_story.json', 'w', encoding='utf-8') as updated_file:
    json.dump(data, updated_file, indent=4, ensure_ascii=False)
