from colorfield.fields import ColorField
from django import forms
from features.forms import FeatureForm, SpatialFeatureForm
from .models import AOI, WindEnergySite

class AOIForm(SpatialFeatureForm):

    def __init__(self, *args, **kwargs):
        super(AOIForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["color"].widget = forms.widgets.TextInput(
                attrs={"type": "color", "title": "fill color", "value":self.instance.color}
            )
            self.fields['fill_opacity'].widget = forms.widgets.NumberInput(
                attrs={"value": self.instance.fill_opacity, "min": 0.0, "max":1.0, "step":0.1}
            )
            self.fields["stroke_color"].widget = forms.widgets.TextInput(
                attrs={"type": "color", "title": "stroke color", "value":"{}".format(self.instance.stroke_color)}
            )
            self.fields['stroke_width'].widget = forms.widgets.NumberInput(
                attrs={"value": self.instance.stroke_width, "min": 0, "max":10, "step": 1}
            )

    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), required=False)
    color = ColorField(help_text="The color to fill your polygon")
    fill_opacity = forms.FloatField(help_text="0.1 is nearly transparent, 0.9 is 90% opaque")
    stroke_color = ColorField()
    stroke_width = forms.IntegerField()
    
    class Meta(SpatialFeatureForm.Meta):
        model = AOI

class WindEnergySiteForm(SpatialFeatureForm):
    class Meta(SpatialFeatureForm.Meta):
        model = WindEnergySite
