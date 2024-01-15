from datetime import datetime

from mailing.models import Mailing


def run_newsletter():
    '''Список рассылок'''

    print('Отправка рассылок')
    сurrent_time = datetime.today().strftime('%H:%M')

    '''После создания новой рассылки, если текущее время больше времени начала и меньше времени окончания,
     то должны быть выбраны из справочника все клиенты, которые указаны в настройках рассылки,
      и запущена отправка для всех этих клиентов.'''

    newskatters = (Mailing.objects.all()
    .filter(status='Создана') \
    .filter(time_mailing__lte=сurrent_time) \
    .filter(
        end_datatime_mailing__gte=f'{datetime.today().strftime("%Y-%m-%d")}T{datetime.today().strftime("%H:%M")}'))

    print(newskatters)

    for newskatter in newskatters:
        newskatter.status = 'Создана'
        newskatter.save()

    # Дальше получаем список клиентов в конце проверяем следующую дату отпраавки, если дата отправки коректна то меняем 'run' на 'created'
