"""Contain input-action mapping, processing action on right input command"""

import pygame


class InputHandler:
    """Store (key/mouse, action) pairing and process action right event"""

    def __init__(self, keydown_map, keyup_map, mouse_targets=[]):
        self.keydown_actions = keydown_map
        self.keyup_actions = keyup_map
        self.mouse_targets = mouse_targets
        self.hovering = False

    def handle_input(self, event):
        """Process input events and invoke corresponding actions."""
        if event.type == pygame.KEYDOWN:
            action_func = self.keydown_actions.get(event.key)
            if action_func:
                action_func()

        if event.type == pygame.KEYUP:
            action_func = self.keyup_actions.get(event.key)
            if action_func:
                action_func()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for target, action_func in self.mouse_targets:
                if target.collidepoint(mouse_pos) and action_func:
                    action_func()
                    break

        if event.type == pygame.MOUSEMOTION:
            hover_pos = pygame.mouse.get_pos()
            is_hovering = any(
                clickable.collidepoint(hover_pos)
                for clickable, *_ in self.mouse_targets
            )

            if self.hovering != is_hovering:
                self.hovering = is_hovering
                self._set_cursor()

    def _set_cursor(self):
        if self.hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)