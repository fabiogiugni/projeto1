from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict

# Usado para type hinting sem causar importação circular
if TYPE_CHECKING:
    from ..database.database import Database 

class DataInterface(ABC):

    @abstractmethod
    def getData(self, db: 'Database') -> Dict[str, Any]:
        """
        Retorna um dicionário com os dados da entidade e, recursivamente, 
        os dados de suas entidades filhas, pronto para serialização.
        """
        pass