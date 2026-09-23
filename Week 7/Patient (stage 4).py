from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Patient:
    """Represents a SmartCare patient."""

    patient_id: str
    name: str
    dob: date
    phone: str
    email: str
    medical_notes: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate the patient when the object is created."""
        self.validate()

    def validate(self) -> None:
        """Validate patient information."""
        if not self.patient_id.strip():
            raise ValueError("Patient ID cannot be empty")

        if not self.name.strip():
            raise ValueError("Patient name cannot be empty")

        if not isinstance(self.dob, date):
            raise TypeError("Date of birth must be a date object")

        if self.dob > date.today():
            raise ValueError("Date of birth cannot be in the future")

        if not self.phone.strip():
            raise ValueError("Phone number cannot be empty")

        if not self.email.strip():
            raise ValueError("Email cannot be empty")

        if "@" not in self.email:
            raise ValueError("Email address must contain '@'")

    def register(self) -> bool:
        """
        Validate the patient record.

        Database persistence is intentionally excluded from this stage.
        """
        self.validate()
        return True

    def __str__(self) -> str:
        return f"Patient({self.patient_id}, {self.name})"

try:
    Patient(
        patient_id="P002",
        name="",
        dob=date(1990, 5, 12),
        phone="0123456789",
        email="bob@example.com",
    )
except ValueError as error:
    print(f"Patient error: {error}")

try:
    Patient(
        patient_id="P003",
        name="Future Patient",
        dob=date(2100, 1, 1),
        phone="0123456789",
        email="future@example.com",
    )
except ValueError as error:
    print(f"Patient error: {error}")

patient = Patient(
    patient_id="P001",
    name="Alice Smith",
    dob=date(1990, 5, 12),
    phone="0123456789",
    email="alice@example.com",
)

print(patient)
print(patient.register())