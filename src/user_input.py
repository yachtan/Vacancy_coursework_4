from src.api import HeadHunter_API, SuperJob_API
from src.saver import JsonSaver
from src.vacancy import Vacancy


def user():
    print('Начинаем поиск вакансий. Для выхода в любой момент, введите "0".')
    # Шаг 1. Выбираем сайт поиска.
    i = 0
    while i == 0:
        site = input('Выберите сайт поиска: 1 - HeadHunter, 2 - SuperJob\n')
        if site == '0':
            exit()
        elif site not in ('1', '2'):
            print('Вы ввели недопустимое значение')
            continue
        else:
            i = 1
    # Шаг 2. Выбираем область поиска.
    while i == 1:
        area = input('Введите город или субъект РФ:\n').title()
        if area == '0':
            exit()
        try:
            area_id = HeadHunter_API.get_id_new(area)
        # except IndexError:
        #     print('Не верно введено наименование')
        #     continue
        except KeyError:
            print('Не верно введено наименование')
            continue
        else:
            i = 2
        # Шаг 3. Задаем ключевые слова для поиска.
        text = input('Введите ключевые слова для поиска вакансий:\n')
        if text == '0':
            exit()
        # Шаг 4. Задаем дату поиска.
        date = input('Введите количество дней, в пределах которых производить поиск по вакансиям:\n')
        if date == '0':
            exit()

        # Создаем класс для парсинга вакансий по полученным параметрам
        if site == '1':
            area_id = HeadHunter_API.get_id_new(area)
            hh_api = HeadHunter_API(text, area_id, date)
            vacancies_all_info = hh_api.get_vacancies()
            # js_saver = JsonSaver(vacancies_all_info)
            # js_saver.write_file('hh_test_2.txt')
            # print(f'Найдено {len(vacancies_all_info)} вакансий')
            # выбираем данные для создания экземпляров класса вакансии
            # all_vacancies = {}
            n = 0
            for vac in vacancies_all_info:
                n += 1
                vacancies_all_info[n-1]['number'] = n
                vac_name = vac['name']
                vac_url = vac['apply_alternate_url']
                vac_salary = vac['salary']
                vac_requirement = vac['snippet']['requirement']
                vac_responsibility = vac['snippet']['responsibility']
                vacancy = Vacancy(n, vac_name, vac_url, vac_salary, vac_requirement, vac_responsibility)

            if len(Vacancy.all) > 0:
                print(f'По Вашему запросу найдено {len(Vacancy.all)} вакансий')
            else:
                print('По вашему запросу вакансии не найдены.')
                exit()

            while i == 2:
                save_input = input('Хотите сохранить найденные вакансии в файл? Ввведите 1 - да или 2 - нет:\n')
                if save_input not in ('1', '2', '0'):
                    print('Вы ввели неверное значение')
                    continue
                elif save_input == '0':
                    print('Работа программы завершена.')
                    exit()
                elif save_input == '1':
                    i = 3
                    file_name = input('Введите имя файла в формате "xxx.txt":\n')
                    js_saver = JsonSaver(vacancies_all_info)
                    js_saver.write_file(file_name)
                    print(f'Найденные вакансии записаны в файл {file_name}\n')
                else:
                    i = 3

            while i == 3:
                user_input = input('Выберите дальнейшие действия:\n'
                                    '0 - выйти\n'
                                    '1 - вывести информацию о всех полученных вакансиях\n'
                                    '2 - сравнить зарплату по двум вакансиям\n'
                                    '3 - показать вакансию с самой высокой зарплатой\n'
                                    '4 - удалить информацию из файла и выйти\n')
                if user_input == '0':
                    exit()

                elif user_input not in ('1', '2', '3', '4', '0'):
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
                    exit()


        elif site == '2':
            pass




