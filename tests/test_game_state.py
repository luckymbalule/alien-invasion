import pytest
from game_state import GameState, GamePhase


class SpySubscriber:
    def __init__(self, game_state):
        self.phase = None
        game_state.subscribe(self.update)

    def update(self, phase):
        self.phase = phase


@pytest.mark.parametrize("phase", list(GamePhase))
def test_start_transitions_phase_correctly(phase, fake_game):
    game_state = GameState(fake_game.settings)
    game_state.phase = phase

    game_state.start()

    if phase not in (
        GamePhase.MENU, GamePhase.PAUSED, GamePhase.GAME_OVER
    ):
        assert game_state.phase == phase
    else:
        assert game_state.phase == GamePhase.PLAYING


@pytest.mark.parametrize("phase",
    [GamePhase.MENU, GamePhase.PAUSED, GamePhase.GAME_OVER]                         
)
def test_start_notifies_subscriber(phase, fake_game):
    game_state = GameState(fake_game.settings)
    game_state.phase = phase
    spy = SpySubscriber(game_state)

    game_state.start()

    assert spy.phase == GamePhase.PLAYING


@pytest.mark.parametrize("phase", list(GamePhase))
def test_pause_transitions_phase_correctly(phase, fake_game):
    game_state = GameState(fake_game.settings)
    game_state.phase = phase

    game_state.pause()

    if phase != GamePhase.PLAYING:
        assert game_state.phase == phase
    else:
        assert game_state.phase == GamePhase.PAUSED


def test_pause_notifies_subscriber(fake_game):
    game_state = GameState(fake_game.settings)
    game_state.phase = GamePhase.PLAYING
    spy = SpySubscriber(game_state)

    game_state.pause()

    assert spy.phase == GamePhase.PAUSED


@pytest.mark.parametrize("phase", list(GamePhase))
def test_resume_transitions_phase_correctly(phase, fake_game):
    game_state = GameState(fake_game.settings)
    game_state.phase = phase

    game_state.resume()

    if phase != GamePhase.PAUSED:
        assert game_state.phase == phase
    else:
        assert game_state.phase == GamePhase.PLAYING


def test_resume_notifies_subscriber(fake_game):
    game_state = GameState(fake_game.settings)
    game_state.phase = GamePhase.PAUSED
    spy = SpySubscriber(game_state)

    game_state.resume()

    assert spy.phase == GamePhase.PLAYING


@pytest.mark.parametrize("phase", list(GamePhase))
def test_end_transitions_phase_correctly(phase, fake_game):
    game_state = GameState(fake_game.settings)
    game_state.phase = phase

    game_state.end()

    if phase != GamePhase.PLAYING:
        assert game_state.phase == phase
    else:
        assert game_state.phase == GamePhase.GAME_OVER


def test_end_notifies_subscriber(fake_game):
    game_state = GameState(fake_game.settings)
    game_state.phase = GamePhase.PLAYING
    spy = SpySubscriber(game_state)

    game_state.end()

    assert spy.phase == GamePhase.GAME_OVER


@pytest.mark.parametrize(
    "count, phase",
    [
        ((1, 0), (GamePhase.PLAYING, GamePhase.GAME_OVER)),
        ((3, 2), (GamePhase.PLAYING, GamePhase.PLAYING))
    ]
)
def test_register_ship_loss_when_phase_playing_update_phase_and_ship_count(
    fake_game, count, phase
):
    initial_count, final_count = count
    initial_phase, final_phase = phase
    game_state = GameState(fake_game.settings)
    game_state.ships_remaining = initial_count
    game_state.phase = initial_phase

    game_state.register_ship_loss()

    assert game_state.ships_remaining == final_count
    assert game_state.phase == final_phase


@pytest.mark.parametrize("phase",
    (GamePhase.MENU, GamePhase.GAME_OVER, GamePhase.PAUSED)
)
def test_register_ship_loss_when_phase_not_playing_ignored(
    fake_game, phase, count=2
):
    game_state = GameState(fake_game.settings)
    game_state.ships_remaining = count
    game_state.phase = phase

    game_state.register_ship_loss()

    assert game_state.ships_remaining == count
    assert game_state.phase == phase