"""module for simpifying string for file pattern"""

import re


def simpling(input_val: str) -> str:
    """Get input-param and sumplifuing into file-pattern.
    NOTE: only first 100 symbols get in output
    """
    return re.sub(r'[/\\:*?"<>|]', "_", input_val[:150:])
