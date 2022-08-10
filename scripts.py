import sys
from random import choice

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject)


def fix_marks(schoolkid: Schoolkid):
    Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    ).update(points=5)


def remove_chastisements(schoolkid: Schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid: Schoolkid, subject: Subject):
    commendations_texts = (
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
    )
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    ).order_by('-date').first()

    Commendation.objects.create(
        created=lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=lesson.teacher,
        text=choice(commendations_texts)
    )


def fix_diary(schoolkid_name: str, subject_title: str):
    schoolkid_fails = (
        Schoolkid.DoesNotExist,
        Schoolkid.MultipleObjectsReturned,
    )
    subject_fails = (
        Subject.DoesNotExist,
        Subject.MultipleObjectsReturned,
    )
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        subject = Subject.objects.get(
            title=subject_title,
            year_of_study=schoolkid.year_of_study
        )
    except (*schoolkid_fails, *subject_fails) as fail:

        if isinstance(fail, schoolkid_fails):
            search_object = "ученика"
        else:
            search_object = "предмета"

        print(
            f'Задайте другую строку поиска {search_object} - такого не нашли '
            '(или нашли несколько); ошибка: ',
            fail,
            file=sys.stderr
        )
        return

    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, subject)
