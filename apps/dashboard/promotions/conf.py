from oscar.core.loading import get_class

SingleProduct = get_class('promotions.models', 'SingleProduct')
RawHTML = get_class('promotions.models', 'RawHTML')
Image = get_class('promotions.models', 'Image')
PagePromotion = get_class('promotions.models', 'PagePromotion')
AutomaticProductList = get_class('promotions.models', 'AutomaticProductList')
HandPickedProductList = get_class('promotions.models', 'HandPickedProductList')
MultiImage = get_class('promotions.models', 'MultiImage')
MultiHTML = get_class('promotions.models', 'MultiHTML')


def get_promotion_classes():
    return (RawHTML, Image, SingleProduct, AutomaticProductList,
            HandPickedProductList, MultiImage, MultiHTML)


PROMOTION_CLASSES = get_promotion_classes()
