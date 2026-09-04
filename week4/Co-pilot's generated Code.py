appointments = []

def book_appointment(patient, practitioner, time):
    """Store a simple appointment in a list."""
    appointment = {
        "patient": patient,
        "practitioner": practitioner,
        "time": time
    }
    appointments.append(appointment)
    return appointment
