import random

from django.db.models import Q, QuerySet

from .constants import CLOTHING_TYPES

# Utility function to generate an outfit from a queryset of garments, filtering by style and weather, and ensuring no more than one garment per clothing category is included.
def generate_outfit(garments: QuerySet, style="Any", weather="Any", rng=None):
    """Return no more than one user-owned garment for each clothing category."""
    filtered = garments
    if style != "Any":
        filtered = filtered.filter(style=style)
    if weather != "Any":
        filtered = filtered.filter(Q(weather="Any") | Q(weather=weather))

    # Use a random number generator to select garments, defaulting to SystemRandom for better randomness if no RNG is provided.
    picker = rng or random.SystemRandom()
    result = []
    for clothing_type, _label in CLOTHING_TYPES:
        candidates = list(filtered.filter(clothing_type=clothing_type))
        if candidates:
            result.append(picker.choice(candidates))
    return result
