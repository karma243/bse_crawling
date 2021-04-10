import json
from enum import Enum


class Direction(Enum):
    UP = 1,
    DOWN = 2


class CrossOver:
    def __init__(self, index, direction: Direction):
        self.index = index
        self.direction = direction


class CrossOverGenerator:
    def __init__(self, data_series: list, smaller_window: int, large_window: int):
        self.data_series = data_series
        self.smaller_window = smaller_window
        self.large_window = large_window
        self.staring_index = large_window - 1
        if large_window <= smaller_window:
            raise Exception("larger window must be larger than smaller window")

    @staticmethod
    def avg_function(data_series, window_size):
        smoothing_factor = 2

        avg_series = [None] * window_size
        yesterday_avg = sum(data_series[:window_size]) / window_size
        for index in range(window_size, len(data_series)):
            today_val = data_series[index]
            today_avg = (today_val * (smoothing_factor / (1 + window_size))) \
                        + yesterday_avg * (1 - (smoothing_factor / (1 + window_size)))
            avg_series.append(today_avg)
            yesterday_avg = today_avg

        return avg_series

    def find_cross_overs(self):
        result = []
        moving_avg_diff = self.find_moving_avg_diff()
        for index in range(self.large_window + 1, len(moving_avg_diff)):
            prev_diff = moving_avg_diff[index - 1]
            cur_diff = moving_avg_diff[index]
            if prev_diff > 0 and cur_diff > 0 or prev_diff < 0 and cur_diff < 0:
                continue
            elif prev_diff > 0:
                result.append(CrossOver(index, Direction.DOWN))
            else:
                result.append(CrossOver(index, Direction.UP))
        return result

    def find_moving_avg_diff(self) -> list:
        # return [(index, self.avg_diff_for_index(index)) for index in range(self.staring_index, len(self.data_series))]
        larger_moving_avg = self.avg_function(self.data_series, self.large_window)
        smaller_moving_avg = self.avg_function(self.data_series, self.smaller_window)
        result = [None] * self.large_window

        for index in range(self.large_window + 1, len(self.data_series)):
            result.append(smaller_moving_avg[index] - larger_moving_avg[index])
        return result



    def avg_diff_for_index(self, index):
        small_window, large_window = self.window_entries(index)
        small_avg = self.avg_func(small_window)
        large_avg = self.avg_func(large_window)
        avg_diff = small_avg - large_avg
        return avg_diff

    def window_entries(self, end_pos):
        large_window = self.data_series[end_pos - (self.large_window - 1): end_pos]
        small_window = self.data_series[end_pos - (self.smaller_window - 1): end_pos]
        return small_window, large_window


class MovingAvgTradeSimulator:
    def __init__(self, file_name, smaller_window, larger_window):
        self.file_name = file_name
        self.smaller_window = smaller_window
        self.larger_window = larger_window

    def kite_series(self):
        file_name_prefix = "/data/kite_websocket_data/historical/"
        with open(file_name_prefix + self.file_name) as handle:
            series = json.load(handle)
        return list(map(lambda tup: (tup[0], tup[1]), series))

    def print_cross_overs(self):
        date_open_series = self.kite_series()
        price_series = list(map(lambda tup: tup[1], date_open_series))
        cross_overs = CrossOverGenerator(price_series, self.smaller_window, self.larger_window).find_cross_overs()
        for cross in cross_overs:
            index = cross.index
            direction = cross.direction
            print("{}: price: {} \t direction from {} to {}".format(
                date_open_series[index][0], price_series[index],
                Direction.UP if direction is Direction.DOWN else Direction.DOWN, direction))

class TradeSimulator:
    def __init__(self, cross_overs):
        self.cross_overs = cross_overs

if __name__ == '__main__':
    file_name = "ADANIPORTS_3861249.json"

    MovingAvgTradeSimulator(file_name, 3, 21).print_cross_overs()
