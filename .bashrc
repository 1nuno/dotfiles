# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Vi mode 
set -o vi

# Eval
eval "$(zoxide init --cmd cd bash)"
eval "$(starship init bash)"

# Variables
export FZF_DEFAULT_COMMAND='fd --type f --color=always --exclude .git --ignore-file ~/.gitignore'
export FZF_CTRL_T_COMMAND=$FZF_DEFAULT_COMMAND
export PATH=$PATH:/usr/bin/obsidian
export PATH=$PATH:~/.local/bin/
export PATH=$PATH:/usr/local/MATLAB/R2023b/bin/
export PATH=~$PATH:~/Desktop/mitteny/
export PATH="$HOME/local/bin:$PATH"
export STARSHIP_CONFIG=~/.config/starship/starship.toml
export term_prompt_bg='#284564'
export term_prompt_fg='#ffffff'

# Functions
gcc_run() {
    local file_name="${1%.*}"
    gcc "$1" -o "$file_name" && ./"$file_name" && rm "$file_name"
}

# Aliases
alias rnote='flatpak run com.github.flxzt.rnote'
alias sd='cd "$(fd . /home/1nuno/ -L --type d | fzf --color=gutter:-1,info:#284564,hl:#284564,prompt:#284564)"'
alias svenv='source "$(fd . /home/1nuno/Desktop/virtual_envs -d 1 -L --type d | fzf --color=gutter:-1,info:#284564,hl:#284564,prompt:#284564)"/bin/activate'
alias sdc='cd "$(fd . /home/1nuno/.config -d 1 -L --type d | fzf --color=gutter:-1,info:#284564,hl:#284564,prompt:#284564)"'
alias sbash='source ~/.bashrc'
