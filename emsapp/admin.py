from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Customer, BankAccount, CryptoTransaction, GiftCardTransaction
from datetime import datetime, timedelta
from django.db.models import Sum


############### FOR USER ACCOUNTS ####################
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)



########### FOR CUSTOMER TABLES AND BANK INFO ##################
class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1


################# FOR FILTER (START)


class TodayCryptoTradedFilter(admin.SimpleListFilter):
    title = 'Crypto traded today'
    parameter_name = 'crypto_traded_today'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now().date()
            # Filter customers based on today's crypto transactions
            return queryset.filter(
                phone_number__in=CryptoTransaction.objects.filter(timestamp__date=today).values_list('customer__phone_number', flat=True)
            )
        return queryset

class ThisMonthCryptoTradedFilter(admin.SimpleListFilter):
    title = 'Crypto traded this month'
    parameter_name = 'crypto_traded_month'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now().date()
            start_of_month = today.replace(day=1)
            # Filter customers based on this month's crypto transactions
            return queryset.filter(
                phone_number__in=CryptoTransaction.objects.filter(timestamp__date__gte=start_of_month).values_list('customer__phone_number', flat=True)
            )
        return queryset

class ThisYearCryptoTradedFilter(admin.SimpleListFilter):
    title = 'Crypto traded this year'
    parameter_name = 'crypto_traded_year'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now().date()
            start_of_year = today.replace(month=1, day=1)
            # Filter customers based on this year's crypto transactions
            return queryset.filter(
                phone_number__in=CryptoTransaction.objects.filter(timestamp__date__gte=start_of_year).values_list('customer__phone_number', flat=True)
            )
        return queryset





class CryptoTradedTodayFilter(admin.SimpleListFilter):
    title = 'Crypto Traded Today'
    parameter_name = 'crypto_traded_today'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Traded Today'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now().date()
            return queryset.filter(cryptotransaction__timestamp__date=today)
        return queryset

class TodayGiftCardTradedFilter(admin.SimpleListFilter):
    title = 'GiftCards Traded Today'
    parameter_name = 'giftcard_traded_today'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Traded Today'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now().date()
            return queryset.filter(
                phone_number__in=GiftCardTransaction.objects.filter(timestamp__date=today).values('customer__phone_number')
            ).order_by('-giftcardtransaction__timestamp')
        return queryset


class ThisMonthGiftCardTradedFilter(admin.SimpleListFilter):
    title = 'GiftCards Traded This Month'
    parameter_name = 'giftcard_traded_month'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Traded This Month'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now()
            start_of_month = today.replace(day=1)
            return queryset.filter(
                phone_number__in=GiftCardTransaction.objects.filter(timestamp__gte=start_of_month).values('customer__phone_number')
            ).order_by('-giftcardtransaction__timestamp')
        return queryset


class ThisYearGiftCardTradedFilter(admin.SimpleListFilter):
    title = 'GiftCards Traded This Year'
    parameter_name = 'giftcard_traded_year'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Traded This Year'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now()
            start_of_year = today.replace(month=1, day=1)
            return queryset.filter(
                phone_number__in=GiftCardTransaction.objects.filter(timestamp__gte=start_of_year).values('customer__phone_number')
            ).order_by('-giftcardtransaction__timestamp')
        return queryset


class TodayTotalAssetsTradedFilter(admin.SimpleListFilter):
    title = 'Total Assets Traded Today'
    parameter_name = 'total_assets_traded_today'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Traded Today'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now().date()
            crypto_today = CryptoTransaction.objects.filter(timestamp__date=today).values('customer__phone_number')
            giftcard_today = GiftCardTransaction.objects.filter(timestamp__date=today).values('customer__phone_number')
            return queryset.filter(
                phone_number__in=crypto_today.union(giftcard_today)
            ).order_by('-cryptotransaction__timestamp', '-giftcardtransaction__timestamp')
        return queryset


class ThisMonthTotalAssetsTradedFilter(admin.SimpleListFilter):
    title = 'Total Assets Traded This Month'
    parameter_name = 'total_assets_traded_month'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Traded This Month'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now()
            start_of_month = today.replace(day=1)
            crypto_this_month = CryptoTransaction.objects.filter(timestamp__gte=start_of_month).values('customer__phone_number')
            giftcard_this_month = GiftCardTransaction.objects.filter(timestamp__gte=start_of_month).values('customer__phone_number')
            return queryset.filter(
                phone_number__in=crypto_this_month.union(giftcard_this_month)
            ).order_by('-cryptotransaction__timestamp', '-giftcardtransaction__timestamp')
        return queryset


