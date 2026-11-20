# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Padrão GoF Builder para os relatórios PDF de uma rotina.

* Builder (abstrato) ......... RoutinePdfBuilder: declara os passos e implementa os comuns
* ConcreteBuilders ........... RoutineLogPdfBuilder (com colunas de registro, paisagem)
                               RoutineTablePdfBuilder (só a tabela de exercícios, retrato)
* Director ................... RoutinePdfDirector: define a ORDEM dos passos
* Product .................... o HttpResponse com o PDF
"""

# Standard Library
from xml.sax.saxutils import escape

# Django
from django.http import HttpResponse
from django.utils.translation import gettext as _

# Third Party
from reportlab.lib.pagesizes import (
    A4,
    landscape,
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

# wger
from wger.manager.helpers import render_workout_day
from wger.manager.models import Routine
from wger.utils.pdf import (
    get_logo,
    render_footer,
    styleSheet,
)


class RoutinePdfBuilder:
    """
    Builder: monta o PDF de uma rotina passo a passo. As subclasses só definem o que varia.
    """

    pagesize = A4
    only_table = True

    def __init__(self, routine: Routine, request):
        self.routine = routine
        self.request = request
        self.elements = []

    def add_logo(self):
        self.elements.append(get_logo())
        self.elements.append(Spacer(10 * cm, 0.5 * cm))

    def add_title(self):
        raise NotImplementedError

    def add_period(self):
        """Start and end date of the routine, below the title"""
        fmt = '%d.%m.%Y'
        period = f'{self.routine.start.strftime(fmt)} – {self.routine.end.strftime(fmt)}'
        self.elements.append(Paragraph(f'<para align="center">{period}</para>'))
        self.elements.append(Spacer(10 * cm, 1 * cm))

    def add_days(self):
        for day_data in self.routine.data_for_iteration():
            if day_data.day is None:
                continue
            self.elements.append(render_workout_day(day_data, only_table=self.only_table))
            self.elements.append(Spacer(10 * cm, 0.5 * cm))

    def add_footer(self):
        self.elements.append(Spacer(10 * cm, 0.5 * cm))
        url = self.request.build_absolute_uri(self.routine.get_absolute_url())
        self.elements.append(render_footer(url))

    def get_result(self) -> HttpResponse:
        response = HttpResponse(content_type='application/pdf')
        doc = SimpleDocTemplate(
            response,
            pagesize=self.pagesize,
            leftMargin=cm,
            rightMargin=cm,
            topMargin=0.5 * cm,
            bottomMargin=0.5 * cm,
            title=_('Workout'),
            author='wger Workout Manager',
            subject=_('Workout for %s') % self.request.user.username,
        )
        doc.build(self.elements)
        response['Content-Length'] = len(response.content)
        return response


class RoutineLogPdfBuilder(RoutinePdfBuilder):
    """PDF with empty columns to write down the logs, landscape"""

    pagesize = landscape(A4)
    only_table = False

    def add_title(self):
        self.elements.append(
            Paragraph(
                f'<para align="center"><strong>{escape(self.routine.name)}</strong></para>',
                styleSheet['HeaderBold'],
            )
        )
        self.elements.append(Spacer(10 * cm, 0.5 * cm))
        if self.routine.description:
            self.elements.append(
                Paragraph(f'<para align="center">{escape(self.routine.description)}</para>')
            )
            self.elements.append(Spacer(10 * cm, 0.5 * cm))


class RoutineTablePdfBuilder(RoutinePdfBuilder):
    """PDF with only the table of exercises, portrait"""

    def add_title(self):
        self.elements.append(
            Paragraph(
                f'<para align="center"><strong>{escape(str(self.routine))}</strong></para>',
                styleSheet['HeaderBold'],
            )
        )
        self.elements.append(Spacer(10 * cm, 0.5 * cm))


class RoutinePdfDirector:
    """
    Director: conhece a sequência de montagem, não os detalhes de cada passo.
    Qualquer builder concreto passa pelo mesmo processo.
    """

    def __init__(self, builder: RoutinePdfBuilder):
        self.builder = builder

    def construct(self) -> HttpResponse:
        self.builder.add_logo()
        self.builder.add_title()
        self.builder.add_period()
        self.builder.add_days()
        self.builder.add_footer()
        return self.builder.get_result()
