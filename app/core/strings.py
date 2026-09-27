class Strings:
    # Roles
    ROLE_PATIENT = "patient"
    ROLE_ADMIN = "admin"

    # Statuses
    STATUS_PENDING = "PENDING"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_FAILED = "FAILED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_SUCCESS = "SUCCESS"

    # Webhook Statuses
    WEBHOOK_PROCESSED = "PROCESSED"
    WEBHOOK_DUPLICATE_NOOP = "DUPLICATE_NOOP"
    WEBHOOK_CONFLICT_IGNORED = "CONFLICT_IGNORED"
    WEBHOOK_UNRECOGNIZED = "UNRECOGNIZED"
    WEBHOOK_RECEIVED = "RECEIVED"

    # Errors
    ERR_BOOKING_NOT_FOUND = "Booking not found."
    ERR_NOT_OWNER = "You do not have permission to access this resource."
    ERR_BOOKING_NOT_PAYABLE = "This booking is not in a payable state."
    ERR_EMAIL_EXISTS = "Email already registered."
    ERR_INVALID_CREDENTIALS = "Invalid email or password."
    ERR_TEST_NOT_FOUND = "Test not found."
    ERR_TEST_INACTIVE = "Test is currently inactive."
    ERR_PAST_DATE = "Appointment date must be in the future."
    ERR_ALREADY_CANCELLED = "Booking is already cancelled."
    ERR_PAST_APPOINTMENT = "Cannot cancel a confirmed booking whose appointment date has passed."

    # Error Codes
    CODE_BOOKING_NOT_FOUND = "BOOKING_NOT_FOUND"
    CODE_NOT_OWNER = "NOT_OWNER"
    CODE_BOOKING_NOT_PAYABLE = "BOOKING_NOT_PAYABLE"
    CODE_EMAIL_EXISTS = "EMAIL_EXISTS"
    CODE_INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    CODE_TEST_NOT_FOUND = "TEST_NOT_FOUND"
    CODE_TEST_INACTIVE = "TEST_INACTIVE"
    CODE_PAST_DATE = "PAST_DATE"
    CODE_INVALID_TRANSITION = "INVALID_TRANSITION"
