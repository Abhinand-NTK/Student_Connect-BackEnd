from django.conf import settings
from rest_framework import  viewsets,status
from rest_framework.response import Response
from rest_framework import serializers
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class DummySerializer(serializers.Serializer):
    """
    Class for the Dummy Serilizer.
    """
    pass

class StripeCheckoutView(viewsets.ModelViewSet):
    """
    Class for Checkout with Strip 
    """

    queryset = []
    serializer_class = None

    def get_serializer_class(self):
        return DummySerializer
    def create(self,request):

        try:
           
            customer = stripe.Customer.create(
            name='Abhinand',
            address={
                'line1': '123 Main Street',
                'city': 'Kanoor',
                'postal_code': '123232',
                'country': 'DK',
            }
            )

            checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1OSZxWSFTtJxmvwulXqU33O3',
                    'quantity': 1,
                },
            ],
            payment_method_types=['card', ],
            mode='subscription',  # make it as the payment if the subscription is not working properly
            currency="inr",
            success_url='http://localhost:5173/users/landing/',
            cancel_url=f'{settings.SITE_URL}/status' + '?canceled=true',
            customer=customer.id
            )

            return Response({'url': checkout_session.url})
        except:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


