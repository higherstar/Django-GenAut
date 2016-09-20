from .models import MenuNode


def menus_processor(request):
    return {'menus': MenuNode.get_root_nodes()}
