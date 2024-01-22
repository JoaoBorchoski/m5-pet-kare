from django.forms.models import model_to_dict
from rest_framework.views import APIView, Response
from groups.models import Group, GroupSerializer
from pets.models import Pet, PetSerializer
from traits.models import Trait, TraitSerializer
from rest_framework.pagination import PageNumberPagination
import ipdb


class PetView(APIView, PageNumberPagination):
    def get(self, req):
        try:
            pets = Pet.objects.all()
            result_page = self.paginate_queryset(pets, req, view=True)
            serializer = PetSerializer(result_page, many=True)
            return self.get_paginated_response(serializer.data)
        except Pet.DoesNotExist:
            return Response({"message: Pet not found"}, 400)

    def post(self, req):
        serializer = PetSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.data["group"]
        verify_group = Group.objects.filter(
            scientific_name=group["scientific_name"]
        ).first()

        if not verify_group:
            verify_group = Group.objects.create(**group)

        serializer.validated_data["group"] = verify_group

        traits = serializer.validated_data.pop("traits", None)

        new_pet = Pet.objects.create(**serializer.validated_data)

        for trait in traits:
            verify_trait = Trait.objects.filter(trait_name=trait["trait_name"]).first()
            if not verify_trait:
                verify_trait = Trait.objects.create(**trait)
            new_pet.traits.add(verify_trait)
        serializer = PetSerializer(new_pet)

        return Response(serializer.data)


class PetDetailView(APIView):
    def get(self, req, pet_id):
        try:
            pet = model_to_dict(Pet.objects.get(pk=pet_id))
            pet["traits"] = [model_to_dict(trait) for trait in pet["traits"]]

            return Response(pet)

        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

    def delete(self, req, pet_id):
        try:
            pet = Pet.objects.get(pk=pet_id)
            pet.delete()
            return Response(None, 204)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

    def patch(self, req, pet_id):
        # essa parte aqui nao desenvolvi ainda, to atrasado com as coisas e to enviando assim mesmo pra n me atrasar com essa sprint tbm
        try:
            pet = Pet.objects.get(pk=pet_id)
            for key, value in req.data.items():
                setattr(pet, key, value)
            pet.save()
            return Response(model_to_dict(pet))

        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, 404)
