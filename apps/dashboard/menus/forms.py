from treebeard.forms import movenodeform_factory

from .models import MenuNode


MenuNodeForm = movenodeform_factory(
    MenuNode,
    fields=['name', 'url']
)
