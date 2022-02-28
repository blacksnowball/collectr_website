from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(Item)
admin.site.register(Collection)
admin.site.register(ReputationFeedback)
admin.site.register(Trade)
admin.site.register(TradeAttachment)
admin.site.register(UserCollectsItem)
admin.site.register(NewCollectionRequest)
admin.site.register(NewItemRequest)


