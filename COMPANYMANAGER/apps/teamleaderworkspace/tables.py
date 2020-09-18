from .models import *
import django_tables2 as tables

class ReferenceAppliedTable(tables.Table):
    class Meta:
        model = ReferenceApplied
        exclude = [
            'id',
            'last_work',
            'date_work',
        ]
        attrs = {
            'class' : "table" 
        }
        sequence = ('tech', 'reference', 'qty', 'job')
        row_attrs = {
            'th' : { 'class': 'orderable col-md-4'},
        }