"""
Safety policies and guards for SAISA agent.
Protections against accidental deletion and harmful actions.
"""

from __future__ import annotations


class DeleteGuard:
    """Requires 5 explicit confirmations before any file deletion."""

    REQUIRED_CONFIRMATIONS = 5
    TOKEN = "YES"

    def confirm_delete(self, path_display: str) -> bool:
        """Confirm file deletion.
        
        Args:
            path_display: Path to delete (for display).
            
        Returns:
            True if confirmed, False otherwise.
        """
        print()
        print("!!! FILE DELETION REQUESTED !!!")
        print(f"  Target: {path_display}")
        print(
            f"  Type exactly '{self.TOKEN}' "
            f"{self.REQUIRED_CONFIRMATIONS} times in a row to confirm."
        )
        print("  Press Enter or type anything else to cancel.")
        print()

        for i in range(1, self.REQUIRED_CONFIRMATIONS + 1):
            raw = input(f"  Confirm {i}/{self.REQUIRED_CONFIRMATIONS}: ").strip()
            if raw != self.TOKEN:
                print("  ❌ Cancelled: confirmation refused or incorrect.")
                return False

        print("  ✅ All confirmations received: deletion authorized.")
        return True
