from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget


class SolitaireState(Widget):
    def render(self)->RenderResult:
        return "Hello [b]World[/b]!"

class SolitaireApp(App):
    # CSS_PATH = ""

    def compose(self) -> ComposeResult:
        yield SolitaireState()

    def on_mount(self) -> None:
        self.screen.styles.background = "darkblue"


if __name__ == "__main__":
    app = SolitaireApp()
    app.run()