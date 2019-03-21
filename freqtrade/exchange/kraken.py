""" Kraken exchange subclass """
import logging
from typing import Dict

from freqtrade import OperationalException
from freqtrade.exchange import Exchange

logger = logging.getLogger(__name__)


class Kraken(Exchange):

    _params: Dict = {"trading_agreement": "agree"}

    def stoploss_limit(self, pair: str, amount: float, stop_price: float, rate: float) -> Dict:
        """
        Creates a stoploss limit order.

        :param pair (str): the pair for which the order should be placed
        :param amount (float): the amount to sell
        :param stop_price (float): stop loss trigger price
        :param rate (float): triggered limit price
        :returns (dict): the order dictionary returned by the API
        """
        ordertype = "stop-loss-limit"

        stop_price = self.symbol_price_prec(pair, stop_price)

        # Ensure rate is less than stop price
        if stop_price <= rate:
            raise OperationalException(
                "In stoploss limit order, stop price should be more than limit price")

        if self._config["dry_run"]:
            dry_order = self.dry_run_order(
                pair, ordertype, "sell", amount, stop_price)
            return dry_order

        params = self._params.copy()
        params.update({"price2": rate})

        order = self.create_order(pair, ordertype, "sell", amount, stop_price, params)
        logger.info(f"stoploss limit order added for {pair}. "
                    f"stop price: {stop_price}. limit: {rate}")
        return order
