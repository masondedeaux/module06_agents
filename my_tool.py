from toolbox import Toolbox


class FaqLookup:  # Keep cafe FAQ data independent of conversation code.
    def __init__(self, answers):  # Receive topic names mapped to factual replies.
        self.answers = answers  # Store the made-up cafe's FAQ dictionary.

    def find_answer(self, text):  # Find an answer for a topic in the message.
        for topic in self.answers:  # Check each known FAQ keyword in order.
            if topic.lower() in text.lower():  # Match regardless of letter case.
                return self.answers[topic]  # Return only a stored FAQ answer.
        return None  # Signal that the tool has no matching information.

    def look_up_faq(self, topic):  # Expose the existing lookup as a model tool.
        """Look up the cafe's hours, parking, or Wi-Fi.

        Args:
            topic: Words copied from the customer, such as hours, parking, or Wi-Fi.
        """
        answer = self.find_answer(topic)  # Read the answer from the stored facts.
        return answer or "I don't have information on that topic. Please ask staff."


class ReservationQueue:  # Keep pending requests separate from confirmed reservations.
    """Store reservation requests until a staff member reviews them."""

    def __init__(self):  # Start each program run with its own in-memory data.
        self.requests = {}  # Index requests by their review number.
        self.reservations = []  # Keep only approved bookings here.

    def request_reservation(self, name, time):  # Make a request for staff review.
        """Request a table reservation that staff must approve.

        Args:
            name: The customer's name as they wrote it.
            time: The requested day and time as the customer wrote it.
        """
        number = len(self.requests) + 1  # Give the request a unique review number.
        # Keep the requested details and mark them as pending for staff.
        request = {"number": number, "name": name, "time": time, "status": "waiting"}
        self.requests[number] = request  # Store the request without reserving a table.
        return f"Request {number} is waiting for staff approval."

    def waiting(self):  # List the requests that still need a staff decision.
        # Approved and rejected requests stay in the record but leave the review list.
        return [item for item in self.requests.values() if item["status"] == "waiting"]

    def approve(
        self, number
    ):  # Convert a waiting request into a confirmed reservation.
        request = self.requests.get(number)  # Get the request by its review number.
        if request is None:  # Handle invalid request numbers safely.
            return f"There is no request {number}."
        if request["status"] != "waiting":  # Enforce one decision per request.
            return f"Request {number} is already {request['status']}."
        # Save the reservation only once, while its request is still waiting.
        self.reservations.append({"name": request["name"], "time": request["time"]})
        request["status"] = "approved"  # Record the decision after saving the booking.
        return f"Request {number} approved."

    def reject(self, number):  # Close a request without creating a reservation.
        request = self.requests.get(number)  # Get the request by its review number.
        if request is None:  # Handle invalid request numbers safely.
            return f"There is no request {number}."
        if request["status"] != "waiting":  # Preserve the existing decision.
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"  # Remove this request from the review list.
        return f"Request {number} rejected."


class CafeToolbox:  # Give Bean one checked entry point for its tools.
    """Check tool requests against the customer's messages before running them."""

    def __init__(self, faq, queue):  # Receive the two cafe tools.
        self.faq = faq  # Keep the existing read-only FAQ lookup.
        self.queue = queue  # Keep the staff review queue.

    def tool_list(self):  # Give the model the two methods it can request.
        # Staff approval is handled by the CLI and never advertised as a model tool.
        return [self.faq.look_up_faq, self.queue.request_reservation]

    def run(self, name, arguments, history):  # Validate and dispatch one model request.
        if name == "look_up_faq":  # Only run the read-only lookup in this branch.
            topic = Toolbox.clean(arguments, "topic")  # Remove extra whitespace.
            if not topic:  # Ask for a topic when the model left it empty.
                return "Ask the customer what they want to know about the cafe."
            if not Toolbox.customer_said(
                history, topic
            ):  # Check that the topic was given.
                return "The customer has not given that topic. Ask them what they need."
            return self.faq.look_up_faq(topic)  # Return the stored answer.
        if name == "request_reservation":  # Check both booking details before queuing.
            customer_name = Toolbox.clean(arguments, "name")  # Read the supplied name.
            time = Toolbox.clean(arguments, "time")  # Read the supplied date and time.
            if not customer_name or not time:  # Require a complete reservation request.
                return "Ask the customer for their name and requested day and time."
            if not Toolbox.customer_said(
                history, customer_name
            ):  # Refuse an invented name.
                return "The customer has not given that name. Ask them for it."
            if not Toolbox.customer_said(
                history, time
            ):  # Refuse an invented day or time.
                return "The customer has not given that time. Ask them for it."
            return self.queue.request_reservation(
                customer_name, time
            )  # Send it to staff.
        return f"There is no tool named {name}."  # Refuse every unlisted tool.
