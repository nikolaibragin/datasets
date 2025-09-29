import json
from datetime import datetime
from pathlib import Path
import sys


REPORT_BASENAME = 'comparison_report'
# --------------------


def find_common_keys_and_analyze_lists(file1, file2, report_file_path):

    print(f"\nНачинаю сравнение файлов '{file1.name}' и '{file2.name}'...")
    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            data1 = json.load(f1)
        with open(file2, 'r', encoding='utf-8') as f2:
            data2 = json.load(f2)
    except FileNotFoundError as e:
        error_message = f"ОШИБКА: Файл не найден - {e.filename}"
        print(error_message)
        return
    except json.JSONDecodeError as e:
        error_message = f"ОШИБКА: Неверный формат JSON в файле. {e}"
        print(error_message)
        return


    with open(report_file_path, 'w', encoding='utf-8') as report:
        report_header = (
            f"Отчет об анализе списков по общим ключам\n"
            f"===========================================\n"
            f"Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Файл 1: {file1.name}\n"
            f"Файл 2: {file2.name}\n"
            f"===========================================\n\n"
        )
        report.write(report_header)

        common_keys = set(data1.keys()) & set(data2.keys())

        if not common_keys:
            message = "Общие ключи не найдены."
            print(message)
            report.write(message + '\n')
            return

        result_header = f"Анализ для {len(common_keys)} общих ключей:\n"
        print(result_header.strip())
        report.write(result_header)

        for key in sorted(list(common_keys)):
            set1 = set(data1.get(key, []))
            set2 = set(data2.get(key, []))

            intersection = sorted(list(set1 & set2))
            uniques_in_file1 = sorted(list(set1 - set2))
            uniques_in_file2 = sorted(list(set2 - set1))
            union_set = set1 | set2

            if not union_set:
                percentage = 100.0
            else:
                percentage = (len(intersection) / len(union_set)) * 100

            output_block = (
                f"----------------------------------------\n"
                f"Ключ: {key}\n"
                f"----------------------------------------\n"
                f"  [+] Пересечение ({len(intersection)} эл.): {intersection if intersection else '[]'}\n"
                f"  [1] Только в '{file1.name}' ({len(uniques_in_file1)} эл.): {uniques_in_file1 if uniques_in_file1 else '[]'}\n"
                f"  [2] Только в '{file2.name}' ({len(uniques_in_file2)} эл.): {uniques_in_file2 if uniques_in_file2 else '[]'}\n"
                f"  [%] Процент пересечения: {percentage:.2f}%\n"
            )
            print(output_block)
            report.write(output_block + "\n")



def main():

    current_directory = Path('.')
    json_files = list(current_directory.glob('*.json'))

    if len(json_files) < 2:
        print(f"ОШИБКА: Найдено меньше двух JSON-файлов ({len(json_files)} шт.).")
        print("Для работы программы необходимо ровно два файла с расширением .json.")
        sys.exit(1)

    if len(json_files) > 2:
        print(f"ОШИБКА: Найдено больше двух JSON-файлов ({len(json_files)} шт.):")
        for f in json_files:
            print(f" - {f.name}")
        print("\nПожалуйста, оставьте в папке только те два файла, которые нужно сравнить.")
        sys.exit(1)

    file1, file2 = json_files[0], json_files[1]
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_filename = f"{REPORT_BASENAME}_{timestamp}.txt"
    # -----------------------------------

    find_common_keys_and_analyze_lists(file1, file2, report_filename)

    print(f"\n Анализ завершен. Подробный отчет сохранен в файл: {report_filename}")


if __name__ == "__main__":

    main()
