import os
import git

def init_git_repo(repo_path):
    try:
        # Initie le repository Git si ce n'est pas déjà fait
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print("Initialisation d'un nouveau repository Git.")
            git.Repo.init(repo_path)
        return git.Repo(repo_path)
    except Exception as e:
        print(f"Erreur lors de l'initialisation du repo Git: {e}")
        return None

def commit_datasets(repo, datasets_path):
    try:
        # Ajoute tous les fichiers de datasets à l'index Git
        repo.index.add([os.path.join(datasets_path, f) for f in os.listdir(datasets_path)
                        if os.path.isfile(os.path.join(datasets_path, f))])
        
        # Création d'un commit
        repo.index.commit("Mise à jour des datasets")
        print("Changements dans les datasets commités avec succès.")
    except Exception as e:
        print(f"Erreur lors du commit des datasets: {e}")

def main():
    # Répertoire contenant les datasets
    datasets_path = "datasets"
    # Répertoire de base (racine du projet avec .git)
    repo_path = os.getcwd()
    
    repo = init_git_repo(repo_path)
    
    if repo is not None:
        commit_datasets(repo, datasets_path)

if __name__ == "__main__":
    main()