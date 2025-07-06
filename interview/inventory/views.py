from django.utils.dateparse import parse_datetime
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryTag,
    InventoryType,
)
from interview.inventory.schemas import InventoryMetaData
from interview.inventory.serializers import (
    InventoryLanguageSerializer,
    InventorySerializer,
    InventoryTagSerializer,
    InventoryTypeSerializer,
)



class InventoryListCreateView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            metadata = InventoryMetaData(**request.data["metadata"])
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        request.data["metadata"] = metadata.dict()
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset(request)
        total_count = queryset.count()

        # Pagination: limit and offset
        try:
            limit = int(request.query_params.get("limit", 3))
            offset = int(request.query_params.get("offset", 0))
        except ValueError:
            return Response({"error": "Invalid limit or offset"}, status=400)

        page = queryset[offset:offset + limit]
        serializer = self.serializer_class(page, many=True)

        base_url = request.build_absolute_uri().split("?")[0]
        next_offset = offset + limit
        prev_offset = max(offset - limit, 0)

        return Response({
            "count": total_count,
            "next": f"{base_url}?limit={limit}&offset={next_offset}" if next_offset < total_count else None,
            "previous": f"{base_url}?limit={limit}&offset={prev_offset}" if offset > 0 else None,
            "results": serializer.data,
        }, status=200)

    def get_queryset(self, request: Request):
        qs = self.queryset.all()
        created_after = request.query_params.get("created_after")

        if created_after:
            try:
                date = parse_datetime(created_after)
                if date is None:
                    raise ValueError
                qs = qs.filter(created_at__gte=date)
            except ValueError:
                return Inventory.objects.none()  # Or raise an error
        
        return qs


class InventoryRetrieveUpdateDestroyView(APIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryTagListCreateView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryTagRetrieveUpdateDestroyView(APIView):
    queryset = InventoryTag.objects.all()
    serializer_class = InventoryTagSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory_tag)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(
            inventory_tag, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory_tag = self.get_queryset(id=kwargs["id"])
        inventory_tag.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryLanguageListCreateView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryLanguageRetrieveUpdateDestroyView(APIView):
    queryset = InventoryLanguage.objects.all()
    serializer_class = InventoryLanguageSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class InventoryTypeListCreateView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=201)

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def get_queryset(self):
        return self.queryset.all()


class InventoryTypeRetrieveUpdateDestroyView(APIView):
    queryset = InventoryType.objects.all()
    serializer_class = InventoryTypeSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory)

        return Response(serializer.data, status=200)

    def patch(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        serializer = self.serializer_class(inventory, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data, status=200)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        inventory = self.get_queryset(id=kwargs["id"])
        inventory.delete()

        return Response(status=204)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)
