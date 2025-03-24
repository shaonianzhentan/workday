import sxtwl
from datetime import datetime, date
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import SENSOR


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([CalendarSensor('农历')], True)


class CalendarSensor(SensorEntity):

    _attr_unique_id = SENSOR
    _attr_device_class = SensorDeviceClass.DATE

    def __init__(self, name: str) -> None:
        self._attr_name = name
        self.today = None

    async def async_update(self) -> None:
        now = datetime.now()
        if self.today is None or self.today.day != now.day:
            lunar = sxtwl.fromSolar(now.year, now.month, now.day)
            year, month, day = lunar.getLunarYear(), lunar.getLunarMonth(), lunar.getLunarDay()
            self.native_value = date(year, month, day)
            self._attr_extra_state_attributes = {
                '月': month,
                '日': day
            }
            self.today = now
