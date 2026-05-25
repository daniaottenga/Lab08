import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()


    def handleWorstCase(self, e):
        self._view._txtOut.controls.clear()
        nercValue = self._view._ddNerc.value
        maxY = self._view._txtYears.value
        maxH = self._view._txtHours.value

        if nercValue is None:
            self._view.create_alert("Attenzione, selezionare un nerc.")
            self._view.update_page()
            return

        if maxY is None:
            self._view.create_alert("Attenzione, selezionare il numero massimo di anni.")
            self._view.update_page()
            return

        if maxH is None:
            self._view.create_alert("Attenzione, selezionare il numero massimo di ore.")
            self._view.update_page()
            return

        result, best_score, totalH = self._model.worstCase(nercValue, maxY, maxH)
        if result is not None:
            self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {best_score}"))
            self._view._txtOut.controls.append(ft.Text(f"Tot hours of outage: {totalH}"))
            for r in result:
                self._view._txtOut.controls.append(ft.Text(r))
            self._view.update_page()

        else:
            self._view._txtOut.controls.append(ft.Text("No solution found"))
            self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()


    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