class ThisYearTotalAssetsTradedFilter(admin.SimpleListFilter):
    title = 'Total Assets Traded This Year'
    parameter_name = 'total_assets_traded_year'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Traded This Year'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.now()
            start_of_year = today.replace(month=1, day=1)
            crypto_this_year = CryptoTransaction.objects.filter(timestamp__gte=start_of_year).values('customer__phone_number')
            giftcard_this_year = GiftCardTransaction.objects.filter(timestamp__gte=start_of_year).values('customer__phone_number')
            return queryset.filter(
                phone_number__in=crypto_this_year.union(giftcard_this_year)
            ).order_by('-cryptotransaction__timestamp', '-giftcardtransaction__timestamp')
        return queryset



########### FILTERS ENDS








""" class CustomerAdmin(admin.ModelAdmin):
    inlines = [BankAccountInline]
    list_display = ('surname', 'othernames', 'gender', 'mobile_number', 'phone_number', 'joined_date')
    search_fields = ('surname', 'othernames', 'mobile_number', 'phone_number')
    list_filter = ('gender', 'joined_date') """


""" class CustomerAdmin(admin.ModelAdmin):
    inlines = [BankAccountInline]
    list_display = ('surname', 'othernames', 'gender', 'mobile_number', 'phone_number', 'joined_date', 'crypto_traded_today', 'crypto_traded_this_month', 'crypto_traded_this_year', 'giftcard_traded_today', 'giftcard_traded_this_month', 'giftcard_traded_this_year', 'total_assets_traded_today', 'total_assets_traded_this_month', 'total_assets_traded_this_year')
    search_fields = ('surname', 'othernames', 'mobile_number', 'phone_number')
    list_filter = ('gender',
                   'joined_date',
                   TodayTotalAssetsTradedFilter, 
                   ThisMonthTotalAssetsTradedFilter, 
                   ThisYearTotalAssetsTradedFilter,
                   TodayCryptoTradedFilter, 
                   #CryptoTradedTodayFilter, 
                   ThisMonthCryptoTradedFilter, 
                   ThisYearCryptoTradedFilter,
                   TodayGiftCardTradedFilter, 
                   ThisMonthGiftCardTradedFilter, 
                   ThisYearGiftCardTradedFilter,
                   )
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)
        first_day_of_year = today.replace(month=1, day=1)

        queryset = queryset.annotate(
            crypto_traded_today=Sum(
                'cryptotransaction__total_amount_paid',
                filter=CryptoTransaction.objects.filter(timestamp__date=today)
            ),
            crypto_traded_this_month=Sum(
                'cryptotransaction__total_amount_paid',
                filter=CryptoTransaction.objects.filter(timestamp__date__gte=first_day_of_month)
            ),
            crypto_traded_this_year=Sum(
                'cryptotransaction__total_amount_paid',
                filter=CryptoTransaction.objects.filter(timestamp__date__gte=first_day_of_year)
            ),
            giftcard_traded_today=Sum(
                'giftcardtransaction__total_amount_paid',
                filter=GiftCardTransaction.objects.filter(timestamp__date=today)
            ),
            giftcard_traded_this_month=Sum(
                'giftcardtransaction__total_amount_paid',
                filter=GiftCardTransaction.objects.filter(timestamp__date__gte=first_day_of_month)
            ),
            giftcard_traded_this_year=Sum(
                'giftcardtransaction__total_amount_paid',
                filter=GiftCardTransaction.objects.filter(timestamp__date__gte=first_day_of_year)
            ),
            total_assets_traded_today=Sum(
                'cryptotransaction__total_amount_paid',
                filter=CryptoTransaction.objects.filter(timestamp__date=today)
            ) + Sum(
                'giftcardtransaction__total_amount_paid',
                filter=GiftCardTransaction.objects.filter(timestamp__date=today)
            ),
            total_assets_traded_this_month=Sum(
                'cryptotransaction__total_amount_paid',
                filter=CryptoTransaction.objects.filter(timestamp__date__gte=first_day_of_month)
            ) + Sum(
                'giftcardtransaction__total_amount_paid',
                filter=GiftCardTransaction.objects.filter(timestamp__date__gte=first_day_of_month)
            ),
            total_assets_traded_this_year=Sum(
                'cryptotransaction__total_amount_paid',
                filter=CryptoTransaction.objects.filter(timestamp__date__gte=first_day_of_year)
            ) + Sum(
                'giftcardtransaction__total_amount_paid',
                filter=GiftCardTransaction.objects.filter(timestamp__date__gte=first_day_of_year)
            )
        )
        return queryset

    

    def get_ordering(self, request):
        # You can return a tuple based on a condition
        return ('surname',)



    def crypto_traded_today(self, obj):
        return obj.crypto_traded_today()
    crypto_traded_today.short_description = 'Crypto Traded Today'
    crypto_traded_today.admin_order_field = 'crypto_traded_today'

    def crypto_traded_this_month(self, obj):
        return obj.crypto_traded_this_month()
    crypto_traded_this_month.short_description = 'Crypto Traded This Month'
    crypto_traded_this_month.admin_order_field = 'crypto_traded_this_month'

    def crypto_traded_this_year(self, obj):
        return obj.crypto_traded_this_year()
    crypto_traded_this_year.short_description = 'Crypto Traded This Year'
    crypto_traded_this_year.admin_order_field = 'crypto_traded_this_year'

    def giftcard_traded_today(self, obj):
        return obj.giftcard_traded_today()
    giftcard_traded_today.short_description = 'GiftCard Traded Today'
    giftcard_traded_today.admin_order_field = 'giftcard_traded_today'

    def giftcard_traded_this_month(self, obj):
        return obj.giftcard_traded_this_month()
    giftcard_traded_this_month.short_description = 'GiftCard Traded This Month'
    giftcard_traded_this_month.admin_order_field = 'giftcard_traded_this_month'

    def giftcard_traded_this_year(self, obj):
        return obj.giftcard_traded_this_year()
    giftcard_traded_this_year.short_description = 'GiftCard Traded This Year'
    giftcard_traded_this_year.admin_order_field = 'giftcard_traded_this_year'

    def total_assets_traded_today(self, obj):
        return obj.total_assets_traded_today()
    total_assets_traded_today.short_description = 'Total Assets Traded Today'
    total_assets_traded_today.admin_order_field = 'total_assets_traded_today'

    def total_assets_traded_this_month(self, obj):
        return obj.total_assets_traded_this_month()
    total_assets_traded_this_month.short_description = 'Total Assets Traded This Month'
    total_assets_traded_this_month.admin_order_field = 'total_assets_traded_this_month'

    def total_assets_traded_this_year(self, obj):
        return obj.total_assets_traded_this_year()
    total_assets_traded_this_year.short_description = 'Total Assets Traded This Year'
    total_assets_traded_this_year.admin_order_field = 'total_assets_traded_this_year'
 """



