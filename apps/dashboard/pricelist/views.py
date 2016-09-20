from django.shortcuts import render
from oscar.views.decorators import staff_member_required

from utils import ExcelImporter
from apps.dashboard.pricelist.forms import PricelistUploadForm, ProductsUploadForm

@staff_member_required
def import_pricelist(request):
    if request.method == 'POST':
        form = PricelistUploadForm(request.POST, request.FILES)

        importer = ExcelImporter(type=request.POST['vehicle'])

        if form.is_valid():
            report = importer.import_file(request.FILES['csvfile'])
            return render(request, 'pricelist/importerrors.html',
                              {'report': report, 'type': 'search_fields'})
    else:
        form = PricelistUploadForm()

    return render(request, 'pricelist/import.html', {
        'form': form,
        'title': 'Import search fields',
    })


@staff_member_required
def import_products(request):
    if request.method == 'POST':
        form = ProductsUploadForm(request.POST, request.FILES)

        importer = ExcelImporter(partner=request.POST['partner'])

        if form.is_valid():
            report = importer.import_products(request.FILES['csvfile'], update=form.cleaned_data['update_if_already_exists'])
            return render(request, 'pricelist/importerrors.html',
                              {'report': report, 'type': 'products'})
    else:
        form = ProductsUploadForm()

    return render(request, 'pricelist/import.html', {
        'form': form,
        'title': 'Import products',
    })
