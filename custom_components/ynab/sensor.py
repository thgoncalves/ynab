"""Sensor platform for YNAB."""

import logging
from homeassistant.helpers.entity import Entity  # type: ignore

#
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

    _LOGGER.info(f"## DOMAIN DATA: {hass.data[DOMAIN_DATA]}")

    categories = hass.data[DOMAIN_DATA]["categories"]
    if categories is not None:
        for category_name, values in categories.items():
            balance = values["balance"]
            budgeted = values["budgeted"]
            print(
                f"Category: {category_name}, Balance: {balance}, Budgeted: {budgeted}"
            )

            sensors.append(YNABCategorySensor(hass, category_name, balance, "balance"))
            sensors.append(
                YNABCategorySensor(hass, category_name, budgeted, "budgeted")
            )

    async_add_entities(sensors, True)


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

    def __init__(self, hass, category_name, state, category_type):
        """Initialize the sensor."""
        self.hass = hass
        self._name = f"YNAB Category {category_name.replace('_', ' ').title()} {category_type.title()}"
        self._state = state
        self._category_name = category_name
        self._type = category_type
        self._measurement = "$"

    async def async_update(self):
        """Update the sensor."""
        await self.hass.data[DOMAIN_DATA]["client"].update_data()
        category_data = self.hass.data[DOMAIN_DATA]["categories"].get(
            self._category_name
        )
        self._state = category_data.get(self._type)

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


# class YNABCategoryBinarySensor(BinarySensorEntity):
#     """Binary sensor for budget category overspending."""
#
#     def __init__(self, hass, category):
#         """Initialize the sensor."""
#         self.hass = hass
#         self._name = f"YNAB {category.replace('_', ' ').title()} Overspend"
#         self._state = None
#         self._category = category
#         self._device_class = "problem"
#
#     async def async_update(self):
#         """Update the sensor."""
#         await self.hass.data[DOMAIN_DATA]["client"].update_data()
#         category_data = self.hass.data[DOMAIN_DATA].get(self._category, {})
#         balance = category_data.get("balance", 0)
#         budgeted = category_data.get("budgeted", 0)
#         self._state = balance > budgeted
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def is_on(self):
#         return self._state
#
#     @property
#     def device_class(self):
#         return self._device_class
#
#     @property
#     def icon(self):
#         return ICON
