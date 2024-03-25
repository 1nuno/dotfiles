return {
	"catppuccin/nvim",
	name = "catppuccin",
	priority = 1000,
	config = function()
		require("catppuccin").setup({
			custom_highlights = function(colors)
				return {
					WinSeparator = { fg = colors.blue }, -- this is working together with the option laststatus=3 to allow it to work with the vertical splits as well
					LineNrAbove = { fg = "#758cbf", bold = false },
					LineNr = { fg = "#ffffff", bold = true },
					LineNrBelow = { fg = "#758cbf", bold = false },
				}
			end,
			flavour = "mocha",
			transparent_background = true,
			integrations = {
				cmp = true,
				gitsigns = true,
				nvimtree = true,
				neotree = true,
				treesitter = true,
				telescope = true,
				which_key = true,
			},
			color_overrides = {
				mocha = {
					overlay0 = "#9fb0c2",
				},
			},
		})

		vim.cmd("colorscheme catppuccin")

        -- add rounded borders to lsp hover
		vim.lsp.handlers["textDocument/hover"] = vim.lsp.with(vim.lsp.handlers.hover, { border = "rounded" })
	end,
}
