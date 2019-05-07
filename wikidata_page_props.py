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
        self._in_memory_csv = in_memory_csv
