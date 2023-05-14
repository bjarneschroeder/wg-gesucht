import pytest

from wg_gesucht.wg_gesucht.search_settings import SearchSettings


class TestSearchSettingsInit:
    def test_city_name_not_set(self):
        with pytest.raises(ValueError):
            SearchSettings(city_name=None)

    def test_city_name_not_str(self):
        with pytest.raises(TypeError):
            SearchSettings(city_name=1)

    def test_only_permanent_contracts_not_bool(self):
        with pytest.raises(TypeError):
            SearchSettings(city_name="Berlin", only_permanent_contracts=1)

    def test_max_rent_not_int(self):
        with pytest.raises(ValueError):
            SearchSettings(city_name="Berlin", max_rent="100asdf")

    def test_max_rent_negative(self):
        with pytest.raises(ValueError):
            SearchSettings(city_name="Berlin", max_rent="-100")

    def test_max_rent_not_in_bounds(self):
        with pytest.raises(ValueError):
            SearchSettings(city_name="Berlin", max_rent="10000")

    def test_min_rooms_not_number(self):
        with pytest.raises(ValueError):
            SearchSettings(city_name="Berlin", min_rooms="1adsf")

    def test_min_rooms_negative(self):
        with pytest.raises(ValueError):
            SearchSettings(city_name="Berlin", min_rooms="-1")

    def test_min_rooms_not_in_viable_bound(self):
        with pytest.raises(ValueError):
            SearchSettings(city_name="Berlin", min_rooms="10")

        with pytest.raises(ValueError):
            SearchSettings(city_name="Berlin", min_rooms="1")

    def test_min_rooms_not_half_step_value(self):
        with pytest.raises(ValueError):
            SearchSettings(city_name="Berlin", min_rooms="3.3")

    def test_min_rooms_half_step(self):
        settings = SearchSettings(city_name="Berlin", min_rooms="2.5")
        assert settings.city_name == "Berlin"
        assert settings.only_permanent_contracts is False
        assert settings.max_rent is None
        assert settings.min_rooms == 2.5

    def test_city_name(self):
        settings = SearchSettings(city_name="Berlin")
        assert settings.city_name == "Berlin"
        assert settings.only_permanent_contracts is False
        assert settings.max_rent is None
        assert settings.min_rooms is None

    def test_max_rent(self):
        settings = SearchSettings(
            city_name="Berlin",
            max_rent="100",
        )
        assert settings.city_name == "Berlin"
        assert settings.only_permanent_contracts is False
        assert settings.max_rent == 100
        assert settings.min_rooms is None

    def test_only_permanent_contracts(self):
        settings = SearchSettings(
            city_name="Berlin",
            only_permanent_contracts="True",
        )
        assert settings.city_name == "Berlin"
        assert settings.only_permanent_contracts is True
        assert settings.max_rent is None
        assert settings.min_rooms is None
