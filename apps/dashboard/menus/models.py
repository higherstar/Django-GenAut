from django.db import models
from treebeard.mp_tree import MP_Node


class MenuNode(MP_Node):
    name = models.CharField(max_length=63, default='', null=False)
    url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
