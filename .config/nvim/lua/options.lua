-- In case you have doubt about any of the options that im setting here
-- just type (while in normal mode) -> :h options. This should bring up
-- a documentation where you can then learn about what exactly each one
-- of these options is doing. For example if i look at this option:
-- << vim.opt.number = true >> and i realize i dont know what it does,
-- i could simply (while in normal mode) -> :h options which normal
-- would then open the documentation where i could again - while in
-- mode - run the command -> /number to find the line with the 
-- informtion about that option.

-- to learn more about options checkout this video -> https://www.youtube.com/watch?v=Cp0iap9u29c&list=PLQtBcyU4pWcTOzhXJ3wPd5eCoDuOP6GnK&index=6&t=38s
-- options
vim.opt.number = true -- this option adds line numbers
vim.opt.relativenumber = true -- this options makes it so that the line numbers are relative
vim.opt.splitbelow = true -- this option makes it so that man pages open from the bottom
vim.opt.splitright = true -- this option makes it so that splits happen to out editors right
vim.opt.wrap = true -- activates text wrapping
vim.opt.expandtab = true -- converts tabs to spaces
vim.opt.tabstop = 4 -- every tab is converted to 4 spaces
vim.opt.shiftwidth = 4 -- when in normal mode, if we use the >> or << to indent, the number of tabs will be 4
vim.opt.clipboard = "unnamedplus" -- syncronizes the system's clipboard to be able to copy to and from neovim
vim.opt.scrolloff = 999 -- when scrolling our cursor will stay on the center of the screen
vim.opt.virtualedit = "block" -- when editing in visual block mode, areas with visual space but no cells are treated like empty cells
vim.opt.ignorecase = true -- when searching for commands vim will ignore the case that we are typing when suggesting commands.
vim.opt.termguicolors = true -- by defautl the colors are very limited, this options helps neovim unleash their full potential.
