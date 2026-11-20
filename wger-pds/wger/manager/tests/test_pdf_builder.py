# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Standard Library
from unittest import mock

# Django
from django.test import SimpleTestCase

# wger
from wger.manager.pdf_builder import RoutinePdfDirector


class RoutinePdfDirectorTestCase(SimpleTestCase):
    def test_construct_calls_steps_in_order(self):
        builder = mock.Mock()
        result = RoutinePdfDirector(builder).construct()

        self.assertEqual(
            [name for name, *_ in builder.method_calls],
            ['add_logo', 'add_title', 'add_period', 'add_days', 'add_footer', 'get_result'],
        )
        self.assertIs(result, builder.get_result.return_value)
