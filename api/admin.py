from django.contrib import admin

from api.models import Dress, DressLoan


class DressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'brand',
        'priceInCents',
        'material',
        'color',
        'size'
    )


class DressLoanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'startDate',
        'endDate',
        'dress_id',
        'user',
        'totalPrice_Euro',
        'loanDurationDays'
    )

    @admin.display()
    def dress_id(self, obj):
        return obj.dress.id

    @admin.display()
    def totalPrice_Euro(self, obj):
        return obj.totalPrice / 100


admin.site.register(Dress, DressAdmin)
admin.site.register(DressLoan, DressLoanAdmin)
