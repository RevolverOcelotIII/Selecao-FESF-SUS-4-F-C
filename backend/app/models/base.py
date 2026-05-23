from app.core.database import Base
# Importar todos os modelos aqui para o Alembic enxergar através de um único arquivo
from .user import User, Role
from .patient import Patient
from .catalog import Medication, Procedure
from .record import MedicalRecord
