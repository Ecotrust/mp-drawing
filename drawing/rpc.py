from rpc4django import rpcmethod

@rpcmethod(login_required=True)
def delete_drawing(uid, **kwargs):
    from features.registry import get_feature_by_uid
    request = kwargs.get('request')
    drawing_obj = get_feature_by_uid(uid)

    viewable, response = drawing_obj.is_viewable(request.user)

    if viewable:
        drawing_obj.delete()
