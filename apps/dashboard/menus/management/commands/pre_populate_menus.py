from django.core.management.base import BaseCommand
from apps.dashboard.menus.models import MenuNode


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = [
            {
                'children': [
                    {
                        'children': [
                            {
                                'children': [
                                    {
                                        'data': {
                                            'name': u'Leaflets',
                                            'url': u'/catalogue/category/leaflets_16/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Promotional',
                                            'url': u'/catalogue/category/promotional_64/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Brochures',
                                            'url': u'/catalogue/category/brochures_65/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Popular',
                                            'url': u'/catalogue/category/popular_104/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Flat Sheets',
                                            'url': u'/catalogue/category/flat-sheets_69/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Digital Posters',
                                            'url': u'/catalogue/category/digital-posters_109/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Paper Stickets',
                                            'url': u'/catalogue/category/paper-stickers_110/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Wedding Stationery',
                                            'url': u'/catalogue/category/wedding-stationery_67/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Funeral Stationery',
                                            'url': u'/catalogue/category/funeral-stationery_68/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Business Stationery',
                                            'url': u'/catalogue/category/business-stationery_112/'
                                        },
                                    }
                                ],
                                'data': {
                                    'name': u'Most popular',
                                    'url': u''}
                            }
                        ],
                        'data': {
                            'name': u'Column 1',
                            'url': u''
                        }
                    },
                    {
                        'children': [
                            {
                                'children': [
                                    {
                                        'data': {
                                            'name': u'Boards',
                                            'url': u'/catalogue/category/boards_36/'
                                        }
                                    },
                                    {
                                        'data': {
                                            'name': u'Banners',
                                            'url': u'/catalogue/category/banners_41/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Posters',
                                            'url': u'/catalogue/category/posters_74/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Architectural Plan Drawings',
                                            'url': u'/catalogue/category/architectural-plan-drawings_77/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Self Adhesive VInyl',
                                            'url': u'/catalogue/category/self-adhesive-vinyl_78/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Printed & Contour Cut Self Adhesive Vinyl',
                                            'url': u'/catalogue/category/printed-contour-cut-self-adhesive-vinyl_79/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Printed Static Cling',
                                            'url': u'/catalogue/category/printed-static-cling_81/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Printed & Contour Cut One Way Vision',
                                            'url': u'/catalogue/category/printed-contour-cut-one-way-vision_84/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Frosted WIndow Vinyl',
                                            'url': u'/catalogue/category/frosted-window-vinyl_85/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Frosted Window Vinyl Contour Cut',
                                            'url': u'/catalogue/category/frosted-window-vinyl-contour-cut_86/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Printed Magnetic Vinyl',
                                            'url': u'/catalogue/category/printed-magnetic-vinyl_87/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Contour Cut Sign Vinyl',
                                            'url': u'/catalogue/category/contour-cut-sign-vinyl_88/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Vehicle Livery',
                                            'url': u'/catalogue/category/vehicle-livery_90/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Wall Paper',
                                            'url': u'/catalogue/category/wall-paper_91/'
                                        },
                                    },
                                    {
                                        'data': {
                                            'name': u'Bespoke',
                                            'url': u'/catalogue/category/bespoke_92/'
                                        },
                                    }
                                ],
                                'data': {
                                    'name': u'Indoor',
                                    'url': u''
                                },
                            }
                        ],
                        'data': {
                            'name': u'Column 2',
                            'url': u''
                        },
                    },
                    {
                        'children': [
                            {
                                'children': [
                                    {
                                        'data': {
                                            'name': u'Indoor Display',
                                            'url': u'/catalogue/category/indoor-display_57/'
                                        },
                                    },
                                    {
                                        'data':
                                        {
                                            'name': u'Outdoor Display',
                                            'url': u'/catalogue/category/outdoor-display_56/'
                                        },
                                    }
                                ],
                                'data': {
                                    'name': u'Outdoors',
                                    'url': u''
                                },
                            }
                        ],
                        'data': {
                            'name': u'Column 3',
                            'url': u''
                        },
                    },
                    {
                        'children': [
                            {
                                'children': [
                                    {
                                        'data': {
                                            'name': u'Accessories',
                                            'url': u'/catalogue/category/accessories_94/'
                                        },
                                    }
                                ],
                                'data': {
                                    'name': u'Posters',
                                    'url': u''
                                },
                            },
                            {
                                'children': [
                                    {
                                        'data': {
                                            'name': u'Design',
                                            'url': u'/catalogue/category/design_108/'
                                        },
                                    }
                                ],
                                'data': {
                                    'name': u'Vinyl',
                                    'url': u''
                                },
                            }
                        ],
                        'data': {
                            'name': u'Column 4',
                            'url': u''
                        },
                    }
                ],
                'data': {
                    'name': u'Products menu',
                    'url': u''
                },
            },

            {
                'children': [
                    {
                        'children': [
                            {
                                'data': {
                                    'name': u'Leaflets',
                                    'url': u'/catalogue/category/leaflets_16/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Promotional',
                                    'url': u'/catalogue/category/promotional_64/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Brochures',
                                    'url': u'/catalogue/category/brochures_65/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Popular',
                                    'url': u'/catalogue/category/popular_104/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Flat Sheets',
                                    'url': u'/catalogue/category/flat-sheets_69/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Digital Posters',
                                    'url': u'/catalogue/category/digital-posters_109/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Paper Stickets',
                                    'url': u'/catalogue/category/paper-stickers_110/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Wedding Stationery',
                                    'url': u'/catalogue/category/wedding-stationery_67/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Funeral Stationery',
                                    'url': u'/catalogue/category/funeral-stationery_68/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Business Stationery',
                                    'url': u'/catalogue/category/business-stationery_112/'
                                },
                            }
                        ],
                        'data': {
                            'name': u'Most popular',
                            'url': u''
                        }
                    },
                    {
                        'children': [
                            {
                                'data': {
                                    'name': u'Boards',
                                    'url': u'/catalogue/category/boards_36/'
                                }
                            },
                            {
                                'data': {
                                    'name': u'Banners',
                                    'url': u'/catalogue/category/banners_41/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Posters',
                                    'url': u'/catalogue/category/posters_74/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Architectural Plan Drawings',
                                    'url': u'/catalogue/category/architectural-plan-drawings_77/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Self Adhesive VInyl',
                                    'url': u'/catalogue/category/self-adhesive-vinyl_78/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Printed & Contour Cut Self Adhesive Vinyl',
                                    'url': u'/catalogue/category/printed-contour-cut-self-adhesive-vinyl_79/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Printed Static Cling',
                                    'url': u'/catalogue/category/printed-static-cling_81/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Printed & Contour Cut One Way Vision',
                                    'url': u'/catalogue/category/printed-contour-cut-one-way-vision_84/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Frosted WIndow Vinyl',
                                    'url': u'/catalogue/category/frosted-window-vinyl_85/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Frosted Window Vinyl Contour Cut',
                                    'url': u'/catalogue/category/frosted-window-vinyl-contour-cut_86/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Printed Magnetic Vinyl',
                                    'url': u'/catalogue/category/printed-magnetic-vinyl_87/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Contour Cut Sign Vinyl',
                                    'url': u'/catalogue/category/contour-cut-sign-vinyl_88/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Vehicle Livery',
                                    'url': u'/catalogue/category/vehicle-livery_90/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Wall Paper',
                                    'url': u'/catalogue/category/wall-paper_91/'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Bespoke',
                                    'url': u'/catalogue/category/bespoke_92/'
                                },
                            }
                        ],
                        'data': {
                            'name': u'Indoor',
                            'url': u''
                        },
                    },
                    {
                        'children': [
                            {
                                'data': {
                                    'name': u'Indoor Display',
                                    'url': u'/catalogue/category/indoor-display_57/'
                                },
                            },
                            {
                                'data':
                                {
                                    'name': u'Outdoor Display',
                                    'url': u'/catalogue/category/outdoor-display_56/'
                                },
                            }
                        ],
                        'data': {
                            'name': u'Outdoors',
                            'url': u''
                        },
                    },
                    {
                        'children': [
                            {
                                'data': {
                                    'name': u'Accessories',
                                    'url': u'/catalogue/category/accessories_94/'
                                },
                            }
                        ],
                        'data': {
                            'name': u'Posters',
                            'url': u''
                        },
                    },
                    {
                        'children': [
                            {
                                'data': {
                                    'name': u'Design',
                                    'url': u'/catalogue/category/design_108/'
                                },
                            }
                        ],
                        'data': {
                            'name': u'Vinyl',
                            'url': u''
                        },
                    }
                ],
                'data': {
                    'name': u'Side menu',
                    'url': u''
                },
            },
            {
                'children': [
                    {
                        'children': [
                            {
                                'data': {
                                    'name': u'Who are we',
                                    'url': u'#'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Our Terms & Conditions',
                                    'url': u'#'
                                },
                            },
                            {
                                'data': {
                                    'name': u'The Prizmatic Team',
                                    'url': u'#'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Our Address',
                                    'url': u'#'
                                },
                            }
                        ],
                        'data': {
                            'name': u'First Area',
                            'url': u''
                        },
                    },
                    {
                        'children': [
                            {
                                'data': {
                                    'name': u'Which link is this',
                                    'url': u'#'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Link Item',
                                    'url': u'#'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Link Item',
                                    'url': u'#'
                                },
                            }
                        ],
                        'data': {
                            'name': u'Title Sample',
                            'url': u''
                        },
                    },
                    {
                        'children': [
                            {
                                'data': {
                                    'name': u'Link Item',
                                    'url': u'#'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Link Item',
                                    'url': u'#'
                                },
                            },
                            {
                                'data': {
                                    'name': u'Link Item',
                                    'url': u'#'
                                },
                            }
                        ],
                        'data': {
                            'name': u'Title Sample',
                            'url': u''
                        },
                    }
                ],
                'data': {
                    'name': u'Footer menu',
                    'url': u''
                },
            }
        ]
        MenuNode.load_bulk(data)
