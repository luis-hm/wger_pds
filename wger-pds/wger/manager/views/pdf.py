# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

# Django
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

# wger
from wger.manager.models import Routine
from wger.manager.pdf_builder import (
    RoutineLogPdfBuilder,
    RoutinePdfDirector,
    RoutineTablePdfBuilder,
)


def _routine_pdf(request, pk: int, builder_class):
    if request.user.is_anonymous:
        return HttpResponseForbidden()
    routine = get_object_or_404(Routine, pk=pk, user=request.user)
    return RoutinePdfDirector(builder_class(routine, request)).construct()


def workout_log(request, pk: int):
    """
    Generates a PDF of the routine with columns to write down the logs
    """
    return _routine_pdf(request, pk, RoutineLogPdfBuilder)


def workout_view(request, pk: int):
    """
    Generates a PDF of the routine with only the table of exercises
    """
    return _routine_pdf(request, pk, RoutineTablePdfBuilder)
