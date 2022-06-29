# VyperTraining Smart Contracts

# 1 - Setting up the environment:

## Recommendations:

The following tools are not required but highly recommended for a better coding experience:

- **Terminal (Mac OS only):** iTerm 2 ([download](https://iterm2.com/))
- **Shell:** Oh my ZSH ([download](https://ohmyz.sh/#install))
- **Code Editor:** VS Code ([download](https://code.visualstudio.com/))
- **VS Code Plugins:**
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  - [Vyper](https://marketplace.visualstudio.com/items?itemName=tintinweb.vscode-vyper)

<br/>
<br/>

## Requirements:

- **Git** of course :-)
- **pyenv-virtualenv** :

  - Mac OS:

    1. Install **Homebrew** ([install](https://brew.sh/))

    1. Install package:
       ```sh
       brew install pyenv-virtualenv
       ```
    1. Add it to path (assuming you are using ZSH)
       ```sh
       echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
       ```
       ```sh
       echo 'eval "$(pyenv init -)"' >> ~/.zshrc
       ```
       ```sh
       echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
       ```

  - Other OS:
    ([Follow instructions to install](https://github.com/pyenv/pyenv-virtualenv))

<br/>
<br/>

## Configuration Steps:

1. Clone the repo

   ```sh
   git clone git@github.com:VyperTraining/smart-contracts.git
   ```

   and then:

   ```sh
   cd smart-contracts
   ```

1. Install python version

   ```sh
   pyenv install 3.9.8
   ```

1. Create the Python virtual environment (Only needed once)

   ```sh
   pyenv virtualenv 3.9.8 vyper-training

   ```

1. Update PIP
   ```sh
   pip install -U pip
   ```
   
1. Install Vyper
   ```sh
   pip install vyper==0.3.3
   ```

1. Install Black (Code formatter)
   ```sh
   pip install black
   ```
   
1. Install Ape Worx
   ```sh
   pip install eth-ape
   ```

1. Install Vyper Plugin
   ```sh
   ape plugins install vyper
   ```
   <br />
   <br />

## Running the project:

- **To Compile** the smart-contracts, run:
  ```sh
  ape compile
  ```
- **Run tests** with:
  ```sh
  ape test
  ```

