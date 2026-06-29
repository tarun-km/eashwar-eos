"""
Training Orchestration System - Main Entry Point
AI-driven training orchestration system for managing internship batch training.
"""

from datetime import datetime, timedelta
from orchestrator import TrainingOrchestrationSystem
from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main entry point for the training orchestration system."""
    
    logger.info("=" * 80)
    logger.info("Training Orchestration System - POC")
    logger.info("=" * 80)
    
    # Initialize the system
    system = TrainingOrchestrationSystem()
    
    try:
        # Example: Create a training batch
        logger.info("Starting interactive training orchestration...")
        
        # Get user input (or use defaults for demo)
        batch_name = input("Enter batch name (default: 'Test Batch 001'): ").strip()
        if not batch_name:
            batch_name = "Test Batch 001"
        
        num_trainees = input("Enter number of trainees (default: 5): ").strip()
        if not num_trainees:
            num_trainees = 5
        else:
            num_trainees = int(num_trainees)
        
        duration_weeks = input("Enter training duration in weeks (default: 2): ").strip()
        if not duration_weeks:
            duration_weeks = 2
        else:
            duration_weeks = int(duration_weeks)
        
        skill_area = input(
            "Enter skill area (default: 'python', options: python/web-development/data-science): "
        ).strip()
        if not skill_area:
            skill_area = "python"
        
        training_type = input("Enter training type (default: 'full-day', options: full-day/half-day): ").strip()
        if not training_type:
            training_type = "full-day"
        
        # Create batch
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        logger.info(f"Creating training batch: {batch_name}")
        
        batch_result = system.create_training_batch(
            batch_name=batch_name,
            num_trainees=num_trainees,
            duration_weeks=duration_weeks,
            start_date=start_date,
            skill_area=skill_area,
            training_type=training_type
        )
        
        logger.info(f"✓ Batch created successfully!")
        logger.info(f"  Batch ID: {batch_result['batch_id']}")
        logger.info(f"  Total Days: {batch_result['plan']['statistics']['total_days']}")
        logger.info(f"  Total Sessions: {batch_result['plan']['statistics']['total_sessions']}")
        logger.info(f"  Total Training Hours: {batch_result['plan']['statistics']['total_training_hours']}")
        
        # Show batch summary
        batch_id = batch_result['batch_id']
        summary = system.get_batch_summary(batch_id)
        
        logger.info("\nBatch Summary:")
        logger.info(f"  Name: {summary['batch_name']}")
        logger.info(f"  Skill Area: {summary['skill_area']}")
        logger.info(f"  Status: {summary['status']}")
        logger.info(f"  Duration: {(summary['end_date'])} to {(summary['end_date'])}")
        
        logger.info("\n✓ Training orchestration system is ready!")
        logger.info("Next steps:")
        logger.info("1. Configure Teams integration in .env file")
        logger.info("2. Run example_usage.py for full workflow demo")
        logger.info("3. Check logs in 'logs' directory for detailed execution logs")
        
    except KeyboardInterrupt:
        logger.info("\nSystem interrupted by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        system.close()
        logger.info("\nTraining Orchestration System shutdown complete")


if __name__ == "__main__":
    main()
