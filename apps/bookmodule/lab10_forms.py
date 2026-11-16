from django import forms
from .models import Book


class BookModelForm(forms.ModelForm):
    """
    Django ModelForm used in Lab 10 Part 2.
    fields = "__all__" keeps the form synchronized with the Book model
    created in the previous labs (including its Lab 9 fields/relations).
    """

    class Meta:
        model = Book
        fields = "__all__"
        widgets = {
            "pubdate": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make optional relation fields easier to use when the database
        # does not contain any related records yet.
        for name, field in self.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                field.required = False
                field.empty_label = "---------"
            elif isinstance(field, forms.ModelMultipleChoiceField):
                field.required = False
