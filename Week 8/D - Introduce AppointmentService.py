class AppointmentService:
    """
    Coordinates workflow and booking rules without bleeding domain logic
    from the Appointment model.
    """
    def __init__(self, appointment_repository):
        self.repository = appointment_repository

    def create_appointment(self, patient_id, practitioner_id, appointment_datetime):
        # 1. Validate input data
        # 2. Check practitioner availability (overlap detection)
        # 3. Book/Instantiate Appointment domain object
        # 4. Save to repository
        # 5. Return confirmation result
        pass

    def cancel_appointment(self, appointment_id, reason):
        # 1. Fetch appointment from repository
        # 2. Delegate to domain model: appointment.cancel(reason)
        # 3. Save updated state to repository
        pass

    def reschedule_appointment(self, appointment_id, new_datetime):
        # 1. Fetch appointment from repository
        # 2. Check practitioner availability for new_datetime
        # 3. Delegate to domain model: appointment.reschedule(new_datetime)
        # 4. Save updated state to repository
        pass

    def get_appointments_for_practitioner(self, practitioner_id, date):
        # 1. Fetch and return practitioner schedule from repository
        pass

    def get_appointments_for_patient(self, patient_id):
        # 1. Fetch and return patient appointment history from repository
        pass