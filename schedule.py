import json
import requests
from sh_blog.models import TodaySchedule
from django.utils import timezone

for lesson in TodaySchedule.objects.all(): #удаляет значения за предыдущий день
    lesson.delete()

group = "967201"

schedule_response = requests.get(f"https://journal.bsuir.by/api/v1/studentGroup/schedule?studentGroup={group}")
schedule_json = json.loads(schedule_response.text)
for numb, parameters in enumerate(schedule_json['todaySchedules'], 1):
    ts = TodaySchedule()
    ts.lesson_numb = numb
    ts.subject = parameters['subject']
    ts.lessonType = parameters['lessonType']
    ts.startLessonTime = timezone.now().strptime(parameters['startLessonTime'], "%H:%M").time()
    print(ts.startLessonTime)
    ts.endLessonTime = timezone.now().strptime(parameters['endLessonTime'], "%H:%M").time()
    print(ts.endLessonTime)
    ts.auditory = parameters['auditory'][0]
    ts.note = parameters['note']
    ts.employee = parameters['employee'][0]['lastName']+' '+parameters['employee'][0]['firstName'][0]+". "+parameters['employee'][0]['middleName'][0]+"."
    ts.save()


exit()

