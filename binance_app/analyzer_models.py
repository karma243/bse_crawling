from enum import Enum
from market_entity import MarketTickEntity


class IndicatorDirection(Enum):
    POSITIVE = 1
    NEGATIVE = 2
    POSITIVE_SUSTAINED = 3
    NEGATIVE_SUSTAINED = 4


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


class Opportunity:
    def __init__(self, market_event: MarketTickEntity, direction: IndicatorDirection,
                 intensity: IndicatorIntensity):
        self.intensity = intensity
        self.direction = direction
        self.market_event = market_event

