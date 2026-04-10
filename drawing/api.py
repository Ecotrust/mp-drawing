"""DRF API view replacing the rpc4django /rpc endpoint for the drawing app.

Replaces this former XML-RPC method:
    delete_drawing
"""
from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class DrawingDeleteView(APIView):
    """DELETE /api/drawings/<uid>/

    Deletes a drawing (AOI or WindEnergySite) identified by its feature uid,
    provided the requesting user has view permission on it.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, uid: str) -> Response:
        from features.registry import get_feature_by_uid

        drawing_obj = get_feature_by_uid(uid)
        viewable, _response = drawing_obj.is_viewable(request.user)
        if viewable:
            drawing_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