from django.db.models import Sum, Case, When, Value, IntegerField

class CustomerAdmin(admin.ModelAdmin):
    inlines = [BankAccountInline]
    list_display = ('surname', 'othernames', 'gender', 'mobile_number', 'phone_number', 'joined_date', 
                    'crypto_traded_today', 'crypto_traded_this_month', 'crypto_traded_this_year', 
                    'giftcard_traded_today', 'giftcard_traded_this_month', 'giftcard_traded_this_year', 
                    'total_assets_traded_today', 'total_assets_traded_this_month', 'total_assets_traded_this_year')
    search_fields = ('surname', 'othernames', 'mobile_number', 'phone_number')
    list_filter = ('gender', 'joined_date', 
                   TodayTotalAssetsTradedFilter, ThisMonthTotalAssetsTradedFilter, ThisYearTotalAssetsTradedFilter,
                   TodayCryptoTradedFilter, ThisMonthCryptoTradedFilter, ThisYearCryptoTradedFilter,
                   TodayGiftCardTradedFilter, ThisMonthGiftCardTradedFilter, ThisYearGiftCardTradedFilter)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)
        first_day_of_year = today.replace(month=1, day=1)

        queryset = queryset.annotate(
            crypto_traded_today=Sum(
                Case(
                    When(cryptotransaction__timestamp__date=today, then='cryptotransaction__total_amount_paid'),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            crypto_traded_this_month=Sum(
                Case(
                    When(cryptotransaction__timestamp__date__gte=first_day_of_month, then='cryptotransaction__total_amount_paid'),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            crypto_traded_this_year=Sum(
                Case(
                    When(cryptotransaction__timestamp__date__gte=first_day_of_year, then='cryptotransaction__total_amount_paid'),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            giftcard_traded_today=Sum(
                Case(
                    When(giftcardtransaction__timestamp__date=today, then='giftcardtransaction__total_amount_paid'),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            giftcard_traded_this_month=Sum(
                Case(
                    When(giftcardtransaction__timestamp__date__gte=first_day_of_month, then='giftcardtransaction__total_amount_paid'),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            giftcard_traded_this_year=Sum(
                Case(
                    When(giftcardtransaction__timestamp__date__gte=first_day_of_year, then='giftcardtransaction__total_amount_paid'),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ),
            total_assets_traded_today=(
                Sum(
                    Case(
                        When(cryptotransaction__timestamp__date=today, then='cryptotransaction__total_amount_paid'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ) + Sum(
                    Case(
                        When(giftcardtransaction__timestamp__date=today, then='giftcardtransaction__total_amount_paid'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                )
            ),
            total_assets_traded_this_month=(
                Sum(
                    Case(
                        When(cryptotransaction__timestamp__date__gte=first_day_of_month, then='cryptotransaction__total_amount_paid'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ) + Sum(
                    Case(
                        When(giftcardtransaction__timestamp__date__gte=first_day_of_month, then='giftcardtransaction__total_amount_paid'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                )
            ),
            total_assets_traded_this_year=(
                Sum(
                    Case(
                        When(cryptotransaction__timestamp__date__gte=first_day_of_year, then='cryptotransaction__total_amount_paid'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                ) + Sum(
                    Case(
                        When(giftcardtransaction__timestamp__date__gte=first_day_of_year, then='giftcardtransaction__total_amount_paid'),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                )
            )
        )
        return queryset

    def crypto_traded_today(self, obj):
        return obj.crypto_traded_today
    crypto_traded_today.short_description = 'Crypto Traded Today'
    crypto_traded_today.admin_order_field = 'crypto_traded_today'

    def crypto_traded_this_month(self, obj):
        return obj.crypto_traded_this_month
    crypto_traded_this_month.short_description = 'Crypto Traded This Month'
    crypto_traded_this_month.admin_order_field = 'crypto_traded_this_month'

    def crypto_traded_this_year(self, obj):
        return obj.crypto_traded_this_year
    crypto_traded_this_year.short_description = 'Crypto Traded This Year'
    crypto_traded_this_year.admin_order_field = 'crypto_traded_this_year'

    def giftcard_traded_today(self, obj):
        return obj.giftcard_traded_today
    giftcard_traded_today.short_description = 'GiftCard Traded Today'
    giftcard_traded_today.admin_order_field = 'giftcard_traded_today'

    def giftcard_traded_this_month(self, obj):
        return obj.giftcard_traded_this_month
    giftcard_traded_this_month.short_description = 'GiftCard Traded This Month'
    giftcard_traded_this_month.admin_order_field = 'giftcard_traded_this_month'

    def giftcard_traded_this_year(self, obj):
        return obj.giftcard_traded_this_year
    giftcard_traded_this_year.short_description = 'GiftCard Traded This Year'
    giftcard_traded_this_year.admin_order_field = 'giftcard_traded_this_year'

    def total_assets_traded_today(self, obj):
        return obj.total_assets_traded_today
    total_assets_traded_today.short_description = 'Total Assets Traded Today'
    total_assets_traded_today.admin_order_field = 'total_assets_traded_today'

    def total_assets_traded_this_month(self, obj):
        return obj.total_assets_traded_this_month
    total_assets_traded_this_month.short_description = 'Total Assets Traded This Month'
    total_assets_traded_this_month.admin_order_field = 'total_assets_traded_this_month'

    def total_assets_traded_this_year(self, obj):
        return obj.total_assets_traded_this_year
    total_assets_traded_this_year.short_description = 'Total Assets Traded This Year'
    total_assets_traded_this_year.admin_order_field = 'total_assets_traded_this_year'




admin.site.register(Customer, CustomerAdmin)
admin.site.register(BankAccount)



############ FOR TRANSACTIONS ###################
class CryptoTransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'customer', 'transaction_type', 'coin_type', 'coin_value', 'coin_quantity', 'rate', 'amount', 'bonus', 'total_amount_paid', 'settled')
    list_filter = ('transaction_type', 'coin_type', 'timestamp', 'settled')
    search_fields = ('customer__phone_number', 'transaction_type', 'coin_type')

admin.site.register(CryptoTransaction, CryptoTransactionAdmin)


class GiftCardTransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'customer', 'transaction_type', 'card_type', 'card_value', 'rate', 'amount', 'bonus', 'total_amount_paid', 'settled')
    list_filter = ('transaction_type', 'card_type', 'timestamp', 'settled')
    search_fields = ('customer__phone_number', 'transaction_type', 'card_type')

admin.site.register(GiftCardTransaction, GiftCardTransactionAdmin)