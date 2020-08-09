from enum import Enum
from functools import wraps

import requests
import logging

from utils import Schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Dofapi(object):
    # __ID__ = '_id'
    # __ANKAMA_ID__ = 'ankamaId'
    # __NAME__ = 'name'

    __DOFAPI_API_ = 'https://fr.dofus.dofapi.fr/'

    class IDSchema(Schema):
        ID = '_id'
        ANKAMA_ID = 'ankamaId'
        NAME = 'name'

    class APISchema(Schema):
        CLASSES = 'classes'
        CONSUMABLES = 'consumables'
        EQUIPMENTS = 'equipments'
        HARNESSES = 'harnesses'
        HAVENBAGS = 'havenbags'
        IDOLS = 'idols'
        MONSTERS = 'monsters'
        MOUNTS = 'mounts'
        PETS = 'pets'
        PROFESSIONS = 'professions'
        RESOURCES = 'resources'
        SETS = 'sets'
        WEAPONS = 'weapons'

    class WeaponsSchema(Schema):
        ARC = 'Arc'
        EPEE = 'Épée'
        DAGUE = 'Dague'
        BAGUETTE = 'Baguette'
        BATON = 'Bâton'
        MARTEAU = 'Marteau'
        PELLE = 'Pelle'
        HACHE = 'Hache'
        OUTIL = 'Outil'
        FAUX = 'Faux'
        PIOCHE = 'Pioche'
        PIERRE_AME = "Pierre d'âme"

    class EquipmentsSchema(Schema):
        AMULETTE = 'Amulette'
        ANNEAU = 'Anneau'
        BOTTES = 'Bottes'
        CEINTURE = 'Ceinture'
        CHAPEAU = 'Chapeau'
        CAPE = 'Cape'
        DOFUS = 'Dofus'
        SAC_DOS = 'Sac à dos'
        BOUCLIER = 'Bouclier'
        OBJET_VIVANT = 'Objet vivant'
        TROPHEE = 'Trophée'

    class ResourcesSchema(Schema):
        PLANCHE = 'Planche'
        SUBSTRAT = 'Substrat'
        ALLIAGE = 'Alliage'
        PIERRE_PRECIEUSE = 'Pierre précieuse'
        ESSENCE = 'Essence de gardien de donjon'
        TEINTURE = 'Teinture'
        IDOLE = 'Idole'
        CLEF = 'Clef'

    class ConsumablesSchema(Schema):
        POTION = 'Potion'
        POTION_TELEPORTATION = 'Potion de téléportation'
        POTION_OUBLI_PERCEPTEUR = 'Potion d\'oubli Percepteur'
        POTION_CONQUETE = 'Potion de conquête'
        OBJET_ELEVAGE = 'Objet d\'élevage'

    class Schema(IDSchema, APISchema, WeaponsSchema, EquipmentsSchema, ResourcesSchema, ConsumablesSchema):
        pass

    def _scan(self, *args, **kwargs):
        endpoints, unique = kwargs.get('endpoints'), kwargs.get('unique', False)
        endpoints = endpoints if isinstance(endpoints, list) else [endpoints]

        result = []
        for endpoint in endpoints:
            response = requests.get(self.__DOFAPI_API_ + endpoint, *args).json()
            result.extend(response)
            logger.info('Retrieved {count} {endpoint}'.format(count=len(response), endpoint=endpoint))

        return list({v[self.Schema.ID]: v for v in result}.values()) if unique else result

    def scan_consumables(self, *args, **kwargs):
        return self._scan(endpoints=self.APISchema.CONSUMABLES, *args, **kwargs)

    def scan_equipments(self, *args, **kwargs):
        return self._scan(endpoints=self.APISchema.EQUIPMENTS, *args, **kwargs)

    def scan_idols(self, *args, **kwargs):
        return self._scan(endpoints=self.APISchema.IDOLS, *args, **kwargs)

    def scan_resources(self, *args, **kwargs):
        return self._scan(endpoints=self.APISchema.RESOURCES, *args, **kwargs)

    def scan_weapons(self, *args, **kwargs):
        return self._scan(endpoints=self.APISchema.WEAPONS, *args, **kwargs)

    def _scan_items(self, *args, **kwargs):
        return self._scan(endpoints=self.APISchema.values(), *args, **kwargs)

    def _scan_professions(self, *args, **kwargs):
        return self._scan(endpoints=self.APISchema.PROFESSIONS, *args, **kwargs)
