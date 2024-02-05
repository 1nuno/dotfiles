-- return {
-- 		"rebelot/kanagawa.nvim",
-- 		config = function()
-- 			require("kanagawa").setup({
-- 				transparent = true,
-- 				overrides = function(colors)
-- 					local theme = colors.theme
-- 					return {
-- 						NormalFloat = { bg = "none" },
-- 						FloatBorder = { bg = "none" },
-- 						FloatTitle = { bg = "none" },
-- 						TelescopeTitle = { fg = theme.ui.special, bold = true },
-- 						TelescopePromptNormal = { bg = theme.ui.bg_p1 },
-- 						TelescopePromptBorder = { fg = theme.ui.bg_p1, bg = theme.ui.bg_p1 },
-- 						TelescopeResultsNormal = { fg = theme.ui.fg_dim, bg = theme.ui.bg_m1 },
-- 						TelescopeResultsBorder = { fg = theme.ui.bg_m1, bg = theme.ui.bg_m1 },
-- 						TelescopePreviewNormal = { bg = theme.ui.bg_dim },
-- 						TelescopePreviewBorder = { bg = theme.ui.bg_dim, fg = theme.ui.bg_dim },
-- 						Pmenu = { fg = theme.ui.shade0, bg = theme.ui.bg_p1 }, -- add `blend = vim.o.pumblend` to enable transparency
-- 						PmenuSel = { fg = "NONE", bg = theme.ui.bg_p2 },
-- 						PmenuSbar = { bg = theme.ui.bg_m1 },
-- 						PmenuThumb = { bg = theme.ui.bg_p2 },
-- 					}
-- 				end,
-- 				colors = {
-- 					theme = {
-- 						all = {
-- 							ui = {
-- 								bg_gutter = "none",
-- 							},
-- 						},
-- 					},
-- 				},
-- 			})
-- 			vim.cmd("colorscheme kanagawa-lotus")
-- 		end,
return {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    config = function()
        require("catppuccin").setup({
            flavour = "mocha",
            transparent_background = true,
            integrations = {
                cmp = true,
                gitsigns = true,
                nvimtree = true,
                treesitter = true,
                telescope = true,
            }
        })
        vim.cmd("colorscheme catppuccin")
    end,
}
