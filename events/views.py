# pylint: disable=no-member
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Event, Review, EventGroup
from .serializers import EventSerializer, PopulatedEventSerializer, ReviewSerializer, EventGroupSerializer, PopulatedEventGroupSerializer


# Event Views

class EventListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        events = Event.objects.all()
        serialized_events = PopulatedEventSerializer(events, many=True)
        return Response(serialized_events.data)

    def post(self, request):
        event = EventSerializer(data=request.data)
        request.data['owner'] = request.user.id
        if event.is_valid():
            event.save()
            return Response(event.data, status=HTTP_201_CREATED)
        return Response(event.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class EventDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serialized_event = PopulatedEventSerializer(event)
            return Response(serialized_event.data)
        except Event.DoesNotExist:
            return Response({'message': 'Not Found'}, status=HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            request.data['owner'] = request.user.id
            updated_event = EventSerializer(event, data=request.data)
            if updated_event.is_valid():
                updated_event.save()
                return Response(updated_event.data, status=HTTP_202_ACCEPTED)
            return Response(updated_event.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        except Event.DoesNotExist:
            return Response({'message': 'Not Found'}, status=HTTP_404_NOT_FOUND)

    def delete(self, _request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response({'message': 'Not Found'}, status=HTTP_404_NOT_FOUND)


# Review Views

class ReviewListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request, pk):
        request.data['event'] = pk
        request.data['owner'] = request.user.id
        review = ReviewSerializer(data=request.data)
        if review.is_valid():
            review.save()
            event = Event.objects.get(pk=pk)
            serialized_event = PopulatedEventSerializer(event)
            return Response(serialized_event.data, status=HTTP_201_CREATED)
        return Response(review.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class ReviewDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def delete(self, request, **kwargs):
        try:
            review = Review.objects.get(pk=kwargs['review_pk'])
            if review.owner.id != request.user.id:
                return Response(status=HTTP_401_UNAUTHORIZED)
            review.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'message': 'Not Found'}, status=HTTP_404_NOT_FOUND)


# Event Group Views

class EventGroupListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request, pk):
        event_groups = EventGroup.objects.all()
        serialized_event_groups = PopulatedEventGroupSerializer(
            event_groups, many=True)
        return Response(serialized_event_groups.data)

    def post(self, request, pk):
        request.data['event'] = pk
        request.data['owner'] = request.user.id
        event_group = EventGroupSerializer(data=request.data)
        if event_group.is_valid():
            event_group.save()
            event = Event.objects.get(pk=pk)
            serialized_event = PopulatedEventSerializer(event)
            return Response(serialized_event.data, status=HTTP_201_CREATED)
        return Response(event_group.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class EventGroupDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request, pk):
        try:
            event_group = EventGroup.objects.get(pk=pk)
            serialized_event_group = PopulatedEventGroupSerializer(event_group)
            return Response(serialized_event_group.data)
        except EventGroup.DoesNotExist:
            return Response({'message': 'Not Found'}, status=HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            event_group = EventGroup.objects.get(pk=pk)
            updated_event_group = EventGroupSerializer(
                event_group, data=request.data)
            if updated_event_group.is_valid():
                updated_event_group.save()
                return Response(updated_event_group.data, status=HTTP_202_ACCEPTED)
            return Response(updated_event_group.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        except EventGroup.DoesNotExist:
            return Response({'message': 'Not Found'}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        try:
            event_group = EventGroup.objects.get(pk=kwargs['event_group_pk'])
            if event_group.owner.id != request.user.id:
                return Response(status=HTTP_401_UNAUTHORIZED)
            event_group.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except EventGroup.DoesNotExist:
            return Response({'message': 'Not Found'}, status=HTTP_404_NOT_FOUND)
