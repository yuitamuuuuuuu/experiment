# -*- coding: utf-8 -*-
from psychopy import visual, core, event, gui
from psychopy.hardware import keyboard
import random
import time

# ==========================================
# СТИМУЛЫ
# ==========================================

words_red = ["корона", "развитие", "душа", "время", "друг", "стекло", "лошадь"]
words_blue = ["привычка", "камень", "лампа", "мелодия", "симпатия", "медицина", "офис"]
words_gray = ["деревня", "газета", "деньги", "ручка", "птица", "смелость", "цирк"]

conditions = [
    {"color": "#E53935", "label": "Red", "words": words_red},
    {"color": "#1E88E5", "label": "Blue", "words": words_blue},
    {"color": "#BDBDBD", "label": "Gray", "words": words_gray}
]

random.shuffle(conditions)

# ==========================================
# ИНФО ОБ УЧАСТНИКЕ
# ==========================================

exp_info = {"ID участника": ""}  # Исправленный ключ
dlg = gui.DlgFromDict(exp_info, title='Эксперимент')
if not dlg.OK:
    core.quit()

participant_id = exp_info["ID участника"]  # Теперь правильно

participant_id = exp_info["ID участника"]
group = random.choice(["A", "B"])

# ==========================================
# ФАЙЛ ДАННЫХ
# ==========================================

filename = f"results_{participant_id}.csv"
data_file = open(filename, "w", encoding="utf-8")
data_file.write("participant,group,condition,shown_words,typed_response,timestamp\n")

# ==========================================
# ОКНО
# ==========================================

win = visual.Window(fullscr=True, color="white", units="height")
text_stim = visual.TextStim(win, text="", height=0.07, color="black")
instruction = visual.TextStim(win, text="", height=0.05, color="black", wrapWidth=1.3)

# ==========================================
# СЛОВАРЬ ДЛЯ РУССКОЙ РАСКЛАДКИ
# ==========================================

# Расширенный словарь с разными вариантами имен клавиш
eng_to_rus = {
    # Основные буквы
    'a': 'ф', 'b': 'и', 'c': 'с', 'd': 'в', 'e': 'у', 'f': 'а', 'g': 'п', 'h': 'р',
    'i': 'ш', 'j': 'о', 'k': 'л', 'l': 'д', 'm': 'ь', 'n': 'т', 'o': 'щ', 'p': 'з',
    'q': 'й', 'r': 'к', 's': 'ы', 't': 'е', 'u': 'г', 'v': 'м', 'w': 'ц', 'x': 'ч',
    'y': 'н', 'z': 'я',

    # Заглавные буквы
    'A': 'Ф', 'B': 'И', 'C': 'С', 'D': 'В', 'E': 'У', 'F': 'А', 'G': 'П', 'H': 'Р',
    'I': 'Ш', 'J': 'О', 'K': 'Л', 'L': 'Д', 'M': 'Ь', 'N': 'Т', 'O': 'Щ', 'P': 'З',
    'Q': 'Й', 'R': 'К', 'S': 'Ы', 'T': 'Е', 'U': 'Г', 'V': 'М', 'W': 'Ц', 'X': 'Ч',
    'Y': 'Н', 'Z': 'Я'
}


# ==========================================
# ПРОСТОЙ И НАДЕЖНЫЙ ВВОД ТЕКСТА
# ==========================================

def get_user_input_simple():
    """
    Простой и надежный ввод русского текста через английскую раскладку
    """
    # Создаем текстовые стимулы
    instruction_text = visual.TextStim(
        win,
        text="Введите слова в том порядке, в котором они были показаны:\n(используйте пробел между словами)",
        height=0.045,
        color="black",
        pos=(0, 0.3)
    )

    input_display = visual.TextStim(
        win,
        text="",
        height=0.05,
        color="black",
        pos=(0, 0)
    )

    hint_text = visual.TextStim(
        win,
        text="Набирайте текст на английской раскладке - он автоматически переведется в русский\nEnter - завершить ввод, Backspace - удалить символ, Escape - выйти",
        height=0.03,
        color="#666666",
        pos=(0, -0.3)
    )

    current_text = []
    kb = keyboard.Keyboard()

    # Очищаем предыдущие нажатия
    kb.clearEvents()

    while True:
        # Отображаем текущий текст с курсором
        display_text = ''.join(current_text) + "_"
        input_display.text = display_text

        # Рисуем все элементы
        instruction_text.draw()
        input_display.draw()
        hint_text.draw()
        win.flip()

        # Получаем нажатия клавиш
        keys = kb.getKeys()

        for key in keys:

            if key.name == 'return':
                # Завершаем ввод
                final_text = ''.join(current_text)
                return final_text.strip()

            elif key.name == 'escape':
                core.quit()

            elif key.name == 'backspace':
                # Удаляем последний символ
                if current_text:
                    current_text.pop()

            elif key.name == 'space':
                # Добавляем пробел
                current_text.append(' ')

            elif key.name in eng_to_rus:
                # Преобразуем английскую букву в русскую
                current_text.append(eng_to_rus[key.name])

            elif key.name.isdigit():
                # Цифры оставляем как есть
                current_text.append(key.name)

            elif key.code in eng_to_rus:
                # Пробуем использовать код клавиши
                current_text.append(eng_to_rus[key.code])


