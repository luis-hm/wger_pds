"""
Dados de demonstração idênticos para os dois projetos (wger-fork e wger-pds).

Uso, de dentro da pasta do projeto:
    uv run python manage.py shell --settings=settings.local_dev < ../docs/seed_demo.py

Cria, para o usuário admin, a rotina "Treino ABC" com 3 dias, 2 exercícios por dia,
configurações de séries/repetições/carga/descanso/RIR e um label "Semana de deload".
Rodar de novo não duplica: a rotina antiga com o mesmo nome é apagada antes.
"""

# Standard Library
import datetime

# Django
from django.contrib.auth.models import User

# wger
from wger.exercises.models import Exercise
from wger.manager.models import (
    Day,
    Label,
    RepetitionsConfig,
    RestConfig,
    RiRConfig,
    Routine,
    SetsConfig,
    Slot,
    SlotEntry,
    WeightConfig,
)

admin = User.objects.get(username='admin')
Routine.objects.filter(user=admin, name='Treino ABC').delete()

start = datetime.date.today()
routine = Routine.objects.create(
    user=admin,
    name='Treino ABC',
    description='Rotina de demonstração do trabalho de PDS',
    start=start,
    end=start + datetime.timedelta(weeks=8),
)
Label.objects.create(routine=routine, start_offset=42, end_offset=49, label='Semana de deload')

exercises = list(Exercise.objects.order_by('id')[:6])
for order, name in enumerate(['A - Peito e tríceps', 'B - Costas e bíceps', 'C - Pernas'], 1):
    day = Day.objects.create(routine=routine, order=order, name=name)
    for slot_order, exercise in enumerate(exercises[(order - 1) * 2 : order * 2], 1):
        slot = Slot.objects.create(day=day, order=slot_order)
        entry = SlotEntry.objects.create(slot=slot, exercise=exercise, order=1)
        SetsConfig.objects.create(slot_entry=entry, iteration=1, value=4)
        RepetitionsConfig.objects.create(slot_entry=entry, iteration=1, value=10)
        WeightConfig.objects.create(slot_entry=entry, iteration=1, value=40)
        RestConfig.objects.create(slot_entry=entry, iteration=1, value=90)
        RiRConfig.objects.create(slot_entry=entry, iteration=1, value=2)

print(f'Rotina "{routine.name}" criada com id={routine.pk}')
