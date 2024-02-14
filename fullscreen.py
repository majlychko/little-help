import json

def recursive_change(obj, is_name_found=False):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "bottom" and value == 20:
                obj[key] = 0
            elif key in ["searchable", "is_commentable"]:
                obj[key] = False
            elif key == "tags" and isinstance(value, list):
                value.append("fullscreen")
            elif isinstance(value, (dict, list)):
                recursive_change(value, is_name_found)
            elif key == "name" and isinstance(value, str):
                if not is_name_found:
                    index = value.find("(TSN")
                    if index != -1:
                        obj[key] = value[:index] + "(фуллскрин) " + value[index:]                
                    is_name_found = True
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                recursive_change(item, is_name_found)

with open('updated_story.json', 'r') as json_file:
    data = json.load(json_file)

recursive_change(data)

with open('updated_story.json', 'w', encoding='utf-8') as updated_file:
    json.dump(data, updated_file, indent=4, ensure_ascii=False)
