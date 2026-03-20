import pytest
from units.models import Unit

class TestUnits:
    @pytest.fixture
    def base_unit(self):
        return Unit.objects.create(
            name="Агентство",
            level="agency",
            short_description="Базовий підрозділ",
            description="Текстовий опис базового підрозділу"
        )

    @pytest.mark.django_db
    def test_create_unit(self, base_unit):
        assert base_unit.id is not None
        assert base_unit.name == "Агентство"
        assert base_unit.level == "agency"
        assert str(base_unit) == "Агентство"


    @pytest.mark.django_db
    def test_unit_hierarchy(self, base_unit):
        child_unit = Unit.objects.create(
            name="Бригада 1",
            level="brigade",
            short_description="Дочірня бригада",
            description="Опис бригади",
            parent=base_unit
        )

        assert child_unit.parent == base_unit
        assert base_unit.children.count() == 1
        assert base_unit.children.first() == child_unit


    @pytest.mark.django_db
    def test_unit_level_choices(self):
        unit = Unit.objects.create(
            name="Спецпідрозділ",
            level="special",
            short_description="Опис спецпідрозділу",
            description="Повний опис спецпідрозділу"
        )

        assert unit.level in dict(Unit.LEVEL_CHOICES)
