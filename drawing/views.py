from django.conf import settings
from django.contrib.auth.models import Group
from features.models import Feature
from features.registry import get_feature_by_uid
from json import dumps

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from .models import AOI, WindEnergySite


def get_drawings(request):


    json = []

    drawings = AOI.objects.filter(user=request.user.id).order_by('date_created')
    for drawing in drawings:
        # Allow for "sharing groups" without an associated MapGroup, for "special" cases
        sharing_groups = [
            group.mapgroup_set.get().name
            for group in drawing.sharing_groups.all()
            if group.mapgroup_set.exists()
        ]
        public_groups = [
            group.name
            for group in Group.objects.filter(name__in=settings.SHARING_TO_PUBLIC_GROUPS)
            if group in drawing.sharing_groups.all()
        ]
        sharing_groups = sharing_groups + public_groups

        json.append({
            'id': drawing.id,
            'uid': drawing.uid,
            'name': drawing.name,
            'description': drawing.description,
            'attributes': drawing.serialize_attributes(),
            'sharing_groups': sharing_groups,
            'owned_by_user': True
        })

    try:
        shared_drawings = AOI.objects.shared_with_user(request.user)
    except Exception as e:
        shared_drawings = AOI.objects.filter(pk=-1)
        pass
    for drawing in shared_drawings:
        if drawing not in drawings:
            username = drawing.user.username
            actual_name = drawing.user.first_name + ' ' + drawing.user.last_name
            permission_groups = [x.permission_group for x in request.user.mapgroup_set.all()]
            sharing_groups = [
                group.mapgroup_set.get().name
                for group in drawing.sharing_groups.filter()
                if group.mapgroup_set.exists() and group in permission_groups
            ]
            owned_by_user = True if len(sharing_groups) > 0 else False
            public_groups = [
                group.name
                for group in Group.objects.filter(name__in=settings.SHARING_TO_PUBLIC_GROUPS)
                if group in drawing.sharing_groups.all()
            ]
            sharing_groups = sharing_groups + public_groups
            json.append({
                'id': drawing.id,
                'uid': drawing.uid,
                'name': drawing.name,
                'description': drawing.description,
                'attributes': drawing.serialize_attributes(),
                'shared': True,
                'sharing_groups': sharing_groups,
                'shared_by_username': username,
                'shared_by_name': actual_name,
                'owned_by_user': owned_by_user
            })

    return HttpResponse(dumps(json))


# def delete_drawing(request, uid):
#     try:
#         drawing_obj = get_feature_by_uid(uid)
#     except Feature.DoesNotExist:
#         raise Http404
#
#     # check permissions
#     viewable, response = drawing_obj.is_viewable(request.user)
#     if not viewable:
#         return response
#
#     drawing_obj.delete()
#
#     return HttpResponse("", status=200)


def aoi_analysis(request, aoi_id):
    from aoi_analysis import display_aoi_analysis
    aoi_obj = get_object_or_404(AOI, pk=aoi_id)
    # check permissions
    viewable, response = aoi_obj.is_viewable(request.user)
    if not viewable:
        return response
    return display_aoi_analysis(request, aoi_obj)


def wind_analysis(request, wind_id):
    from wind_analysis import display_wind_analysis
    wind_obj = get_object_or_404(WindEnergySite, pk=wind_id)
    # check permissions
    viewable, response = wind_obj.is_viewable(request.user)
    if not viewable:
        return response
    return display_wind_analysis(request, wind_obj)
