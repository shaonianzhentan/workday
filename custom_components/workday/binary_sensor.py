import time, requests
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import SENSOR

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the platform from config_entry."""
    name = entry.data.get(CONF_NAME, '工作日')
    async_add_entities([WorkdaySensor(name, hass)], True)

class WorkdaySensor(BinarySensorEntity):

    _attr_unique_id = SENSOR

    def __init__(self, name: str, hass) -> None:
        self._attr_name = name
        self.hass = hass
        self.today = None

    async def async_update(self) -> None:
        today = time.localtime()
        if self.today is None or self.today.tm_mday != today.tm_mday:
            is_on = False
            today_str = time.strftime('%Y-%m-%d', today)
            # 计算闰年
            year_day = 365            
            if (today.tm_year % 100 == 0 and today.tm_year % 400 == 0) or today.tm_year % 4 == 0:
                year_day = 366
            weeks = ['一', '二', '三', '四', '五', '六', '日']
            # 判断是否周一至周五
            if today.tm_wday >= 0 and today.tm_wday < 5:
                is_on = True
            # 判断是否节假日
            res = await self.hass.async_add_executor_job(requests.get, f'https://cdn.jsdelivr.net/gh/bastengao/chinese-holidays-node@master/data/{today.tm_year}.json')
            holiday = res.json()
            for holi in holiday:
                holi_range = holi['range']
                holi_type = holi['type']
                if len(holi_range) == 1:
                    if holi_range[0] == today_str:
                        is_on = holi_type == 'workingday'
                elif len(holi_range) == 2:
                    if today_str >= holi_range[0] and today_str <= holi_range[1]:
                        is_on = holi_type == 'workingday'
            self._attr_is_on = is_on
            self._attr_extra_state_attributes = {
                '周': weeks[today.tm_wday],
                '日期': today_str,
                '今年天数': year_day,
                '已过天数': today.tm_yday,
                '剩余天数': year_day - today.tm_yday
            }
            self.today = today