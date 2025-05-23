from colorfield.fields import ColorField
from django.contrib.gis.geos import WKTReader, WKTWriter
from django.db import models
from django.utils.html import escape
from features.registry import register
from features.models import PolygonFeature, GeometryFeature
from nursery.unit_conversions.unit_conversions import sq_meters_to_sq_miles

@register
class AOI(GeometryFeature):
    class Meta:
        verbose_name = 'AOI'
        verbose_name_plural = 'AOIs'

    COLOR_PALETTE = []

    COLOR_PALETTE.append(("#FFFFFF", 'white'))
    COLOR_PALETTE.append(("#888888", 'gray'))
    COLOR_PALETTE.append(("#000000", 'black'))
    COLOR_PALETTE.append(("#FF0000", 'red'))
    COLOR_PALETTE.append(("#FFFF00", 'yellow'))
    COLOR_PALETTE.append(("#00FF00", 'green'))
    COLOR_PALETTE.append(("#00FFFF", 'cyan'))
    COLOR_PALETTE.append(("#0000FF", 'blue'))
    COLOR_PALETTE.append(("#FF00FF", 'magenta'))

    description = models.TextField(null=True, blank=True)
    color = ColorField(
        blank=True,
        null=True,
        default="#EE9900",
        verbose_name="Fill Color",
        samples=COLOR_PALETTE,
    )
    fill_opacity = models.FloatField(
        default=0.7,
    )
    stroke_color = ColorField(
        blank=True,
        null=True,
        default="#EE9900",
        verbose_name="Stroke Color",
        samples=COLOR_PALETTE,
    )
    stroke_width = models.IntegerField(null=True, blank=True, default=2, verbose_name="Stroke Width")

    def save(self, *args, **kwargs):
        if self.geometry_orig.hasz:
            
            wkt_2d = WKTWriter(dim=2).write(self.geometry_orig)
            self.geometry_orig = WKTReader().read(wkt_2d)

        super(AOI, self).save(*args, **kwargs)

    @property
    def area_in_sq_miles(self):
        true_area = self.geometry_final.transform(2163, clone=True).area
        return sq_meters_to_sq_miles(true_area)

    @property
    def formatted_area(self):
        return int((self.area_in_sq_miles * 10) + .5) / 10.

    @property
    def kml(self):
        return """
        <Placemark id="%s">
            <visibility>1</visibility>
            <name>%s</name>
            <styleUrl>#%s-default</styleUrl>
            <ExtendedData>
                <Data name="name"><value>%s</value></Data>
                <Data name="area"><value>%s</value></Data>
                <Data name="user"><value>%s</value></Data>
                <Data name="desc"><value>%s</value></Data>
                <Data name="type"><value>%s</value></Data>
                <Data name="modified"><value>%s</value></Data>
            </ExtendedData>
            %s
        </Placemark>
        """ % (self.uid, escape(self.name), self.model_uid(),
               escape(self.name), self.formatted_area, self.user,
               escape(self.description), self.Options.verbose_name,
               self.date_modified.replace(microsecond=0), self.geom_kml)

    @property
    def kml_style(self):
        return """
        <Style id="%s-default">
            <BalloonStyle>
                <bgColor>ffeeeeee</bgColor>
                <text> <![CDATA[
                    <font color="#1A3752"><strong>$[name]</strong></font>
                    <p>Area: $[area] sq miles</p>
                    <p>$[desc]</p>
                    <font size=1>$[type] created by $[user] on $[modified]</font>
                ]]> </text>
            </BalloonStyle>
            <PolyStyle>
                <color>%s</color>
            </PolyStyle>
            <LineStyle>
                <color>%s</color>
            </LineStyle>
        </Style>
        """ % (self.model_uid(), self.fill_color(), self.outline_color())

    def serialize_attributes(self):
        attributes = []
        if self.geometry_final.geom_type in ['Polygon', 'MultiPolygon']:
            attributes.append({'title': 'Area', 'data': '%.1f sq miles' % (self.area_in_sq_miles)})
            attributes.append({'title': 'Description', 'data': self.description})
        else:
            # Assume GeometryCollection
            total_area = 0
            total_length = 0
            points = []
            try:
                feature_type = self.geometry_final[0].geom_type
                if feature_type in ['Polygon', 'MultiPolygon', 'LineString']:
                    geometry = self.geometry_final.transform(2163, clone=True)
                    for feature in geometry:
                        if feature.geom_type in ['Polygon', 'MultiPolygon']:
                            total_area += feature.area
                        elif feature.geom_type in ['LineString',]:
                            total_length += feature.length
                elif feature_type == 'Point':
                    geometry = self.geometry_final.transform(4326, clone=True)
                    for feature in geometry:
                        points.append("[{:.4f}, {:.4f}]".format(feature.coords[1], feature.coords[0]))

                if total_area > 0:
                    attributes.append({'title': 'Area', 'data': '%.1f sq miles' % (self.area_in_sq_miles)})
                if total_length > 0:
                    if total_length < 800:
                        report_length = "{} feet ({} yds)".format(int(total_length/0.3048), int(total_length/0.9144))
                    else:
                        report_length = "{:.2f} miles".format(total_length/1609.344)
                    attributes.append({'title': 'Line Length', 'data': '{}'.format(report_length)})
                if len(points) > 0:
                    attributes.append({'title': 'Point Coordinates', 'data': '{}'.format('; '.join(points))})
                attributes.append({'title': 'Description', 'data': self.description})
            except Exception as e:
                # Most likely geometry collection contained multiple geometry types
                attributes = []
                pass

        return { 'event': 'click', 'attributes': attributes }

    @classmethod
    def fill_color(self):
        return '776BAEFD'

    @classmethod
    def outline_color(self):
        return '776BAEFD'

    class Options:
        verbose_name = 'Area of Interest'
        icon_url = 'marco/img/aoi.png'
        export_png = False
        manipulators = []
        # optional_manipulators = ['clipping.manipulators.ClipToShoreManipulator']
        optional_manipulators = []
        form = 'drawing.forms.AOIForm'
        form_template = 'aoi/form.html'
        show_template = 'aoi/show.html'

