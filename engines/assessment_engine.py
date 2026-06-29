"""
Assessment Engine - Generates and manages assessments.
"""
import json
import random
from datetime import datetime
from typing import Dict, Any, List
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AssessmentEngine:
    """Engine for generating and managing assessments."""
    
    def __init__(self):
        self.questions_per_session = Settings.assessment.QUESTIONS_PER_SESSION
        self.passing_score = Settings.assessment.PASSING_SCORE
        self.assessment_time = Settings.assessment.ASSESSMENT_TIME_MINUTES
    
    def generate_assessment(
        self,
        session_topic: str,
        num_questions: int = None,
        difficulty: str = "mixed"
    ) -> Dict[str, Any]:
        """
        Generate assessment questions for a session.
        
        Args:
            session_topic: Topic of the session
            num_questions: Number of questions (default from config)
            difficulty: Question difficulty level
        
        Returns:
            Assessment with questions
        """
        if num_questions is None:
            num_questions = self.questions_per_session
        
        try:
            logger.info(f"Generating assessment for topic: {session_topic}")
            
            questions = self._generate_questions(session_topic, num_questions, difficulty)
            
            assessment = {
                "assessment_id": self._generate_id(),
                "topic": session_topic,
                "num_questions": len(questions),
                "questions": questions,
                "difficulty": difficulty,
                "time_limit_minutes": self.assessment_time,
                "passing_score": self.passing_score,
                "created_at": datetime.utcnow().isoformat(),
                "status": "created"
            }
            
            logger.info(f"Assessment created with {len(questions)} questions")
            return assessment
        
        except Exception as e:
            logger.error(f"Error generating assessment: {str(e)}")
            raise
    
    def submit_assessment(
        self,
        assessment: Dict[str, Any],
        responses: List[Dict[str, Any]],
        time_taken_minutes: int
    ) -> Dict[str, Any]:
        """
        Submit and score assessment.
        
        Args:
            assessment: Assessment object
            responses: List of question responses with answers
            time_taken_minutes: Time taken to complete
        
        Returns:
            Scored assessment result
        """
        try:
            logger.info(f"Submitting assessment {assessment['assessment_id']}")
            
            score = self._calculate_score(assessment, responses)
            passed = score >= self.passing_score
            
            result = {
                "assessment_id": assessment["assessment_id"],
                "responses": responses,
                "score": score,
                "passed": passed,
                "time_taken_minutes": time_taken_minutes,
                "feedback": self._generate_feedback(score, assessment),
                "submitted_at": datetime.utcnow().isoformat(),
                "status": "completed"
            }
            
            logger.info(f"Assessment scored: {score}% - {'PASSED' if passed else 'FAILED'}")
            return result
        
        except Exception as e:
            logger.error(f"Error submitting assessment: {str(e)}")
            raise
    
    def _generate_questions(
        self,
        topic: str,
        num_questions: int,
        difficulty: str
    ) -> List[Dict[str, Any]]:
        """
        Generate question templates for a topic.
        
        Args:
            topic: Topic name
            num_questions: Number of questions to generate
            difficulty: Difficulty level
        
        Returns:
            List of questions
        """
        question_templates = {
            "multiple-choice": [
                {
                    "id": 1,
                    "type": "multiple-choice",
                    "question": f"What is a fundamental concept in {topic}?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 0
                },
                {
                    "id": 2,
                    "type": "multiple-choice",
                    "question": f"Which statement is true about {topic}?",
                    "options": ["Statement 1", "Statement 2", "Statement 3", "Statement 4"],
                    "correct_answer": 1
                },
            ],
            "true-false": [
                {
                    "id": 3,
                    "type": "true-false",
                    "question": f"{topic} requires extensive setup.",
                    "correct_answer": "false"
                },
            ],
            "short-answer": [
                {
                    "id": 4,
                    "type": "short-answer",
                    "question": f"Explain the key benefit of using {topic}.",
                    "correct_answer": "Provides efficiency and scalability"
                },
            ]
        }
        
        questions = []
        question_id = 1
        
        for _ in range(num_questions):
            q_type = random.choice(list(question_templates.keys()))
            template = random.choice(question_templates[q_type])
            
            question = template.copy()
            question["id"] = question_id
            question["difficulty"] = difficulty
            questions.append(question)
            question_id += 1
        
        return questions
    
    def _calculate_score(
        self,
        assessment: Dict[str, Any],
        responses: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate assessment score.
        
        Args:
            assessment: Assessment object
            responses: User responses
        
        Returns:
            Score as percentage
        """
        if not assessment["questions"]:
            return 0.0
        
        correct_count = 0
        
        for response in responses:
            question_id = response["question_id"]
            user_answer = response["answer"]
            
            # Find corresponding question
            question = next(
                (q for q in assessment["questions"] if q["id"] == question_id),
                None
            )
            
            if question and user_answer == question.get("correct_answer"):
                correct_count += 1
        
        score = (correct_count / len(assessment["questions"])) * 100
        return round(score, 2)
    
    def _generate_feedback(
        self,
        score: float,
        assessment: Dict[str, Any]
    ) -> str:
        """
        Generate feedback based on score.
        
        Args:
            score: Assessment score
            assessment: Assessment object
        
        Returns:
            Feedback message
        """
        if score >= 90:
            return "Excellent! You have mastered the topic."
        elif score >= 75:
            return "Good job! You have strong understanding of the topic."
        elif score >= self.passing_score:
            return "You passed! Continue to review areas you found challenging."
        else:
            return "You need to review the material and retake the assessment."
    
    def _generate_id(self) -> str:
        """Generate unique assessment ID."""
        return f"ASSESS_{int(datetime.utcnow().timestamp() * 1000)}"
