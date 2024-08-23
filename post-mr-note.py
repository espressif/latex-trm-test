#!/usr/bin/env python3

import sys, os, urllib3, argparse
# Silence the irritating insecure warnings. I'm not insecure you're insecure!
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add the location of python-gitlab to the path so we can import it
repo_top = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
python_gitlab_dir = os.path.join(repo_top, "external/python-gitlab")
sys.path.append(python_gitlab_dir)
import gitlab
from collections import OrderedDict

def getArgs():
    """
    Parse the command line arguments.
    Usage: python post-mr-note.py [PROJECT-TOKEN] [PROJECT] [MR-IID]
    Sample usage: python post-mr-note.py [PROJECT-TOKEN] documentation/latex-sample-chip-errata-repo 19
    """
    parser = argparse.ArgumentParser(description='Post note to existing MR.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( "authkey", type=str, help="Project or personal access token for authentication with GitLab. Create one at https://gitlab.com/profile/personal_access_tokens" )
    parser.add_argument( "project", type=str, help="Path to GitLab project in the form <namespace>/<project>")
    parser.add_argument( "mr_iid", type=str, help="Merge request number to post the message")
    parser.add_argument( "--url",  help="Gitlab URL.")
    return parser, parser.parse_args()


class PythonGitlabNotes():
    """
    Collect links to artifacts saved by other jobs in logs folder.
    Post the links as a note to an existing merge request.
    """
    def __init__(self, url, authkey, project, mr_iid):
        # Parse command line arguments
        self.url = url
        self.url_api = url + '/api/v4'
        self.authkey = authkey
        self.project_name = project
        self.mr_iid = mr_iid
        # Create python-gitlab server instance
        server = gitlab.Gitlab(self.url, myargs.authkey, api_version=4, ssl_verify=False)
        # Get an instance of the project and store it off
        self.project = server.projects.get(self.project_name)

    def collect_data(self):
        """
        Collect data with links to PDFs in form of a dictionary.
        Chip Series (series_links)
            Module name (module_links)
                Language (language_links)
                    PDF link
        """
        series_links = {}
        for filename in os.listdir("logs"):
            file_path = os.path.join("logs", filename)
            # Process only files.
            if os.path.isfile(file_path) and filename.startswith('doc-url-3-'):
                with open(file_path, "r") as file:
                    desc_url = file.readline()
                    file.close()
                tokens = desc_url.split('\t')
                # The file contains 4 tab separated fields:
                chip_series = tokens[0].strip()
                module_name = tokens[1].strip()
                language = tokens[2].strip()
                pdf_link = tokens[3].strip()

                # Prepare a dictionary with links.
                if chip_series not in series_links:
                    series_links[chip_series] = {}
                if module_name not in series_links[chip_series]:
                    series_links[chip_series][module_name] = {}
                if language not in series_links[chip_series][module_name]:
                    series_links[chip_series][module_name][language] = pdf_link

        self.series_links = series_links

    def prepare_note(self):
        """
        Prepare a note with links to be posted in .md format.
        """
        note = "TRM preview:\n\n"
        for chip_series, module_links in self.series_links.items():
            note += f"{chip_series}:\n"
            for module_name, language_links in module_links.items():
                note += f"- {module_name} "
                # Order the language links
                language_links_ordered = OrderedDict(sorted(language_links.items()))
                for language, pdf_link in language_links_ordered.items():
                    note += f"[{language}]({pdf_link}) / "
                note = note[:-3]  # Remove the trailing " / "
                note += "\n"
            note += "\n"

        self.note = note

    def post_note(self):
        """
        Post the note to the merge request.
        """
        mr = self.project.mergerequests.get(self.mr_iid)  # Get the MR
        mr.notes.create({'body': self.note})  # Post the note to the MR

    def run(self):
        self.collect_data()
        self.prepare_note()
        self.post_note()


if __name__ == '__main__':
    myParser, myargs = getArgs()
    sys.exit(PythonGitlabNotes(url=myargs.url, authkey=myargs.authkey,
        project=myargs.project, mr_iid=myargs.mr_iid).run())
