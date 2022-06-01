from datetime import datetime
from base.products import Products
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import *
from base.serializer import OrderSerializer, ProductSerializer,OrderItemSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(req):
    # print(">>>>>>>>>>>>>>>>>>>>>>>>addOrderItems")
    user = req.user
    data = req.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # (1) Create order

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        # (2) Create shipping address

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

        # (3) Create order items adn set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )

            # (4) Update stock

            product.countInStock -= item.qty
            product.save()

        serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(req,pk):
    # print("getOrderById>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    user = req.user
    order = Order.objects.get(_id=pk)
    o=Order.objects.all()
    p=OrderItemSerializer(o,many=True)
    print(p.data)
    try:
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'details':'Not authorized to view this order'}, status=status.HTTP_401_UNAUTHORIZED)

    except:
        return Response({'details':'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(req):
    user = req.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(req,pk):
    order=Order.objects.get(_id=pk)

    order.isPaid= True
    order.paidAt = datetime.now()
    order.save()

    return Response('Order was paid')

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(req):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(req,pk):

    order=Order.objects.get(_id=pk)

    order.isDelivered= True
    order.paidAt = datetime.now()
    order.save()

    return Response('Order was delivered')