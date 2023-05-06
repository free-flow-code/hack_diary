from datacenter.models import Schoolkid, Teacher, Subject, Lesson, Mark, Chastisement, Commendation
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.utils.encoding import force_str
import random


def get_schoolkid_entry(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(
            full_name__contains=force_str(
                schoolkid_name,
                encoding='utf-8',
                strings_only=False,
                errors='strict'
            )
        )
        return schoolkid
    except Schoolkid.DoesNotExist:
        print('Имя не найдено. Проверьте правильность ввода.')
        exit()
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько записей, уточните имя.')
        exit()


def get_subject_entry(schoolkid, subject_name):
    try:
        subject = Subject.objects.get(
            title=subject_name,
            year_of_study=schoolkid.year_of_study,
        )
        return subject
    except Subject.DoesNotExist:
        print('Предмет не найден. Проверьте правильность ввода.')


def fix_bad_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)
    return True


def delete_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()
    return True


def create_commendation(schoolkid, subject):
    praise_examples = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Очень хороший ответ!',
        'Сказано здорово – просто и ясно!'
    ]

    schoolkid_year_of_study = schoolkid.year_of_study
    schoolkid_group_letter = schoolkid.group_letter
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid_year_of_study,
        group_letter=schoolkid_group_letter,
        subject=subject
    ).order_by('-date').first()
    praise_text = random.choice(praise_examples)
    teacher = lesson.teacher
    date = lesson.date
    Commendation.objects.create(
        text=praise_text,
        created=date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=teacher
    )
    return True


def hack_diary():
    print(
        'Что вы хотите сделать?\nВведите соответствующую цифру:\n',
        '1 - Исправить плохие оценки\n',
        '2 - Удалить замечания\n',
        '3 - Добавить похвалу'
    )
    number = input()

    if number == '1':
        schoolkid_name = input('Введите ФИО ученика: ')
        schoolkid = get_schoolkid_entry(schoolkid_name)
        if fix_bad_marks(schoolkid):
            print('Оценки исправлены.')
    elif number == '2':
        schoolkid_name = input('Введите ФИО ученика: ')
        schoolkid = get_schoolkid_entry(schoolkid_name)
        if delete_chastisements(schoolkid):
            print('Все замечания удалены.')
    elif number == '3':
        schoolkid_name = input('Введите ФИО ученика: ')
        schoolkid = get_schoolkid_entry(schoolkid_name)
        subject_name = input('Введите название предмета: ')
        subject = get_subject_entry(schoolkid, subject_name)
        if create_commendation(schoolkid, subject):
            print('Новая похвала создана.')
    else:
        print('Неверный ввод.')
