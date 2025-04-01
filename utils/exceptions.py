class ProcessingError(Exception):
    """Generic Exception durong internal process."""
    pass

class AudioProcessingError(ProcessingError):
    """Exception during transcription or audio treatment."""
    pass

class PDFProcessingError(ProcessingError):
    """Exception during pdf reading or analysis."""
    pass