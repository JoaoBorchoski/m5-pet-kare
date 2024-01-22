from django.forms.models import model_to_dict
from rest_framework.views import APIView, Response
from groups.models import Group, GroupSerializer
from pets.models import Pet, PetSerializer
from traits.models import Trait, TraitSerializer


full_pet_data = {
    "name": "Strogonoff",
    "age": 4,
    "weight": 5,
    "sex": "Female",
    "group": {"scientific_name": "Felis catus"},
    "traits": [{"trait_name": "curious"}, {"trait_name": "hairy"}],
}


class GroupView(APIView):
    def post(self, req):
        group_data = {"scientific_name": "canis familiaris"}
        pet_data = {"name": "Mada", "age": 1, "weight": 10, "sex": "Female"}

        # group = Group.objects.create(**group_data)
        group = Group.objects.get(id=1)
        pet = Pet.objects.create(**pet_data, group=group)

        return Response(model_to_dict(pet), 201)

    def get(self, req):
        group = Group.objects.get(id=3)
        groups = group.pets.all()
        pets = [model_to_dict(pet) for pet in groups]

        return Response(model_to_dict(group))

        # full_pet_data = {
        #     "name": "Strogonoff",
        #     "age": 4,
        #     "weight": 5,
        #     "sex": "Female",
        #     "group": {"scientific_name": "Felis catus"},
        #     "traits": [{"trait_name": "curious"}, {"trait_name": "hairy"}],
        # }

        # serializer = PetSerializer(data=full_pet_data)
        # valid = serializer.is_valid()
        # data = serializer.validated_data
        # erros = serializer.errors

        # return Response((valid, data, erros))


class GroupViewDetail(APIView):
    def post(self, req):
        trait_1_data = Trait.objects.create(**{"name": "curious"})
        trait_2_data = Trait.objects.create(**{"name": "hairy"})
        pet = Pet.objects.get(id=2)
        pet.traits.add(trait_1_data)

        return Response(model_to_dict(pet))

    def get(self, req):
        trait_1 = Trait.objects.get(id=1)
        pets = [model_to_dict(pet) for pet in trait_1.pets.all()]

        return Response(pets)
