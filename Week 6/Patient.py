# Patient.py
from datetime import date, datetime
from typing import Optional


class Patient:
    """Patient entity managing registration and profile."""

    def __init__(self, patient_id: str, name: str, dob: date,
                 phone: str, email: str, medical_notes: str = ""):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.phone = phone  # Will be encrypted by SecurityManager
        self.email = email  # Will be encrypted by SecurityManager
        self.medical_notes = medical_notes
        self.created_timestamp = datetime.now()

    def register(self) -> bool:
        """Create new patient record in system. Return True if successful."""
        pass

    def search_by_name(self, name: str) -> list:
        """Search for patients by full or partial name. Return list of matching Patient objects."""
        pass

    def search_by_id(self, patient_id: str) -> Optional['Patient']:
        """Retrieve patient by unique ID. Return Patient object or None if not found."""
        pass

    def validate_data(self) -> bool:
        """Validate patient data (non-empty name, valid email, valid DOB). Return True if valid."""
        pass

    def get_appointments(self) -> list:
        """Retrieve all appointments for this patient. Return list of Appointment objects."""
        pass