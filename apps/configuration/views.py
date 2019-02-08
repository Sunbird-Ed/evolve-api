from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Book,State
from .serializers import DetailListSerializer


@permission_classes((IsAuthenticated,))
class DetailList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = DetailListSerializer
    def get(self, request):
        try:
            state = request.query_params.get('state', None)
            if state is not None:
                # import ipdb; ipdb.set_trace()
                queryset=self.get_queryset().filter(subject__grade__medium__state_id=state,)
                serializer = DetailListSerializer(queryset, many=True)
            else:
                queryset = self.get_queryset()
                serializer = DetailListSerializer(queryset, many=True)
            # print((serializer))
            context = {"success": True, "message": "List", "error": "", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'error': str(error), 'success': "false", 'message': 'Failed to get Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class DownloadApprovedHardSpot():
#     queryset=Book.objects.all()
#     def get(self,request):
#         pass