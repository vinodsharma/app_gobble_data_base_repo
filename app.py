from src.app_utils.logging_utils import logger
import src.app_utils.logging_utils as logging_utils
import src.app_utils.settings as settings
import argparse


def main():
    logger.info("Application Started")
    parser = argparse.ArgumentParser(
        description='Create Meal Recommendations for customers served '+\
                'by a regional menu')
    parser.add_argument(
        '-a', '--arg', type=int, required=True,
        help='regional_menu_id for which to create meal assignments')
    args = parser.parse_args()
    logger.info("Parameter a value %d" % (args.arg))
    logger.info("Application Ended")


if __name__ == "__main__":
    logging_utils.configure_console_logging()
    logging_utils.configure_logdna_logging(
        settings.logdna_key, settings.logdna_app)
    logging_utils.configure_bugsnag_error_monitoring(
        settings.bugsnag_key, settings.bugsnag_release_stage)
    main()
