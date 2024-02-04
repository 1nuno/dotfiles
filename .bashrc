# .bashrc

# Options
set -o vi
unset rc
eval "$(starship init bash)"

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
	for rc in ~/.bashrc.d/*; do
		if [ -f "$rc" ]; then
			. "$rc"
		fi
	done
fi

gcc_run() {
    local file_name="${1%.*}"
    gcc "$1" -o "$file_name" && ./"$file_name" && rm "$file_name"
}

alias sd="cd \$(fd --type d | fzf --color=gutter:-1,info:#284564,hl:#284564,prompt:#284564)"

# Variables
#
# fzf
#export FZF_DEFAULT_COMMAND='fd -t f --strip-cwd-prefix --color=always'
export FZF_DEFAULT_COMMAND='fd --type f --color=always --exclude .git --ignore-file ~/.gitignore'
export FZF_CTRL_T_COMMAND=$FZF_DEFAULT_COMMAND
#
# starship
export STARSHIP_CONFIG=~/.config/starship/starship.toml

export PATH=$PATH:/usr/bin/obsidian


export term_prompt_bg='#284564'
export term_prompt_fg='#ffffff'
