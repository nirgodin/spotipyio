import os.path
from tempfile import TemporaryDirectory

import toml
import git
from git import Repo

PYPROJECT_PATH = "pyproject.toml"
PACKAGE_NAME = "spotipyio"


class TestPackageVersion:
    def test_valid_package_version(self):
        with TemporaryDirectory() as remote_path:
            remote_repo = git.Repo.clone_from(
                url='https://github.com/nirgodin/spotipyio.git',
                to_path=remote_path,
                branch='main',
                depth=1
            )
            local_repo = git.Repo("")

            if self._has_package_changed(remote_repo, local_repo) and self._has_identical_version(remote_path):
                raise AssertionError("Package's version must change on any logical change")

    @staticmethod
    def _has_package_changed(remote_repo: Repo, local_repo: Repo) -> bool:
        local_hexsha = local_repo.head.commit.hexsha
        remote_hexsha = remote_repo.head.commit.hexsha
        diffs = local_repo.commit(local_hexsha).diff(remote_hexsha)

        for diff in diffs:
            if diff.a_path.startswith(PACKAGE_NAME) or diff.b_path.startswith(PACKAGE_NAME):
                return True

        return False

    def _has_identical_version(self, remote_path: str) -> bool:
        remote_pyproject_path = os.path.join(remote_path, PYPROJECT_PATH)
        remote_version = self._extract_package_version(remote_pyproject_path)
        local_version = self._extract_package_version(PYPROJECT_PATH)

        return remote_version == local_version

    @staticmethod
    def _extract_package_version(path: str) -> str:
        with open(path) as f:
            pyproject = toml.load(f)

        return pyproject["tool"]["poetry"]["version"]
