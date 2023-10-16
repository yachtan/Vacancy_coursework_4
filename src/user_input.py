from src.api import HeadHunter_API, SuperJob_API
from src.saver import JsonSaver
from src.vacancy import Vacancy


def user():
    print('Начинаем поиск вакансий. Для выхода в любой момент, введите "0".')
    # Шаг 1. Выбираем сайт поиска.
    i = 1
    while i == 1:
        site = input('Выберите сайт поиска: 1 - HeadHunter, 2 - SuperJob\n')
        if site == '0':
            exit()
        elif site not in ('1', '2'):
            print('Вы ввели недопустимое значение')
            continue
        else:
            i = 2

    # Шаг 2. Выбираем область поиска.
    while i == 2:
        area = input('Введите город или субъект РФ:\n').title()
        if area == '0':
            exit()

        if site == '1':
            try:
                area_id = HeadHunter_API.get_id(area)
            except KeyError:
                print('Не верно введено наименование')
                continue
            else:
                i = 3

        elif site == '2':
            pass

        # Шаг 3. Задаем ключевые слова для поиска.
        text = input('Введите ключевые слова для поиска вакансий (через запятую, если несколько):\n')
        if text == '0':
            exit()

        i = 4
        # Шаг 4. Задаем дату поиска.
        while i == 4:
            date = input('Введите количество дней, в пределах которых производить поиск по вакансиям:\n')
            if date == '0':
                exit()
            elif int(date) < 0 or date.isalpha():
                print('Не верный ввод!')
            else:
                i = 5

        # Шаг 5. Создаем класс для парсинга вакансий по полученным параметрам
        while i == 5:
            if site == '1':
                hh_api = HeadHunter_API(text, area_id, date)

            elif site == '2':
                sj_api = SuperJob_API(text, area, date)

            i = 6
            # Шаг 6. Работаем с полученными вакансиями
            while i == 6:
                if site == '1':
                    vacancies_all_info = hh_api.get_vacancies()
                    hh_api.create_vacancy(vacancies_all_info)
                elif site == '2':
                    vacancies_all_info = sj_api.get_vacancies()
                    sj_api.create_vacancy(vacancies_all_info)

                # Подшаг 1. Сохранение информации в файл
                j = 0
                while j == 0:
                    save_input = input('Хотите сохранить найденные вакансии в файл? Ввведите 1 - да или 2 - нет:\n')
                    if save_input not in ('1', '2', '0'):
                        print('Вы ввели неверное значение')
                        continue
                    elif save_input == '0':
                        exit()
                    elif save_input == '1':
                        j = 1
                        file_name = input('Введите имя файла в формате "xxx.txt":\n')
                        js_saver = JsonSaver(vacancies_all_info)
                        js_saver.write_file(file_name)
                        print(f'Найденные вакансии записаны в файл {file_name}\n')
                    else:
                        j = 1

                # Подшаг 2. Выбор действий с полученными вакансиями
                while j == 1:
                    user_input = input('Выберите дальнейшие действия:\n'
                                       '0 - выйти\n'
                                       '1 - вывести информацию о всех полученных вакансиях\n'
                                       '2 - сравнить зарплату по двум вакансиям\n'
                                       '3 - показать вакансию с самой высокой зарплатой\n'
                                       '4 - удалить информацию из файла\n'
                                       '5 - изменить параметры поиска\n')
                    if user_input == '0':
                        exit()

                    elif user_input not in ('1', '2', '3', '4', '5', '0'):
                        print('Вы ввели неверное значение')
                        continue

                    elif user_input == '1':
                        Vacancy.print_info_all()

                    elif user_input == '2':
                        vac_numbers = input('Введите порядковые номера двух вакансий для сравнения (через запятую):\n')
                        vac_numbers = vac_numbers.split(',')
                        if len(vac_numbers) != 2:
                            print('Не верный ввод!')
                        else:
                            try:
                                diff = Vacancy.all[int(vac_numbers[0])] - Vacancy.all[int(vac_numbers[1])]
                                if diff > 0:
                                    print(f'ЗП вакансии номер {vac_numbers[0]} больше ЗП вакансии номер {vac_numbers[1]}'
                                          f' на {diff} рублей')
                                elif diff == 0:
                                    print('У выбранных вакансий одинаковый уровень ЗП')
                                else:
                                    print(f'ЗП вакансии номер {vac_numbers[1]} больше ЗП вакансии номер {vac_numbers[0]}'
                                          f' на {0 - diff} рублей')
                            except KeyError:
                                print('Не верный ввод!')

                    elif user_input == '3':
                        Vacancy.get_max()

                    elif user_input == '4':
                        js_saver.del_info()

                    elif user_input == '5':
                        j = 2
                        print('Задайте новые параметры. Если хотите оставить параметр без изменения, нажмите Enter')
                        new_date = input('Введите количество дней, в пределах которых производить поиск:\n')
                        if new_date == '':
                            new_date = date
                        else:
                            if site == '1':
                                hh_api.change_date(new_date)
                            elif site == '2':
                                sj_api.change_date(new_date)

                        new_words = input('Введите дополнительные слова для поиска:\n')
                        if new_words == '':
                            new_words = text
                        else:
                            if site == '1':
                                hh_api.add_words(new_words)
                            elif site == '2':
                                sj_api.add_words(new_words)

                        new_area = input('Введите город или субъект РФ для поиска:\n')
                        if new_area == '':
                            if site == '1':
                                new_area_id = area_id
                            elif site == '2':
                                new_area = area
                        else:
                            if site == '1':
                                new_area_id = HeadHunter_API.get_id(new_area)
                                hh_api.change_area(new_area_id)
                            elif site == '2':
                                sj_api.change_area(new_area)

                        # возвращаемся на шаг 6
                        i = 6
