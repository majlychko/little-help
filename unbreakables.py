import json
import re

def replace_space(text):
    # ищем слова из 1 или 2 символов за которыми пробел рег выражением,
    pattern = r'(\b\w{1,2}\b) '
    result = re.sub(pattern, r'\1\\u00A0', text)
    
    # ниже всякие палочки 
    # Заменяем пробелы на неразрывные, если после пробела идет длинное тире
    result = re.sub(r' —', r'\\u00A0—', result)
    # Заменяем пробелы на неразрывные, если после пробела идет тире со стрелочкой
    result = re.sub(r' →', r'\\u00A0→', result)
    # Заменяем короткое тире на неразнывное
    result = re.sub(r'-', r'\\u2011', result)

    #ниже идут валюты и цифры и все что с ними связано
    # Заменяем пробелы на неразрывные, до знака рубль
    result = re.sub(r' ₽', r'\\u00A0₽', result)
    # Заменяем пробелы на неразрывные, до слова рублей
    result = re.sub(r' рублей', r'\\u00A0рублей', result)
    # Заменяем пробелы на неразрывные, до знака доллар
    result = re.sub(r' $', r'\\u00A0$', result)
    # Заменяем пробелы на неразрывные, до знака евро
    result = re.sub(r' €', r'\\u00A0€', result)
    # Заменяем пробелы на неразрывные, до знака  юань
    result = re.sub(r' ¥', r'\\u00A0¥', result)
    # Заменяем пробелы на неразрывные, до 000 
    result = re.sub(r' 000', r'\\u00A0000', result)
    # Заменяем пробелы на неразрывные, до тыс
    result = re.sub(r' тыс', r'\\u00A0тыс', result)
    # Заменяем пробелы на неразрывные, до млн
    result = re.sub(r' млн', r'\\u00A0млн', result)
    # Заменяем пробелы на неразрывные, до млрд 
    result = re.sub(r' млрд', r'\\u00A0млрд', result)

    # Заменяем т-ж на т-ж с неразрывными пробелами нулевой ширины
    result = re.sub(r'Т—Ж', r'Т\\u2060—\\u2060Ж', result)

    # продукты тинька, редактор сказал ставить в них неразрывники
    result = re.sub(r'Tinkoff ', r'Tinkoff\\u00A0', result)
    result = re.sub(r'Тинькофф ', r'Тинькофф\\u00A0', result)
    result = re.sub(r'ALL ', r'ALL\\u00A0', result)

    return result

# при помощи рекурсии в которой находим с json файле ключи, в которых необходимо заменить пробелы
def replace_text_by_tag(json_obj):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if key == 'text_with_tags' or key == 'name' or key == 'subtitle' or key == 'alternative_title':
                json_obj[key] = replace_space(value)
            else:
                replace_text_by_tag(value)
    elif isinstance(json_obj, list):
        for item in json_obj:
            replace_text_by_tag(item)

# загружаем json файл
with open('story.json', 'r') as json_file:
    data = json.load(json_file)

# вызываем функцию для замены значений тегов text_with_tags и name (печенька) + subtitlе (перслента) + alternative_title (перслента заг)
replace_text_by_tag(data)

# сохраняем измененные данные json в новый файл
with open('updated_story.json', 'w') as updated_file:
    json.dump(data, updated_file, ensure_ascii=False, indent=4)
