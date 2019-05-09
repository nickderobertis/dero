from typing import Union, List, Tuple, Dict

from dero.latex.models import Item
from dero.latex.models.documentitem import DocumentItem

AnyItem = Union[Item, DocumentItem]
ListOfItems = List[AnyItem]
DictOfItems = Dict[str, AnyItem]
ListOrDictOfItems = Union[ListOfItems, DictOfItems]
ListOrDictOrItem = Union[ListOrDictOfItems, AnyItem]
ItemOrListOfItems = Union[AnyItem, ListOfItems]
StrList = List[str]
StrListOrNone = Union[StrList, None]
ItemAndPreEnvContents = Tuple[AnyItem, StrListOrNone]