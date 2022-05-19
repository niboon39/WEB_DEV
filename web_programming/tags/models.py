from django.db import models
# from store.models import Product  อย่า import เเบบนี้เพราะในอนาคตอาจไม่ได้มีเเค่ product
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:   #show title name of object
        return self.label
    
    class Meta:                 #sorting by title name
        ordering = ['label']

class TaggedItem(models.Model):
    #what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product) #not work
    # Type (Product, Video, Article) 
    # ID       
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