# ==========================================
# АЛЬТЕРНАТИВНЫЙ ВАРИАНТ - используем event.getKeys()
# ==========================================

def get_user_input_alternative():
    """
    Альтернативный вариант ввода через event.getKeys()
    """
    instruction_text = visual.TextStim(
        win,
        text="Введите слова в том порядке, в котором они были показаны:\n(используйте пробел между словами)",
        height=0.045,
        color="black",
        pos=(0, 0.3)
    )

    input_display = visual.TextStim(
        win,
        text="",
        height=0.05,
        color="black",
        pos=(0, 0)
    )

    hint_text = visual.TextStim(
        win,
        text="Набирайте текст на английской раскладке\nEnter - завершить, Backspace - удалить, Escape - выйти",
        height=0.03,
        color="#666666",
        pos=(0, -0.3)
    )

    # Упрощенный словарь для event.getKeys()
    simple_eng_to_rus = {
        'a': 'ф', 'b': 'и', 'c': 'с', 'd': 'в', 'e': 'у', 'f': 'а', 'g': 'п', 'h': 'р',
        'i': 'ш', 'j': 'о', 'k': 'л', 'l': 'д', 'm': 'ь', 'n': 'т', 'o': 'щ', 'p': 'з',
        'q': 'й', 'r': 'к', 's': 'ы', 't': 'е', 'u': 'г', 'v': 'м', 'w': 'ц', 'x': 'ч',
        'y': 'н', 'z': 'я',
        'space': ' ', 'backspace': '[backspace]'
    }

    current_text = []

    # Очищаем буфер клавиш
    event.clearEvents()

    while True:
        # Отображаем текущий текст с курсором
        display_text = ''.join(current_text) + "_"
        input_display.text = display_text

        # Рисуем все элементы
        instruction_text.draw()
        input_display.draw()
        hint_text.draw()
        win.flip()

        # Получаем нажатия через event.getKeys()
        keys = event.getKeys()

        for key in keys:
            if key == 'return':
                return ''.join(current_text).strip()
            elif key == 'escape':
                core.quit()
            elif key == 'backspace':
                if current_text:
                    current_text.pop()
            elif key in simple_eng_to_rus:
                if key == 'backspace':
                    if current_text:
                        current_text.pop()
                elif key == 'space':
                    current_text.append(' ')
                else:
                    current_text.append(simple_eng_to_rus[key])


# ==========================================
# ФУНКЦИИ
# ==========================================

def show_text(msg):
    instruction.text = msg
    instruction.draw()
    win.flip()
    event.waitKeys()


# ==========================================
# ИНСТРУКЦИИ ПО ГРУППАМ
# ==========================================

if group == "A":
    intro = (
        "Вам будут показаны слова.\n"
        "Ваша задача — просто внимательно смотреть на них.\n"
        "Нажмите любую клавишу, чтобы начать."
    )
else:
    intro = (
        "Вам будут показаны слова.\n"
        "Ваша задача — запомнить слова, чтобы потом воспроизвести их в порядке, в котором они были вам показаны.\n\n"
        "Нажмите любую клавишу, чтобы начать."
    )

show_text(intro)

# ==========================================
# ОСНОВНОЙ ЦИКЛ
# ==========================================

for i, cond in enumerate(conditions):

    win.color = cond["color"]
    win.flip()
    core.wait(0.3)

    for w in cond["words"]:
        text_stim.text = w
        text_stim.draw()
        win.flip()
        core.wait(2.0)

        win.flip()
        core.wait(0.5)

    # ВВОД ТЕКСТА - используем альтернативный вариант
    win.color = "white"
    show_text("Теперь введите слова.\nНажмите любую клавишу, чтобы начать.")

    # Пробуем альтернативный вариант
    typed = get_user_input_alternative()
    timestamp = time.time()

    data_file.write(
        f"{participant_id},{group},{cond['label']},"
        f"{' '.join(cond['words'])},{typed},{timestamp}\n"
    )

    if i < len(conditions) - 1:
        wait_text = visual.TextStim(
            win,
            text="Пауза 30 секунд...",
            height=0.06,
            color="black"
        )
        wait_text.draw()
        win.flip()
        core.wait(30)

# ==========================================
# КОНЕЦ
# ==========================================

show_text("Эксперимент завершён.\nСпасибо за участие!")
data_file.close()
win.close()
core.quit()