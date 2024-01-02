from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from .models import Department
from .serializer import DataValidationSerilzier,ListViewSerilzer
from rest_framework.response import Response
from superadmin.models import RegisterCollege

class AddCourseView(viewsets.ModelViewSet):
    """
    View For Adding The Course in The College 
    """
    queryset = Department.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = DataValidationSerilzier

    def create(self,request):

        """function for creating the subject """
        user_id = request.data.get('id')
        college = RegisterCollege.objects.get(user_details=user_id)
        permission_classes=[IsAuthenticated]

        department_data = {
            'name' : request.data.get('name'),
            'college_name': college.id
        }

        serilizer = DataValidationSerilzier(data=department_data)
        serilizer.Meta.model = Department
        if serilizer.is_valid():
            instance = serilizer.save()
            return Response(serilizer.data,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,*args,**kwargs):
        """function for updating  the instance of the departmental model"""
        serilizer = DataValidationSerilzier(data=request.data)
        serilizer.Meta.model = Department
        instance = self.get_object()
        serializer = DataValidationSerilzier(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request,**kwargs):  # Fix the typo 
        """function for list  the all objects of the departmental model"""
        user_id = request.GET.get('id', None)
        print("_------------------------")
        print("_------------------------")
        print("_------------------------")
        print(user_id)
        print("_------------------------")
        print("_------------------------")
        print("_------------------------")
        college_instance = RegisterCollege.objects.get(user_details=user_id)

        queryset = Department.objects.filter(college_name = college_instance.id)
        serializer = ListViewSerilzer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)







