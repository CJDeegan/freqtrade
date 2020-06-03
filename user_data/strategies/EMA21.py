
# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy # noqa


# This class is a sample. Feel free to customize it.
class EMA21(IStrategy):
    __test__ = False  # pytest expects to find tests here because of the name
    """
    This is a test strategy to inspire you.
    More information in https://github.com/freqtrade/freqtrade/blob/develop/docs/bot-optimization.md

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the prototype for the methods: minimal_roi, stoploss, populate_indicators, populate_buy_trend,
    populate_sell_trend, hyperopt_space, buy_strategy_generator
    """

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.15
    }

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.023
    trailing_stop = True
    trailing_only_offset_is_reached = False
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.03


    # Optimal ticker interval for the strategy
    ticker_interval = '1d'

    # run "populate_indicators" only for new candle
    ta_on_candle = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Raw data from the exchange and parsed by parse_ticker_dataframe()
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # EMA - Exponential Moving Average
        dataframe['ema3'] = ta.EMA(dataframe, timeperiod=3)
        dataframe['ema6'] = ta.EMA(dataframe, timeperiod=6)
        dataframe['ema13'] = ta.EMA(dataframe, timeperiod=13)
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (dataframe['ema13'] < dataframe['ema21']) &
                (dataframe['ema3'] > dataframe['ema6'])
                # qtpylib.crossed_above(dataframe['ema3'], dataframe['ema6'])
                # (((dataframe['ema18'] - dataframe['ema36']) / dataframe['ema18']) * 100) > 1.5
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (dataframe['ema3'] < dataframe['ema6'])
            ),
            'sell'] = 1
        return dataframe
