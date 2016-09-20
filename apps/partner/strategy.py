from oscar.apps.partner import strategy, availability


class Selector(object):
    """
    Custom selector to return a UK-specific strategy that charges VAT
    """

    def strategy(self, request=None, user=None, **kwargs):
        return Strategy()


class StockAndDeliveryOptionRequired(strategy.StockRequired):
    def availability_policy(self, product, stockrecord):
        try: #TODO check if delivery_options exist normally
            if not product.delivery_options.is_available:
                return availability.Unavailable()
        except:
            pass
        return super(StockAndDeliveryOptionRequired, self).availability_policy(product, stockrecord)


class Strategy(strategy.UseFirstStockRecord, strategy.NoTax, StockAndDeliveryOptionRequired, strategy.Structured):
    pass