from textual.app import App, ComposeResult
from textual.widgets import Button, RadioSet, Label, Input, ListView
from textual.screen import Screen
from textual.containers import Vertical, Horizontal


class SelecaoCluster(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Bem vindo à criação de jobs!")
        yield RadioSet(
            "Cluster 01",
            "Cluster 02",
            "Cluster 03",
            "Cluster 04",
            "Cluster 05",
            id="cluster_selecionado"
        )
        yield Button("Próximo", id="prox_botao")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "prox_botao":
            radioset = self.query_one("cluster_selecionado", RadioSet)
            selecionado = radioset.pressed
            if selecionado:
                valor = selecionado.label
                self.app.data["cluster_selecionado"] = valor
            self.app.push_screen("segundo")


class InformacoesJob(Screen):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Informacoes do job:")
            yield Input(placeholder="Nome do job", id="job_name", type="text")
            yield Input(placeholder="Nome do arquivo de saida", id="output_name", type="text")
            yield Input(placeholder="Numero de processos", id="num_procs", type="integer")
            yield Input(placeholder="CPUs por processo", id="cpus_per_proc", type="integer")
            yield Input(placeholder="Memoria por No (Gb)", id="memory_per_node", type="number")
            yield Input(
                placeholder="Tempo maximo (ex: 10m, 10m:00s, 1h:10m:00s, 1d-01h, 1d-01h:00m:00s)",
                id="max_time"
            )
            yield RadioSet(
                "Alocamento exclusivo",
                "Alocamento nao exclusivo",
                id="allocation_type"
            )
            with Horizontal():
                yield Button("Anterior", id="anterior_botao")
                yield Button("Proximo", id="prox_botao")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "anterior_botao":
            self.app.pop_screen()
        elif event.button.id == "prox_botao":
            self.app.push_screen("terceiro")


class ComandosDoJob(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Informe os comandos a serem executados")
        yield Input(placeholder="Digite o comando e pressione enter", id="comando_input")
        yield Button("Adicionar comando", id="adicionar_botao")
        yield ListView(id="lista_comandos")
        with Horizontal():
            yield Button("Anterior", id="anterior_botao")
            yield Button("Proximo", id="prox_botao")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "anterior_botao":
            self.app.pop_screen()
        elif event.button.id == "prox_botao":
            self.app.push_screen("quarto")
        elif event.button.id == "adicionar_botao":
            input_widget = self.query_one("#comando_input", Input)
            lista = self.query_one("#lista_comandos", ListView)
            lista.append(Label(input_widget.value))
            input_widget.value = ""

class RevisaoJob(Screen):
    def compose(self) -> ComposeResult:
        cluster = self.app.data.get("cluster_selecionado","nenhum")
        yield Label("O cluster selecionado foi {cluster}")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "anterior_botao":
            self.app.pop_screen()
        elif event.button.id == "prox_botao":
            self.app.exit()

class AppMain(App):
    def on_ready(self) -> None:
        self.data = {}
        self.install_screen(SelecaoCluster(), name="primeiro")
        self.install_screen(InformacoesJob(), name="segundo")
        self.install_screen(ComandosDoJob(), name="terceiro")
        self.install_screen(RevisaoJob(), name="quarto")
        self.push_screen("primeiro")
    

if __name__ == "__main__":
    app = AppMain()
    app.run()