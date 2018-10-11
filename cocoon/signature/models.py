from django.db import models

# Cocoon modules
from cocoon.userAuth.models import MyUser


class HunterDocManagerModel(models.Model):
    user = models.OneToOneField(MyUser, related_name="doc_manager", on_delete=models.CASCADE)

    def is_all_signed(self):
        if HunterDocTemplateModel.objects.count() != self.documents.count():
            return False
        pass


class HunterDocTemplateModel(models.Model):
    template_id = models.CharField(max_length=200)


class HunterDocModel(models.Model):
    doc_manager = models.ForeignKey(HunterDocManagerModel, related_name="documents", on_delete=models.CASCADE)
    template = models.ForeignKey(HunterDocTemplateModel, related_name="documents", on_delete=models.CASCADE)
    is_signed = models.BooleanField(default=False)
    envelope_id = models.CharField(max_length=200)

    def check_signed(self):
        pass
