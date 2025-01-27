import json
from enum import Enum
from market_tick import MarketTickEntity


class IndicatorDirection(Enum):
    POSITIVE = 1
    NEGATIVE = 2
    POSITIVE_SUSTAINED = 3
    NEGATIVE_SUSTAINED = 4
    NOT_ANALYZED = 5


class IndicatorIntensity(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class PositionStrategy(Enum):
    MovingAvg = 1
    DEMA = 2
    MACD = 3
    NONE = 4
    CUSTOM_MACD = 5


class Opportunity:
    def __init__(self, market_event: MarketTickEntity, direction: IndicatorDirection, intensity: IndicatorIntensity,
                 attrs=None):
        self.intensity = intensity
        self.direction = direction
        self.market_event = market_event
        self.attrs = attrs

    def __str__(self):
        return json.dumps({
            "intensity": self.intensity.name,
            "direction": self.direction.name if self.direction else None,
            "market_event": self.market_event.raw_json(),
            "attrs": self.attrs
        })
