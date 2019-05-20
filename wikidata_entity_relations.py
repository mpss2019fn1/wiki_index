import threading

from .exceptions import AlreadyLoadedException, NotYetLoadedException
from .in_memory_csv import InMemoryCsv


class WikidataEntityRelations:

    __instance = None
    __instance_lock = threading.Lock()

    @staticmethod
    def initialize_instance_from_csv(csv):
        with WikidataEntityRelations.__instance_lock:
            if WikidataEntityRelations.__instance:
                raise AlreadyLoadedException()

            in_memory_csv = InMemoryCsv.load(csv)
            WikidataEntityRelations.__instance = WikidataEntityRelations(in_memory_csv)
            return WikidataEntityRelations.__instance

    @staticmethod
    def instance():
        with WikidataEntityRelations.__instance_lock:
            if not WikidataEntityRelations.__instance:
                raise NotYetLoadedException()

            return WikidataEntityRelations.__instance

    def __init__(self, in_memory_csv):
        self._mapping = {}
        self._build_mapping(in_memory_csv)

    def _build_mapping(self, in_memory_csv):
        for row in in_memory_csv.rows():
            if row["source"] not in self._mapping:
                self._mapping[row["source"]] = []

            self._mapping[row["source"]].append({row["name"]: row["value"]})

    def relations(self, wikidata_entity_id):
        return [{"source": wikidata_entity_id, "name": row["name"], "value": row["value"]} for row in
                self._mapping[wikidata_entity_id]]

    def __contains__(self, wikidata_entity_id):
        return wikidata_entity_id in self._mapping
