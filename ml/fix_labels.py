import numpy as np
import re
import json


def extract_number(label):
    """Извлекает целое число из строки любого вида"""
    match = re.search(r'\d+', str(label))
    if match:
        return int(match.group())
    raise ValueError(f"Не удалось извлечь число из метки: {label}")


def fix_labels(labels):
    """
    Принимает массив повреждённых строковых меток.
    Возвращает массив int, переиндексированный с 0.
    Также возвращает словарь маппинга {новый_индекс: имя_класса}.
    """
    numbers = [extract_number(l) for l in labels]
    unique_sorted = sorted(set(numbers))
    remap = {old: new for new, old in enumerate(unique_sorted)}
    fixed = np.array([remap[n] for n in numbers], dtype=np.int32)
    label_map = {new: f"class_{old}" for old, new in remap.items()}
    return fixed, label_map


if __name__ == '__main__':
    data = np.load('data/train.npz', allow_pickle=True)
    train_y = data['train_y']
    valid_y = data['valid_y']

    train_y_fixed, label_map = fix_labels(train_y)
    valid_y_fixed, _ = fix_labels(valid_y)

    print(f"Классов всего: {len(label_map)}")
    print(f"Пример: {list(label_map.items())[:5]}")

    np.savez('data/train_fixed.npz',
             train_x=data['train_x'],
             train_y=train_y_fixed,
             valid_x=data['valid_x'],
             valid_y=valid_y_fixed)

    with open('ml/label_map.json', 'w') as f:
        json.dump(label_map, f, ensure_ascii=False, indent=2)

    print("Готово. Сохранено в data/train_fixed.npz и ml/label_map.json")
