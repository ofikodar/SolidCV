import argparse
import os

from src.chatbot.chatgpt import Chatgpt
from src.chatbot.prompts import DATA_FORMAT
from src.utils import parse_pdf, build_html_resume, export_html


def improve_resume(args):
    """
    This function takes the command line arguments, parses the input pdf resume using the parse_pdf function from the utils
    module, passes the parsed data to the Chatgpt model's improve_resume method to generate an improved version of the
    resume, and then exports the improved resume in html format using the export_html_resume function from the utils
    module.
    :param args: command line arguments containing the input and output file paths, and the data directory
    :type args: argparse.Namespace
    """
    input_path = os.path.join(args.data_dir, args.input_resume)
    parsed_resume = parse_pdf(input_path)

    # chatbot = Chatgpt(args.config_path)
    # new_resume_data = chatbot.improve_resume(parsed_resume)

    new_resume_data = DATA_FORMAT
    html_resume = build_html_resume(new_resume_data)
    output_path = os.path.join(args.data_dir, args.output_resume)
    export_html(html_resume, output_path)


def main():
    """
    Main function to parse command line arguments and call the parse_and_improve_resume function.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_dir", type=str, default='../data', help="Directory containing input and output files")
    parser.add_argument("--config_path", type=str, default='config.json', help="Path to the configuration file")
    parser.add_argument("--input_resume", type=str, default='example_input.pdf', help="Name of input resume file")
    parser.add_argument("--output_resume", type=str, default='new_resume.html', help="Name of output resume file")

    args = parser.parse_args()
    try:
        improve_resume(args)
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
