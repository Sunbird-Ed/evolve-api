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
from .models import Book,State,Medium,Subject,Grade
from .serializers import DetailListSerializer
from .serializers  import (
    StateListSerializer,
    MediumListSerializer,
    GradeListSerializer,
    SubjectListSerializer,
    BookListSerializer,
    )


@permission_classes((IsAuthenticated,))
class DetailList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = DetailListSerializer
    def get(self, request):
        try:
            state = request.query_params.get('state', None)
            if state is not None:
                queryset=self.get_queryset().filter(subject__grade__medium__state_id=state,)
                serializer = DetailListSerializer(queryset, many=True)
            else:
                queryset = self.get_queryset()
                serializer = DetailListSerializer(queryset, many=True)
            context = {"success": True, "message": "List", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class StateList(ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateListSerializer
    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = StateListSerializer(queryset, many=True)
            context = {"success": True, "message": "State List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get state Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MediumList(ListAPIView):
    queryset = Medium.objects.all()
    serializer_class = MediumListSerializer
    def get(self, request):
        try:
            state = request.query_params.get('state', None)
            req = request.query_params.get('req', None)
            if state is not None:
                if req is not None and str(req) == 'hardspot':
                    queryset=self.get_queryset().filter(state__id=state, grade__subject__book__hardspot_only=True).order_by('medium')
                elif req is not None and str(req) == 'content':
                    queryset=self.get_queryset().filter(state__id=state, grade__subject__book__content_only=True).order_by('medium')
            else:
                queryset = self.get_queryset().order_by('medium')
            serializer = MediumListSerializer(set(queryset), many=True)
            context = {"success": True, "message": "Medium List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get medium Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GradeList(ListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeListSerializer
    def get(self, request):
        try:
            medium = request.query_params.get('medium', None)
            req = request.query_params.get('req', None)
            if medium is not None:
                if req is not None and str(req) == 'hardspot':
                    queryset=self.get_queryset().filter(medium__id=medium , subject__book__hardspot_only=True)
                elif req is not None and str(req) == 'content':
                    queryset=(self.get_queryset().filter(medium__id=medium, subject__book__content_only=True))
            else:
                queryset = self.get_queryset()
            serializer = GradeListSerializer((set(queryset)) , many=True)
            sorted_data=(sorted(serializer.data, key = lambda i: int(i['grade'].split(" ")[1])))
            context = {"success": True, "message": "Grade List","data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get grade Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectList(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectListSerializer
    def get(self, request):
        try:
            grade = request.query_params.get('grade', None)
            req = request.query_params.get('req', None)
            if grade is not None:
                if req is not None and str(req) == 'hardspot':
                    queryset=self.get_queryset().filter(grade__id=grade,book__hardspot_only=True).order_by('Subject')
                elif req is not None and str(req) == 'content':
                    queryset=self.get_queryset().filter(grade__id=grade, book__content_only=True).order_by('Subject')
            else:
                queryset = self.get_queryset().order_by('Subject')
            serializer = SubjectListSerializer(set((queryset).order_by('Subject')), many=True)
            context = {"success": True, "message": "Subject List", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get subject Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    def get(self, request):
        try:
            subject = request.query_params.get('subject', None)
            if subject is not None:
                queryset=self.get_queryset().filter(subject__id=subject)
            else:
                queryset = self.get_queryset()
            serializer = BookListSerializer(queryset, many=True)
            context = {"success": True, "message": "book List", "data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as error:
            context = {'success': "false", 'message': 'Failed to get book Details.'}
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


