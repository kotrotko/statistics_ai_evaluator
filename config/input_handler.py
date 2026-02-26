"""
input_handler.py
Handles user input collection and validation for grading system.
"""
import select
import sys

class InputHandler:
    """Handles collecting and validating student answers from command line."""

    @staticmethod
    def collect_input(prompt_message: str = None, end_message: str = None) -> str:
        """
        Collect multi-line input from user.

        Args:
            prompt_message: Custom message to display before input
            end_message: Custom instruction for ending input

        Returns:
            Collected input as a string
        """
        if prompt_message:
            print(prompt_message)

        if end_message:
            print(end_message)
        else:
            print("(Press Enter twice when finished, or type 'END' on a new line)\n")

        # Green italic styling
        print('\033[92m\033[3m', end='')

        lines = []
        import time

        while True:
            try:
                line = input()
            except EOFError:
                break

            if line.strip().upper() == 'END':
                break

            lines.append(line)

            # Check if last two lines are empty (double Enter)
            if len(lines) >= 2 and lines[-1] == '' and lines[-2] == '':
                lines = lines[:-2]  # Remove the two empty lines
                # This is the key: it checks if there's more data in the pipe.
                # If you pasted, select.select will see the data and return True.
                # If you actually stopped typing, it returns False after 0.1 seconds.

                import select
                import sys
                # ready_to_read, _, _ = select.select([sys.stdin], [], [], 0.1)
                readable, _, _ = select.select([sys.stdin], [], [], 0.1)

                if not readable:
                    # No more data in the clipboard buffer.
                    # Now the program officially 'stops' and moves to evaluation.
                    break
                else:
                    # Still receiving pasted data; ignore the enters and keep going.
                    continue

                # if not ready_to_read:
                #     lines = lines[:-2]  # Clean up the two Enters
                #     break
                # # if not select.select([sys.stdin], [], [], 0.1)[0]:
                # #     break
                # break

        # Reset styling
        print('\033[0m', end='')

        return '\n'.join(lines)

    @staticmethod
    def validate_input(input_text: str, min_length: int = 1) -> bool:
        """
        Validate that input meets minimum requirements.

        Args:
            input_text: The text to validate
            min_length: Minimum character length required

        Returns:
            True if valid, False otherwise
        """
        return bool(input_text.strip()) and len(input_text.strip()) >= min_length

    def collect_and_validate_input(
            self,
            question_name: str,
            question_description: str,
            min_length: int = 10
    ) -> str:
        """
        Collect and validate student input with proper formatting.

        Args:
            question_name: Name of the question (e.g., "QUESTION 1.1")
            question_description: Brief description of the question
            min_length: Minimum character length required

        Returns:
            Validated student answer or empty string if invalid
        """
        print("=" * 60)
        print(f"{question_name} EVALUATOR")
        print(question_description)
        print("=" * 60)
        print(f"\nPlease enter the student's answer to {question_name}.")

        student_answer = self.collect_input()

        if not self.validate_input(student_answer, min_length):
            print(f"\n❌ Error: Answer must be at least {min_length} characters. Exiting.")
            return ""

        return student_answer