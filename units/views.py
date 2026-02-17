from django.shortcuts import render, get_object_or_404
from .models import Unit

def unit(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)

    hierarchy = [unit]
    parent = unit.parent
    while parent:
        hierarchy.append(parent)
        parent = parent.parent
    hierarchy.reverse()

    context = {
        "unit": unit,
        "hierarchy": hierarchy
    }
    return render(request, "units/unit.html", context)
