from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from .models import Department
from .serializer import DataValidationSerilzier
from rest_framework.response import Response

class AddCourseView(viewsets.ModelViewSet):
    """
    View For Adding The Course in The College 
    """
    queryset = Department.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DataValidationSerilzier
    def create(self,request):

        """function for creating the subject """
        serilizer = DataValidationSerilzier(data=request.data)
        serilizer.Meta.model = Department
        if serilizer.is_valid():
            instance = serilizer.save()
            return Response(serilizer.data,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

