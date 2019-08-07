from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from dero.latex.models.presentation.beamer.overlay.overlay import Overlay
from dero.latex.models.item import SimpleItem


class Uncover(SimpleItem):
    name = 'uncover'

    def __init__(self, contents, overlay: Optional['Overlay'] = None):
        super().__init__(self.name, contents, overlay=overlay)