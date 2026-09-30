smartcare/
├── app/
│   ├── presentation/
│   │   ├── cli/
│   │   │   ├── appointment_cli.py
│   │   │   └── patient_cli.py
│   │   └── views/
│   │       └── console_view.py
│   └── main.py
│   ├── domain/
│   │   ├── models/
│   │   │   ├── patient.py
│   │   │   ├── practitioner.py
│   │   │   ├── appointment.py
│   │   │   └── appointment_status.py
│   │   ├── services/
│   │   │   ├── appointment_service.py
│   │   │   ├── patient_service.py
│   │   │   └── practitioner_service.py
│   │   └── rules/
│   │       └── validation.py
│   ├── repository/
│   │   ├── patient_repository.py
│   │   ├── appointment_repository.py
│   │   ├── practitioner_repository.py
│   │   └── repository_interfaces.py
│   ├── persistence/
│   │   ├── sqlite_patient_repository.py
│   │   ├── sqlite_appointment_repository.py
│   │   └── database.py
│   └── utils/
│       ├── datetime_helpers.py
│       └── validation_helpers.py
└── tests/
    ├── test_appointment_service.py
    ├── test_patient_service.py
    └── test_repository.py