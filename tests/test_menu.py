import pytest
from button import ButtonConfig
from menu import Menu


@pytest.fixture
def menu_env(fake_game):
    menu = Menu(fake_game.screen, fake_game.settings)
    buttons = [
        ButtonConfig("1"),
        ButtonConfig("w", False),
        ButtonConfig("1", action=fake_callable),
        ButtonConfig("5", False, action=fake_callable),
    ]

    return menu, buttons


def fake_callable():
    pass


def test_build_when_argument_is_valid_appends_buttons(menu_env):
    menu, buttons = menu_env
    assert len(menu.buttons) == 0

    menu.build(buttons)

    assert len(menu.buttons) == 4


@pytest.mark.parametrize("arg",[
    None, [], 2, "Hello", [8,"8"]
])
def test_build_when_argument_is_invalid_raises_type_error(menu_env, arg):
    menu, _ = menu_env
    assert len(menu.buttons) == 0

    with pytest.raises(TypeError):
        menu.build(arg)


def test_get_mouse_targets_returns_only_enabled_and_actionable_buttons(menu_env):
    menu, buttons = menu_env
    menu.build(buttons)

    mouse_targets = menu.get_mouse_targets()

    assert len(mouse_targets) == 1