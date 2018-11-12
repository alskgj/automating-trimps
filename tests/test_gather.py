from unittest.mock import Mock
from modules import gather


def test_building():
    """Ensure that if the building queue has two or more objects
     the player is set to building"""
    trimps_mock = Mock()
    trimps_mock.building_queue = ['mine', 'house']
    gather.run(trimps_mock)
    assert trimps_mock.player_build.called


def test_gather():
    """Ensure that we are gathering the resource with the lowest amount stored
    if the building queue is empty"""
    trimps_mock = Mock()
    trimps_mock.building_queue = []
    trimps_mock.food = 100
    trimps_mock.wood = 200
    trimps_mock.metal = 300

    gather.run(trimps_mock)
    assert trimps_mock.gather.call_args[0][0] == 'Food'


test_building()
test_gather()
