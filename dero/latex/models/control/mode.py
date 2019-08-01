from typing import Optional
from dero.latex.models.item import ItemBase
from dero.latex.texgen import no_options_no_contents_str
from dero.mixins.repr import ReprMixin

class Mode(ItemBase, ReprMixin):
    name = 'mode'
    repr_cols = [
        'mode_type',
        'contents'
    ]

    def __init__(self, mode_type: str = 'presentation', contents: Optional = None):
        self.mode_type = mode_type
        self.contents = contents
        super().__init__()

    def __str__(self):
        """
        \mode must be on its own line with no whitespace in some cases, so must have a custom __str__ method
        """
        from dero.latex.logic.builder import _build
        from dero.latex.logic.format.contents import format_contents
        mode_definition = no_options_no_contents_str(self.name)  # \mode
        mode_type_str = f'<{self.mode_type}>'
        contents_str = f'{{{format_contents(self.contents)}}}'
        mode_contents = f'{mode_type_str}{contents_str}'
        return _build([
            mode_definition,
            mode_contents
        ])
