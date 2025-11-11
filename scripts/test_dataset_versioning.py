import pytest
import os
import git
from unittest.mock import patch, MagicMock
from scripts.dataset_versioning import init_git_repo, commit_datasets, main

@pytest.fixture
def mock_repo_path(tmp_path):
    """Fixture to create a temporary directory for the git repository."""
    return str(tmp_path)

@pytest.fixture
def mock_datasets_path(tmp_path):
    """Fixture to create a temporary directory for the datasets."""
    datasets_dir = tmp_path / "datasets"
    datasets_dir.mkdir()
    # Create a dummy dataset file
    (datasets_dir / "dataset1.csv").write_text("dummy data")
    return str(datasets_dir)

def test_init_git_repo_initializes_repo(mock_repo_path):
    """Test that a new git repository is initialized if it doesn't exist."""
    repo = init_git_repo(mock_repo_path)
    assert repo is not None, "The repository should be initialized successfully."
    assert os.path.exists(os.path.join(mock_repo_path, '.git')), "The .git directory should exist."

def test_init_git_repo_existing_repo(mock_repo_path):
    """Test that an existing git repository is returned."""
    git.Repo.init(mock_repo_path)  # Manually initialize the repo
    repo = init_git_repo(mock_repo_path)
    assert repo is not None, "The existing repository should be returned."
    assert os.path.exists(os.path.join(mock_repo_path, '.git')), "The .git directory should exist."

def test_init_git_repo_exception_handling():
    """Test that init_git_repo handles exceptions and returns None."""
    with patch('git.Repo.init', side_effect=Exception("Initialization error")):
        repo = init_git_repo("/invalid/path")
        assert repo is None, "The function should return None if an exception occurs."

def test_commit_datasets_commits_changes(mock_repo_path, mock_datasets_path):
    """Test that datasets are committed successfully."""
    repo = git.Repo.init(mock_repo_path)
    commit_datasets(repo, mock_datasets_path)
    assert repo.head.commit.message == "Mise à jour des datasets", "The commit message should match."

def test_commit_datasets_no_files(mock_repo_path):
    """Test commit_datasets with no files to commit."""
    repo = git.Repo.init(mock_repo_path)
    empty_datasets_path = os.path.join(mock_repo_path, "empty_datasets")
    os.mkdir(empty_datasets_path)
    commit_datasets(repo, empty_datasets_path)
    assert repo.head.commit.message != "Mise à jour des datasets", "No commit should be made if no files are present."

def test_commit_datasets_exception_handling(mock_repo_path, mock_datasets_path):
    """Test that commit_datasets handles exceptions."""
    repo = git.Repo.init(mock_repo_path)
    with patch.object(repo.index, 'add', side_effect=Exception("Add error")):
        commit_datasets(repo, mock_datasets_path)
        assert repo.head.commit.message != "Mise à jour des datasets", "No commit should be made if an exception occurs."

def test_main_function(mock_repo_path, mock_datasets_path):
    """Test the main function end-to-end."""
    with patch('os.getcwd', return_value=mock_repo_path):
        with patch('scripts.dataset_versioning.datasets_path', new=mock_datasets_path):
            main()
            repo = git.Repo(mock_repo_path)
            assert repo.head.commit.message == "Mise à jour des datasets", "The main function should commit changes successfully."