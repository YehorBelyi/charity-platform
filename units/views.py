from django.shortcuts import render, get_object_or_404
from .models import Unit

def unit(request, unit_id):
    """
    Display details of a specific unit and its hierarchical path.

    This view fetches the unit by ID and reconstructs the full path from the 
    top-level parent down to the current unit for navigation purposes.

    Args:
        request (HttpRequest): The incoming request.
        unit_id (int): The primary key of the unit to display.

    Returns:
        HttpResponse: Rendered unit detail page with hierarchy context.
    """
    unit = get_object_or_404(Unit, pk=unit_id)

    # Building the hierarchy path
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
