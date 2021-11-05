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

    description = models.TextField(null=True, blank=True)

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
            for feature in self.geometry_final:
                feature = feature.transform(2163, clone=True)
                if feature.geom_type in ['Polygon', 'MultiPolygon']:
                    total_area += feature.area
                elif feature.geom_type in ['LineString',]:
                    total_length += feature.length
                elif feature.geom_type in ['Point',]:
                    feature = feature.transform(4326, clone=True)
                    points.append("[{0:.4g}, {1:.4g}]".format(feature.coords[0], feature.coords[1]))
                else:
                    print("NEW FEATURE TYPE: {}".format(feature.geom_type))
            if total_area > 0:
                attributes.append({'title': 'Area', 'data': '%.1f sq miles' % (self.area_in_sq_miles)})
            if total_length > 0:
                if total_length < 800:
                    report_length = "{} feet ({} yds)".format(int(total_length/0.3048), int(total_length/0.9144))
                else:
                    report_length = "{0:.2g} miles".format(total_length/1609.344)
                attributes.append({'title': 'Line Length', 'data': '{}'.format(report_length)})
            if len(points) > 0:
                attributes.append({'title': 'Point Coordinates', 'data': '{}'.format('; '.join(points))})
            attributes.append({'title': 'Description', 'data': self.description})
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
