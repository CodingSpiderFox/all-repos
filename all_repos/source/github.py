import time
from typing import Dict, List, Any
from typing import NamedTuple

from all_repos import github_api


class Settings(NamedTuple):
    api_key: str
    username: str
    collaborator: bool = False
    forks: bool = False
    private: bool = False
    archived: bool = False
    base_url: str = 'https://api.github.com'


def list_repos(settings: Settings) -> Dict[str, str]:
    new_repos : List[Dict[str, Any]] = []
    all_repos: List[Dict[str, Any]] = []
    page_num: int = 1
    per_page: int = 100
    max_total_number: int = 1

    print(f'Getting repository list for user {settings.base_url}')

    while True:
        if len(all_repos) > max_total_number:
            break
        time.sleep(1)
        print(f'Processing page number {page_num} with batch size {per_page}')
        new_repos = github_api.get_all(
            f'{settings.base_url}/users/{settings.username}/repos?per_page={per_page}&page={page_num}',
            headers={'Authorization': f'token {settings.api_key}'},
        )
        all_repos.extend(new_repos)
        page_num = page_num+1
        if len(new_repos) < per_page:
            break

    return github_api.filter_repos(
        settings.username,
        all_repos,
        forks=settings.forks,
        private=settings.private,
        collaborator=settings.collaborator,
        archived=settings.archived,
    )
