from django.forms import BooleanField, ModelForm

from recipient.models import Recipient


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipient
        fields = "__all__"
        exclude = ["owner"]
