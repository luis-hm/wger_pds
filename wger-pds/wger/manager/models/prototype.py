# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Standard Library
import copy


class Prototype:
    """
    Padrão GoF Prototype.

    Um objeto que sabe criar uma cópia de si mesmo. O cliente (a view de cópia) só chama
    ``clone()`` e não precisa conhecer a estrutura interna (dias, slots, entries, configs).

    Cada classe concreta pode:
    * passar em ``overrides`` os campos que mudam na cópia (ex.: o novo pai da relação);
    * sobrescrever ``clone_children`` para clonar as partes que ela possui (Information Expert).
    """

    def clone(self, **overrides):
        # Django's Model.__getstate__ already copies _state, so the copy does not share
        # the related-object cache with the original
        twin = copy.copy(self)
        twin.pk = None
        twin._state.adding = True
        for field, value in overrides.items():
            setattr(twin, field, value)
        twin.save()

        self.clone_children(twin)
        return twin

    def clone_children(self, twin):
        """Hook: clones the objects owned by this one. Leaves have nothing to copy."""
        pass
