from groq import Groq
import os

# GROQ API KEY
os.environ["GROQ_API_KEY"] = "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"

class Question2Evaluator:
    def __init__(self):
        """Initialize the evaluator with Groq API key."""
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Please set GROQ_API_KEY in the code above")

        self.client = Groq(api_key=self.api_key)

    def create_prompt(self, student_submission):
        """Create evaluation prompt matching instructor's grading style"""

        return f"""You are a statistics professor evaluating Question 2 of a hypothesis testing assignment. 

**THE GRADING PHILOSOPHY:**
- Focus on conceptual understanding over formatting
- Ignore minor symbol errors (e.g., =/= instead of ≠ is just a typing issue)
- Be strict about missing conceptual elements
- Award partial credit appropriately
- Write brief, helpful comments like a real professor would

**GRADING CRITERIA (Total 20 points):**

**Checkpoint 1 - Name the method applied to check the normality assumption (5 points):**
This checkpoint asks the student to explicitly state in their written answer which method they will use to check the normality assumption.

Must explicitly write the method name in a sentence (e.g., "I will use the Shapiro-Wilk test" or "I applied the Shapiro-Wilk test")
The method name appearing only in a table header or table title does NOT count as explicitly stating the method
The student must write it in their own words as part of their answer text
Common mistake: Only showing the method name in the table header without writing it in the answer text
Common mistake: Not mentioning the method at all
Deduction: No explicit written statement of the method (even if it appears in table header) = -5 points (give 0/5)
Deduction: Incomplete or unclear statement = -2 points (give 3/5)

**Checkpoint 2 - Check Normality with α = 0.001 and Insert Table (5 points):**
This checkpoint asks the student to provide the normality test results.
- Must include a table (the output from JASP)
- The table should contain the normality test results
- **Common mistake:** Providing results without proper table format
- **Common mistake:** Missing or empty table
- **Deduction:** Results provided but not in table format = -1 point (give 4/5)
- **Deduction:** Missing table or no results at all = -5 points (give 0/5)

**Checkpoint 3 - Is This Distribution Normal? (5 points):**
This checkpoint asks the student to state whether the distribution is normal or not.
CRITICAL: The student MUST provide a clear yes/no statement about normality.
- If there is NO clear yes/no statement, give 0/5
- **Deduction:** No clear yes/no statement about normality = -5 points (give 0/5)
- **Deduction:** Wrong conclusion (contradicts test results) = -5 points (give 0/5)

**Checkpoint 4 - Explain Your Reasoning (5 points):**
This checkpoint evaluates three elements:
1. Did student attempt to explain? (1 point)
2. Is the conclusion correct? (1 point)
3. Is the reasoning correct? (3 points)

- **Deduction:** No explanation attempted = -1 point
- **Deduction:** Wrong or missing conclusion = -1 point
- **Deduction:** Wrong reasoning = -3 points

---

**STUDENT SUBMISSION:**
{student_submission}

---
**THE EVALUATION FORMAT:**

For each checkpoint, provide:
1. Score (X/5)
2. Quote the relevant part of student's text
3. Brief comment explaining the issue (like a real professor)
4. Helpful hint (not a directive)

**Checkpoint 1 - Name the normality method: X/5 points**

Student wrote: "[quote their method statement]"

Comment: [Brief explanation of what's wrong/right, in conversational tone]

Hint: [Gentle guidance on how to improve, not a directive]

---

**Checkpoint 2 - Check Normality with α = 0.001 and Insert Table: X/5 points**

Student wrote: "[quote their table or results]"

Comment: [Brief explanation]

Hint: [Gentle guidance]

---

**Checkpoint 3 - Is This Distribution Normal? X/5 points**

Student wrote: "[quote their normality conclusion]"

Comment: [Brief explanation]

Hint: [Gentle guidance]

---

**Checkpoint 4 - Explain Your Reasoning: X/5 points**

Student wrote: "[quote their reasoning]"

Comment: [Brief explanation]

Hint: [Gentle guidance]

---

**TOTAL: XX/20 points**

**Overall Comment:** [1 sentence summarizing the main issues and strengths]"""

    def evaluate(self, student_submission):
        """Evaluate student's Question 2 submission"""
        prompt = self.create_prompt(student_submission)

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are a helpful statistics professor who grades fairly, writes brief conversational comments, and gives hints rather than directives. You focus on conceptual understanding and ignore minor formatting issues.

CRITICAL GRADING RULES:

For Checkpoint 1:
- Look for a sentence that explicitly states the method name (e.g., "I used Shapiro-Wilk test")
- Method name ONLY in table header does NOT count
- If no such sentence exists, give 0/5

For Checkpoint 2:
- Look for a properly formatted table with test results
- If results are provided but not in table format, give 4/5
- If no results at all, give 0/5

For Checkpoint 3:
- Look for explicit statement "the distribution is normal" or "the distribution is not normal"
- General explanations about p-values do NOT count as answering this checkpoint
- If no clear yes/no statement exists, give 0/5

For Checkpoint 4:
- Checkpoint 4 reasoning must use α = 0.001 from Checkpoint 3. If student uses different α, deduct 3 points.
- Look for explanation of HOW they determined normality (p-value comparison with α=0.001)
- Evaluate three elements independently:
  * Did student attempt to explain? (1 point)
  * Is the conclusion correct? (1 point)
  * Is the reasoning correct? (3 points)
- Wrong reasoning (using wrong α, incorrect statistical logic) = deduct 3 points
- Calculate: 5 - (sum of deductions)

Do not reuse the same text for multiple checkpoints. Each checkpoint requires different content."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=2500
            )

            evaluation = chat_completion.choices[0].message.content

            # Try to extract total score
            total_score = None
            for line in evaluation.split('\n'):
                if 'TOTAL:' in line.upper():
                    try:
                        parts = line.split(':')[1].strip().split('/')
                        total_score = int(parts[0].strip())
                    except:
                        pass

            return {
                "status": "success",
                "evaluation": evaluation,
                "total_score": total_score,
                "model": chat_completion.model,
                "tokens_used": chat_completion.usage.total_tokens
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def print_evaluation(self, result):
        """Pretty print the evaluation results"""
        if result['status'] == 'success':
            print("=" * 80)
            print("QUESTION 2 EVALUATION")
            print("=" * 80)
            print(result['evaluation'])
            print("=" * 80)
            if result['total_score'] is not None:
                print(f"\n📊 FINAL SCORE: {result['total_score']}/20")
            print(f"🤖 Model: {result['model']}")
            print(f"🔧 Tokens used: {result['tokens_used']}")
        else:
            print(f"❌ ERROR: {result['error']}")


if __name__ == "__main__":
    evaluator = Question2Evaluator()

    print("Paste the student's submission (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    submission = "\n".join(lines)
    result = evaluator.evaluate(submission)
    evaluator.print_evaluation(result)