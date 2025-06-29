from django.forms import ModelForm, BooleanField

from message.models import Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        exclude = ["owner"]
