import json
import re

#+ обязательно нужно учитывать, что у нас бывают подстановки, те если слова написаны в фигурных скобка {{XXX}}, в них ничего на неразрывники не должно меняться
def replace_space(text):
    # используем регулярное выражение для поиска слов из 1 или 2 символов,
    pattern = r'(\b\w{1,2}\b) '
    result = re.sub(pattern, r'\1\\u00A0', text)
    # тут есть исключение, слова "бы" "ли" "же" не должен быть неразрывник вместо пробела после, а только перед частицей: если" неразрывник "бы" обычный пробел
    
    # Заменяем пробелы на неразрывные, если после пробела идет длинное тире
    result = re.sub(r' —', r'\\u00A0—', result)

    # Заменяем пробелы на неразрывные, до год*
    result = re.sub(r' год', r'\\u00A0год', result)

    # Заменяем т тире ж на т-ж с неразрывными пробелами нулевой ширины
    result = re.sub(r'Т—Ж', r'Т\\u2060—\\u2060Ж', result)
    # лучше думаю смотреть есть ли пробел до и после тире, и если пробела нет, то вокруг нужно поставить пробелы нулевой ширины (потому что бывают кейсы с диапазонами 20 000—40 000 ₽, XIX—XX века ну и тж, но в целом везде где тире без пробелов предполагается неразрывник (или бывает неразрывное тире, не нашла))

    # Заменяем пробелы на неразрывные, если после пробела идет тире со стрелочкой
    result = re.sub(r' →', r'\\u00A0→', result)

    #ниже идут валюты и цифры
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
    result = re.sub(r' 000', r'\\u00A0000', result) #тут в идеале должны любые цифры находиться, но чаще всего числа с нулями (да вообще все равно сколько разрядов с нулями)
    # Заменяем пробелы на неразрывные, до тыс
    result = re.sub(r' тыс', r'\\u00A0тыс', result)
    # Заменяем пробелы на неразрывные, до млн
    result = re.sub(r' млн', r'\\u00A0млн', result)
    # Заменяем пробелы на неразрывные, до млрд 
    result = re.sub(r' млрд', r'\\u00A0млрд', result)

    # Заменяем дефис на неразрывний дефис
    result = re.sub(r'-', r'\\u2011', result)

    #ниже идут продукты тинька
    #увы не можем просто после слова тинькофф ставить неразрывник, ибо оно не всегда с продутом идет
    #result = re.sub(r'Tinkoff ', r'Tinkoff\\u00A0', result)
    #result = re.sub(r'Тинькофф ', r'Тинькофф\\u00A0', result)
    result = re.sub(r'ALL ', r'ALL\\u00A0', result)

    # Заменяем Tinkoff Pro на Tinkoff неразрывник Pro
    result = re.sub(r'Tinkoff Pro', r'Tinkoff\\u00A0Pro', result)
    # Заменяем Tinkoff Premium на Tinkoff неразрывник Premium
    result = re.sub(r'Tinkoff Premium', r'Tinkoff\\u00A0Premium', result)
    # Заменяем Tinkoff Private на Tinkoff неразрывник Private
    result = re.sub(r'Tinkoff Private', r'Tinkoff\\u00A0Private', result)
    # Заменяем Tinkoff Black на Tinkoff неразрывник Black
    result = re.sub(r'Tinkoff Black', r'Tinkoff\\u00A0Black', result)
    # Заменяем Tinkoff ID на Tinkoff неразрывник ID
    result = re.sub(r'Tinkoff ID', r'Tinkoff\\u00A0ID', result)
    # Заменяем Tinkoff Pay на Tinkoff неразрывник Pay
    result = re.sub(r'Tinkoff Pay', r'Tinkoff\\u00A0Pay', result)
    # Заменяем Тинькофф Платинум на Тинькофф неразрывник Платинум
    result = re.sub(r'Тинькофф Платинум', r'Тинькофф\\u00A0Платинум', result)
    # Заменяем Тинькофф Сторис на Тинькофф неразрывник Сторис
    result = re.sub(r'Тинькофф Сторис', r'Тинькофф\\u00A0Сторис', result)
    # Заменяем Тинькофф Страхование на Тинькофф неразрывник Страхование
    result = re.sub(r'Тинькофф Страхование', r'Тинькофф\\u00A0Страхование', result)
    # Заменяем Тинькофф Бизнес на Тинькофф неразрывник Бизнес
    result = re.sub(r'Тинькофф Бизнес', r'Тинькофф\\u00A0Бизнес', result)
    # Заменяем Тинькофф Путешествия на Тинькофф неразрывник Путешествия
    result = re.sub(r'Тинькофф Путешествия', r'Тинькофф\\u00A0Путешествия', result)
    # Заменяем Тинькофф Квест на Тинькофф неразрывник Квест
    result = re.sub(r'Тинькофф Квест', r'Тинькофф\\u00A0Квест', result)
    # Заменяем Тинькофф Банк на Тинькофф неразрывник Банк
    result = re.sub(r'Тинькофф Банк', r'Тинькофф\\u00A0Банк', result)
    # Заменяем Тинькофф Мобайл на Тинькофф неразрывник Мобайл
    result = re.sub(r'Тинькофф Мобайл', r'Тинькофф\\u00A0Мобайл', result)
    # Заменяем Тинькофф Инвестиции на Тинькофф неразрывник Инвестиции
    result = re.sub(r'Тинькофф Инвестиции', r'Тинькофф\\u00A0Инвестиции', result)
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


# сохраняем измененные данные json в старый файл файл
with open('story.json', 'w') as updated_file:
    json.dump(data, updated_file, ensure_ascii=False, indent=4)

#я так и не разобралась, как нормально это реализовать и почему у меня лишний слеш берется, поэтому пока так
def replace_backslashes(text):
    # Заменяем двойной обратный слеш на одиночный обратный слеш
    result = text.replace('\\\\', '\\')
    return result

# загружаем json файл
with open('story.json', 'r') as json_file:
    data = json.load(json_file)

# выполняем замену двойного обратного слеша на одинарный обратный слеш
json_str = json.dumps(data, ensure_ascii=False, indent=4)
updated_json_str = replace_backslashes(json_str)

# сохраняем измененные данные в новый файл
with open('updated_story.json', 'w') as updated_file:
    updated_file.write(updated_json_str)
