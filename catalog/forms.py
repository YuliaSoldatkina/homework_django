from django import forms

from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(
                    f"Название не должно содержать запрещённое слово: {word}"
                )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(
                    f"Описание не должно содержать запрещённое слово: {word}"
                )
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "image":
                field.widget.attrs.update(
                    {
                        "class": "form-control",
                    }
                )
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update(
                    {
                        "class": "form-check-input",
                    }
                )
            else:
                field.widget.attrs.update(
                    {
                        "class": "form-control",
                    }
                )
