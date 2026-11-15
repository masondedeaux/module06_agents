class FallbackModel:  # Give a chatbot two compatible sources of decisions.
    """Ask the backup model if the primary model has no answer."""

    def __init__(
        self, primary, backup
    ):  # Receive both models when creating the wrapper.
        self.primary = primary  # Keep the model to try first.
        self.backup = backup  # Keep the model to try when the primary is unavailable.

    def decide(
        self, instructions, history, tools
    ):  # Use the same contract as each model.
        decision = self.primary.decide(instructions, history, tools)  # Try the primary.
        if decision is None:  # None means that the primary could not answer.
            return self.backup.decide(instructions, history, tools)  # Ask the backup.
        return decision  # Forward a valid primary decision unchanged.
