from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Supplier)
admin.site.register(Film)
admin.site.register(Package)
admin.site.register(Cut)
admin.site.register(WorkshopJob)
admin.site.register(Packer)
admin.site.register(StockFilmHistory)
admin.site.register(StockFilm)
admin.site.register(LayoutPlan)
admin.site.register(WasteWorkshop)
admin.site.register(FilmReel)
admin.site.register(StockWorkshop)
admin.site.register(StockHistoryWorkshop)
admin.site.register(Printer)