@register
class WindEnergySite(GeometryFeature):
    description = models.TextField(null=True, blank=True)

    @property
    def area_in_sq_miles(self):
        return sq_meters_to_sq_miles(self.geometry_final.area)

    @property
    def formatted_area(self):
        return int((self.area_in_sq_miles * 10) + .5) / 10.

    @property
    def kml(self):
        return """
        <Placemark id="%s">
            <visibility>1</visibility>
            <name>%s</name>
            <styleUrl>#%s-default</styleUrl>
            <ExtendedData>
                <Data name="name"><value>%s</value></Data>
                <Data name="area"><value>%s</value></Data>
                <Data name="user"><value>%s</value></Data>
                <Data name="desc"><value>%s</value></Data>
                <Data name="type"><value>%s</value></Data>
                <Data name="modified"><value>%s</value></Data>
            </ExtendedData>
            %s
        </Placemark>
        """ % (self.uid, escape(self.name), self.model_uid(),
               escape(self.name), self.formatted_area, self.user,
               escape(self.description), self.Options.verbose_name,
               self.date_modified.replace(microsecond=0), self.geom_kml)

    @property
    def kml_style(self):
        return """
        <Style id="%s-default">
            <BalloonStyle>
                <bgColor>ffeeeeee</bgColor>
                <text> <![CDATA[
                    <font color="#1A3752"><strong>$[name]</strong></font>
                    <p>Area: $[area] sq miles</p>
                    <p>$[desc]</p>
                    <font size=1>$[type] created by $[user] on $[modified]</font>
                ]]> </text>
            </BalloonStyle>
            <PolyStyle>
                <color>%s</color>
            </PolyStyle>
            <LineStyle>
                <color>%s</color>
            </LineStyle>
        </Style>
        """ % (self.model_uid(), self.fill_color(), self.outline_color())

    @classmethod
    def fill_color(self):
        return '7776B9DE'

    @classmethod
    def outline_color(self):
        return '7776B9DE'

    class Options:
        verbose_name = 'Wind Energy Site'
        icon_url = 'marco/img/wind.png'
        export_png = False
        form = 'drawing.forms.WindEnergySiteForm'
        form_template = 'wind/form.html'
        show_template = 'wind/show.html'
