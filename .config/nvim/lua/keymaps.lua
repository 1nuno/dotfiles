-- this is the leader key. (did i really need to write this?)
vim.g.mapleader = " "

-- this for dealing with lines that wrap
vim.keymap.set("n", "k", "v:count == 0 ? 'gk' : 'k'", { expr = true, silent = true })
vim.keymap.set("n", "j", "v:count == 0 ? 'gj' : 'j'", { expr = true, silent = true })
vim.keymap.set("v", "k", "v:count == 0 ? 'gk' : 'k'", { expr = true, silent = true })
vim.keymap.set("v", "j", "v:count == 0 ? 'gj' : 'j'", { expr = true, silent = true })

-- this is gold! thank you primagen!!!!! this is equivalent to pressing alt+arrow in vscode to move lines arround
-- but here we instead press shift+j or shift+k to move selections around while in visual mode.
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

-- this is to copy into my system clipboard. prime said is better to keep yanks from vim and from the clipboard
-- i dont know why this is true, but he is ThePrimagen so it must be true. (ill keep it commented for now though
-- cuz im using the clipboard sync option)
-- vim.keymap.set("n", "<leader>y", "\"+y")
-- vim.keymap.set("v", "<leader>y", "\"+y")
-- vim.keymap.set("n", "<leader>Y", "\"+Y")

-- ThePrimagen cant stop giving me gold. this is a search and replace type thingy.
vim.keymap.set("n", "<leader>s", [[:%s/\<<C-r><C-w>\>/<C-r><C-w>/gI<Left><Left><Left>]])

-- more magic from the primagen. paste without losing it from the registry.
vim.keymap.set("v", "<Leader>p" , "\"_dP")


