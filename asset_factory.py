"""
This module provides a factory for loading and caching images/assets
"""

import pygame


# Cache asset surfaces to optimise perfomance.
_asset_cache = {}


def load_image(path: str, target_height: int) -> pygame.Surface:
    """Processes image scaling and caching."""
    
    # Compound key as the ID
    cache_key = (path, target_height)

    # Lookup cache 
    if path in _asset_cache:
        return _asset_cache[cache_key]
    
    image = pygame.image.load(path).convert_alpha()

    # Scale image
    ratio = target_height / image.get_height()
    target_width = int(image.get_width() * ratio)
    image = pygame.transform.smoothscale(
        image, (target_width, target_height)
    )

    # Cache image using compound key
    _asset_cache[cache_key] = image
    return image