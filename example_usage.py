"""
Example usage and demonstration of the Training Orchestration System.
"""
from datetime import datetime, timedelta
from orchestrator import TrainingOrchestrationSystem


def demo_full_workflow():
    """Demonstrate complete training orchestration workflow."""
    
    print("=" * 80)
    print("TRAINING ORCHESTRATION SYSTEM - DEMO")
    print("=" * 80)
    
    # Initialize system
    system = TrainingOrchestrationSystem()
    
    try:
        # 1. Create a training batch
        print("\n[1] Creating Training Batch...")
        print("-" * 80)
        
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        trainees = [
            {"name": "Alice Johnson", "email": "alice@example.com"},
            {"name": "Bob Smith", "email": "bob@example.com"},
            {"name": "Carol White", "email": "carol@example.com"},
            {"name": "David Brown", "email": "david@example.com"},
        ]
        
        batch_result = system.create_training_batch(
            batch_name="Python Intensive - Batch 001",
            num_trainees=len(trainees),
            duration_weeks=2,
            start_date=start_date,
            skill_area="python",
            training_type="full-day",
            trainee_list=trainees
        )
        
        batch_id = batch_result["batch_id"]
        print(f"✓ Batch Created: {batch_result['batch_name']} (ID: {batch_id})")
        print(f"  Duration: {batch_result['plan']['statistics']['total_days']} days")
        print(f"  Total Sessions: {batch_result['plan']['statistics']['total_sessions']}")
        print(f"  Total Training Hours: {batch_result['plan']['statistics']['total_training_hours']}")
        
        # 2. View batch summary
        print("\n[2] Viewing Batch Summary...")
        print("-" * 80)
        
        summary = system.get_batch_summary(batch_id)
        print(f"Batch: {summary['batch_name']}")
        print(f"Trainees: {summary['num_trainees']}")
        print(f"Total Sessions: {summary['total_sessions']}")
        print(f"Skill Area: {summary['skill_area']}")
        
        # 3. Schedule Teams meetings
        print("\n[3] Scheduling Teams Meetings...")
        print("-" * 80)
        
        meetings_result = system.schedule_batch_with_teams_meetings(
            batch_id=batch_id,
            organizer_email="trainer@example.com"
        )
        
        print(f"✓ Teams Meetings Scheduled: {meetings_result['meetings_created']} meetings")
        
        # 4. Generate assessment for first session
        print("\n[4] Generating Assessment for Session...")
        print("-" * 80)
        
        assessment = system.generate_session_assessment(session_id=1)
        print(f"✓ Assessment Generated: {assessment['assessment_id']}")
        print(f"  Topic: {assessment['topic']}")
        print(f"  Number of Questions: {assessment['num_questions']}")
        print(f"  Time Limit: {assessment['time_limit_minutes']} minutes")
        print(f"  Passing Score: {assessment['passing_score']}%")
        
        # 5. Record trainee attendance
        print("\n[5] Recording Trainee Attendance...")
        print("-" * 80)
        
        now = datetime.now()
        joined_time = now
        left_time = now + timedelta(minutes=35)
        
        attendance = system.record_trainee_attendance(
            session_id=1,
            trainee_id=1,
            joined_time=joined_time,
            left_time=left_time
        )
        
        print(f"✓ Attendance Recorded")
        print(f"  Trainee ID: 1")
        print(f"  Session ID: 1")
        print(f"  Status: {attendance['status']}")
        
        # 6. Execute a session
        print("\n[6] Executing Training Session...")
        print("-" * 80)
        
        execution = system.execute_scheduled_session(session_id=1)
        print(f"✓ Session Execution Started")
        print(f"  Session ID: {execution['session_id']}")
        print(f"  Status: {execution['status']}")
        print(f"  Content Started: {execution['content_started']}")
        print(f"  Meeting Started: {execution['meeting_started']}")
        
        print("\n" + "=" * 80)
        print("DEMO COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        system.close()


def demo_training_plan_only():
    """Demonstrate training plan generation."""
    
    print("\n" + "=" * 80)
    print("TRAINING PLAN GENERATION DEMO")
    print("=" * 80)
    
    system = TrainingOrchestrationSystem()
    
    try:
        # Create a training plan
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        plan = system.plan_engine.create_training_plan(
            num_trainees=20,
            duration_weeks=1,
            start_date=start_date,
            skill_area="web-development",
            training_type="full-day"
        )
        
        print(f"\nTraining Plan Created:")
        print(f"  Skill Area: {plan['skill_area']}")
        print(f"  Duration: {plan['duration_weeks']} weeks")
        print(f"  Number of Business Days: {plan['total_business_days']}")
        print(f"  Total Sessions: {plan['statistics']['total_sessions']}")
        print(f"  Total Training Hours: {plan['statistics']['total_training_hours']}")
        
        # Display first day schedule
        if plan['daily_schedule']:
            print(f"\nFirst Day Schedule:")
            first_day = plan['daily_schedule'][0]
            print(f"  Date: {first_day['date']}")
            print(f"  Sessions:")
            for session in first_day['sessions']:
                print(f"    - {session['topic']} ({session['session_type']}) - {session['duration_minutes']}min")
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        system.close()


if __name__ == "__main__":
    # Run the full workflow demo
    demo_full_workflow()
    
    # Uncomment to run plan-only demo
    # demo_training_plan_only()
