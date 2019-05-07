import threading

from .exceptions import AlreadyLoadedException, NotYetLoadedException
from .in_memory_csv import InMemoryCsv


class WikidataPageProps:

    __instance = None
    __instance_lock = threading.Lock()

    @staticmethod
    def initialize_instance_from_csv(csv):
        with WikidataPageProps.__instance_lock:
            if WikidataPageProps.__instance:
                raise AlreadyLoadedException

            in_memory_csv = InMemoryCsv.load(csv, row_filter=WikidataPageProps._row_filter)
            WikidataPageProps.__instance = WikidataPageProps(in_memory_csv)
            return WikidataPageProps.__instance

    @staticmethod
    def _row_filter(row):
        # we only want to keep rows, which reference the wikidata id
        return row["pp_propname"] == "wikibase_item"

    @staticmethod
    def instance():
        with WikidataPageProps.__instance_lock:
            if not WikidataPageProps.__instance:
                raise NotYetLoadedException

            return WikidataPageProps.__instance

    def __init__(self, in_memory_csv):
        self._mapping = {}
        self._build_mapping(in_memory_csv)

    def _build_mapping(self, in_memory_csv):
        for row in in_memory_csv.rows():
            self._mapping[int(row["pp_page"])] = row["pp_value"]

    def wikidata_id(self, wikipedia_page_id):
        return self._mapping[wikipedia_page_id]

    def __contains__(self, wikipedia_page_id):
        return wikipedia_page_id in self._mapping