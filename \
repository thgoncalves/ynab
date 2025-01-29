"""Sensor platform for YNAB."""

import logging
from homeassistant.helpers.entity import Entity, BinarySensorEntity

from .const import CATEGORY_ERROR, DOMAIN_DATA, ICON

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up sensor platform."""
    sensors = []
    binary_sensors = []

    # Fetch YNAB data
    await hass.data[DOMAIN_DATA]["client"].update_data()

    # Create main budget sensors
    main_sensors = [
        "budgeted_this_month",
        "activity_this_month",
        "age_of_money",
        "total_balance",
        "need_approval",
        "uncleared_transactions",
        "overspent_categories",
    ]

    for sensor_name in main_sensors:
        sensors.append(YNABSensor(hass, sensor_name))

    _LOGGER.info(config)

    # Create category sensors separately
    categories = hass.data[DOMAIN_DATA].get("categories", [])
    for category in categories:
        sensors.append(YNABCategorySensor(hass, category, "balance"))
        sensors.append(YNABCategorySensor(hass, category, "budgeted"))
        binary_sensors.append(YNABCategoryBinarySensor(hass, category))

    async_add_entities(sensors, True)
    async_add_entities(binary_sensors, True)


class YNABSensor(Entity):
    """General YNAB Sensor class for main metrics."""

    def __init__(self, hass, name):
        """Initialize the sensor."""
        self.hass = hass
        self._name = f"YNAB {name.replace('_', ' ').title()}"
        self._state = None
        self._data_key = name
        self._measurement = "$"

    async def async_update(self):
        """Update the sensor."""
        await self.hass.data[DOMAIN_DATA]["client"].update_data()
        self._state = self.hass.data[DOMAIN_DATA].get(self._data_key)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._measurement

    @property
    def icon(self):
        return ICON


class YNABCategorySensor(Entity):
    """Sensor for individual budget categories."""

    def __init__(self, hass, category, metric):
        """Initialize the sensor."""
        self.hass = hass
        self._name = f"YNAB {category.replace('_', ' ').title()} {metric.title()}"
        self._state = None
        self._category = category
        self._metric = metric
        self._measurement = "$"

    async def async_update(self):
        """Update the sensor."""
        await self.hass.data[DOMAIN_DATA]["client"].update_data()
        category_data = self.hass.data[DOMAIN_DATA].get(self._category, {})
        self._state = category_data.get(self._metric)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._measurement

    @property
    def icon(self):
        return ICON


class YNABCategoryBinarySensor(BinarySensorEntity):
    """Binary sensor for budget category overspending."""

    def __init__(self, hass, category):
        """Initialize the sensor."""
        self.hass = hass
        self._name = f"YNAB {category.replace('_', ' ').title()} Overspend"
        self._state = None
        self._category = category
        self._device_class = "problem"

    async def async_update(self):
        """Update the sensor."""
        await self.hass.data[DOMAIN_DATA]["client"].update_data()
        category_data = self.hass.data[DOMAIN_DATA].get(self._category, {})
        balance = category_data.get("balance", 0)
        budgeted = category_data.get("budgeted", 0)
        self._state = balance > budgeted

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def device_class(self):
        return self._device_class

    @property
    def icon(self):
        return ICON
