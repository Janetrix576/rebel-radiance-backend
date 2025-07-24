from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def create_order(request):
    data = request.data
    print("Order received:", data)
    return Response({"message": "Order received!"}, status=status.HTTP_201_CREATED)
