return {
	"jpalardy/vim-slime",
	lazy = false,
	init = function()
		--         vim.g.slime_no_mappings = 1
		vim.g.slime_target = "tmux"
		vim.api.nvim_set_keymap("v", "<Leader>s", "<Plug>SlimeRegionSend", { noremap = true })
  --       vim.g.slime_cell_delimiter = "# %%"
  --       vim.api.nvim_set_keymap(
  --       "n",
  --       "<Leader>c",
  --       ':execute "normal \\<Plug>SlimeSendCell"<CR>/' .. vim.g.slime_cell_delimiter .. "<CR>:nohlsearch<CR>",
  --       {noremap = true}
  --       )
    end,
}
