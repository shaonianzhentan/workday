from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SENSOR

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the platform from config_entry."""
    name = entry.data.get(CONF_NAME) or DOMAIN
    async_add_entities([WorkdaySensor(name)], True)


class WorkdaySensor(BinarySensorEntity):

    _attr_unique_id = SENSOR
    _attr_icon = "mdi:calendar-month"

    def __init__(self, name: str) -> None:
        self._attr_name = name

    async def async_update(self) -> None:
        self._attr_native_value = True