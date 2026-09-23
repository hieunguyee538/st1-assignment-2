from dataclasses import dataclass


@dataclass
class Practitioner:
    """Represents a SmartCare practitioner."""

    practitioner_id: str
    name: str
    specialty: str

    def __post_init__(self) -> None:
        """Validate the practitioner when the object is created."""
        self.validate()

    def validate(self) -> None:
        """Validate practitioner information."""
        if not self.practitioner_id.strip():
            raise ValueError("Practitioner ID cannot be empty")

        if not self.name.strip():
            raise ValueError("Practitioner name cannot be empty")

        if not self.specialty.strip():
            raise ValueError("Practitioner specialty cannot be empty")

    def __str__(self) -> str:
        return (
            f"Practitioner("
            f"{self.practitioner_id}, "
            f"{self.name}, "
            f"{self.specialty}"
            f")"
        )

practitioner = Practitioner(
    practitioner_id="DR001",
    name="Dr. John Doe",
    specialty="General Practice",
)

print(practitioner)

try:
    Practitioner(
        practitioner_id="DR002",
        name="Dr. Jane Roe",
        specialty="",
    )
except ValueError as error:
    print(error)