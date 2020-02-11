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
        sharing_groups = [group.mapgroup_set.get().name
                          for group in drawing.sharing_groups.all()
                          if group.mapgroup_set.exists()]
        json.append({
            'id': drawing.id,
            'uid': drawing.uid,
            'name': drawing.name,
            'description': drawing.description,
            'attributes': drawing.serialize_attributes(),
            'sharing_groups': sharing_groups
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
            json.append({
                'id': drawing.id,
                'uid': drawing.uid,
                'name': drawing.name,
                'description': drawing.description,
                'attributes': drawing.serialize_attributes(),
                'shared': True,
                'shared_by_username': username,
                'shared_by_name': actual_name
            })

    return HttpResponse(dumps(json))

# from drawing.rpc import *
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

'''
'''
def get_attributes(request, uid):
    from django.contrib.auth.models import User
    from marineplanner import settings as mpSettings
    try:
        scenario_obj = get_feature_by_uid(uid)
    except Scenario.DoesNotExist:
        raise Http404

    #check permissions
    viewable, response = scenario_obj.is_viewable(request.user)
    if not viewable:

        if mpSettings.ALLOW_ANONYMOUS_DRAW:

            anonUser = User.objects.get(pk=mpSettings.ANONYMOUS_USER_PK)
            anonViewable, response = scenario_obj.is_viewable(anonUser)
            if not anonViewable:
                return response
        else:
            return response

    if 'serialize_attributes' in dir(scenario_obj):
        if hasattr(scenario_obj,'is_loading') and scenario_obj.is_loading:
            scenario_obj.save()
        return HttpResponse(dumps(scenario_obj.serialize_attributes()))
    else:
        return HttpResponse(dumps([]))


def wind_analysis(request, wind_id):
    from wind_analysis import display_wind_analysis
    wind_obj = get_object_or_404(WindEnergySite, pk=wind_id)
    # check permissions
    viewable, response = wind_obj.is_viewable(request.user)
    if not viewable:
        return response
    return display_wind_analysis(request, wind_obj)
