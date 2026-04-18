# Git workflow for this project

Follow these steps in order the first time, then use the **ongoing workflow** for everyday changes.

---

## Before you start

1. **Install Git** (if needed): [https://git-scm.com/download/win](https://git-scm.com/download/win)  
   Confirm in PowerShell: `git --version`

2. **Secrets**: Never commit API keys. This repo uses `IBM_QUANTUM_TOKEN` via the environment (see `.env.example`). Do **not** commit `.env`.

3. **Large files**: `.gitignore` excludes big CSVs, reference PDFs under `Documents/`, and PCAPs. If `git status` still shows huge files, unstage them (`git reset HEAD -- path`) and extend `.gitignore`.

---

## First-time setup (local repository)

Open PowerShell **in the project folder** (the one that contains `README.md` and `repo_paths.py`):

```powershell
cd "C:\Users\ishan\OneDrive\Desktop\GRA\Feature Selection"
```

### Step 1 — Initialize Git (once per folder)

```powershell
git init
```

### Step 2 — See what will be tracked

```powershell
git status
```

### Step 3 — Stage all allowed files

```powershell
git add .
```

### Step 4 — Review the staged set (recommended)

```powershell
git status
```

Check that no secrets, `.env`, or multi-gigabyte data files appear. To unstage a file:

```powershell
git reset HEAD path\to\file
```

### Step 5 — Create the first commit

```powershell
git commit -m "Initial commit: feature selection project layout and notebooks"
```

---

## Connect to GitHub (remote)

### Step 6 — Create an empty repository on GitHub

- On [github.com](https://github.com): **New repository**  
- Name it (e.g. `feature-selection-quantum`).  
- Do **not** add a README or `.gitignore` on GitHub if you already have them locally (avoids merge noise).

### Step 7 — Link your folder to that repository

Replace `YOUR_USER` and `YOUR_REPO` with your GitHub username and repo name:

```powershell
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git branch -M main
```

### Step 8 — Push

```powershell
git push -u origin main
```

If GitHub asks for credentials, use a **Personal Access Token** (not your account password) when using HTTPS, or set up SSH keys.

---

## Ongoing workflow (after the first push)

After you edit notebooks, `repo_paths.py`, or docs:

```powershell
cd "C:\Users\ishan\OneDrive\Desktop\GRA\Feature Selection"
git status
git add .
git commit -m "Short description of what changed"
git push
```

Useful commands:

| Command | Purpose |
|--------|---------|
| `git status` | See modified / staged files |
| `git diff` | See unstaged changes |
| `git log --oneline -5` | Last five commits |

---

## Optional: branch for experiments

```powershell
git checkout -b experiment/grid-tweak
# work, commit, then:
git push -u origin experiment/grid-tweak
```

---

## If something goes wrong

- **Committed a secret by mistake**: Revoke the key on the provider (e.g. IBM Quantum), remove the file from history or use GitHub guidance for removing sensitive data, then rotate keys.  
- **Push rejected**: Run `git pull --rebase origin main` then `git push` (or resolve conflicts as prompted).  
- **Wrong remote URL**: `git remote set-url origin https://github.com/YOUR_USER/YOUR_REPO.git`
