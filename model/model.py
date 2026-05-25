import copy
from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = None
        self._best_score = 0
        self._totalH = 0
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()


    def worstCase(self, nercValue, maxY, maxH):
        self._solBest = None
        self._totalH = 0
        self._best_score = 0

        for n in self._listNerc:
            if n._value == nercValue:
                self.loadEvents(n)
                break

        self._listEvents.sort(key=lambda x: x._date_event_began)
        self.find_best_combination(maxY, maxH)
        return self._solBest, self._best_score, self._totalH


    def find_best_combination(self, maxY, maxH):

        # cambio il punto di partenza
        for i in range(len(self._listEvents)):
            start_event = self._listEvents[i]
            parziale = [start_event]
            ore_iniziali = (start_event._date_event_finished - start_event._date_event_began).total_seconds() / 3600

            if ore_iniziali <= int(maxH):
                self.ricorsione(parziale, maxY, maxH, ore_iniziali)


    def ricorsione(self, parziale, maxY, maxH, oreTot):
        if self.calcola_soggetti(parziale) > self._best_score:
            self._best_score = self.calcola_soggetti(parziale)
            self._totalH = oreTot
            self._solBest = copy.deepcopy(parziale)

        # Cerchiamo il prossimo evento
        ultimo_evento = parziale[-1]
        anno_max = parziale[0]._date_event_began.year + int(maxY)

        for i in range(self._listEvents.index(ultimo_evento) + 1, len(self._listEvents)):
            evento_cand = self._listEvents[i]

            # Vincolo Anno
            if evento_cand._date_event_began.year <= anno_max:

                # Vincolo Ore
                ore_evento = (evento_cand._date_event_finished - evento_cand._date_event_began).total_seconds() / 3600
                if oreTot + ore_evento <= int(maxH):

                    # Backtracking
                    parziale.append(evento_cand)
                    self.ricorsione(parziale, maxY, maxH, oreTot + ore_evento)
                    parziale.pop()


    def calcola_soggetti(self, parziale):
        tot = 0
        for evento in parziale:
            tot += evento._customers_affected
        return tot


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)


    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc

