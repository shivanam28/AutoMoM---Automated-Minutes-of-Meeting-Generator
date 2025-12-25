"""
Exception Utility for AutoMoM
-----------------------------
Provides a detailed custom exception handler.
"""

import sys
from automom.utils.logger import logger


class AutoMoMException(Exception):
    """
    Custom exception with detailed context (file name, line number, error message).
    """

    def __init__(self, error_message, error_detail: sys = None):
        super().__init__(error_message)
        self.error_message = AutoMoMException.get_detailed_error_message(
            error_message, error_detail
        )

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        detailed_message = (
            f"\n❌ Error in file: {file_name}"
            f"\n🧩 Line: {line_number}"
            f"\n💬 Message: {str(error_message)}"
        )

        logger.error(detailed_message)
        return detailed_message

    def __str__(self):
        return self.error_message


__all__ = ["AutoMoMException"]

# Example usage:
# try:
#     1 / 0
# except Exception as e:
#     raise AutoMoMException(e, sys)
